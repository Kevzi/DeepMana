"""Hearthstone Simulator - Game Engine.

Main game loop and state management.
"""

from __future__ import annotations

import random
from typing import Optional, List, Dict, Any, Callable, Tuple
from dataclasses import dataclass, field

from .enums import GamePhase, Step, Zone, CardType, PlayState, Mulligan, GameTag
from .entities import Entity, Card, CardData, Minion, Spell, Weapon, Hero, HeroPower
from .player import Player


@dataclass
class GameConfig:
    """Game configuration."""
    max_turns: int = 89  # Turn 45 for each player
    max_actions_per_turn: int = 100
    starting_health: int = 30


class Game:
    """Main game engine."""
    
    def __init__(self, config: Optional[GameConfig] = None):
        self.config = config or GameConfig()
        
        # Reset entity IDs
        Entity.reset_ids()
        
        # Players
        self.players: List[Player] = []
        self.current_player_idx: int = 0
        
        # Game state
        self.phase: GamePhase = GamePhase.INVALID
        self.step: Step = Step.INVALID
        self.turn: int = 0
        self.actions_this_turn: int = 0
        
        # Trigger system
        self._triggers: Dict[str, List[Tuple[Entity, Callable]]] = {
            "on_turn_start": [],
            "on_turn_end": [],
            "on_minion_summon": [],
            "on_minion_death": [],
            "on_damage_taken": [],
            "on_card_played": [],
            "on_hero_power": [],
            # Secret triggers
            "on_attack": [],           # Before any attack
            "on_spell_cast": [],       # When opponent plays a spell
            "on_minion_played": [],    # When opponent plays a minion
            "on_hero_attacked": [],    # When hero is attacked
            "on_friendly_death": [],   # When friendly minion dies
        }
        
        # Death processing
        self._pending_deaths: List[Card] = []
        self._pending_deathrattles: List[Tuple[Card, Callable]] = []
        
        # Effect handlers (to be populated by effect system)
        self._battlecry_handlers: Dict[str, Callable] = {}
        self._deathrattle_handlers: Dict[str, Callable] = {}
        self._target_handlers: Dict[str, Callable] = {}
        self._trigger_handlers: Dict[str, List[Callable]] = {}
        self._aura_handlers: Dict[str, Callable] = {}
        
        # Game log
        self.action_history: List[Dict[str, Any]] = []
        
        # Discover system
        self.pending_choices: Optional[Dict[str, Any]] = None

    def clone(self) -> 'Game':
        """Create a deep copy of the game state for MCTS."""
        import copy
        
        # 1. Create new empty game
        new_game = Game(self.config)
        new_game.phase = self.phase
        new_game.step = self.step
        new_game.turn = self.turn
        new_game.actions_this_turn = self.actions_this_turn
        new_game.current_player_idx = self.current_player_idx
        
        # 2. Clone Players
        # (We need to maintain cross-references, so we create both first)
        new_p1 = self.players[0].clone()
        new_p2 = self.players[1].clone()
        
        new_p1.game = new_game
        new_p2.game = new_game
        
        new_game.players = [new_p1, new_p2]
        new_p1.opponent = new_p2
        new_p2.opponent = new_p1  # Fix missing assignment
        
        # 3. Clone Entities and link them to new game/players
        # Helper to clone a list of cards
        def clone_card_list(source_list, owner):
            new_list = []
            for card in source_list:
                new_card = card.clone()
                new_card.game = new_game
                new_card.controller = owner
                new_list.append(new_card)
            return new_list

        # P1 Assets
        if self.players[0].hero:
            new_p1.hero = self.players[0].hero.clone()
            new_p1.hero.game = new_game
            new_p1.hero.controller = new_p1
            
        if self.players[0].hero_power:
            new_p1.hero_power = self.players[0].hero_power.clone()
            new_p1.hero_power.game = new_game
            new_p1.hero_power.controller = new_p1

        new_p1.deck = clone_card_list(self.players[0].deck, new_p1)
        new_p1.hand = clone_card_list(self.players[0].hand, new_p1)
        new_p1.board = clone_card_list(self.players[0].board, new_p1)
        new_p1.graveyard = clone_card_list(self.players[0].graveyard, new_p1)
        
        # P2 Assets
        if self.players[1].hero:
            new_p2.hero = self.players[1].hero.clone()
            new_p2.hero.game = new_game
            new_p2.hero.controller = new_p2

        if self.players[1].hero_power:
            new_p2.hero_power = self.players[1].hero_power.clone()
            new_p2.hero_power.game = new_game
            new_p2.hero_power.controller = new_p2

        new_p2.deck = clone_card_list(self.players[1].deck, new_p2)
        new_p2.hand = clone_card_list(self.players[1].hand, new_p2)
        new_p2.board = clone_card_list(self.players[1].board, new_p2)
        new_p2.graveyard = clone_card_list(self.players[1].graveyard, new_p2)
        
        # 4. Handlers (Shallow copy is mostly fine for function references, 
        # BUT triggers might bind to old entity instances via closure?)
        # For MCTS, we might lose dynamic triggers if we don't re-register them.
        # Ideally, cards re-register their triggers on 'setup' or we copy the internal trigger list mapping old entities to new ones.
        # Complex Trigger Cloning Strategy:
        # The `_triggers` dict maps {event: [(entity, callback), ...]}
        # We need to map old_entity -> new_entity in this list.
        
        # Map IDs to new entities for lookup
        # Problem: Entities might share IDs (copies). We rely on object identity in logic usually?
        # Actually our engine uses object references.
        # We need a mapping: old_entity_obj -> new_entity_obj
        
        entity_map = {}
        # Populate map
        def map_entities(p_old, p_new):
            if p_old.hero: entity_map[p_old.hero] = p_new.hero
            if p_old.hero_power: entity_map[p_old.hero_power] = p_new.hero_power
            for i in range(len(p_old.deck)): entity_map[p_old.deck[i]] = p_new.deck[i]
            for i in range(len(p_old.hand)): entity_map[p_old.hand[i]] = p_new.hand[i]
            for i in range(len(p_old.board)): entity_map[p_old.board[i]] = p_new.board[i]
            for i in range(len(p_old.graveyard)): entity_map[p_old.graveyard[i]] = p_new.graveyard[i]

        map_entities(self.players[0], new_p1)
        map_entities(self.players[1], new_p2)
        
        # Rebuild Triggers
        # Warning: The 'callback' itself might be a closure capturing the OLD entity (e.g. "def on_end(game, trig_src=OLD_SOURCE)...").
        # If we just copy the callback, it will run using the OLD entity constant.
        # However, most of our auto-generated triggers use `trig_src` passed as argument!
        # `callback(game, source, ...)` -> `source` is passed by the trigger system loop.
        # So as long as we update the `source` in the `_triggers` list, the callback will receive the NEW source.
        # Perfect!
        
        new_game._triggers = {k: [] for k in self._triggers}
        for event, listeners in self._triggers.items():
            for old_source, cb in listeners:
                if old_source in entity_map:
                    new_source = entity_map[old_source]
                    new_game._triggers[event].append((new_source, cb))
                else:
                    # Source might be dead or not tracked? Or Hero?
                    # If not found, skip (probably dead)
                    pass

        # Copy static handlers
        new_game._battlecry_handlers = self._battlecry_handlers # Stateless
        new_game._deathrattle_handlers = self._deathrattle_handlers # Stateless
        
        return new_game

    def discover(self, player: Player, options: List[Card], callback: Callable) -> None:
        """Pause game and wait for player to choose one of 3 cards."""
        self.pending_choices = {
            "player": player,
            "options": options,
            "callback": callback
        }
    
    def choose_discover(self, choice_idx: int) -> bool:
        """Resolve a pending discover choice."""
        if not self.pending_choices:
            return False
            
        options = self.pending_choices["options"]
        if choice_idx < 0 or choice_idx >= len(options):
            return False
            
        choice = options[choice_idx]
        callback = self.pending_choices["callback"]
        
        # === DARK GIFT: Apply random bonus to discovered minions ===
        source = self.pending_choices.get("source")
        if source and hasattr(source, 'data') and source.data.dark_gift:
            if choice.card_type == CardType.MINION:
                self._apply_dark_gift(choice)
        
        self.pending_choices = None  # Clear before callback to avoid loops
        
        callback(self, choice)
        
        # Process deaths after effect
        self.process_deaths()
        self.check_for_game_over()
        return True
    
    def discover_from_sideboard(self, parent_card: Card, callback: Callable) -> bool:
        """Start a discover from a card's sideboard (e.g. E.T.C. Band)."""
        player = parent_card.controller
        if not player or parent_card.card_id not in player.sideboard:
            return False
            
        module_ids = player.sideboard[parent_card.card_id]
        if not module_ids:
            return False
            
        from .factory import create_card
        options = [create_card(cid, player) for cid in module_ids]
        
        self.pending_choices = {
            "source": parent_card,
            "options": options,
            "callback": callback
        }
        return True

    def invoke(self, player: Player) -> None:
        """Invoke Galakrond - triggers the current Galakrond hero power."""
        # Find Galakrond hero power or current hero power if it's already Galakrond
        self._log_action("invoke", {"player": player.name})
        player.hero_power.use() # Simplified: just use hero power for now
        
        # Increment Galakrond upgrade counter
        player.galakrond_invocations = getattr(player, 'galakrond_invocations', 0) + 1
        self.fire_event("on_invoke", player)

    def adapt(self, minion: Card, callback: Optional[Callable] = None) -> bool:
        """Adapt a minion: choice of 3 from 10 bonuses."""
        from .factory import create_card
        
        # The 10 Adapt options (as dummy cards for choice UI)
        adapt_options = [
            "ADAPT_01", # +1/+1
            "ADAPT_02", # Divine Shield
            "ADAPT_03", # Taunt
            "ADAPT_04", # Poisonous
            "ADAPT_05", # Liquid Membrane (Can't be targeted)
            "ADAPT_06", # Windfury
            "ADAPT_07", # Stealth until next turn
            "ADAPT_08", # Deathrattle: Summon 2 1/1s
            "ADAPT_09", # +3 Health
            "ADAPT_10", # +3 Attack
        ]
        
        import random
        chosen_ids = random.sample(adapt_options, 3)
        options = [create_card(cid, minion.controller) for cid in chosen_ids]
        
        def adapt_callback(game, choice):
            if choice.card_id == "ADAPT_01": minion._attack += 1; minion._health += 1; minion._max_health += 1
            elif choice.card_id == "ADAPT_02": minion._divine_shield = True
            elif choice.card_id == "ADAPT_03": minion._taunt = True
            elif choice.card_id == "ADAPT_04": minion._poisonous = True
            elif choice.card_id == "ADAPT_05": minion.cant_be_targeted = True
            elif choice.card_id == "ADAPT_06": minion._windfury = True
            elif choice.card_id == "ADAPT_07": minion._stealth = True
            elif choice.card_id == "ADAPT_08": minion._dark_gift_deathrattle = "summon_two_1_1" # Reuse deathrattle system
            elif choice.card_id == "ADAPT_09": minion._health += 3; minion._max_health += 3
            elif choice.card_id == "ADAPT_10": minion._attack += 3
            
            if callback:
                callback(game, minion)

        self.pending_choices = {
            "source": minion,
            "options": options,
            "callback": adapt_callback
        }
        return True

    def joust(self, initiator: Player) -> bool:
        """
        Perform a Joust.
        Reveals a minion from each player's deck. 
        Initiator wins if their minion costs more.
        """
        opponent = self.get_opponent(initiator)
        
        # Get random minions from decks
        from .enums import CardType
        my_minions = [c for c in initiator.deck if c.card_type == CardType.MINION]
        opp_minions = [c for c in opponent.deck if c.card_type == CardType.MINION]
        
        if not my_minions:
            return False
        
        import random
        my_card = random.choice(my_minions)
        opp_card = random.choice(opp_minions) if opp_minions else None
        
        opp_cost = opp_card.cost if opp_card else -1
        
        win = my_card.cost > opp_cost
        
        self._log_action("joust", {
            "initiator": initiator.name,
            "my_card": my_card.card_id,
            "opp_card": opp_card.card_id if opp_card else None,
            "win": win
        })
        
        return win

    def _apply_dark_gift(self, minion: Card) -> None:
        """
        Apply a random Dark Gift bonus to a minion.
        The 10 Dark Gifts from Into the Emerald Dream:
        1. Terreur en éveil (Waking Terror) - +2/+2
        2. Repos serein (Peaceful Rest) - Deathrattle: Draw a card
        3. Courtes griffes (Short Claws) - Costs (2) less, -2 Attack
        4. Posture de défense (Defensive Stance) - +1/+3 and Taunt
        5. Cauchemar vivant (Living Nightmare) - +1/+1 and Reborn
        6. Somnambule (Sleepwalker) - Stealth for 1 turn
        7. Réveil brutal (Rude Awakening) - Battlecries trigger twice
        8. Beaux rêves (Sweet Dreams) - +2 Health and Lifesteal
        9. Horreur persistante (Lingering Horror) - Deathrattle: summon 1/1
        10. Serres de harpie (Harpy Talons) - +2 Attack and Rush
        """
        import random
        
        # Build list of applicable gifts
        applicable_gifts = []
        
        # 1. Terreur en éveil - +2/+2
        applicable_gifts.append(("Terreur en éveil", lambda m: (
            setattr(m, '_attack', m._attack + 2),
            setattr(m, '_health', m._health + 2),
            setattr(m, '_max_health', m._max_health + 2)
        )))
        
        # 2. Repos serein - Deathrattle: Draw
        applicable_gifts.append(("Repos serein", lambda m: (
            setattr(m, '_dark_gift_deathrattle', 'draw')
        )))
        
        # 3. Courtes griffes - Cost -2, Attack -2 (only if attack > 2)
        if minion._attack > 2:
            applicable_gifts.append(("Courtes griffes", lambda m: (
                setattr(m, '_cost', max(0, m._cost - 2)),
                setattr(m, '_attack', m._attack - 2)
            )))
        
        # 4. Posture de défense - +1/+3 and Taunt
        applicable_gifts.append(("Posture de défense", lambda m: (
            setattr(m, '_attack', m._attack + 1),
            setattr(m, '_health', m._health + 3),
            setattr(m, '_max_health', m._max_health + 3),
            setattr(m, '_taunt', True)
        )))
        
        # 5. Cauchemar vivant - +1/+1 and Reborn
        applicable_gifts.append(("Cauchemar vivant", lambda m: (
            setattr(m, '_attack', m._attack + 1),
            setattr(m, '_health', m._health + 1),
            setattr(m, '_max_health', m._max_health + 1),
            setattr(m, '_reborn', True)
        )))
        
        # 6. Somnambule - Stealth
        applicable_gifts.append(("Somnambule", lambda m: (
            setattr(m, '_stealth', True)
        )))
        
        # 7. Réveil brutal - Battlecries trigger twice (only if has battlecry)
        if minion.data.battlecry:
            applicable_gifts.append(("Réveil brutal", lambda m: (
                setattr(m, '_double_battlecry', True)
            )))
        
        # 8. Beaux rêves - +2 Health and Lifesteal
        applicable_gifts.append(("Beaux rêves", lambda m: (
            setattr(m, '_health', m._health + 2),
            setattr(m, '_max_health', m._max_health + 2),
            setattr(m, '_lifesteal', True)
        )))
        
        # 9. Horreur persistante - Deathrattle: summon 1/1
        applicable_gifts.append(("Horreur persistante", lambda m: (
            setattr(m, '_dark_gift_deathrattle', 'summon_1_1')
        )))
        
        # 10. Serres de harpie - +2 Attack and Rush
        applicable_gifts.append(("Serres de harpie", lambda m: (
            setattr(m, '_attack', m._attack + 2),
            setattr(m, '_rush', True)
        )))
        
        # Pick one random gift
        gift_name, gift_func = random.choice(applicable_gifts)
        gift_func(minion)
        minion._dark_gift_name = gift_name  # Store for display

    def register_trigger(self, event_name: str, source: Entity, callback: Callable) -> None:
        """Register a trigger callback."""
        if event_name in self._triggers:
            self._triggers[event_name].append((source, callback))
    
    def unregister_triggers(self, source: Entity) -> None:
        """Remove all triggers for a specific source."""
        for event_name in self._triggers:
            self._triggers[event_name] = [t for t in self._triggers[event_name] if t[0] != source]

    def fire_event(self, event_name: str, *args, **kwargs) -> None:
        """Execute all callbacks for an event."""
        if event_name not in self._triggers:
            return
            
        # Filter out triggers whose source is no longer in play
        # (unless it's a graveyard trigger, but we'll simplify for now)
        valid_triggers = []
        for source, callback in self._triggers[event_name]:
            if source.zone == Zone.PLAY or source.zone == Zone.HAND or isinstance(source, Hero):
                valid_triggers.append((source, callback))
        
        # Update triggers list (remove dead triggers)
        self._triggers[event_name] = valid_triggers
        
        # Execute callbacks
        for source, callback in valid_triggers:
            try:
                callback(self, source, *args, **kwargs)
            except Exception as e:
                print(f"CRITICAL ERROR executing trigger '{event_name}' for {source.name} ({source.card_id}): {e}")
                raise e

    def trigger_secrets(self, event_type: str, triggering_player: Player, **kwargs) -> Optional[Card]:
        """
        Check and trigger secrets for the opponent of triggering_player.
        
        Args:
            event_type: Type of event (attack, spell_cast, minion_played, hero_attacked)
            triggering_player: The player who performed the action
            **kwargs: Additional context (attacker, defender, spell, minion, etc.)
            
        Returns:
            The triggered secret card, or None if no secret triggered.
        """
        # Secrets trigger for the OPPONENT of the acting player
        opponent = self.get_opponent(triggering_player)
        if not opponent or not opponent.secrets:
            return None
        
        triggered_secret = None
        
        for secret in list(opponent.secrets):  # Copy list to allow modification
            # Get the secret's effect handler
            handler = self._get_secret_handler(secret.card_id, event_type)
            if handler:
                # Check if the secret should trigger
                should_trigger = handler(self, opponent, secret, **kwargs)
                if should_trigger:
                    # Secret triggered! Remove it from play
                    opponent.secrets.remove(secret)
                    secret.zone = Zone.GRAVEYARD
                    opponent.graveyard.append(secret)
                    triggered_secret = secret
                    # Only one secret triggers per event
                    break
        
        return triggered_secret

    def _get_secret_handler(self, card_id: str, event_type: str) -> Optional[Callable]:
        """Get the secret handler for a specific card and event type."""
        try:
            # Try to import the effect module
            import importlib
            
            # Search in multiple effect folders
            for folder in ['classic', 'basic', 'naxx', 'gvg', 'tgt', 'wog', 'msg', 
                          'ungoro', 'kft', 'knc', 'witchwood', 'boomsday', 'rastakhan',
                          'ros', 'uldum', 'dragons', 'outland', 'scholomance', 'darkmoon',
                          'barrens', 'stormwind', 'alterac', 'sunken', 'nathria', 'lich',
                          'titans', 'badlands', 'whizbang', 'great_dark_beyond', 'perils',
                          'space', 'core']:
                try:
                    module = importlib.import_module(f"card_effects.{folder}.effect_{card_id}")
                    # Look for the event handler in the module
                    handler_name = f"on_{event_type}"
                    if hasattr(module, handler_name):
                        return getattr(module, handler_name)
                except ImportError:
                    continue
            return None
        except Exception:
            return None

    def _get_effect_handler(self, card_id: str, handler_name: str) -> Optional[Callable]:
        """Get a specific effect handler for a card (spellburst, frenzy, etc.)."""
        try:
            import importlib
            
            folders = ['classic', 'basic', 'naxx', 'gvg', 'tgt', 'wog', 'msg', 
                      'ungoro', 'kft', 'knc', 'witchwood', 'boomsday', 'rastakhan',
                      'ros', 'uldum', 'dragons', 'outland', 'scholomance', 'darkmoon',
                      'barrens', 'stormwind', 'alterac', 'sunken', 'nathria', 'lich',
                      'titans', 'badlands', 'whizbang', 'great_dark_beyond', 'perils',
                      'space', 'core', 'time_travel', 'starcraft']
            
            for folder in folders:
                try:
                    module = importlib.import_module(f"card_effects.{folder}.effect_{card_id}")
                    if hasattr(module, handler_name):
                        return getattr(module, handler_name)
                except ImportError:
                    continue
            return None
        except Exception:
            return None

    @property
    def current_player(self) -> Player:
        """Get the current player."""
        return self.players[self.current_player_idx]
    
    @property
    def opponent(self) -> Player:
        """Get the opponent of the current player."""
        return self.players[1 - self.current_player_idx]
    
    def get_opponent(self, player: Player) -> Player:
        """Get the opponent of a specific player."""
        return player.opponent
    
    @property
    def ended(self) -> bool:
        """Check if the game has ended."""
        return self.phase == GamePhase.GAME_OVER
    
    @property
    def winner(self) -> Optional[Player]:
        """Get the winner, if any."""
        for player in self.players:
            if player.play_state == PlayState.WON:
                return player
        return None
    
    def setup(self, player1: Player, player2: Player) -> None:
        """Setup a new game with two players."""
        self.players = [player1, player2]
        
        # Link players
        player1.game = self
        player2.game = self
        player1.opponent = player2
        player2.opponent = player1
        
        # Randomly decide who goes first
        if random.random() < 0.5:
            self.players = [player2, player1]
        
        # Give second player The Coin (using create_card to Ensure effects are loaded)
        from .factory import create_card
        coin = create_card("GAME_005", self.players[1])
        self.players[1].add_to_hand(coin)
        
        self.phase = GamePhase.MULLIGAN
    
    def start_mulligan(self) -> None:
        """Start the mulligan phase."""
        # Draw starting hands
        self.players[0].draw(Player.STARTING_HAND_FIRST)
        self.players[1].draw(Player.STARTING_HAND_SECOND)
        
        for player in self.players:
            player.mulligan_state = Mulligan.INPUT
    
    def do_mulligan(self, player: Player, cards_to_replace: List[Card]) -> None:
        """Process mulligan for a player."""
        if player.mulligan_state != Mulligan.INPUT:
            return
        
        # Put cards back in deck
        for card in cards_to_replace:
            if card in player.hand:
                player.hand.remove(card)
                player.deck.append(card)
        
        player.shuffle_deck()
        
        # Draw new cards
        player.draw(len(cards_to_replace))
        
        player.mulligan_state = Mulligan.DONE
        
        # Check if both players done
        if all(p.mulligan_state == Mulligan.DONE for p in self.players):
            self.start_game()
    
    def skip_mulligan(self) -> None:
        """Skip mulligan for all players (keep all cards)."""
        for player in self.players:
            player.mulligan_state = Mulligan.DONE
        self.start_game()
    
    def start_game(self) -> None:
        """Start the main game."""
        self.phase = GamePhase.MAIN_ACTION
        self.turn = 1
        self.current_player_idx = 0
        
        # === START OF GAME: Trigger effects for cards in deck/hand ===
        for player in self.players:
            # Check deck and hand for Start of Game cards
            all_potential_cards = player.deck + player.hand
            for card in all_potential_cards:
                if card.data.start_of_game:
                    handler = self._get_effect_handler(card.card_id, "on_start_of_game")
                    if handler:
                        handler(self, player, card)
        
        # First player starts their turn
        self.fire_event("on_turn_start", self.current_player)
        self.current_player.start_turn()
        self.step = Step.MAIN_ACTION
    
    def end_turn(self) -> None:
        """End the current player's turn."""
        self.fire_event("on_turn_end", self.current_player)
        self.current_player.end_turn()
        
        # Process any pending deaths
        self.process_deaths()
        
        # Switch player
        self.current_player_idx = 1 - self.current_player_idx
        self.turn += 1
        self.actions_this_turn = 0
        
        # Check turn limit
        if self.turn > self.config.max_turns:
            self._end_game_draw()
            return
        
        # Reset turn trackers
        self.current_player.damage_taken_this_turn = 0
        self.current_player.healing_taken_this_turn = 0
        self.current_player.cards_played_this_turn = 0
        self.current_player.minions_played_this_turn = 0
        self.current_player.spells_played_this_turn = 0
        self.current_player.hero_power_uses_this_turn = 0
        
        # === ELEMENTAL SYNERGY: Track for next turn ===
        ending_player = self.players[1 - self.current_player_idx]  # Player who just ended
        ending_player.elementals_played_last_turn = ending_player.elementals_played_this_turn
        ending_player.elementals_played_this_turn = 0
        
        # === ECHO: Remove echo copies from hand ===
        for player in self.players:
            player.hand = [c for c in player.hand if not getattr(c, '_echo_copy', False)]
        
        # Start next player's turn
        self.fire_event("on_turn_start", self.current_player)
        self.current_player.start_turn()
        
        # Check for death after draw (fatigue)
        self.process_deaths()
        self.check_for_game_over()
    
    def play_card(
        self, 
        card: Card, 
        target: Optional[Card] = None, 
        position: int = -1,
        choose_option: int = 0
    ) -> bool:
        """Play a card from hand."""
        player = self.current_player
        
        if not player.can_play_card(card):
            return False
        
        # Spend mana
        if not player.spend_mana(card.cost):
            return False
        
        # Remove from hand
        player.remove_from_hand(card)
        
        return self._finish_play_card(player, card, target, position, is_echo, is_quickdraw, is_outcast)

    def trade_card(self, card: Card) -> bool:
        """Trade a card from hand for 1 mana."""
        player = self.current_player
        if not card.data.tradeable or player.mana < 1:
            return False
            
        player.mana -= 1
        player.remove_from_hand(card)
        player.add_to_deck(card)
        player.shuffle_deck()
        player.draw(1)
        
        self._log_action("trade_card", {"card": card.card_id})
        return True

    def forge_card(self, card: Card) -> bool:
        """Forge a card from hand for 2 mana."""
        player = self.current_player
        if not card.data.forge or player.mana < 2:
            return False
            
        player.mana -= 2
        # Transform card in hand to its forged version
        from .factory import create_card
        forged = create_card(card.data.forged_version, player)
        if forged:
            idx = player.hand.index(card)
            player.hand[idx] = forged
            forged._forged = True
            self._log_action("forge_card", {"card": card.card_id, "forged_into": forged.card_id})
            return True
        return False

    def use_titan_ability(self, titan: Card, ability_idx: int, target: Optional[Card] = None) -> bool:
        """Use one of the 3 Titan abilities."""
        if not titan.data.titan or titan.attacks_this_turn > 0:
            return False
            
        if ability_idx >= len(titan.data.titan_abilities):
            return False
            
        ability_id = titan.data.titan_abilities[ability_idx]
        if ability_id in titan.titan_abilities_used:
            return False
            
        # Trigger ability effect
        handler = self._get_effect_handler(titan.card_id, f"titan_ability_{ability_idx}")
        if handler:
            handler(self, titan.controller, titan, target=target)
            
        titan.titan_abilities_used.append(ability_id)
        titan.attacks_this_turn += 1
        titan.exhausted = True # Titan is exhausted after using ability
        
        # If all abilities used, Titan can attack normally from next turn
        if len(titan.titan_abilities_used) >= 3:
            # Maybe set a flag or just let it attack normally next turn
            pass
            
        self._log_action("titan_ability", {"titan": titan.card_id, "ability": ability_id})
        return True

    def _finish_play_card(self, player, card, target, position, is_echo, is_quickdraw, is_outcast) -> bool:
        """Internal helper to finish the play card logic."""
        
        # Log action
        self._log_action("play_card", {
            "card": card.card_id,
            "target": target.card_id if target else None,
            "position": position
        })
        
        
        player.cards_played_this_turn += 1
        player.combo_cards_played += 1
        player.cards_played_this_game.append(card.card_id)
        self.fire_event("on_card_played", card, target)
        
        # Store echo flag before playing (card might be modified)
        is_echo = card.data.echo
        
        # Track elementals for synergy
        if card.data.race and 'ELEMENTAL' in str(card.data.race):
            player.elementals_played_this_turn += 1
            
        # === OUTCAST: Check position in hand ===
        # Must be leftmost (index 0) or rightmost (last index)
        hand_idx = player.hand.index(card) if card in player.hand else -1
        is_outcast = (hand_idx == 0 or hand_idx == len(player.hand) - 1)
        card._outcast_active = is_outcast
        
        # === QUICKDRAW: Check if added to hand this turn ===
        is_quickdraw = getattr(card, 'turn_added_to_hand', -1) == self.turn
        card._quickdraw_active = is_quickdraw
        
        if card.card_type == CardType.MINION:
            result = self._play_minion(card, target, position)
        elif card.card_type == CardType.SPELL:
            player.spells_played_this_game.append(card.card_id)
            player.spells_played_this_turn += 1
            result = self._play_spell(card, target)
        elif card.card_type == CardType.WEAPON:
            result = self._play_weapon(card)
        elif card.card_type == CardType.HERO:
            result = self._play_hero(card)
        elif card.card_type == CardType.LOCATION:
            result = self._play_location(card, position)
        else:
            return False
        
        # === MINIATURIZE: Add 1/1 copy to hand ===
        if result and card.data.miniaturize and len(player.hand) < 10:
            from simulator.factory import create_card
            mini_copy = create_card(card.card_id, self)
            if mini_copy:
                mini_copy._attack = 1
                mini_copy._health = 1
                mini_copy._max_health = 1
                mini_copy._cost = 1
                mini_copy.mini = True
                player.add_to_hand(mini_copy)
        
        # === ECHO: Add a copy back to hand ===
        if result and is_echo and len(player.hand) < 10:
            from simulator.factory import create_card
            echo_copy = create_card(card.card_id, self)
            if echo_copy:
                echo_copy._echo_copy = True  # Mark as echo copy (disappears at end of turn)
                player.add_to_hand(echo_copy)
        
        # === CORRUPT: Upgrade cards in hand with lower cost ===
        if result:
            played_cost = card.data.cost
            for hand_card in player.hand:
                if hand_card.data.corrupt and hand_card.data.corrupted_version:
                    if played_cost > hand_card.data.cost and not getattr(hand_card, '_corrupted', False):
                        # Transform into corrupted version
                        corrupted = create_card(hand_card.data.corrupted_version, self)
                        if corrupted:
                            idx = player.hand.index(hand_card)
                            player.hand[idx] = corrupted
                            corrupted._corrupted = True
        
        return result
    
    def _play_minion(
        self, 
        card: Card, 
        target: Optional[Card] = None, 
        position: int = -1
    ) -> bool:
        """Play a minion card."""
        minion = card if isinstance(card, Minion) else Minion(card.data, self)
        player = self.current_player
        
        # === MAGNETIC: Check if played to the left of a Mech ===
        if minion.data.magnetic and position != -1 and position < len(player.board):
            target_mech = player.board[position]
            if target_mech.data.race and 'MECH' in str(target_mech.data.race):
                # Fuse into the target mech
                target_mech._attack += minion.attack
                target_mech._health += minion.health
                target_mech._max_health += minion.max_health
                # Transfer keywords
                if minion.taunt: target_mech._taunt = True
                if minion.divine_shield: target_mech._divine_shield = True
                if minion.rush: target_mech._rush = True
                if minion.lifesteal: target_mech._lifesteal = True
                if minion.poisonous: target_mech._poisonous = True
                if minion.windfury: target_mech._windfury = True
                
                # Magnetic play is successful but doesn't summon a new entity
                self.fire_event("on_minion_played", minion)
                return True
        
        if not player.summon(minion, position):
            return False
        
        player.minions_played_this_turn += 1
        player.minions_played_this_game_list.append(minion.card_id)
        self.fire_event("on_minion_summon", minion)
        
        # === COLOSSAL: Summon appendages ===
        if card.data.colossal and card.data.colossal_appendages:
            for appendage_id in card.data.colossal_appendages:
                if len(player.board) >= 7:
                    break
                from simulator.factory import create_card
                appendage = create_card(appendage_id, self)
                if appendage:
                    app_minion = Minion(appendage.data, self) if not isinstance(appendage, Minion) else appendage
                    app_minion.controller = player
                    player.summon(app_minion)
        
        # === TRIGGER SECRETS AFTER SUMMON ===
        # Check for minion-played secrets (e.g., Mirror Entity, Snipe, Potion of Polymorph)
        self.trigger_secrets("minion_played", player, minion=minion)
        
        # Check if minion is still alive after secret (e.g., Snipe killed it)
        if minion.health <= 0:
            self.process_deaths()
            return True
        
        # Trigger battlecry
        if card.data.battlecry:
            self._trigger_battlecry(minion, target)
        
        # Process deaths
        self.process_deaths()
        self.check_for_game_over()
        
        return True
    
    def _play_spell(self, card: Card, target: Optional[Card] = None) -> bool:
        """Play a spell card."""
        player = self.current_player
        player.spells_played_this_turn += 1
        
        # === TRIGGER SECRETS BEFORE SPELL EFFECT ===
        # Check for spell-triggered secrets (e.g., Counterspell, Spellbender)
        triggered = self.trigger_secrets("spell_cast", player, spell=card, target=target)
        
        # If Counterspell triggered, the spell is countered
        if triggered and triggered.card_id in ["EX1_287", "CORE_EX1_287"]:  # Counterspell IDs
            # Move to graveyard without effect
            card.zone = Zone.GRAVEYARD
            player.graveyard.append(card)
            return True
        
        # Trigger spell effect
        if card.card_id in self._battlecry_handlers:
            self._battlecry_handlers[card.card_id](self, card, target)
        
        # === SPELLBURST: Trigger friendly minions with Spellburst ===
        for minion in player.board:
            if minion.data.spellburst and not minion._spellburst_triggered:
                handler = self._get_effect_handler(minion.card_id, "on_spellburst")
                if handler:
                    handler(self, player, minion, spell=card)
                minion._spellburst_triggered = True  # One-time trigger
        
        # Fire event for Quest advancement
        self.fire_event("on_spell_cast", player, card)
        player.spells_played_this_game.append(card.card_id)
        
        # === TWINSPELL: Add copy back to hand (without twinspell) ===
        is_twinspell = card.data.twinspell and not getattr(card, '_is_twinspell_copy', False)
        if is_twinspell and len(player.hand) < 10:
            from simulator.factory import create_card
            twin_copy = create_card(card.card_id, self)
            if twin_copy:
                twin_copy._is_twinspell_copy = True  # Second cast doesn't twinspell
                twin_copy.data = twin_copy.data  # Keep same data but mark as copy
                player.add_to_hand(twin_copy)
        
        # Move to graveyard
        card.zone = Zone.GRAVEYARD
        player.graveyard.append(card)
        
        # === OVERLOAD: Lock mana next turn ===
        if card.data.overload_value > 0:
            player.overload_next_turn += card.data.overload_value
        
        # Process deaths
        self.process_deaths()
        self.check_for_game_over()
        
        return True
    
    def _play_weapon(self, card: Card) -> bool:
        """Equip a weapon."""
        weapon = card if isinstance(card, Weapon) else Weapon(card.data, self)
        self.current_player.equip_weapon(weapon)
        return True
    
    def _play_hero(self, card: Card) -> bool:
        """Play a hero card (replaces current hero)."""
        # Hero cards are complex - simplified for now
        return True
    
    def _play_location(self, card: Card, position: int = -1) -> bool:
        """Play a location card."""
        player = self.current_player
        
        if not player.summon(card, position):
            return False
        
        return True
    
    def attack(self, attacker: Card, defender: Card) -> bool:
        """Execute an attack."""
        player = self.current_player
        
        # Validate attack
        if not attacker.can_attack():
            return False
        
        valid_targets = player.get_valid_attack_targets(attacker)
        if defender not in valid_targets:
            return False
        
        # Log action
        self._log_action("attack", {
            "attacker": attacker.card_id,
            "defender": defender.card_id
        })
        
        # Remove stealth
        if attacker.stealth:
            attacker._stealth = False
        
        # Increment attack counter
        attacker.attacks_this_turn += 1
        
        # === TRIGGER SECRETS BEFORE ATTACK ===
        # Check for attack-triggered secrets (e.g., Explosive Trap, Misdirection)
        self.trigger_secrets("attack", player, attacker=attacker, defender=defender)
        
        # Check if attacker is still alive after secret
        if not attacker or (hasattr(attacker, 'health') and attacker.health <= 0):
            self.process_deaths()
            return True
        
        # Check for hero-attacked secrets (e.g., Ice Barrier, Vaporize)
        if defender.card_type == CardType.HERO:
            self.trigger_secrets("hero_attacked", player, attacker=attacker, defender=defender)
            # Re-check attacker health after secret
            if hasattr(attacker, 'health') and attacker.health <= 0:
                self.process_deaths()
                return True
        
        # Calculate damage
        attacker_damage = attacker.attack
        defender_damage = defender.attack
        
        # Deal damage
        self.deal_damage(defender, attacker_damage, attacker)
        
        # Defender hits back (unless attacking a hero with a weapon)
        if defender.card_type != CardType.HERO or not isinstance(attacker, Hero):
            self.deal_damage(attacker, defender_damage, defender)
        
        # Weapon loses durability
        if isinstance(attacker, Hero) and attacker.weapon:
            attacker.weapon.lose_durability()
        
        # Process deaths
        self.process_deaths()
        self.check_for_game_over()
        
        return True
    
    def deal_damage(
        self, 
        target: Card, 
        amount: int, 
        source: Optional[Card] = None
    ) -> int:
        """Deal damage to a target."""
        if target.immune or target.dormant > 0:
            return 0
        
        # Divine Shield absorbs damage
        if target.divine_shield:
            target._divine_shield = False
            self.fire_event("on_divine_shield_lost", target)
            return 0
        
        # Deal damage
        if isinstance(target, Hero):
            actual_damage = target.take_damage(amount)
        else:
            target._damage += amount
            actual_damage = amount
        
        if actual_damage > 0:
            if isinstance(target, Hero) and target.controller:
                target.controller.damage_taken_this_turn += actual_damage
            self.fire_event("on_damage_taken", target, actual_damage, source)
        
        # Freeze
        if source and source.has_tag(GameTag.FROZEN) or getattr(source, 'freezes', False):
            target.frozen = True
            
        # Lifesteal
        if source and source.lifesteal and source.controller:
            source.controller.hero.take_damage(-actual_damage)  # Heal
        
        # Poisonous kills minions
        if source and source.poisonous and target.card_type == CardType.MINION:
            target.destroy()
        
        # === FRENZY: Trigger once when minion takes damage ===
        if target.card_type == CardType.MINION and target.data.frenzy and not target._frenzy_triggered:
            if actual_damage > 0 and target.health > 0:  # Must survive the damage
                handler = self._get_effect_handler(target.card_id, "on_frenzy")
                if handler and target.controller:
                    handler(self, target.controller, target)
                target._frenzy_triggered = True
        
        # === OVERKILL: Trigger when excess damage kills target ===
        if source and source.data.overkill and target.card_type == CardType.MINION:
            if target.health <= 0:  # Target is dead
                excess_damage = -target.health  # How much overkill
                if excess_damage >= 0:
                    handler = self._get_effect_handler(source.card_id, "on_overkill")
                    if handler and source.controller:
                        handler(self, source.controller, source, excess=excess_damage)
        
        # === HONORABLE KILL: Trigger when exact lethal damage (no excess) ===
        if source and source.data.honorable_kill and target.card_type == CardType.MINION:
            if target.health == 0:  # Exactly lethal
                handler = self._get_effect_handler(source.card_id, "on_honorable_kill")
                if handler and source.controller:
                    handler(self, source.controller, source, target=target)
        
        return actual_damage
    
    def heal(self, target: Card, amount: int, source: Card = None) -> int:
        """Heal a target."""
        if target.dormant > 0:
            return 0
        
        # Calculate overheal (amount that would go past full health)
        current_damage = getattr(target, '_damage', 0) if hasattr(target, '_damage') else 0
        potential_overheal = max(0, amount - current_damage)
            
        if target.card_type == CardType.HERO and isinstance(target, Hero):
            healed = min(amount, target.damage)
            target._damage -= healed
            if healed > 0 and target.controller:
                target.controller.healing_taken_this_turn += healed
            
            # === OVERHEAL: Trigger if healing past full ===
            if potential_overheal > 0 and source and source.data.overheal:
                handler = self._get_effect_handler(source.card_id, "on_overheal")
                if handler and target.controller:
                    handler(self, target.controller, source, overheal=potential_overheal)
            
            return healed
        elif isinstance(target, Card):
            healed = min(amount, target.damage)
            target._damage -= healed
            
            # === OVERHEAL: Trigger for minions too ===
            if potential_overheal > 0 and source and source.data.overheal:
                handler = self._get_effect_handler(source.card_id, "on_overheal")
                if handler and target.controller:
                    handler(self, target.controller, source, overheal=potential_overheal)
            
            return healed
        return 0
    
    def destroy(self, entity: Card) -> None:
        """Mark an entity for destruction."""
        if entity not in self._pending_deaths:
            self._pending_deaths.append(entity)
    
    def silence(self, target: Card) -> None:
        """
        Silence a minion - removes all card text and enchantments.
        Resets to base stats, removes keywords and abilities.
        """
        if target.card_type != CardType.MINION:
            return
        
        target.silenced = True
        
        # Reset keywords to False
        target._taunt = False
        target._divine_shield = False
        target._stealth = False
        target._poisonous = False
        target._lifesteal = False
        target._windfury = False
        target._reborn = False
        target._rush = False
        target._charge = False
        
        # Remove frozen/immune states
        target.frozen = False
        target.immune = False
        target.cant_attack = False
        target.cant_be_targeted = False
        
        # Remove any buff/debuff enchantments (reset to base stats)
        # Note: We keep current damage, but reset attack/health buffs
        base_attack = target.data.attack
        base_health = target.data.health
        current_damage = target._damage
        
        target._attack = base_attack
        target._max_health = base_health
        target._health = base_health
        target._damage = min(current_damage, base_health - 1)  # Can't silence to death
        
        # Clear all triggers registered by this minion
        self.unregister_triggers(target)
        
        self.fire_event("on_silence", target)

    
    def process_deaths(self) -> None:
        """Process all pending deaths."""
        while self._pending_deaths or any(
            m.is_dead() for p in self.players for m in p.board
        ):
            # Check for new deaths
            for player in self.players:
                for minion in player.board[:]:
                    if minion.is_dead() and minion not in self._pending_deaths:
                        self._pending_deaths.append(minion)
            
            if not self._pending_deaths:
                break
            
            # Process deaths in order
            deaths = self._pending_deaths[:]
            self._pending_deaths.clear()
            
            for entity in deaths:
                if entity.controller:
                    # Remove from board
                    entity.controller.remove_from_board(entity)
                    
                    # Trigger deathrattle
                    if entity.data.deathrattle and not entity.silenced:
                        self._trigger_deathrattle(entity)
                    
                    # Handle reborn
                    if entity.reborn and not entity.silenced:
                        self._handle_reborn(entity)
                    
                    # Move to graveyard
                    entity.zone = Zone.GRAVEYARD
                    entity.controller.graveyard.append(entity)
                    if entity.card_type == CardType.MINION:
                        entity.controller.dead_minions.append(entity.card_id)
                        
                        # === CORPSE: Death Knight gains a corpse ===
                        entity.controller.corpses += 1
                        
                        # === STARSHIP: Components are added to storage ===
                        if entity.data.starship_piece:
                            entity.controller.starship_pieces.append(entity.card_id)
                        
                        # === INFUSE: Advance infuse on cards in hand ===
                        for card in entity.controller.hand:
                            if card.data.infuse and not card._infused:
                                card._infuse_progress += 1
                                if card._infuse_progress >= card.data.infuse_cost:
                                    card._infused = True
                                    # Trigger infuse transformation
                                    handler = self._get_effect_handler(card.card_id, "on_infuse")
                                    if handler:
                                        handler(self, entity.controller, card)
                        
                        self.fire_event("on_minion_death", entity)
    
    def _trigger_battlecry(self, minion: Card, target: Optional[Card]) -> None:
        """Trigger a battlecry effect."""
        if minion.card_id in self._battlecry_handlers:
            self._battlecry_handlers[minion.card_id](self, minion, target)
    
    def _trigger_deathrattle(self, minion: Card) -> None:
        """Trigger a deathrattle effect."""
        if minion.card_id in self._deathrattle_handlers:
            self._deathrattle_handlers[minion.card_id](self, minion)
    
    def _handle_reborn(self, minion: Card) -> None:
        """Handle reborn mechanic."""
        # Create a copy with 1 health and no reborn
        new_data = CardData(
            card_id=minion.card_id,
            name=minion.name,
            cost=minion.data.cost,
            attack=minion.data.attack,
            health=1,  # Reborn with 1 health
            card_type=CardType.MINION,
            taunt=minion.data.taunt,
            divine_shield=minion.data.divine_shield,
            # No reborn on reborn copy
        )
        reborn_minion = Minion(new_data, self)
        reborn_minion._reborn = False  # Can't reborn again
        
        if minion.controller:
            minion.controller.summon(reborn_minion, minion.zone_position)
    
    def summon_token(self, player: Player, card_id: str, position: int = -1) -> Optional[Minion]:
        """Summon a token/minion for a player."""
        from .card_loader import create_card
        card = create_card(card_id, self)
        if isinstance(card, Minion):
            if player.summon(card, position):
                return card
        return None

    def use_hero_power(self, target: Optional[Card] = None) -> bool:
        """Use the hero power."""
        player = self.current_player
        hero_power = player.hero_power
        
        if not hero_power or not hero_power.can_use():
            return False
        
        if not player.spend_mana(hero_power.cost):
            return False
        
        hero_power.used_this_turn = True
        
        # Log action
        self._log_action("hero_power", {
            "target": target.card_id if target else None
        })
        
        # Trigger effect
        if hero_power.card_id in self._battlecry_handlers:
            self._battlecry_handlers[hero_power.card_id](self, hero_power, target)
        
        # Process deaths
        self.process_deaths()
        self.check_for_game_over()
        
        return True
    
    def check_for_game_over(self) -> bool:
        """Check if the game is over."""
        dead_players = [p for p in self.players if p.hero and p.hero.health <= 0]
        
        if len(dead_players) == 2:
            # Draw
            self._end_game_draw()
            return True
        elif len(dead_players) == 1:
            # One winner
            loser = dead_players[0]
            winner = self.players[1 - self.players.index(loser)]
            self._end_game(winner)
            return True
        
        return False
    
    def _end_game(self, winner: Player) -> None:
        """End the game with a winner."""
        self.phase = GamePhase.GAME_OVER
        winner.play_state = PlayState.WON
        winner.opponent.play_state = PlayState.LOST
    
    def _end_game_draw(self) -> None:
        """End the game in a draw."""
        self.phase = GamePhase.GAME_OVER
        for player in self.players:
            player.play_state = PlayState.TIED
    
    def concede(self, player: Player) -> None:
        """Player concedes the game."""
        player.play_state = PlayState.CONCEDED
        winner = player.opponent
        self._end_game(winner)
    
    def _log_action(self, action_type: str, data: Dict[str, Any]) -> None:
        """Log an action for replay/training."""
        self.action_history.append({
            "turn": self.turn,
            "player": self.current_player_idx,
            "type": action_type,
            "data": data
        })
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current game state as a dictionary."""
        return {
            "turn": self.turn,
            "phase": self.phase.name,
            "current_player": self.current_player_idx,
            "ended": self.ended,
            "players": [
                {
                    "name": p.name,
                    "health": p.health,
                    "armor": p.armor,
                    "mana": p.mana,
                    "mana_crystals": p.mana_crystals,
                    "hand_size": len(p.hand),
                    "deck_size": len(p.deck),
                    "board": [
                        {"name": m.name, "attack": m.attack, "health": m.health}
                        for m in p.board
                    ]
                }
                for p in self.players
            ]
        }
    
    def __repr__(self) -> str:
        return f"<Game Turn:{self.turn} Phase:{self.phase.name}>"
