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

    # Class to Hero ID mapping
    CLASS_TO_HERO = {
        "WARRIOR": "HERO_01", "SHAMAN": "HERO_02", "ROGUE": "HERO_03",
        "PALADIN": "HERO_04", "HUNTER": "HERO_05", "DRUID": "HERO_06",
        "WARLOCK": "HERO_07", "MAGE": "HERO_08", "PRIEST": "HERO_09",
        "DEATHKNIGHT": "HERO_10", "DEMONHUNTER": "HERO_10a"
    }

    def reset(self, deck1=None, deck2=None, class1=None, class2=None, randomize_first=True) -> GameState:
        # Use Meta decks, Arena decks, or fallback
        if deck1 is None or deck2 is None:
            # 50% chance of Meta deck, 50% chance of Arena deck
            if random.random() > 0.5:
                c1, d1, _ , _ = DeckGenerator.get_random_meta_deck()
            else:
                c1, d1, _ = DeckGenerator.get_arena_deck()
                
            if random.random() > 0.5:
                c2, d2, _, _ = DeckGenerator.get_random_meta_deck()
            else:
                c2, d2, _ = DeckGenerator.get_arena_deck()
        else:
            c1, d1, c2, d2 = class1 or "MAGE", deck1, class2 or "WARRIOR", deck2
        
        p1, p2 = Player("P1"), Player("P2")
        self._game = Game()
        self._game.setup(p1, p2)
        
        # === CREATE HEROES ===
        hero1_id = self.CLASS_TO_HERO.get(c1.upper(), "HERO_08")
        hero2_id = self.CLASS_TO_HERO.get(c2.upper(), "HERO_08")
        
        p1.hero = create_card(hero1_id, self._game)
        if p1.hero:
            p1.hero.controller = p1
            p1.hero._max_health = 30
            p1.hero._damage = 0
        
        p2.hero = create_card(hero2_id, self._game)
        if p2.hero:
            p2.hero.controller = p2
            p2.hero._max_health = 30
            p2.hero._damage = 0
        
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
        # Initialize health tracking for reward shaping
        self._prev_my_health = 30
        self._prev_enemy_health = 30
        return self.get_state()

    def get_state(self) -> GameState:
        return GameState.from_simulator_game(self.game, self.perspective)
    
    def get_action_mask(self) -> np.ndarray:
        """Returns a binary mask of valid actions for the current state."""
        mask = np.zeros(ACTION_SPACE_SIZE, dtype=np.float32)
        valid_actions = self.get_valid_actions()
        for action in valid_actions:
            idx = action.to_index()
            if 0 <= idx < ACTION_SPACE_SIZE:
                mask[idx] = 1.0
        return mask
    
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
        
        # === REWARD SHAPING ===
        # Primary goal: KILL THE ENEMY HERO
        # Victory = +1.0, Defeat = -1.0
        # Intermediate rewards to guide learning:
        #   - Damage to enemy hero: small positive reward
        #   - Taking damage: small negative reward
        
        my_p = self.game.players[0] if self.perspective == 1 else self.game.players[1]
        enemy_p = my_p.opponent
        
        reward = 0.0
        
        if done:
            # Terminal rewards (most important)
            if self.game.winner == my_p:
                reward = 1.0  # VICTORY - highest reward
            elif self.game.winner is not None:
                reward = -1.0  # DEFEAT - highest penalty
            # Draw = 0.0
        else:
            # Intermediate reward shaping (small values to not overshadow win/loss)
            # Track health changes from last step
            my_health = my_p.hero.health if my_p.hero else 0
            enemy_health = enemy_p.hero.health if enemy_p.hero else 0
            
            # Store previous health for comparison
            prev_my_health = getattr(self, '_prev_my_health', 30)
            prev_enemy_health = getattr(self, '_prev_enemy_health', 30)
            
            # Reward for dealing damage to enemy hero
            enemy_damage_dealt = prev_enemy_health - enemy_health
            if enemy_damage_dealt > 0:
                reward += enemy_damage_dealt * 0.02  # +0.02 per damage to enemy hero
            
            # Small penalty for taking damage (encourages efficient trades)
            my_damage_taken = prev_my_health - my_health
            if my_damage_taken > 0:
                reward -= my_damage_taken * 0.005  # -0.005 per damage taken
            
            # Update tracking
            self._prev_my_health = my_health
            self._prev_enemy_health = enemy_health
                
        return self.get_state(), reward, done, {}

def play_random_game(verbose: bool = False) -> int:
    env = HearthstoneGame()
    env.reset()
    while not env.is_game_over and env._step_count < 200:
        actions = env.get_valid_actions()
        if not actions: break
        env.step(random.choice(actions))
    return 1 if env.game.winner == env.game.players[0] else (2 if env.game.winner == env.game.players[1] else 0)
