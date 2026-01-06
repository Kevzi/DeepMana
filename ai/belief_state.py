"""Gestion des États de Croyance Publics (PBS) pour HearthstoneOne.

Permet de modéliser les mains probables de l'adversaire en fonction
des actions publiques observées (cartes jouées, mana utilisé, etc.).
"""

import numpy as np
from typing import Dict, List, Optional, Set
from collections import defaultdict

class BeliefState:
    """
    Modélise l'incertitude sur la main et le deck de l'adversaire.
    Utilise une mise à jour bayésienne simplifiée.
    """
    
    def __init__(self, enemy_class: str, initial_deck_size: int = 30):
        self.enemy_class = enemy_class
        self.deck_size = initial_deck_size
        self.known_enemy_cards: List[str] = [] # Cartes déjà jouées par l'adversaire
        
        # Probabilités des cartes du core/meta pour cette classe
        self.probabilities: Dict[str, float] = {}
        self._initialize_meta_probabilities()
        
    def _initialize_meta_probabilities(self):
        """Initialise les probas basées sur les decks 'Meta' connus."""
        # Note: Dans une version réelle, on chargerait des stats de HSReplay par exemple.
        # Ici on utilise le DeckGenerator pour simuler une connaissance du meta.
        try:
            from simulator.deck_generator import DeckGenerator
            meta_decks = DeckGenerator.get_meta_decks_for_class(self.enemy_class)
            
            if not meta_decks:
                return
                
            counts = defaultdict(int)
            total = len(meta_decks)
            for deck in meta_decks:
                # On regarde la présence de chaque carte
                for card_id in set(deck):
                    counts[card_id] += 1
            
            for card_id, count in counts.items():
                self.probabilities[card_id] = count / total
        except Exception:
            # Fallback uniform si échec
            pass

    def update_on_enemy_action(self, action_type: str, action_data: Dict):
        """
        Met à jour les croyances après une observation publique.
        
        - 'play_card': L'adversaire avait cette carte (P=1 pour cette instance).
        - 'end_turn': S'il avait du mana, il n'avait probablement pas de carte jouable.
        """
        if action_type == "play_card":
            card_id = action_data.get("card_id")
            if card_id:
                self.known_enemy_cards.append(card_id)
                # On ajuste la probabilité qu'il en ait une DEUXIÈME copie
                if card_id in self.probabilities:
                    self.probabilities[card_id] *= 0.5 # Réduit la proba
        
        elif action_type == "end_turn":
            mana_left = action_data.get("mana_remaining", 0)
            if mana_left >= 2:
                # Inférence : Il n'avait probablement pas de drop de coût <= mana_left
                for cid, prob in self.probabilities.items():
                    # Simulation simplifiée du coût (devrait ideally venir du CardDatabase)
                    estimated_cost = 2 # Placeholder
                    if estimated_cost <= mana_left:
                        self.probabilities[cid] *= 0.8 # Légère baisse de proba

    def sample_hand(self, hand_size: int) -> List[str]:
        """Échantillonne une main possible de l'adversaire."""
        if not self.probabilities:
            return []
            
        cards = list(self.probabilities.keys())
        probs = np.array([self.probabilities[c] for c in cards])
        
        # Normalisation
        total = probs.sum()
        if total > 0:
            probs = probs / total
        else:
            probs = np.ones(len(cards)) / len(cards)
            
        count = min(hand_size, len(cards))
        if count <= 0: return []
        
        # Tirage sans remise
        sampled = np.random.choice(cards, size=count, replace=False, p=probs)
        return list(sampled)

    def get_most_likely_hand(self, hand_size: int) -> List[str]:
        """Retourne la main la plus probable statistiquement."""
        # Trier par probabilité décroissante
        sorted_cards = sorted(self.probabilities.items(), key=lambda x: x[1], reverse=True)
        return [c for c, p in sorted_cards[:hand_size]]
