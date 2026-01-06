"""Hearthstone Simulator - Event Sequence System.

Implements the Sequence/Phase/Step architecture from the PDF specification:
- Sequence: Global wrapper initiated by an action (Play Minion, Cast Spell, Attack)
- Phase: Logical blocks within a sequence (Battlecry Phase, After Summon Phase)
- Step: Atomic unit of calculation (Apply Damage)
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Callable, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game
    from .entities import Card, Entity
    from .player import Player


class SequenceType(Enum):
    """Types of sequences (top-level actions)."""
    PLAY_CARD = auto()
    ATTACK = auto()
    HERO_POWER = auto()
    END_TURN = auto()
    START_TURN = auto()
    DEATH_PROCESSING = auto()


class PhaseType(Enum):
    """Types of phases within a sequence."""
    # Play sequence phases
    ON_PLAY = auto()           # Card leaves hand
    ENTER_PLAY = auto()        # Card enters play zone
    BATTLECRY = auto()         # Battlecry resolution
    SECRET_ACTIVATION = auto() # Check opponent secrets
    AFTER_PLAY = auto()        # After Play triggers
    AFTER_SUMMON = auto()      # After Summon triggers
    
    # Attack sequence phases
    ATTACK_DECLARATION = auto()  # "When you attack" triggers
    ATTACK_TARGETING = auto()    # Ogre rule, redirects
    COMBAT_DAMAGE = auto()       # Simultaneous damage
    AFTER_ATTACK = auto()        # "After you attack" triggers
    
    # Turn phases
    TURN_START = auto()
    DRAW = auto()
    MAIN_ACTION = auto()
    TURN_END = auto()
    
    # Special
    DEATH_CHECK = auto()


@dataclass
class Step:
    """Atomic unit of calculation within a phase."""
    action: Callable[['Game'], None]
    description: str = ""
    executed: bool = False
    
    def execute(self, game: 'Game') -> None:
        """Execute this step."""
        if not self.executed:
            self.action(game)
            self.executed = True


@dataclass
class Phase:
    """A logical block within a sequence."""
    phase_type: PhaseType
    steps: List[Step] = field(default_factory=list)
    completed: bool = False
    
    def add_step(self, action: Callable[['Game'], None], description: str = "") -> Step:
        """Add a step to this phase."""
        step = Step(action=action, description=description)
        self.steps.append(step)
        return step
    
    def execute(self, game: 'Game') -> None:
        """Execute all steps in this phase, then process deaths."""
        for step in self.steps:
            step.execute(game)
        
        # Per PDF: Death check at end of phase
        game.process_deaths()
        self.completed = True


@dataclass
class Sequence:
    """Global wrapper for a game action."""
    sequence_type: SequenceType
    phases: List[Phase] = field(default_factory=list)
    source: Optional['Entity'] = None  # Card/Entity that initiated
    target: Optional['Entity'] = None  # Target if applicable
    completed: bool = False
    
    def add_phase(self, phase_type: PhaseType) -> Phase:
        """Add a phase to this sequence."""
        phase = Phase(phase_type=phase_type)
        self.phases.append(phase)
        return phase
    
    def execute(self, game: 'Game') -> None:
        """Execute all phases in order."""
        for phase in self.phases:
            if not phase.completed:
                phase.execute(game)
        self.completed = True


class SequenceManager:
    """Manages the execution of game sequences."""
    
    def __init__(self, game: 'Game'):
        self.game = game
        self.current_sequence: Optional[Sequence] = None
        self.sequence_stack: List[Sequence] = []
    
    def start_sequence(self, seq_type: SequenceType, source: Optional['Entity'] = None) -> Sequence:
        """Start a new sequence."""
        seq = Sequence(sequence_type=seq_type, source=source)
        
        # If already in a sequence, push to stack
        if self.current_sequence:
            self.sequence_stack.append(self.current_sequence)
        
        self.current_sequence = seq
        return seq
    
    def end_sequence(self) -> None:
        """End the current sequence and return to parent if any."""
        if self.current_sequence:
            self.current_sequence.completed = True
        
        if self.sequence_stack:
            self.current_sequence = self.sequence_stack.pop()
        else:
            self.current_sequence = None
    
    def create_play_minion_sequence(self, minion: 'Card', target: Optional['Card'] = None) -> Sequence:
        """Create a standard 'Play Minion' sequence per PDF spec."""
        seq = self.start_sequence(SequenceType.PLAY_CARD, source=minion)
        seq.target = target
        
        # Phase 1: ON_PLAY (card leaves hand)
        seq.add_phase(PhaseType.ON_PLAY)
        
        # Phase 2: ENTER_PLAY (card enters play zone)
        seq.add_phase(PhaseType.ENTER_PLAY)
        
        # Phase 3: BATTLECRY (if has battlecry)
        if minion.data.battlecry:
            seq.add_phase(PhaseType.BATTLECRY)
        
        # Phase 4: SECRET_ACTIVATION (check opponent secrets)
        seq.add_phase(PhaseType.SECRET_ACTIVATION)
        
        # Phase 5: AFTER_PLAY (triggers)
        seq.add_phase(PhaseType.AFTER_PLAY)
        
        # Phase 6: AFTER_SUMMON (triggers)
        seq.add_phase(PhaseType.AFTER_SUMMON)
        
        return seq
    
    def create_attack_sequence(self, attacker: 'Card', defender: 'Card') -> Sequence:
        """Create a standard 'Attack' sequence per PDF spec."""
        seq = self.start_sequence(SequenceType.ATTACK, source=attacker)
        seq.target = defender
        
        # Phase 1: ATTACK_DECLARATION ("When you attack" triggers)
        seq.add_phase(PhaseType.ATTACK_DECLARATION)
        
        # Phase 2: ATTACK_TARGETING (Ogre rule, redirects)
        seq.add_phase(PhaseType.ATTACK_TARGETING)
        
        # Phase 3: COMBAT_DAMAGE (simultaneous damage)
        seq.add_phase(PhaseType.COMBAT_DAMAGE)
        
        # Phase 4: AFTER_ATTACK ("After you attack" triggers)
        seq.add_phase(PhaseType.AFTER_ATTACK)
        
        return seq
