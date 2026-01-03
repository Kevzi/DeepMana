import numpy as np
import torch
from .game_state import GameState
from .actions import ACTION_SPACE_SIZE

class FeatureEncoder:
    """
    Encodes the GameState into a tensor representation suitable for Neural Networks.
    
    Representation typically includes:
    - Scalar features (Mana, Health, Deck Size, Hand Size)
    - Board features (Minion stats, keywords)
    - Hand features (Card costs, types)
    - Hero features
    - History features
    """
    
    def __init__(self):
        # Define dimensions
        self.scalar_dim = 20 # Mana, Health, Armor, Overload, Fatigue, Deck, Hand, etc.
        self.card_dim = 25   # Cost, Atk, HP, MaxHP, Type(4), Keywords(10), State(5), etc.
        self.max_hand = 10
        self.max_board = 7
        self.input_dim = self.scalar_dim + (self.max_hand * 2 * self.card_dim) + (self.max_board * 2 * self.card_dim) 
        
    def encode(self, state: GameState) -> torch.Tensor:
        """Encodes state to tensor."""
        # 1. Scalars (Global context)
        p1, p2 = state.friendly_player, state.enemy_player
        scalars = [
            p1.mana / 10.0,
            p1.max_mana / 10.0,
            p1.hero.health / 30.0,
            p1.hero.armor / 20.0,
            p1.overload / 10.0,
            p1.fatigue / 10.0,
            len(p1.hand) / 10.0,
            p1.deck_size / 30.0,
            
            p2.hero.health / 30.0,
            p2.hero.armor / 20.0,
            p2.overload / 10.0,
            p2.fatigue / 10.0,
            len(p2.hand) / 10.0,
            p2.deck_size / 30.0,
            
            1.0 if state.is_my_turn else 0.0,
        ]
        # Pad scalars to scalar_dim
        scalars.extend([0.0] * (self.scalar_dim - len(scalars)))
        
        # 2. Hand Cards
        hand_features = []
        for card in p1.hand:
            hand_features.extend(self._encode_card(card))
        hand_features.extend([0.0] * (self.card_dim * (self.max_hand - len(p1.hand))))
        
        # Opponent hand (Hidden - limited info)
        opp_hand_features = [0.0] * (self.card_dim * self.max_hand)
        
        # 3. Board Minions
        board_features = []
        for minion in p1.board:
            board_features.extend(self._encode_card(minion))
        board_features.extend([0.0] * (self.card_dim * (self.max_board - len(p1.board))))
        
        opp_board_features = []
        for minion in p2.board:
            opp_board_features.extend(self._encode_card(minion))
        opp_board_features.extend([0.0] * (self.card_dim * (self.max_board - len(p2.board))))
        
        # Combine
        full_vector = scalars + hand_features + opp_hand_features + board_features + opp_board_features
        return torch.tensor(full_vector, dtype=torch.float32)

    def _encode_card(self, card) -> list:
        """Detailed encoding of a card/minion."""
        # Stats normalized roughly
        res = [
            getattr(card, 'cost', 0) / 10.0,
            getattr(card, 'attack', 0) / 10.0,
            getattr(card, 'health', 0) / 10.0,
            getattr(card, 'max_health', 1) / 10.0,
        ]
        
        # Card Type (One-hot: Minion, Spell, Weapon, Other)
        ctype = getattr(card, 'card_type', 0)
        res.extend([
            1.0 if ctype == 4 else 0.0, # MINION
            1.0 if ctype == 5 else 0.0, # SPELL
            1.0 if ctype == 7 else 0.0, # WEAPON
            1.0 if ctype not in [4, 5, 7] else 0.0
        ])
        
        # Keywords (Binary)
        res.extend([
            1.0 if getattr(card, 'taunt', False) else 0.0,
            1.0 if getattr(card, 'divine_shield', False) else 0.0,
            1.0 if getattr(card, 'rush', False) else 0.0,
            1.0 if getattr(card, 'lifesteal', False) else 0.0,
            1.0 if getattr(card, 'poisonous', False) else 0.0,
            1.0 if getattr(card, 'stealth', False) else 0.0,
            1.0 if getattr(card, 'windfury', False) else 0.0,
            1.0 if getattr(card, 'reborn', False) else 0.0,
            # New mechanics
            1.0 if getattr(card, 'cleave', False) else 0.0,
            1.0 if getattr(card, 'magnetic', False) else 0.0,
        ])
        
        # States
        res.extend([
            1.0 if getattr(card, 'dormant', 0) > 0 else 0.0,
            1.0 if getattr(card, 'frozen', False) else 0.0,
            1.0 if getattr(card, 'silenced', False) else 0.0,
            1.0 if getattr(card, 'exhausted', False) else 0.0,
            getattr(card, 'dormant', 0) / 5.0 # Counter value
        ])
        
        # Fill rest to card_dim
        if len(res) < self.card_dim:
            res.extend([0.0] * (self.card_dim - len(res)))
        return res[:self.card_dim]

    @property
    def observation_shape(self):
        return (self.input_dim,)
