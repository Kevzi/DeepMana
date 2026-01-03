
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    opponent = game.get_opponent(player)
    if not opponent.deck:
        return
        
    space = 10 - len(player.hand)
    if space <= 0:
        return
        
    # Get all cards from opponent's deck
    deck_copy = list(opponent.deck)
    game.random.shuffle(deck_copy)
    
    for i in range(min(space, len(deck_copy))):
        orig_card = deck_copy[i]
        new_card = create_card(orig_card.card_id, game)
        if new_card:
            new_card.mod_cost -= 3
            player.add_to_hand(new_card)
