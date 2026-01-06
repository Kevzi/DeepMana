"""Structures de données immuables avec partage structurel.

Permet de cloner l'état du jeu en O(1) au lieu de O(N).
Basé sur le principe du 'Public Belief State' et du versioning léger.
"""

from typing import Dict, List, Any, Optional

class ImmutableDict:
    """Dict immuable avec Copy-on-Write (CoW)."""
    
    __slots__ = ('_parent', '_changes', '_version')
    
    def __init__(self, parent: 'ImmutableDict' = None, initial: Dict = None):
        self._parent = parent
        self._changes: Dict[str, Any] = initial or {}
        self._version = (parent._version + 1) if parent else 0
    
    def get(self, key: str, default=None):
        if key in self._changes:
            return self._changes[key]
        if self._parent:
            return self._parent.get(key, default)
        return default
    
    def set(self, key: str, value: Any) -> 'ImmutableDict':
        """Retourne une NOUVELLE version avec la modification."""
        new = ImmutableDict(parent=self)
        new._changes[key] = value
        return new
    
    def fork(self) -> 'ImmutableDict':
        """Clone léger : O(1) au lieu de O(n)."""
        return ImmutableDict(parent=self)
    
    def to_dict(self) -> Dict:
        """Matérialise en dict Python classique."""
        result = {}
        if self._parent:
            result = self._parent.to_dict()
        result.update(self._changes)
        return result


class GameSnapshot:
    """Snapshot complet de l'état du jeu avec versioning.
    
    Utilisé pour le clonage ultra-rapide dans MCTS.
    """
    
    def __init__(self, parent: 'GameSnapshot' = None):
        self._parent = parent
        self._version = (parent._version + 1) if parent else 0
        
        # Deltas uniquement
        self._player_changes: Dict[int, Dict] = {}
        self._board_changes: Dict[int, List] = {}
        self._global_changes: Dict[str, Any] = {}
    
    def fork(self) -> 'GameSnapshot':
        """Clone O(1)."""
        return GameSnapshot(parent=self)
    
    def set_player_stat(self, player_idx: int, key: str, value: Any):
        if player_idx not in self._player_changes:
            self._player_changes[player_idx] = {}
        self._player_changes[player_idx][key] = value
    
    def get_player_stat(self, player_idx: int, key: str, default=None):
        if player_idx in self._player_changes and key in self._player_changes[player_idx]:
            return self._player_changes[player_idx][key]
        if self._parent:
            return self._parent.get_player_stat(player_idx, key, default)
        return default
