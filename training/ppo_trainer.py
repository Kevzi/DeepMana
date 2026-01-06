"""Trainer PPO pour HearthstoneOne.

Implémente le pipeline complet :
1. Collecte de trajectoires (Self-Play ou League)
2. Optimisation PPO (Actor-Critic)
3. Gestion des adversaires via la League
4. Logging TensorBoard et Checkpointing
"""

import os
import sys
import time
import torch
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime

# Path adjustment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.transformer_model import HearthstoneTransformer
from ai.ppo import PPO
from ai.encoder import FeatureEncoder
from ai.game_wrapper import HearthstoneGame
from ai.actions import ACTION_SPACE_SIZE
from training.league import League, create_league

class PPOTrainer:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Hyperparameters
        self.lr = self.config.get("lr", 3e-4)
        self.gamma = self.config.get("gamma", 0.99)
        self.batch_size = self.config.get("batch_size", 128)
        self.ppo_epochs = self.config.get("ppo_epochs", 10)
        self.games_per_iter = self.config.get("games_per_iter", 20)
        
        # Model & Optimization
        self.model = HearthstoneTransformer(action_dim=ACTION_SPACE_SIZE).to(self.device)
        self.ppo = PPO(
            self.model, 
            lr=self.lr, 
            gamma=self.gamma, 
            ppo_epochs=self.ppo_epochs,
            batch_size=self.batch_size
        )
        
        # Components
        self.encoder = FeatureEncoder()
        self.league = create_league({
            "save_dir": "models/league_ppo",
            "snapshot_interval": 20
        })
        
        # Logging
        run_name = datetime.now().strftime("PPO_%Y-%m-%d_%Hh%M")
        self.writer = SummaryWriter(log_dir=f"runs/{run_name}")
        
        print(f"PPO Trainer initialized on {self.device}")
        
    def train(self, num_iterations: int = 500):
        for iteration in range(num_iterations):
            print(f"\n--- Iteration {iteration+1}/{num_iterations} ---")
            
            # 1. Collect trajectories
            start_time = time.time()
            game_stats = self._collect_trajectories()
            collect_time = time.time() - start_time
            
            # 2. Update model
            if len(self.ppo.memory.states) > self.batch_size:
                loss_dict = self.ppo.update()
                
                # Logging losses
                for k, v in loss_dict.items():
                    self.writer.add_scalar(f"Loss/{k}", v, iteration)
            
            # 3. League management
            self.league.add_main_agent(self.model, iteration)
            if iteration % self.league.snapshot_interval == 0:
                self.league.save()
            
            # 4. logging stats
            win_rate = game_stats["p1_wins"] / max(1, game_stats["total_games"])
            avg_steps = game_stats["total_steps"] / max(1, game_stats["total_games"])
            
            self.writer.add_scalar("Game/WinRate_P1", win_rate, iteration)
            self.writer.add_scalar("Game/AvgSteps", avg_steps, iteration)
            self.writer.add_scalar("League/Main_ELO", self.league.main_agents[-1].elo_rating if self.league.main_agents else 1500, iteration)
            
            print(f"  Collect: {collect_time:.1f}s | WinRate: {win_rate:.2%}")
            
            # 5. Checkpoint
            if iteration % 50 == 0:
                self.save_checkpoint(f"ppo_checkpoint_{iteration}.pt")

    def _collect_trajectories(self) -> dict:
        """Runs self-play or league matches to fill PPO memory."""
        stats = {"p1_wins": 0, "total_games": 0, "total_steps": 0}
        
        # Collect games_per_iter games
        for _ in range(self.games_per_iter):
            # Sample opponent from league (or just self for now)
            opponent_snapshot = self.league.sample_opponent("main")
            
            # Play a game
            env = HearthstoneGame(perspective=1)
            env.reset()
            
            # Prepare opponent model if needed
            opp_model = None
            if opponent_snapshot and opponent_snapshot.archetype != "main":
                opp_model = HearthstoneTransformer(action_dim=ACTION_SPACE_SIZE).to(self.device)
                opp_model.load_state_dict(opponent_snapshot.model_state)
                opp_model.eval()
            
            step_count = 0
            while not env.is_game_over and step_count < 300:
                current_p_idx = env.game.current_player_idx
                
                # Encode state (Structured for Transformer)
                env.perspective = current_p_idx + 1
                state_structured = self.encoder.structured_encode(env.get_state())
                action_mask = torch.tensor(env.get_action_mask(), dtype=torch.float32)
                
                # Prepare inputs for model
                # (hand, board, en_board, global, masks)
                input_args = (
                    state_structured["hand"],
                    state_structured["my_board"],
                    state_structured["enemy_board"],
                    state_structured["global_state"],
                    state_structured["masks"],
                    action_mask
                )
                # Move to device
                input_args = [self._to_device(arg) for arg in input_args]
                
                if current_p_idx == 0 or opp_model is None:
                    # Decision from current/main model
                    action_idx, log_prob, value = self.ppo.select_action_structured(input_args)
                    
                    # Execute step
                    from ai.actions import Action
                    action = Action.from_index(action_idx)
                    _, reward, done, _ = env.step(action)
                    
                    # Store in memory (Only for P1 or if both are training)
                    # We store the structured input components directly
                    # input_args: (hand, board, en_board, global, masks, action_mask)
                    state_to_store = input_args[:5]
                    self.ppo.memory.store_structured(
                        state_to_store, action_idx, action_mask, log_prob, reward, value, done
                    )
                else:
                    # Decision from opponent model
                    with torch.no_grad():
                        policy, _ = opp_model(*input_args)
                        action_idx = torch.multinomial(policy, 1).item()
                        from ai.actions import Action
                        action = Action.from_index(action_idx)
                        env.step(action)
                
                step_count += 1
            
            if env.game.winner == env.game.players[0]: stats["p1_wins"] += 1
            stats["total_games"] += 1
            stats["total_steps"] += step_count
            
        return stats

    def _to_device(self, obj):
        if isinstance(obj, torch.Tensor):
            return obj.to(self.device).unsqueeze(0)
        elif isinstance(obj, tuple):
            return tuple(self._to_device(t) for t in obj)
        elif isinstance(obj, dict):
            return {k: self._to_device(v) for k, v in obj.items()}
        return obj

    def save_checkpoint(self, name):
        path = os.path.join("models", name)
        os.makedirs("models", exist_ok=True)
        torch.save(self.model.state_dict(), path)

if __name__ == "__main__":
    # Standard training scale
    trainer = PPOTrainer({
        "games_per_iter": 10,  # 10 games for more stable winrate
        "ppo_epochs": 10,      # Standard PPO updates
        "batch_size": 256
    })
    trainer.train(num_iterations=1000)

# Add helper methods to PPO class in ppo.py to handle structured inputs
