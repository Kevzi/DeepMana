
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    # Register the passive aura
    game.register_trigger("on_calculate_damage", card, on_calculate_damage)
    
    # Combo effect
    if player.combo_cards_played > 1: # Already played something else
        backstab = create_card("CS2_072", game)
        if backstab:
            player.add_to_hand(backstab)

def on_calculate_damage(game: Game, owner_card: Card, target: Card, source: Card, modifier: dict):
    # Undamaged enemy minions take double damage
    if target.owner != owner_card.owner:
        if hasattr(target, 'health') and hasattr(target, 'max_health'):
            if target.health == target.max_health:
                modifier["amount"] *= 2
