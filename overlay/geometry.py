from dataclasses import dataclass
from typing import Tuple

@dataclass
class Point:
    x: int
    y: int

class HearthstoneGeometry:
    """
    Calculates screen coordinates for Hearthstone entities based on relative geometry.
    Assumes standard aspect ratio logic.
    """
    
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        
        # Geometry Constants (Relative 0.0-1.0)
        # These are approximations based on typical HS layout
        self.HAND_Y_PCT = 0.95
        self.PLAYER_BOARD_Y_PCT = 0.55
        self.OPPONENT_BOARD_Y_PCT = 0.42
        self.OPPONENT_HERO_Y_PCT = 0.18
        self.PLAYER_HERO_Y_PCT = 0.82
        
        self.BOARD_CENTER_X_PCT = 0.5
        # Width of board area where minions sit
        self.BOARD_WIDTH_PCT = 0.6 
        
    def resize(self, width: int, height: int):
        self.width = width
        self.height = height

    def _to_pixels(self, x_pct: float, y_pct: float) -> Point:
        return Point(int(x_pct * self.width), int(y_pct * self.height))

    def get_hand_card_pos(self, index: int, total_cards: int) -> Point:
        """Returns center position of a card in player's hand."""
        if total_cards <= 0: return self._to_pixels(0.5, 0.9)
        
        # Cards fan out. Logic simplifies to linear spread for now.
        # Max spread width approx 50% of screen
        spread = min(0.5, total_cards * 0.05) 
        start_x = 0.5 - (spread / 2)
        step = spread / max(1, (total_cards - 1))
        
        # If 1 card, it's at center
        if total_cards == 1:
            x_pct = 0.5
        else:
            x_pct = start_x + (index * step)
            
        return self._to_pixels(x_pct, self.HAND_Y_PCT)

    def get_player_minion_pos(self, index: int, total_minions: int) -> Point:
        """Returns center position of a minion on player's board."""
        return self._get_board_pos(index, total_minions, self.PLAYER_BOARD_Y_PCT)

    def get_opponent_minion_pos(self, index: int, total_minions: int) -> Point:
        """Returns center position of a minion on opponent's board."""
        return self._get_board_pos(index, total_minions, self.OPPONENT_BOARD_Y_PCT)

    def _get_board_pos(self, index: int, total_minions: int, y_pct: float) -> Point:
        if total_minions <= 0: return self._to_pixels(0.5, y_pct)
        
        # Minions are centered.
        # Each minion takes approx 12% width max? No, 7 minions max.
        # Let's say spread is dynamic.
        # Max width is ~60% of screen for 7 minions.
        
        full_width_for_7 = 0.55
        # Width per minion
        slot_width = full_width_for_7 / 7
        
        current_spread = total_minions * slot_width
        start_x = 0.5 - (current_spread / 2) + (slot_width / 2) # Center of first minion
        
        x_pct = start_x + (index * slot_width)
        return self._to_pixels(x_pct, y_pct)

    def get_hero_pos(self, is_opponent: bool) -> Point:
        y = self.OPPONENT_HERO_Y_PCT if is_opponent else self.PLAYER_HERO_Y_PCT
        return self._to_pixels(0.5, y)
    
    def get_turn_button_pos(self) -> Point:
        return self._to_pixels(0.82, 0.45) # Approx right middle
