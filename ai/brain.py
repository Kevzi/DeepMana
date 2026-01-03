"""
AIBrain - Interface between AlphaZero model and the overlay.

This module provides a high-level interface to use the trained model
for suggesting actions during live gameplay.
"""

import os
import torch
import numpy as np
from typing import Optional, Tuple, List

from ai.model import HearthstoneModel
from ai.encoder import FeatureEncoder
from ai.actions import Action, ActionType
from ai.game_wrapper import HearthstoneGame


class AIBrain:
    """
    High-level AI interface for the overlay.
    
    Usage:
        brain = AIBrain()
        brain.load_model("models/checkpoint_iter_100.pt")
        action, confidence = brain.suggest_action(game_state)
    """
    
    def __init__(self, input_dim: int = 690, action_dim: int = 200, use_gpu: bool = True):
        self.input_dim = input_dim
        self.action_dim = action_dim
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        
        # Initialize model
        self.model = HearthstoneModel(input_dim, action_dim).to(self.device)
        self.encoder = FeatureEncoder()
        
        # State
        self.model_loaded = False
        self.model_path = None
        
    def load_model(self, path: str) -> bool:
        """Load a trained model checkpoint."""
        if not os.path.exists(path):
            print(f"Model not found: {path}")
            return False
            
        try:
            state_dict = torch.load(path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self.model_loaded = True
            self.model_path = path
            print(f"Model loaded from {path}")
            return True
        except Exception as e:
            print(f"Failed to load model: {e}")
            return False
    
    def load_latest_model(self, models_dir: str = "models") -> bool:
        """Load the most recent checkpoint from models directory."""
        if not os.path.exists(models_dir):
            print(f"Models directory not found: {models_dir}")
            return False
            
        # Find all checkpoints
        checkpoints = [f for f in os.listdir(models_dir) if f.endswith('.pt')]
        if not checkpoints:
            print("No checkpoints found")
            return False
            
        # Sort by iteration number (assumes format: checkpoint_iter_X.pt)
        def get_iter(name):
            try:
                return int(name.split('_')[-1].replace('.pt', ''))
            except:
                return 0
                
        checkpoints.sort(key=get_iter, reverse=True)
        latest = os.path.join(models_dir, checkpoints[0])
        
        return self.load_model(latest)
    
    def suggest_action(self, game_state: dict) -> Tuple[Optional[Action], float, str]:
        """
        Get the best action for the current game state.
        
        Args:
            game_state: Dictionary with game state from the parser
            
        Returns:
            (action, confidence, description)
            - action: Action object or None
            - confidence: float 0-1
            - description: Human-readable description
        """
        if not self.model_loaded:
            return None, 0.0, "Model not loaded"
            
        try:
            # Encode state to tensor
            state_tensor = self.encoder.encode(game_state)
            state_tensor = torch.tensor(state_tensor, dtype=torch.float32).unsqueeze(0).to(self.device)
            
            # Get model prediction
            with torch.no_grad():
                policy, value = self.model(state_tensor)
            
            # Policy is action probabilities
            probs = policy.cpu().numpy()[0]
            
            # Apply action masking (only valid actions)
            valid_mask = self._get_valid_action_mask(game_state)
            masked_probs = probs * valid_mask
            
            # Normalize
            if masked_probs.sum() > 0:
                masked_probs = masked_probs / masked_probs.sum()
            else:
                # No valid actions - suggest end turn
                return Action(ActionType.END_TURN), 1.0, "End Turn (no valid actions)"
            
            # Get best action
            best_idx = np.argmax(masked_probs)
            confidence = float(masked_probs[best_idx])
            
            action = Action.from_index(best_idx)
            description = self._action_to_description(action, game_state)
            
            return action, confidence, description
            
        except Exception as e:
            print(f"Error in suggest_action: {e}")
            return None, 0.0, f"Error: {e}"
    
    def get_value_estimate(self, game_state: dict) -> float:
        """Get the model's value estimate for the current state (-1 to 1)."""
        if not self.model_loaded:
            return 0.0
            
        try:
            state_tensor = self.encoder.encode(game_state)
            state_tensor = torch.tensor(state_tensor, dtype=torch.float32).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                _, value = self.model(state_tensor)
                
            return float(value.cpu().numpy()[0])
        except:
            return 0.0
    
    def _get_valid_action_mask(self, game_state: dict) -> np.ndarray:
        """
        Create a mask of valid actions based on game state.
        Returns array of 0s and 1s for each action index.
        """
        mask = np.zeros(self.action_dim, dtype=np.float32)
        
        # End turn is always valid
        mask[0] = 1.0  # Assuming END_TURN is index 0
        
        # Check playable cards
        mana = game_state.get('mana', 0)
        hand = game_state.get('hand', [])
        
        for i, card in enumerate(hand[:10]):  # Max 10 cards
            card_cost = card.get('cost', 99)
            if card_cost <= mana:
                # PLAY_CARD action indices (assuming layout)
                action_idx = 1 + i  # Cards start at index 1
                if action_idx < self.action_dim:
                    mask[action_idx] = 1.0
        
        # Check hero power
        hero_power = game_state.get('hero_power', {})
        hp_cost = hero_power.get('cost', 2)
        hp_used = hero_power.get('used_this_turn', False)
        
        if mana >= hp_cost and not hp_used:
            mask[11] = 1.0  # Assuming HERO_POWER is index 11
        
        # Attack actions
        board = game_state.get('board', [])
        for i, minion in enumerate(board[:7]):  # Max 7 minions
            if minion.get('can_attack', False):
                # Attack actions start at index 12+
                attack_idx = 12 + i * 8  # Each minion can attack 8 targets
                for t in range(8):
                    if attack_idx + t < self.action_dim:
                        mask[attack_idx + t] = 1.0
        
        return mask
    
    def _action_to_description(self, action: Action, game_state: dict) -> str:
        """Convert action to human-readable description."""
        if action.action_type == ActionType.END_TURN:
            return "End Turn"
            
        elif action.action_type == ActionType.PLAY_CARD:
            hand = game_state.get('hand', [])
            if action.card_index is not None and action.card_index < len(hand):
                card = hand[action.card_index]
                card_name = card.get('name', f'Card {action.card_index}')
                return f"Play: {card_name}"
            return f"Play card {action.card_index}"
            
        elif action.action_type == ActionType.HERO_POWER:
            return "Use Hero Power"
            
        elif action.action_type == ActionType.ATTACK:
            return f"Attack: Minion {action.attacker_index} → Target {action.target_index}"
            
        elif action.action_type == ActionType.USE_LOCATION:
            return f"Activate Location {action.card_index}"
            
        return str(action)


# Singleton instance for easy access
_brain_instance: Optional[AIBrain] = None

def get_brain() -> AIBrain:
    """Get the global AIBrain instance."""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = AIBrain()
    return _brain_instance
