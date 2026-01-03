"""Hearthstone Simulator - Player.

Manages player state: hero, hand, deck, board, mana, etc.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from .enums import Zone, PlayState, Mulligan, CardType
from .entities import Entity, Card, Hero, HeroPower, Weapon, Minion

if TYPE_CHECKING:
    from .game import Game


class Player(Entity):
    """A player in the game."""
    
    MAX_HAND_SIZE: int = 10
    MAX_BOARD_SIZE: int = 7
    MAX_DECK_SIZE: int = 60
    STARTING_HAND_FIRST: int = 3
    STARTING_HAND_SECOND: int = 4
    MAX_MANA: int = 10
    
    def __init__(self, name: str = "Player", game: Optional[Game] = None):
        super().__init__(game)
        self.name: str = name
        
        # Hero
        self.hero: Optional[Hero] = None
        
        # Zones
        self.deck: List[Card] = []
        self.hand: List[Card] = []
        self.board: List[Minion] = []
        self.graveyard: List[Card] = []
        self.setaside: List[Card] = [] # For Discover options, created cards, etc.
        self.choices: List[Card] = [] # Subset of setaside specifically for current choices
        self.secrets: List[Card] = []
        
        # Quest System
        self.quest: Optional[Card] = None  # Active Quest (max 1)
        self.quest_progress: int = 0       # Progress counter
        self.quest_goal: int = 0           # Goal to complete quest
        self.quest_reward_id: str = ""     # Card ID of reward
        self.sidequests: List[Card] = []   # Sidequests (can have multiple)
        self.questline_step: int = 0       # For Questlines (0, 1, 2)
        
        # Mana
        self.mana_crystals: int = 0
        self.mana: int = 0
        self.overload: int = 0
        self.overload_next_turn: int = 0
        self.temp_mana: int = 0
        
        # State
        self.play_state: PlayState = PlayState.PLAYING
        self.mulligan_state: Mulligan = Mulligan.INVALID
        self.fatigue_counter: int = 0
        
        # History and Trackers
        self.cards_played_this_game: List[str] = []
        self.spells_played_this_game: List[str] = []
        self.minions_played_this_game_list: List[str] = []
        self.dead_minions: List[str] = []  # Graveyard (card IDs)
        self.cards_drawn_this_game: List[str] = []
        
        # Turn based trackers
        self.damage_taken_this_turn: int = 0
        self.healing_taken_this_turn: int = 0
        self.cards_played_this_turn: int = 0
        self.minions_played_this_turn: int = 0
        self.spells_played_this_turn: int = 0
        self.hero_power_uses_this_turn: int = 0
        
        # Combo tracker (Rogue)
        self.combo_cards_played: int = 0
        
        # Death Knight Corpses
        self.corpses: int = 0  # Current corpse count
        
        # Expansion Synergy Trackers
        self.elementals_played_last_turn: int = 0  # For elemental synergy
        self.elementals_played_this_turn: int = 0  # Track current turn
        self.cthun_attack: int = 6     # C'Thun base stats
        self.cthun_health: int = 6
        self.jade_counter: int = 0     # Current jade golem size
        self.excavate_progress: int = 0  # Excavate tier (0-3, resets at 4)
        
        # Starship Pieces
        self.starship_pieces: List[str] = []  # IDs of pieces collected
        
        # Sideboard (Zilliax, E.T.C. Band)
        self.sideboard: Dict[str, List[str]] = {}  # key: parent card_id, value: list of child card_ids
        
        # Temp reductions
        self.next_spell_cost_reduction = 0
        self.next_hero_power_cost_reduction = 0
        
        # Status
        self.conceded: bool = False
        self.opponent: Optional[Player] = None

    def clone(self) -> 'Player':
        """Create a deep copy of the player (excluding entities managed by Game.clone)."""
        new_player = Player(self.name, None)
        # Stats
        new_player.mana_crystals = self.mana_crystals
        new_player.mana = self.mana
        new_player.overload = self.overload
        new_player.overload_next_turn = self.overload_next_turn
        new_player.temp_mana = self.temp_mana
        new_player.play_state = self.play_state
        new_player.mulligan_state = self.mulligan_state
        new_player.fatigue_counter = self.fatigue_counter
        
        # History (Lists of strings/ints are safe to shallow copy if we create new list)
        new_player.cards_played_this_game = list(self.cards_played_this_game)
        new_player.spells_played_this_game = list(self.spells_played_this_game)
        new_player.minions_played_this_game_list = list(self.minions_played_this_game_list)
        new_player.dead_minions = list(self.dead_minions)
        new_player.cards_drawn_this_game = list(self.cards_drawn_this_game)
        
        # Custom attribs (like corpses, rafaams_played)
        # We should define a way to copy dynamic attributes.
        # For now, just copy specific known ones or __dict__?
        # __dict__ copy is safer for dynamic attributes
        for k, v in self.__dict__.items():
            if k not in ['hero', 'hero_power', 'deck', 'hand', 'board', 'graveyard', 'secrets', 'game', 'opponent', '_game']:
                if isinstance(v, (int, str, bool, float)) or v is None:
                    setattr(new_player, k, v)
                elif isinstance(v, list) and (not v or isinstance(v[0], (int, str))):
                     setattr(new_player, k, list(v))
                elif isinstance(v, set):
                     setattr(new_player, k, set(v))
                     
        return new_player
    
    @property
    def spell_damage(self) -> int:
        """Calculate total spell damage from board."""
        total = 0
        for minion in self.board:
            total += minion.get_tag(GameTag.SPELLPOWER)
        return total

    @property
    def weapon(self) -> Optional[Weapon]:
        """Get the hero's weapon."""
        return self.hero.weapon if self.hero else None
    
    @property
    def hero_power(self) -> Optional[HeroPower]:
        """Get the hero's hero power."""
        return self.hero.hero_power if self.hero else None
    
    @property
    def health(self) -> int:
        """Get hero's current health."""
        return self.hero.health if self.hero else 0
    
    @property
    def armor(self) -> int:
        """Get hero's armor."""
        return self.hero.armor if self.hero else 0
    
    def add_to_deck(self, card: Card) -> bool:
        """Add a card to the deck."""
        if len(self.deck) >= self.MAX_DECK_SIZE:
            return False
        card.controller = self
        card.zone = Zone.DECK
        self.deck.append(card)
        return True
    
    def shuffle_deck(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.deck)
    
    def draw_specific_card(self, card: Card) -> Optional[Card]:
        """Draw a specific card instance from the deck."""
        if card in self.deck:
            self.deck.remove(card)
            if len(self.hand) >= self.MAX_HAND_SIZE:
                card.zone = Zone.GRAVEYARD
                self.graveyard.append(card)
                return None
            else:
                card.zone = Zone.HAND
                self.hand.append(card)
                self.cards_drawn_this_game.append(card.card_id)
                return card
        return None

    def draw(self, count: int = 1) -> List[Card]:
        """Draw cards from deck."""
        drawn: List[Card] = []
        
        for _ in range(count):
            if not self.deck:
                # Fatigue damage
                self.fatigue_counter += 1
                if self.hero:
                    self.game.deal_damage(self.hero, self.fatigue_counter)
                continue
            
            card = self.deck.pop(0)
            
            if len(self.hand) >= self.MAX_HAND_SIZE:
                # Mill the card
                card.zone = Zone.GRAVEYARD
                self.graveyard.append(card)
            else:
                card.zone = Zone.HAND
                # Track turn for Quickdraw
                if self.game:
                    card.turn_added_to_hand = self.game.turn
                self.hand.append(card)
                self.cards_drawn_this_game.append(card.card_id)
                drawn.append(card)
        
        return drawn
    
    def dredge(self) -> Optional[Card]:
        """
        Dredge: Look at the bottom 3 cards of your deck and put one on top.
        Simplified: AI picks the highest cost card.
        """
        if len(self.deck) == 0:
            return None
        
        # Get bottom 3 cards
        bottom_count = min(3, len(self.deck))
        bottom_cards = self.deck[-bottom_count:]
        
        # AI strategy: pick the highest cost card (or random for simplicity)
        import random
        chosen = max(bottom_cards, key=lambda c: c.data.cost) if bottom_cards else None
        
        if chosen:
            # Remove from current position and put on top
            self.deck.remove(chosen)
            self.deck.insert(0, chosen)
        
        return chosen
    
    def add_to_hand(self, card: Card) -> bool:
        """Add a card to hand (not from deck)."""
        if len(self.hand) >= self.MAX_HAND_SIZE:
            card.zone = Zone.GRAVEYARD
            self.graveyard.append(card)
            return False
        
        card.controller = self
        card.zone = Zone.HAND
        # Track turn for Quickdraw
        if self.game:
            card.turn_added_to_hand = self.game.turn
        self.hand.append(card)
        return True
    
    def remove_from_hand(self, card: Card) -> bool:
        """Remove a card from hand."""
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False
    
    def discard(self, count: int = 1) -> List[Card]:
        """Discard random cards from hand."""
        discarded: List[Card] = []
        for _ in range(count):
            if not self.hand:
                break
            card = random.choice(self.hand)
            self.hand.remove(card)
            card.zone = Zone.GRAVEYARD
            self.graveyard.append(card)
            discarded.append(card)
            self.game.fire_event("on_card_discarded", self, card)
        return discarded
    
    def summon(self, minion: Minion, position: int = -1) -> bool:
        """Summon a minion to the board."""
        if len(self.board) >= self.MAX_BOARD_SIZE:
            return False
        
        if position < 0 or position > len(self.board):
            position = len(self.board)
        
        minion.controller = self
        minion.zone = Zone.PLAY
        minion.zone_position = position
        minion.exhausted = True  # Summoning sickness
        
        self.board.insert(position, minion)
        
        # Update positions
        for i, m in enumerate(self.board):
            m.zone_position = i
        
        return True
    
    def remove_from_board(self, minion: Minion) -> bool:
        """Remove a minion from board."""
        if minion in self.board:
            self.board.remove(minion)
            # Update positions
            for i, m in enumerate(self.board):
                m.zone_position = i
            return True
        return False
    
    def equip_weapon(self, weapon: Weapon) -> None:
        """Equip a weapon (destroys existing one)."""
        if self.hero:
            if self.hero.weapon:
                old_weapon = self.hero.weapon
                old_weapon.zone = Zone.GRAVEYARD
                self.graveyard.append(old_weapon)
            
            weapon.controller = self
            weapon.zone = Zone.PLAY
            self.hero.weapon = weapon
    
    def spend_mana(self, amount: int) -> bool:
        """Spend mana if available."""
        available = self.mana + self.temp_mana
        if available < amount:
            return False
        
        # Use temp mana first
        temp_used = min(self.temp_mana, amount)
        self.temp_mana -= temp_used
        amount -= temp_used
        
        self.mana -= amount
        return True
    
    def gain_mana_crystal(self, count: int = 1, filled: bool = True) -> None:
        """Gain mana crystals."""
        self.mana_crystals = min(self.MAX_MANA, self.mana_crystals + count)
        if filled:
            self.mana = min(self.mana_crystals, self.mana + count)
    
    def start_turn(self) -> None:
        """Called at the start of player's turn."""
        # Gain mana crystal
        self.mana_crystals = min(self.MAX_MANA, self.mana_crystals + 1)
        
        # Refresh mana
        self.mana = self.mana_crystals
        
        # Apply overload from last turn
        self.mana = max(0, self.mana - self.overload)
        self.overload = self.overload_next_turn
        self.overload_next_turn = 0
        self.temp_mana = 0
        
        # Reset hero power
        if self.hero_power:
            self.hero_power.reset_for_turn()
        
        # Draw a card
        self.draw(1)
            
        # Unfreeze, refresh minions and handle Dormant
        for minion in self.board:
            minion.exhausted = False
            minion.attacks_this_turn = 0
            if minion.frozen:
                minion.frozen = False
            
            # === DORMANT: Wake up management ===
            if minion.dormant > 0:
                minion._dormant -= 1
                if minion.dormant == 0:
                    if self.game:
                        self.game.fire_event("on_awake", minion)
                        handler = self.game._get_effect_handler(minion.card_id, "on_awake")
                        if handler:
                            handler(self.game, self, minion)
        
        # Reset hero attacks
        if self.hero:
            self.hero.exhausted = False
            self.hero.attacks_this_turn = 0
        
        # Reset turn trackers
        self.cards_played_this_turn = 0
        self.minions_played_this_turn = 0
        self.spells_played_this_turn = 0
        self.hero_power_uses_this_turn = 0
        self.combo_cards_played = 0
        self.elementals_played_last_turn = self.elementals_played_this_turn
        self.elementals_played_this_turn = 0
        self.spells_played_this_turn = 0
        self.hero_power_uses_this_turn = 0
        self.combo_cards_played = 0
        
        # Draw a card
        self.draw(1)
    
    def end_turn(self) -> None:
        """Called at the end of player's turn."""
        # Stealth is removed when attacking, not at end of turn
        pass
    
    def can_play_card(self, card: Card) -> bool:
        """Check if a card can be played."""
        if card not in self.hand:
            return False
        
        # Calculate current cost via game if available
        if self.game:
            current_cost = self.game.get_card_cost(self, card)
        else:
            current_cost = card.cost
            
        available_mana = self.mana + self.temp_mana
        if current_cost > available_mana:
            return False
        
        # Check board space for minions
        if card.card_type == CardType.MINION:
            if len(self.board) >= self.MAX_BOARD_SIZE:
                return False
        
        return True
    
    def get_valid_targets(self, card: Card) -> List[Entity]:
        """Get valid targets for a card."""
        # Use custom target handler if available
        if self.game and card.card_id in self.game._target_handlers:
            return self.game._target_handlers[card.card_id](self.game, card)
            
        # Base implementation: all characters
        targets: List[Entity] = []
        
        # Add all characters as potential targets
        if self.hero:
            targets.append(self.hero)
        targets.extend([m for m in self.board if m.dormant == 0])
        
        if self.opponent:
            if self.opponent.hero:
                targets.append(self.opponent.hero)
            targets.extend([m for m in self.opponent.board if m.dormant == 0])
        
        return targets
    
    def get_valid_attack_targets(self, attacker: Card) -> List[Card]:
        """Get valid attack targets for an attacker."""
        if not self.opponent:
            return []
        
        targets: List[Card] = []
        
        # Check for taunt
        taunts = [m for m in self.opponent.board if m.taunt and not m.stealth and m.dormant == 0]
        
        if taunts:
            # Must attack taunt minions
            targets = taunts
        else:
            # Can attack hero or any minion without stealth
            if self.opponent.hero and not self.opponent.hero.immune:
                targets.append(self.opponent.hero)
            targets.extend([m for m in self.opponent.board if not m.stealth and m.dormant == 0])
        
        # Rush minions can't attack hero on first turn
        if attacker.rush and attacker.exhausted:
            targets = [t for t in targets if t.card_type != CardType.HERO]
        
        return targets
    
    # === QUEST SYSTEM ===
    
    def play_quest(self, quest_card: Card, goal: int, reward_id: str) -> bool:
        """Play a quest card."""
        if self.quest is not None:
            return False  # Already have a quest
        
        self.quest = quest_card
        self.quest_progress = 0
        self.quest_goal = goal
        self.quest_reward_id = reward_id
        return True
    
    def advance_quest(self, amount: int = 1) -> bool:
        """Advance quest progress. Returns True if quest completed."""
        if self.quest is None:
            return False
        
        self.quest_progress += amount
        
        if self.quest_progress >= self.quest_goal:
            return self.complete_quest()
        return False
    
    def complete_quest(self) -> bool:
        """Complete the quest and add reward to hand."""
        if self.quest is None or not self.quest_reward_id:
            return False
        
        from simulator.factory import create_card
        
        reward = create_card(self.quest_reward_id, self.game)
        if reward:
            self.add_to_hand(reward)
        
        # Move quest to graveyard
        self.graveyard.append(self.quest)
        self.quest = None
        self.quest_progress = 0
        self.quest_goal = 0
        self.quest_reward_id = ""
        
        return True
    
    def play_sidequest(self, sidequest_card: Card) -> bool:
        """Play a sidequest (can have multiple)."""
        if len(self.sidequests) >= 3:  # Max 3 sidequests
            return False
        self.sidequests.append(sidequest_card)
        return True
    
    # === SYNERGY HELPERS ===
    
    def played_elemental_last_turn(self) -> bool:
        """Check if an elemental was played last turn (for elemental synergy)."""
        return self.elementals_played_last_turn > 0
    
    def is_holding_dragon(self) -> bool:
        """Check if holding a dragon in hand (for dragon synergy)."""
        for card in self.hand:
            if card.data.race and 'DRAGON' in str(card.data.race):
                return True
        return False
    
    def has_no_duplicates(self) -> bool:
        """Check if deck has no duplicates (for Highlander effects)."""
        card_ids = [c.card_id for c in self.deck]
        return len(card_ids) == len(set(card_ids))
    
    def summon_jade_golem(self) -> None:
        """Summon a Jade Golem (Jade counter increases each time)."""
        self.jade_counter = min(self.jade_counter + 1, 30)  # Max 30/30
        
        if len(self.board) < 7 and self.game:
            from simulator.factory import create_card
            from simulator.entities import Minion
            
            jade = create_card("CS2_231", self.game)  # Wisp base
            if jade:
                m = Minion(jade.data, self.game)
                m.attack = self.jade_counter
                m.health = self.jade_counter
                m.max_health = self.jade_counter
                m.name = "Jade Golem"
                m.controller = self
                self.summon(m)
    
    def buff_cthun(self, attack: int = 0, health: int = 0) -> None:
        """Buff C'Thun wherever it is."""
        self.cthun_attack += attack
        self.cthun_health += health
    
    def excavate(self) -> int:
        """
        Excavate: Advance excavation tier and get reward based on tier.
        Tier 1: Common treasure, Tier 2: Rare, Tier 3: Epic, Tier 4: Legendary (resets)
        """
        self.excavate_progress += 1
        current_tier = self.excavate_progress
        
        # Excavate treasures pools (simplified IDs for the simulator)
        treasures = {
            1: ["WW_400t1", "WW_400t2", "WW_400t3", "WW_400t4", "WW_400t5"], # Tier 1
            2: ["WW_400t6", "WW_400t7", "WW_400t8", "WW_400t9"],             # Tier 2
            3: ["WW_400t10", "WW_400t11", "WW_400t12"],                      # Tier 3
            4: ["WW_401"]                                                    # Tier 4 (Legendary generic)
        }
        
        tier_to_use = min(current_tier, 4)
        import random
        treasure_id = random.choice(treasures.get(tier_to_use, treasures[1]))
        
        from simulator.factory import create_card
        treasure_card = create_card(treasure_id, self)
        if treasure_card:
            self.add_to_hand(treasure_card)
        
        if self.excavate_progress >= 4:
            self.excavate_progress = 0  # Reset after tier 4
            
        return current_tier
    
    def launch_starship(self) -> None:
        """Launch the Starship, combining all collected pieces."""
        if not self.starship_pieces or len(self.board) >= 7:
            return
            
        from simulator.factory import create_card
        from simulator.entities import Minion
        
        # Create base Starship (usually a specific token or the 'Starship' card)
        # We'll use a generic token for now
        starship_data = create_card("STARSHIP_TOKEN", self.game).data
        ship = Minion(starship_data, self.game)
        ship.name = "The Starship"
        ship.controller = self
        
        # Sum stats and abilities from all pieces
        for piece_id in self.starship_pieces:
            piece_card = create_card(piece_id, self.game)
            if piece_card:
                ship._attack += piece_card.data.attack
                ship._health += piece_card.data.health
                ship._max_health += piece_card.data.health
                # Copy keywords
                if piece_card.data.taunt: ship._taunt = True
                if piece_card.data.divine_shield: ship._divine_shield = True
                if piece_card.data.rush: ship._rush = True
                if piece_card.data.lifesteal: ship._lifesteal = True
                
        # Clear pieces after launch
        self.starship_pieces = []
        self.summon(ship)
    
    def __repr__(self) -> str:
        return f"<Player '{self.name}' HP:{self.health} Mana:{self.mana}/{self.mana_crystals}>"
