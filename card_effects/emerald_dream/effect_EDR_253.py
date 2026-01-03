
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_equip(game: Game, player: Player, weapon: Card):
    game.register_trigger("on_hero_attack", weapon, on_hero_attack_trigger)

def on_hero_attack_trigger(game: Game, weapon: Card, attacker: Card):
    # attacker is player.hero
    player = weapon.owner
    if attacker == player.hero:
        # Draw highest cost card
        if player.deck:
            # Get costs
            costs = [(c, game.get_card_cost(player, c)) for c in player.deck]
            costs.sort(key=lambda x: x[1], reverse=True)
            
            top_card = costs[0][0]
            player.draw_specific_card(top_card)
