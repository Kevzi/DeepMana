
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    damage = 2
    enemies = game.get_enemy_targets(player, include_hero=True)
    for enemy in enemies:
        game.deal_damage(enemy, damage, source=card)

def get_cost_modifier(game: Game, player: Player, card: Card) -> int:
    # Costs (1) less for each Elemental you control.
    elemental_count = sum(1 for m in player.board if "ELEMENTAL" in m.races)
    return -elemental_count
