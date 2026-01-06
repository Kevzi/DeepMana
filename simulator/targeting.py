"""Hearthstone Simulator - Targeting System.

Implements the targeting matrix from PDF Section 8.2:
Stealth vs Immune vs Elusive with different action types.
"""

from __future__ import annotations
from enum import Enum, auto
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import Card, Entity
    from .player import Player


class TargetingType(Enum):
    """Types of targeting actions."""
    SPELL = auto()           # Spell targeting
    HERO_POWER = auto()      # Hero Power targeting
    BATTLECRY = auto()       # Battlecry targeting
    ATTACK = auto()          # Physical attack
    OWNER_BUFF = auto()      # Owner buffing own minion
    RANDOM = auto()          # Random selection (Deadly Shot)
    AOE_DAMAGE = auto()      # Area damage (Flamestrike)
    AOE_DESTROY = auto()     # Area destroy (Twisting Nether)


def can_target(
    target: 'Card',
    targeting_type: TargetingType,
    is_friendly: bool = False
) -> bool:
    """Check if a target can be selected based on the targeting matrix.
    
    PDF Section 8.2 Matrix:
    ┌─────────────────────┬──────────┬──────────┬──────────┐
    │ Action              │ Stealth  │ Elusive  │ Immune   │
    ├─────────────────────┼──────────┼──────────┼──────────┤
    │ Spell Target        │ BLOCKED  │ BLOCKED  │ BLOCKED  │
    │ Hero Power Target   │ BLOCKED  │ BLOCKED  │ BLOCKED  │
    │ Battlecry Target    │ BLOCKED  │ ALLOWED! │ BLOCKED  │
    │ Attack              │ BLOCKED  │ ALLOWED  │ BLOCKED  │
    │ Owner Buff          │ ALLOWED  │ ALLOWED  │ ALLOWED  │
    │ Random              │ ALLOWED  │ ALLOWED  │ BLOCKED* │
    │ AOE Damage          │ ALLOWED  │ ALLOWED  │ BLOCKED* │
    │ AOE Destroy         │ ALLOWED  │ ALLOWED  │ ALLOWED! │
    └─────────────────────┴──────────┴──────────┴──────────┘
    
    *BLOCKED means targeting ok but damage = 0 (handled elsewhere)
    
    Args:
        target: The card being targeted
        targeting_type: Type of targeting action
        is_friendly: Whether the targeter owns this target
        
    Returns:
        True if targeting is allowed, False otherwise
    """
    # Get target states
    has_stealth = getattr(target, 'stealth', False) or getattr(target, '_stealth', False)
    has_elusive = getattr(target, 'elusive', False) or getattr(target.data, 'elusive', False) if hasattr(target, 'data') else False
    has_immune = getattr(target, 'immune', False)
    is_dormant = getattr(target, 'dormant', 0) > 0
    
    # Dormant minions can never be targeted
    if is_dormant:
        return False
    
    # Owner can always target their own minions (buffs)
    if targeting_type == TargetingType.OWNER_BUFF and is_friendly:
        return True
    
    # Check Stealth
    if has_stealth and not is_friendly:
        if targeting_type in [
            TargetingType.SPELL,
            TargetingType.HERO_POWER,
            TargetingType.BATTLECRY,
            TargetingType.ATTACK
        ]:
            return False
        # Stealth doesn't protect from AOE or Random
    
    # Check Elusive ("Can't be targeted by Spells or Hero Powers")
    if has_elusive:
        if targeting_type in [TargetingType.SPELL, TargetingType.HERO_POWER]:
            return False
        # NOTE: Elusive ALLOWS Battlecry targeting! (PDF critical note)
    
    # Check Immune
    if has_immune:
        if targeting_type in [
            TargetingType.SPELL,
            TargetingType.HERO_POWER,
            TargetingType.BATTLECRY,
            TargetingType.ATTACK
        ]:
            return False
        # Immune minions can still be affected by Twisting Nether (AOE_DESTROY)
        if targeting_type == TargetingType.AOE_DESTROY:
            return True
        # For RANDOM and AOE_DAMAGE: targeting works but damage is prevented
        # (damage prevention handled in damage calculation, not here)
    
    return True


def filter_targets(
    potential_targets: List['Card'],
    targeting_type: TargetingType,
    controller: 'Player'
) -> List['Card']:
    """Filter a list of targets based on targeting rules.
    
    Args:
        potential_targets: All potential targets
        targeting_type: Type of targeting
        controller: The player doing the targeting
        
    Returns:
        List of valid targets
    """
    valid = []
    for target in potential_targets:
        is_friendly = getattr(target, 'controller', None) == controller
        if can_target(target, targeting_type, is_friendly):
            valid.append(target)
    return valid


def get_all_targetable(
    player: 'Player',
    targeting_type: TargetingType,
    include_friendly: bool = True,
    include_enemy: bool = True,
    include_heroes: bool = True
) -> List['Card']:
    """Get all targetable entities for a player.
    
    Args:
        player: The player doing the targeting
        targeting_type: Type of targeting action
        include_friendly: Include own minions/hero
        include_enemy: Include opponent minions/hero
        include_heroes: Include heroes (not just minions)
        
    Returns:
        List of valid targets
    """
    targets = []
    
    if include_friendly:
        targets.extend(filter_targets(
            list(player.board), targeting_type, player
        ))
        if include_heroes and player.hero:
            targets.append(player.hero)
    
    if include_enemy and player.opponent:
        targets.extend(filter_targets(
            list(player.opponent.board), targeting_type, player
        ))
        if include_heroes and player.opponent.hero:
            if can_target(player.opponent.hero, targeting_type, False):
                targets.append(player.opponent.hero)
    
    return targets
