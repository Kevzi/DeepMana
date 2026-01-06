"""Hearthstone Simulator - Death Knight System.

Implements the Death Knight specific mechanics from PDF Section 7.1:
- Corpse System: Resource generated when friendly minions die
- Rune System: Deckbuilding constraints (Blood/Frost/Unholy)
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import Card
    from .player import Player


class RuneType(Enum):
    """Types of Death Knight runes."""
    BLOOD = auto()    # Red - survivability, self-damage
    FROST = auto()    # Blue - control, freeze
    UNHOLY = auto()   # Green - summons, corpses


@dataclass
class RuneRequirement:
    """Rune requirement for a card."""
    blood: int = 0
    frost: int = 0
    unholy: int = 0
    
    def total(self) -> int:
        return self.blood + self.frost + self.unholy
    
    def __str__(self) -> str:
        parts = []
        if self.blood:
            parts.append('B' * self.blood)
        if self.frost:
            parts.append('F' * self.frost)
        if self.unholy:
            parts.append('U' * self.unholy)
        return ''.join(parts) or 'None'


@dataclass
class DeckRunes:
    """Rune configuration for a Death Knight deck.
    
    A DK has 3 rune slots that can be any combination of B/F/U.
    Example: BBF, UFU, BBB
    """
    blood: int = 0
    frost: int = 0
    unholy: int = 0
    
    def set_runes(self, blood: int = 0, frost: int = 0, unholy: int = 0) -> None:
        """Set rune configuration. Total must be 3."""
        total = blood + frost + unholy
        if total != 3:
            raise ValueError(f"Deck must have exactly 3 runes, got {total}")
        self.blood = blood
        self.frost = frost
        self.unholy = unholy
    
    def can_include_card(self, requirement: RuneRequirement) -> bool:
        """Check if a card with given rune requirements can be in this deck."""
        return (
            requirement.blood <= self.blood and
            requirement.frost <= self.frost and
            requirement.unholy <= self.unholy
        )
    
    def __str__(self) -> str:
        return 'B' * self.blood + 'F' * self.frost + 'U' * self.unholy


class CorpseManager:
    """Manages the Death Knight corpse resource.
    
    Per PDF Section 7.1:
    - +1 Corpse whenever a friendly minion dies
    - Risen minions (from corpses) have DONT_LEAVE_CORPSE tag
    - Cards can "Spend Corpses" for enhanced effects
    """
    
    def __init__(self, player: 'Player'):
        self.player = player
        self._corpses: int = 0
    
    @property
    def count(self) -> int:
        return self._corpses
    
    def add(self, amount: int = 1) -> None:
        """Add corpses (usually from minion deaths)."""
        self._corpses += amount
    
    def spend(self, amount: int) -> bool:
        """Spend corpses for an effect. Returns True if successful."""
        if self._corpses >= amount:
            self._corpses -= amount
            return True
        return False
    
    def can_spend(self, amount: int) -> bool:
        """Check if we have enough corpses."""
        return self._corpses >= amount
    
    def reset(self) -> None:
        """Reset corpse count (e.g., for new game)."""
        self._corpses = 0


def parse_rune_requirement(rune_string: str) -> RuneRequirement:
    """Parse a rune requirement string like 'BB' or 'UF' into RuneRequirement.
    
    Args:
        rune_string: String of B/F/U characters
        
    Returns:
        RuneRequirement object
    """
    blood = rune_string.upper().count('B')
    frost = rune_string.upper().count('F')
    unholy = rune_string.upper().count('U')
    return RuneRequirement(blood=blood, frost=frost, unholy=unholy)


def validate_dk_deck(
    deck_cards: List['Card'],
    deck_runes: DeckRunes
) -> List[str]:
    """Validate a Death Knight deck against rune constraints.
    
    Args:
        deck_cards: List of cards in the deck
        deck_runes: The deck's rune configuration
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    for card in deck_cards:
        # Get rune requirement from card data
        rune_req = getattr(card.data, 'rune_requirement', None)
        if rune_req is None:
            continue
            
        if isinstance(rune_req, str):
            rune_req = parse_rune_requirement(rune_req)
        
        if not deck_runes.can_include_card(rune_req):
            errors.append(
                f"Card '{card.name}' requires {rune_req} but deck has {deck_runes}"
            )
    
    return errors
