import logging
from typing import Dict, Any, List

class StateManager:
    """
    Reconstruit l'état du jeu à partir des TAG_CHANGE du Power.log.
    Le but est de produire un JSON compatible avec l'encodeur de l'IA côté serveur.
    """
    
    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.player_id: int = 1 # Sera mis à jour par les logs
        self.current_step: str = "BEGIN_MULLIGAN"
        
    def update_tag(self, entity_id: str, tag: str, value: str):
        if entity_id not in self.entities:
            self.entities[entity_id] = {"id": entity_id, "tags": {}}
        
        # Conversion de valeur si possible
        try:
            if value.isdigit():
                val = int(value)
            else:
                val = value
        except:
            val = value
            
        self.entities[entity_id]["tags"][tag] = val
        
        if tag == "STEP":
            self.current_step = value

    def get_game_state_json(self) -> Dict[str, Any]:
        """
        Produit un snapshot propre de la partie.
        On filtre pour ne garder que l'essentiel (Main, Board, Hero).
        """
        state = {
            "step": self.current_step,
            "entities": self.entities,
            "timestamp": None # To be added
        }
        
        # Logique simplifiée pour le prototype:
        # On pourrait classer par ZONE (HAND, PLAY, DECK)
        return state

    def reset(self):
        self.entities = {}
