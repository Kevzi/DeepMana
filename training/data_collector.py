import sys
import os
import torch
import numpy as np
import time
from typing import List, Tuple, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Path hacks (assuming run from root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.model import HearthstoneModel
from ai.encoder import FeatureEncoder
from ai.mcts import MCTS
from ai.game_wrapper import HearthstoneGame
from ai.replay_buffer import ReplayBuffer
from ai.actions import Action

def _play_game_worker(model, mcts_sims, game_idx, verbose):
    """Worker function for multithreading."""
    try:
        # Load card database ONCE (Thread-safe)
        from simulator import CardDatabase
        db = CardDatabase.get_instance()
        if not db.is_loaded:
            db.load()
        
        # Threads share the same model on GPU
        encoder = FeatureEncoder()
        
        # Randomize perspective
        perspective = 1 if np.random.random() > 0.5 else 2
        
        pid = os.getpid()
        if verbose: print(f"  [Worker {pid}] Starting Game #{game_idx} (Perspective: P{perspective})")
        env = HearthstoneGame(perspective=perspective)
        env.reset()
        
        trajectory = []
        step_count = 0
        max_steps = 500
        
        # Create MCTS once per game
        mcts = MCTS(model, encoder, None, num_simulations=mcts_sims)
        
        while not env.is_game_over and step_count < max_steps:
            # Dynamic perspective
            current_p_idx = 0 if env.game.current_player == env.game.players[0] else 1
            env.perspective = current_p_idx + 1
            
            root_game_state = env.game.clone()
            mcts_probs, _ = mcts.search(root_game_state)
            
            encoded_state = encoder.encode(env.get_state())
            current_p_id = env.perspective
            
            if step_count % 20 == 0 and verbose:
                print(f"  [Worker {pid}] Game #{game_idx} - Step {step_count}...")
            
            trajectory.append((encoded_state, mcts_probs, current_p_id))
            
            action_idx = np.random.choice(len(mcts_probs), p=mcts_probs)
            action = Action.from_index(action_idx)
            env.step(action)
            step_count += 1
            
        # Determine winner
        winner = 0
        if env.game.winner:
            winner = 1 if env.game.winner == env.game.players[0] else 2
        if verbose: print(f"  [Worker {pid}] Game #{game_idx} FINISHED at step {step_count}.")
        return trajectory, winner

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e

class DataCollector:
    def __init__(self, model: HearthstoneModel, buffer: ReplayBuffer, num_workers: int = 4):
        self.model = model
        self.buffer = buffer
        self.encoder = FeatureEncoder()
        self.num_workers = num_workers
        
    def collect_games(self, num_games: int, mcts_sims: int = 25, verbose: bool = False):
        """Run self-play games using multiprocessing."""
        
        # CRITICAL FIX: Buffer was poisoned by biased P1-only games and P2 random moves.
        # Clearing once to ensure new training is healthy.
        if len(self.buffer) > 0 and not hasattr(self, '_buffer_flushed'):
            print("Cleaning biased replay buffer to restart with healthy symmetric data (P1/P2 random perspective)...")
            self.buffer.clear()
            self._buffer_flushed = True

        print(f"Starting parallel selection of {num_games} games...")
        
        start_time = time.time()
        winners = {0: 0, 1: 0, 2: 0}
        
        # Use model directly on GPU
        model_state = self.model.state_dict()
        
        completed_games = 0
        
        if self.num_workers == 0:
            # Sequential execution for debugging/stability
            for i in range(num_games):
                try:
                    trajectory, winner = _play_game_worker(
                        self.model,
                        mcts_sims,
                        i,
                        verbose
                    )
                    self.buffer.add_game(trajectory, winner)
                    winners[winner] = winners.get(winner, 0) + 1
                    
                    completed_games += 1
                    elapsed = time.time() - start_time
                    avg_time = elapsed / completed_games if completed_games > 0 else 0
                    
                    winner_str = f"Player {winner}" if winner > 0 else "Draw/Timeout"
                    print(f"[{completed_games}/{num_games}] Game completed. Winner: {winner_str}. Buffer: {len(self.buffer)}. Avg: {avg_time:.2f}s/game")
                except Exception as e:
                    print(f"Sequential game failed: {e}")
                    
        else:
            # Parallel execution using Threads to allow GPU sharing
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                futures = []
                for i in range(num_games):
                    futures.append(executor.submit(
                        _play_game_worker, 
                        self.model,
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
