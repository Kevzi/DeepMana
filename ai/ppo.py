"""Proximal Policy Optimization (PPO) pour HearthstoneOne.

Implémentation robuste basée sur AlphaStar et OpenAI Five.
Remplace MCTS pour une meilleure gestion de l'information imparfaite
et un débit de simulation 10x supérieur.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

class PPOMemory:
    """Stockage des trajectoires pour PPO avec support structuré."""
    
    def __init__(self):
        self.states = []        # Now can hold lists/dicts for Transformer
        self.actions = []
        self.action_masks = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []
    
    def store_structured(self, state_tuple, action, action_mask, log_prob, reward, value, done):
        """Store a structured state (from Transformer model input)."""
        self.states.append(state_tuple)
        self.actions.append(action)
        self.action_masks.append(action_mask)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)
    
    def clear(self):
        self.states = []
        self.actions = []
        self.action_masks = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []
    
    def get_batch(self, device="cpu"):
        """Returns batches. For structured states, it returns a list of tuples/dicts."""
        # Collate structured states
        # The result 'states' will be a list of lists of components if we use Transformer
        
        # Helper to collate nested structures
        def collate_recursive(list_of_items):
            if isinstance(list_of_items[0], torch.Tensor):
                # Shape could be [1, ...] or [...]
                if list_of_items[0].dim() > 0 and list_of_items[0].size(0) == 1:
                    return torch.cat(list_of_items).to(device)
                else:
                    return torch.stack(list_of_items).to(device)
            elif isinstance(list_of_items[0], (tuple, list)):
                collated = [collate_recursive([item[i] for item in list_of_items]) 
                             for i in range(len(list_of_items[0]))]
                return tuple(collated) if isinstance(list_of_items[0], tuple) else collated
            elif isinstance(list_of_items[0], dict):
                return {k: collate_recursive([item[k] for item in list_of_items]) 
                        for k in list_of_items[0].keys()}
            return list_of_items

        collated_states = collate_recursive(self.states)
        
        return (
            collated_states,
            torch.tensor(self.actions, dtype=torch.long).to(device),
            torch.stack(self.action_masks).to(device),
            torch.tensor(self.log_probs, dtype=torch.float32).to(device),
            torch.tensor(self.rewards, dtype=torch.float32).to(device),
            torch.tensor(self.values, dtype=torch.float32).to(device),
            torch.tensor(self.dones, dtype=torch.float32).to(device)
        )


class PPO:
    """Proximal Policy Optimization implementation."""
    
    def __init__(self, 
                 model: nn.Module,
                 lr: float = 3e-4,
                 gamma: float = 0.99,
                 gae_lambda: float = 0.95,
                 clip_epsilon: float = 0.2,
                 entropy_coef: float = 0.01,
                 value_coef: float = 0.5,
                 max_grad_norm: float = 0.5,
                 ppo_epochs: int = 10,
                 batch_size: int = 64):
        
        self.model = model
        self.device = next(model.parameters()).device
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_epsilon = clip_epsilon
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef
        self.max_grad_norm = max_grad_norm
        self.ppo_epochs = ppo_epochs
        self.batch_size = batch_size
        
        self.memory = PPOMemory()
    
    def select_action_structured(self, input_args: List[Any]) -> Tuple[int, float, float]:
        """Sélectionne une action à partir d'entrées structurées (Transformer)."""
        self.model.eval()
        with torch.no_grad():
            # input_args: (hand, board, en_board, global, masks, action_mask)
            policy, value = self.model(*input_args)
            
            dist = torch.distributions.Categorical(policy)
            action = dist.sample()
            log_prob = dist.log_prob(action)
            
        return action.item(), log_prob.item(), value.item()
    
    def compute_gae(self, rewards, values, dones, next_value):
        """Calcule les avantages généralisés (GAE)."""
        advantages = []
        gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_val = next_value
            else:
                next_val = values[t + 1]
            
            # delta = r_t + gamma * V(s_{t+1}) - V(s_t)
            delta = rewards[t] + self.gamma * next_val * (1 - dones[t]) - values[t]
            # gae = delta + gamma * lambda * (1 - done) * gae_prev
            gae = delta + self.gamma * self.gae_lambda * (1 - dones[t]) * gae
            advantages.insert(0, gae)
        
        advantages = torch.tensor(advantages, dtype=torch.float32).to(self.device)
        returns = advantages + torch.tensor(values, dtype=torch.float32).to(self.device)
        
        return advantages, returns
    
    def update(self, next_value: float = 0.0) -> Dict[str, float]:
        """Met à jour la politique avec les données de trajectoires collectées."""
        if len(self.memory.actions) == 0:
            return {}
            
        states, actions, action_masks, old_log_probs, rewards, values, dones = self.memory.get_batch(self.device)
        
        # Calculer les avantages (GAE)
        advantages, returns = self.compute_gae(
            rewards.tolist(), values.tolist(), dones.tolist(), next_value
        )
        
        # Normaliser les avantages pour la stabilité
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        
        num_samples = len(actions)
        
        def index_recursive(item, idx):
            if isinstance(item, torch.Tensor):
                return item[idx]
            elif isinstance(item, (tuple, list)):
                indexed = [index_recursive(sub, idx) for sub in item]
                return tuple(indexed) if isinstance(item, tuple) else indexed
            elif isinstance(item, dict):
                return {k: index_recursive(v, idx) for k, v in item.items()}
            return item

        # PPO epochs
        for _ in range(self.ppo_epochs):
            indices = np.random.permutation(num_samples)
            
            for start in range(0, num_samples, self.batch_size):
                end = start + self.batch_size
                batch_idx = indices[start:end]
                
                # Slicing tensor-like batch
                b_states = index_recursive(states, batch_idx)
                b_actions = actions[batch_idx]
                b_masks = action_masks[batch_idx]
                b_old_log_probs = old_log_probs[batch_idx]
                b_advantages = advantages[batch_idx]
                b_returns = returns[batch_idx]
                
                # Forward Pass
                self.model.train()
                # b_states is expected to be (hand, board, en_board, global, masks)
                if isinstance(b_states, (list, tuple)):
                    policy, values_pred = self.model(*b_states, action_mask=b_masks)
                else:
                    policy, values_pred = self.model(b_states, action_mask=b_masks)
                    
                dist = torch.distributions.Categorical(policy)
                
                new_log_probs = dist.log_prob(b_actions)
                entropy = dist.entropy().mean()
                
                # Importance sampling ratio: exp(new_log_prob - old_log_prob)
                ratio = torch.exp(new_log_probs - b_old_log_probs)
                
                # Clipped Surrogated Objective
                surr1 = ratio * b_advantages
                surr2 = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * b_advantages
                
                policy_loss = -torch.min(surr1, surr2).mean()
                
                # Critic Loss (Value Loss)
                value_loss = F.mse_loss(values_pred.squeeze(), b_returns)
                
                # Perte Totale = Actor + Critic - Entropy (bonus exploration)
                loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy
                
                # Optimisation
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()
                
                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
        
        num_updates = self.ppo_epochs * (num_samples // self.batch_size + 1)
        
        # Nettoyage
        self.memory.clear()
        
        return {
            "policy_loss": total_policy_loss / num_updates,
            "value_loss": total_value_loss / num_updates,
            "entropy": total_entropy / num_updates
        }
