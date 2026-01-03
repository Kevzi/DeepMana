"""
Trainer for HearthstoneOne AI.

Implements the AlphaZero training loop:
1. Self-Play Data Collection (using MCTS)
2. Neural Network Training (Policy + Value Loss)
3. Evaluation / Checkpointing
"""

import sys
import os
import time
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter

# Path hacks
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.model import HearthstoneModel
from ai.replay_buffer import ReplayBuffer
from training.data_collector import DataCollector

class Trainer:
    def __init__(self, config=None):
        self.config = config or {}
        
        # Hyperparameters - Optimized for RTX 3070 Ti
        self.input_dim = 690
        self.action_dim = 200
        self.learning_rate = 1e-4         # More stable for long training
        self.batch_size = 128             # RTX 3070 Ti can handle this
        self.epochs_per_iter = 5
        self.num_iterations = 100         # More iterations for better learning
        self.games_per_iter = 20          # More self-play games per iteration
        self.mcts_sims = 100              # More MCTS simulations = better decisions
        self.buffer_capacity = 100000     # Keep more history
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Components
        self.model = HearthstoneModel(self.input_dim, self.action_dim).to(self.device)
        self.buffer = ReplayBuffer(self.buffer_capacity)
        self.collector = DataCollector(self.model, self.buffer)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # TensorBoard
        self.writer = SummaryWriter(log_dir="runs/hearthstone_training")
        print(f"TensorBoard: tensorboard --logdir=runs")
        
    def train(self):
        """Main training loop."""
        print(f"Starting training on {self.device}...")
        
        for iteration in range(self.num_iterations):
            print(f"\n=== Iteration {iteration + 1}/{self.num_iterations} ===")
            
            # 1. Self-Play
            self.model.eval() # Collect in eval mode
            self.model.to("cpu")
            winners = self.collector.collect_games(self.games_per_iter, self.mcts_sims)
            
            # Log winner stats to TensorBoard
            self.writer.add_scalar("Games/Winners_Draw", winners.get(0, 0), iteration)
            self.writer.add_scalar("Games/Winners_P1", winners.get(1, 0), iteration)
            self.writer.add_scalar("Games/Winners_P2", winners.get(2, 0), iteration)
            self.writer.add_scalar("Buffer/Size", len(self.buffer), iteration)
            
            # 2. Training
            if len(self.buffer) < self.batch_size:
                print("Buffer too small, skipping train...")
                continue
                
            self.model.to(self.device)
            self.model.train()
            avg_loss = self._train_epochs(iteration)
            
            # Log loss to TensorBoard
            self.writer.add_scalar("Loss/Total", avg_loss, iteration)
            
            # 3. Checkpoint
            self.save_checkpoint(f"checkpoint_iter_{iteration+1}.pt")
            self.writer.flush()
            
    def _train_epochs(self, iteration: int):
        """Train on buffer data for several epochs."""
        total_loss = 0
        total_policy_loss = 0
        total_value_loss = 0
        num_batches = 0
        
        # Let's do 100 updates per iteration
        num_updates = 100
        
        for i in range(num_updates):
            states, target_pis, target_vs = self.buffer.sample(self.batch_size)
            
            states = states.to(self.device)
            target_pis = target_pis.to(self.device)
            target_vs = target_vs.to(self.device)
            
            # Forward
            pred_pis, pred_vs = self.model(states)
            
            # Loss
            # Clamp for stability
            pred_pis = torch.clamp(pred_pis, 1e-8, 1.0)
            policy_loss = -torch.sum(target_pis * torch.log(pred_pis)) / target_pis.size(0)
            
            # Value Loss: MSE
            value_loss = F.mse_loss(pred_vs, target_vs)
            
            loss = policy_loss + value_loss
            
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            total_policy_loss += policy_loss.item()
            total_value_loss += value_loss.item()
            num_batches += 1
            
        avg_loss = total_loss / num_batches
        print(f"Training Loss: {avg_loss:.4f}")
        
        # Log detailed losses for the last batch or average
        self.writer.add_scalar("Loss/Policy", total_policy_loss / num_batches, iteration)
        self.writer.add_scalar("Loss/Value", total_value_loss / num_batches, iteration)
        
        return avg_loss
        
    def save_checkpoint(self, filename: str):
        """Save model."""
        path = os.path.join("models", filename)
        os.makedirs("models", exist_ok=True)
        torch.save(self.model.state_dict(), path)
        print(f"Saved model to {path}")

if __name__ == "__main__":
    trainer = Trainer()
    trainer.train()
