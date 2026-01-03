
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    damage = 3
    if target:
        game.deal_damage(target, damage, source=card)
        
    # Condition: holding a minion (5)+
    has_big_minion = any(c.card_type == 1 and game.get_card_cost(player, c) >= 5 for c in player.hand if c != card)
    
    if has_big_minion:
        # Draw a minion
        minions_in_deck = [c for c in player.deck if c.card_type == 1]
        if minions_in_deck:
            drawn = game.random.choice(minions_in_deck)
            player.draw_specific_card(drawn)
        else:
            player.draw(1) # Fallback draw if no minions but deck not empty
