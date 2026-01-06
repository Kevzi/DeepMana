"""League Training System - AlphaStar style.

This module implements population-based training to avoid meta-game cycles.
Key concepts:
- Main Agents: The agents we're optimizing
- Exploiters: Agents that find weaknesses in Main Agents
- Historical Pool: Past versions to prevent forgetting

Reference: AlphaStar (DeepMind, 2019)
"""

import random
import copy
import pickle
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import numpy as np

try:
    import torch
except ImportError:
    torch = None


@dataclass
class AgentSnapshot:
    """Snapshot of an agent at a specific training iteration."""
    
    iteration: int
    model_state: Dict[str, Any]
    win_rate: float = 0.5
    archetype: str = "main"  # "main", "exploiter", "league_exploiter"
    games_played: int = 0
    elo_rating: float = 1500.0
    deck_preferences: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.deck_preferences is None:
            self.deck_preferences = {}


@dataclass
class MatchResult:
    """Result of a match between two agents."""
    agent1_id: str
    agent2_id: str
    winner: int  # 1 = agent1, 2 = agent2, 0 = draw
    turns: int
    agent1_final_hp: int
    agent2_final_hp: int


class PayoffMatrix:
    """Tracks win rates between all agent pairs."""
    
    def __init__(self):
        self._wins: Dict[Tuple[str, str], int] = {}
        self._games: Dict[Tuple[str, str], int] = {}
    
    def record_result(self, agent1_id: str, agent2_id: str, winner: int):
        """Record a match result."""
        key = (agent1_id, agent2_id)
        reverse_key = (agent2_id, agent1_id)
        
        self._games[key] = self._games.get(key, 0) + 1
        self._games[reverse_key] = self._games.get(reverse_key, 0) + 1
        
        if winner == 1:
            self._wins[key] = self._wins.get(key, 0) + 1
        elif winner == 2:
            self._wins[reverse_key] = self._wins.get(reverse_key, 0) + 1
        # Draw: no wins recorded
    
    def get_win_rate(self, agent1_id: str, agent2_id: str) -> float:
        """Get win rate of agent1 vs agent2."""
        key = (agent1_id, agent2_id)
        games = self._games.get(key, 0)
        if games == 0:
            return 0.5  # Unknown matchup
        wins = self._wins.get(key, 0)
        return wins / games
    
    def get_exploitability(self, agent_id: str, all_agents: List[str]) -> float:
        """
        Calculate how exploitable an agent is.
        Lower is better (less exploitable).
        """
        worst_matchup = 1.0
        for other in all_agents:
            if other != agent_id:
                win_rate = self.get_win_rate(agent_id, other)
                worst_matchup = min(worst_matchup, win_rate)
        return 1.0 - worst_matchup  # Convert to exploitability


class EloSystem:
    """ELO rating system for agent ranking."""
    
    K_FACTOR = 32  # How much ratings change per game
    
    @staticmethod
    def expected_score(rating_a: float, rating_b: float) -> float:
        """Expected score for player A against player B."""
        return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400))
    
    @staticmethod
    def update_ratings(rating_a: float, rating_b: float, 
                       result: float) -> Tuple[float, float]:
        """
        Update ratings based on result.
        result: 1.0 = A wins, 0.0 = B wins, 0.5 = draw
        """
        expected_a = EloSystem.expected_score(rating_a, rating_b)
        expected_b = 1.0 - expected_a
        
        new_rating_a = rating_a + EloSystem.K_FACTOR * (result - expected_a)
        new_rating_b = rating_b + EloSystem.K_FACTOR * ((1.0 - result) - expected_b)
        
        return new_rating_a, new_rating_b


