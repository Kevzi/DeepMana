
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    # Register end of turn trigger
    game.register_trigger("on_turn_end", card, on_turn_end_trigger)

def on_turn_end_trigger(game: Game, owner_card: Card, active_player: Player):
    # Triggers at the end of the owner's turn
    if active_player == owner_card.owner:
        damaged_minions = [m for m in active_player.board if m.health < m.max_health]
        if damaged_minions:
            target = game.random.choice(damaged_minions)
            target._attack += 2
            target._health += 2
            target._max_health += 2
