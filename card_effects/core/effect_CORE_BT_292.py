
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    if target:
        target._attack += 2
        target._health += 1
        target._max_health += 1
    player.draw(1)
