
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_deathrattle(game: Game, player: Player, card: Card):
    enemies = game.get_enemy_targets(player, include_hero=True)
    for enemy in enemies:
        game.deal_damage(enemy, 2, source=card)
