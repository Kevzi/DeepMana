
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    # Summon 3 Silver Hand Recruits
    for _ in range(3):
        game.summon_token(player, "CS2_101t")
    
    # Equip a 1/4 Weapon (Light's Justice)
    weapon_card = create_card("CS2_091", game)
    if weapon_card:
        game._play_weapon(weapon_card)