class League:
    """
    Manages a population of agents for training.
    
    Structure:
    - Main Agents: The primary agents being trained
    - Main Exploiters: Find weaknesses in the current Main Agent
    - League Exploiters: Train against historical pool
    - Historical Pool: Snapshots of past Main Agents
    """
    
    def __init__(self,
                 main_agent_count: int = 1,
                 exploiter_count: int = 2,
                 league_exploiter_count: int = 1,
                 history_size: int = 50,
                 snapshot_interval: int = 10,
                 save_dir: str = "models/league"):
        
        self.main_agent_count = main_agent_count
        self.exploiter_count = exploiter_count
        self.league_exploiter_count = league_exploiter_count
        self.history_size = history_size
        self.snapshot_interval = snapshot_interval
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Agent storage
        self.main_agents: List[AgentSnapshot] = []
        self.exploiters: List[AgentSnapshot] = []
        self.league_exploiters: List[AgentSnapshot] = []
        self.historical_pool: List[AgentSnapshot] = []
        
        # Statistics
        self.payoff = PayoffMatrix()
        self.total_games = 0
        self.iteration = 0
    
    def _generate_agent_id(self, archetype: str, iteration: int) -> str:
        """Generate unique agent ID."""
        return f"{archetype}_{iteration}"
    
    def add_main_agent(self, model, iteration: int) -> str:
        """
        Add a new Main Agent snapshot to the league.
        
        Args:
            model: PyTorch model (or any with state_dict())
            iteration: Current training iteration
            
        Returns:
            Agent ID
        """
        if torch is not None:
            model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        else:
            model_state = copy.deepcopy(model.state_dict() if hasattr(model, 'state_dict') else {})
        
        agent_id = self._generate_agent_id("main", iteration)
        
        snapshot = AgentSnapshot(
            iteration=iteration,
            model_state=model_state,
            archetype="main"
        )
        
        self.main_agents.append(snapshot)
        
        # Add to historical pool periodically
        if iteration % self.snapshot_interval == 0:
            hist_snapshot = AgentSnapshot(
                iteration=iteration,
                model_state=copy.deepcopy(model_state),
                archetype="historical"
            )
            self.historical_pool.append(hist_snapshot)
            
            # Trim history if too large
            if len(self.historical_pool) > self.history_size:
                # Keep diverse snapshots (not just recent ones)
                # Remove every other old snapshot
                if len(self.historical_pool) > self.history_size * 1.5:
                    self.historical_pool = (
                        self.historical_pool[:self.history_size // 2:2] +  # Old, sparse
                        self.historical_pool[self.history_size // 2:]      # Recent, dense
                    )[-self.history_size:]
        
        self.iteration = iteration
        return agent_id
    
    def add_exploiter(self, model, iteration: int, exploiter_type: str = "main") -> str:
        """
        Add or update an Exploiter agent.
        
        Args:
            model: PyTorch model
            iteration: Current training iteration
            exploiter_type: "main" (exploits current main) or "league" (exploits history)
        """
        if torch is not None:
            model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        else:
            model_state = copy.deepcopy(model.state_dict() if hasattr(model, 'state_dict') else {})
        
        archetype = f"{exploiter_type}_exploiter"
        agent_id = self._generate_agent_id(archetype, iteration)
        
        snapshot = AgentSnapshot(
            iteration=iteration,
            model_state=model_state,
            archetype=archetype
        )
        
        if exploiter_type == "main":
            self.exploiters.append(snapshot)
            # Keep only recent exploiters
            if len(self.exploiters) > self.exploiter_count * 3:
                self.exploiters = self.exploiters[-self.exploiter_count * 2:]
        else:
            self.league_exploiters.append(snapshot)
            if len(self.league_exploiters) > self.league_exploiter_count * 3:
                self.league_exploiters = self.league_exploiters[-self.league_exploiter_count * 2:]
        
        return agent_id
    
    def sample_opponent(self, agent_type: str = "main") -> Optional[AgentSnapshot]:
        """
        Sample an opponent for training based on agent type.
        
        Sampling strategy:
        - Main Agent: Weighted mix of exploiters (high priority) + historical + self
        - Exploiter: Only the current Main Agent
        - League Exploiter: Only historical pool
        
        Args:
            agent_type: "main", "exploiter", or "league_exploiter"
            
        Returns:
            AgentSnapshot of the sampled opponent, or None if no valid opponent
        """
        if agent_type == "main":
            # Main Agent plays against everyone
            candidates = []
            weights = []
            
            # High priority: Exploiters (they find weaknesses)
            for exp in self.exploiters[-self.exploiter_count:]:
                candidates.append(exp)
                weights.append(5.0)  # High weight
            
            # Medium priority: League exploiters
            for lexp in self.league_exploiters[-self.league_exploiter_count:]:
                candidates.append(lexp)
                weights.append(3.0)
            
            # Lower priority: Historical pool (prevent forgetting)
            for hist in self.historical_pool[-20:]:  # Recent history
                candidates.append(hist)
                weights.append(1.0)
            
            # Self-play with previous versions
            for prev in self.main_agents[-5:-1]:  # Recent main agents
                candidates.append(prev)
                weights.append(2.0)
            
            if not candidates:
                # Fallback: self-play with current
                return self.main_agents[-1] if self.main_agents else None
            
            return random.choices(candidates, weights=weights)[0]
        
        elif agent_type == "exploiter":
            # Exploiter ONLY plays against current Main Agent
            if self.main_agents:
                return self.main_agents[-1]
            return None
        
        elif agent_type == "league_exploiter":
            # League Exploiter plays against historical pool
            if self.historical_pool:
                # Weighted towards agents that are hard to beat
                return random.choice(self.historical_pool)
            return None
        
        return None
    
    def sample_training_batch(self, batch_size: int, 
                              agent_type: str = "main") -> List[AgentSnapshot]:
        """Sample a batch of opponents for training."""
        opponents = []
        for _ in range(batch_size):
            opp = self.sample_opponent(agent_type)
            if opp:
                opponents.append(opp)
        return opponents
    
    def record_game_result(self, main_agent_id: str, opponent_snapshot: AgentSnapshot,
                           winner: int, turns: int = 0):
        """
        Record the result of a training game.
        
        Args:
            main_agent_id: ID of the main agent
            opponent_snapshot: The opponent that was played
            winner: 1 = main agent won, 2 = opponent won, 0 = draw
        """
        opponent_id = self._generate_agent_id(
            opponent_snapshot.archetype, 
            opponent_snapshot.iteration
        )
        
        self.payoff.record_result(main_agent_id, opponent_id, winner)
        self.total_games += 1
        
        # Update ELO for main agents
        if self.main_agents:
            current_main = self.main_agents[-1]
            result = 1.0 if winner == 1 else (0.0 if winner == 2 else 0.5)
            
            new_main_elo, new_opp_elo = EloSystem.update_ratings(
                current_main.elo_rating,
                opponent_snapshot.elo_rating,
                result
            )
            current_main.elo_rating = new_main_elo
            opponent_snapshot.elo_rating = new_opp_elo
            current_main.games_played += 1
    
    def get_main_agent_stats(self) -> Dict[str, Any]:
        """Get statistics for the current Main Agent."""
        if not self.main_agents:
            return {}
        
        current = self.main_agents[-1]
        all_agent_ids = [
            self._generate_agent_id(a.archetype, a.iteration)
            for agents in [self.main_agents, self.exploiters, self.historical_pool]
            for a in agents
        ]
        
        return {
            "iteration": current.iteration,
            "elo_rating": current.elo_rating,
            "games_played": current.games_played,
            "win_rate": current.win_rate,
            "exploitability": self.payoff.get_exploitability(
                self._generate_agent_id("main", current.iteration),
                all_agent_ids
            ),
            "league_size": len(self.main_agents) + len(self.exploiters) + len(self.historical_pool)
        }
    
    def get_nash_distribution(self) -> Dict[int, float]:
        """
        Compute approximate Nash equilibrium distribution over Main Agents.
        
        This is a simplified version - true Nash requires LP solving.
        Here we use a heuristic based on ELO ratings.
        """
        if not self.main_agents:
            return {}
        
        # Use softmax over ELO ratings
        ratings = [a.elo_rating for a in self.main_agents[-10:]]  # Recent agents
        if not ratings:
            return {}
        
        # Temperature scaling
        temp = 100.0
        exp_ratings = [np.exp((r - max(ratings)) / temp) for r in ratings]
        total = sum(exp_ratings)
        
        return {i: exp_ratings[i] / total for i in range(len(exp_ratings))}
    
    def save(self, path: Optional[str] = None):
        """Save league state to disk."""
        save_path = Path(path) if path else self.save_dir / "league_state.pkl"
        
        state = {
            "main_agents": self.main_agents,
            "exploiters": self.exploiters,
            "league_exploiters": self.league_exploiters,
            "historical_pool": self.historical_pool,
            "payoff_wins": self.payoff._wins,
            "payoff_games": self.payoff._games,
            "total_games": self.total_games,
            "iteration": self.iteration
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(state, f)
    
    def load(self, path: Optional[str] = None) -> bool:
        """Load league state from disk."""
        load_path = Path(path) if path else self.save_dir / "league_state.pkl"
        
        if not load_path.exists():
            return False
        
        try:
            with open(load_path, 'rb') as f:
                state = pickle.load(f)
            
            self.main_agents = state.get("main_agents", [])
            self.exploiters = state.get("exploiters", [])
            self.league_exploiters = state.get("league_exploiters", [])
            self.historical_pool = state.get("historical_pool", [])
            self.payoff._wins = state.get("payoff_wins", {})
            self.payoff._games = state.get("payoff_games", {})
            self.total_games = state.get("total_games", 0)
            self.iteration = state.get("iteration", 0)
            
            return True
        except Exception as e:
            print(f"Failed to load league state: {e}")
            return False
    
    def __repr__(self) -> str:
        return (
            f"<League main={len(self.main_agents)} "
            f"exploiters={len(self.exploiters)} "
            f"history={len(self.historical_pool)} "
            f"games={self.total_games}>"
        )


# Convenience function for integration
def create_league(config: Optional[Dict] = None) -> League:
    """Create a League instance with optional configuration."""
    default_config = {
        "main_agent_count": 1,
        "exploiter_count": 2,
        "league_exploiter_count": 1,
        "history_size": 50,
        "snapshot_interval": 10,
        "save_dir": "models/league"
    }
    
    if config:
        default_config.update(config)
    
    return League(**default_config)
