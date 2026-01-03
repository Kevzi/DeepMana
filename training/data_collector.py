import sys
import os
import torch
import numpy as np
import time
from typing import List, Tuple, Optional, Dict
from concurrent.futures import ProcessPoolExecutor, as_completed

# Path hacks (assuming run from root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.model import HearthstoneModel
from ai.encoder import FeatureEncoder
from ai.mcts import MCTS
from ai.game_wrapper import HearthstoneGame
from ai.replay_buffer import ReplayBuffer
from ai.actions import Action

def _play_game_worker(model_state, input_dim, action_dim, mcts_sims, game_idx, verbose):
    """Worker function for multiprocessing."""
    # Crucial for Windows: limit torch threads per process to save RAM
    torch.set_num_threads(1)
    
    # Each process needs its own model instance on CPU
    model = HearthstoneModel(input_dim, action_dim)
    model.load_state_dict(model_state)
    model.eval()
    
    encoder = FeatureEncoder()
    env = HearthstoneGame()
    env.reset(randomize_first=True)
    
    trajectory = []
    step_count = 0
    max_steps = 150
    
    while not env.is_game_over and step_count < max_steps:
        root_game_state = env.game.clone()
        mcts = MCTS(model, encoder, root_game_state, num_simulations=mcts_sims)
        mcts_probs = mcts.search(root_game_state)
        
        encoded_state = encoder.encode(env.get_state())
        p_id = 1 if env.current_player == env.game.players[0] else 2
        
        trajectory.append((encoded_state, mcts_probs, p_id))
        
        # Pick action
        # Epsilon-greedy for P2 to break the bias
        if p_id == 2 and np.random.random() < 0.2:
            action_idx = np.random.choice(len(mcts_probs))
        else:
            action_idx = np.random.choice(len(mcts_probs), p=mcts_probs)
        
        # Execute action
        action = Action.from_index(action_idx)
        try:
            env.step(action)
        except Exception as e:
            if verbose:
                print(f"Worker Error in game {game_idx}: {e}")
            break # Stop game on error
            
        step_count += 1
        
    # Determine winner
    winner = 0
    if env.game.winner:
        winner = 1 if env.game.winner == env.game.players[0] else 2
        
    return trajectory, winner

class DataCollector:
    def __init__(self, model: HearthstoneModel, buffer: ReplayBuffer, num_workers: int = 4):
        self.model = model
        self.buffer = buffer
        self.encoder = FeatureEncoder()
        self.num_workers = num_workers
        
    def collect_games(self, num_games: int, mcts_sims: int = 25, verbose: bool = False):
        """Run self-play games using multiprocessing."""
        
        # Security check: if buffer is full of P1 wins, clear it to force new learning
        # (Only if buffer is already significant)
        if len(self.buffer) > 1000:
             # This is a bit aggressive but necessary for early training health
             pass 

        print(f"Starting parallel collection of {num_games} games (Mirror Matches enforced)...")
        
        start_time = time.time()
        winners = {0: 0, 1: 0, 2: 0}
        
        # Pull model state to pass to workers on CPU
        cpu_model_state = {k: v.cpu() for k, v in self.model.state_dict().items()}
        
        completed_games = 0
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = []
            for i in range(num_games):
                futures.append(executor.submit(
                    _play_game_worker, 
                    cpu_model_state,
                    self.model.input_dim,
                    self.model.action_dim,
                    mcts_sims,
                    i,
                    verbose
                ))
            
            for future in as_completed(futures):
                try:
                    trajectory, winner = future.result()
                    self.buffer.add_game(trajectory, winner)
                    winners[winner] = winners.get(winner, 0) + 1
                    
                    completed_games += 1
                    elapsed = time.time() - start_time
                    avg_time = elapsed / completed_games
                    
                    winner_str = f"Player {winner}" if winner > 0 else "Draw/Timeout"
                    print(f"[{completed_games}/{num_games}] Game completed. Winner: {winner_str}. Buffer: {len(self.buffer)}. Avg: {avg_time:.2f}s/game")
                except Exception as e:
                    print(f"Game worker failed: {e}")
                    
        return winners
