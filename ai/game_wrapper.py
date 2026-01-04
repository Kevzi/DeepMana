"""
Fireplace game wrapper for DeepMana AI. Optimized for speed.
"""
from typing import List, Optional, Tuple, Any, Dict
import random
import numpy as np

from .game_state import GameState
from .actions import Action, ActionType, ACTION_SPACE_SIZE
from .card import CardInstance

from simulator import Game, Player, CardDatabase, create_card, Hero, CardType, CardData
from simulator.deck_generator import DeckGenerator

class HearthstoneGame:
    def __init__(self, perspective: int = 1):
        self.perspective = perspective
        self._game: Optional[Game] = None
        self._step_count = 0
        self._max_steps = 500
        self._cache = {} # Action cache for MCTS
        # Pre-load DB on init
        CardDatabase.get_instance().load()

    @property
    def game(self) -> Game:
        if self._game is None: raise RuntimeError("Reset first.")
        return self._game

    @property
    def current_player(self) -> Player: return self.game.current_player

    @property
    def is_game_over(self) -> bool: return self.game.ended

    def reset(self, deck1=None, deck2=None, class1=None, class2=None, randomize_first=True) -> GameState:
        # Use Meta decks or fallback
        if deck1 is None or deck2 is None:
            c1, d1, _, _ = DeckGenerator.get_random_meta_deck()
            c2, d2, _, _ = DeckGenerator.get_random_meta_deck()
        else:
            c1, d1, c2, d2 = class1 or "MAGE", deck1, class2 or "WARRIOR", deck2
        
        p1, p2 = Player("P1"), Player("P2")
        self._game = Game()
        self._game.setup(p1, p2)
        
        for cid in d1:
            c = create_card(cid, self._game)
            if c: p1.add_to_deck(c)
        for cid in d2:
            c = create_card(cid, self._game)
            if c: p2.add_to_deck(c)
            
        p1.shuffle_deck()
        p2.shuffle_deck()
        self._game.start_mulligan()
        self._game.start_game()
        self._step_count = 0
        self._cache = {}
        return self.get_state()

    def get_state(self) -> GameState:
        return GameState.from_simulator_game(self.game, self.perspective)
    
    def get_valid_actions(self) -> List[Action]:
        if self.is_game_over: return []
        
        # State-based cache key
        p = self.current_player
        state_key = f"{self.game.turn}_{self.game.current_player_idx}_{len(p.hand)}_{len(p.board)}_{p.mana}"
        if state_key in self._cache: return self._cache[state_key]

        actions = []
        
        # 1. Play cards
        for i, card in enumerate(p.hand):
            if p.can_play_card(card):
                targets = p.get_valid_targets(card)
                if targets:
                    for t in targets:
                        # Find target index
                        is_friendly = (t.controller == p)
                        target_idx = -1
                        if t.card_type == CardType.MINION:
                            target_idx = t.controller.board.index(t)
                        
                        act = Action.play_card(i, target_idx, is_friendly)
                        act._sim_action = ("play", card, t)
                        actions.append(act)
                        break # Limit exploration speed
                else:
                    act = Action.play_card(i)
                    act._sim_action = ("play", card, None)
                    actions.append(act)
                    
        # 2. Minion Attacks
        for i, m in enumerate(p.board):
            if m.can_attack():
                targets = p.get_valid_attack_targets(m)
                for t in targets:
                    # Target index (relative to enemy board if minion)
                    is_hero = (t.card_type == CardType.HERO)
                    target_idx = -1 if is_hero else p.opponent.board.index(t)
                    
                    act = Action.attack(i, target_idx)
                    act._sim_action = ("attack", m, t)
                    actions.append(act)
                    if is_hero: break # Prioritize face
                    
        # 3. Hero Attack
        if p.hero and p.hero.can_attack():
            targets = p.get_valid_attack_targets(p.hero)
            for t in targets:
                is_hero = (t.card_type == CardType.HERO)
                target_idx = -1 if is_hero else p.opponent.board.index(t)
                act = Action.attack(-1, target_idx)
                act._sim_action = ("attack", p.hero, t)
                actions.append(act)
                if is_hero: break
                
        # 4. Hero Power
        if p.hero_power and p.hero_power.can_use():
            act = Action.hero_power()
            act._sim_action = ("hero_power", p.hero_power, None)
            actions.append(act)
            
        actions.append(Action.end_turn())
        self._cache[state_key] = actions
        return actions

    def step(self, action: Action) -> Tuple[GameState, float, bool, Dict[str, Any]]:
        self._step_count += 1
        self._cache = {} # Clear cache
        try:
            op, ent, target = getattr(action, '_sim_action', (None, None, None))
            if action.action_type == ActionType.END_TURN: 
                self.game.end_turn()
            elif op == "play": 
                self.game.play_card(ent, target=target)
            elif op == "attack": 
                self.game.attack(ent, target)
            elif op == "hero_power": 
                self.game.use_hero_power(target=target)
            else:
                # Direct index fallback
                valid = self.get_valid_actions()
                for v in valid:
                    if v.to_index() == action.to_index():
                        return self.step(v)
        except: pass
        
        done = self.is_game_over
        # Perspective-aware reward
        reward = 0.0
        if done:
            my_p = self.game.players[0] if self.perspective == 1 else self.game.players[1]
            if self.game.winner == my_p:
                reward = 1.0
            elif self.game.winner is not None:
                reward = -1.0
                
        return self.get_state(), reward, done, {}

def play_random_game(verbose: bool = False) -> int:
    env = HearthstoneGame()
    env.reset()
    while not env.is_game_over and env._step_count < 200:
        actions = env.get_valid_actions()
        if not actions: break
        env.step(random.choice(actions))
    return 1 if env.game.winner == env.game.players[0] else (2 if env.game.winner == env.game.players[1] else 0)
