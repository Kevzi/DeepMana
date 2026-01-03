
from simulator.entities import Card, Minion
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    if target and target.owner == player and target.card_type == 1: # MINION
        if len(player.board) < 7:
            # Create a copy with same stats and buffs
            copy = Minion(target.data, game)
            copy._attack = target.attack
            copy._health = target.health
            copy._max_health = target.max_health
            # Copy keywords
            copy._taunt = target.taunt
            copy._divine_shield = target.divine_shield
            copy._rush = target.rush
            copy._stealth = target.stealth
            copy._lifesteal = target.lifesteal
            copy._poisonous = target.poisonous
            
            player.summon(copy)
