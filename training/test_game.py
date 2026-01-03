"""
Test script to see bot actions in detail.
Run with: python -m training.test_game
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.model import HearthstoneModel
from ai.replay_buffer import ReplayBuffer
from training.data_collector import DataCollector

def main():
    print("=" * 60)
    print("HearthstoneOne - Verbose Self-Play Test")
    print("=" * 60)
    
    # Initialize model (untrained)
    model = HearthstoneModel(input_dim=690, action_dim=200)
    buffer = ReplayBuffer(capacity=1000)
    collector = DataCollector(model, buffer)
    
    # Run 1 game with verbose output
    print("\nRunning 1 game with detailed action logs...\n")
    collector.collect_games(num_games=1, mcts_sims=20, verbose=True)
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print(f"Buffer size: {len(buffer)} positions")
    print("=" * 60)

if __name__ == "__main__":
    main()
