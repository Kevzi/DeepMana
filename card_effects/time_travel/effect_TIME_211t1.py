
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    # Find all spells
    all_spells = [cid for cid, c in game.db.cards.items() if c.get("type") == "SPELL" and c.get("set") != "CORE"]
    
    if not all_spells:
        return
        
    space = 10 - len(player.hand)
    for _ in range(space):
        cid = game.random.choice(all_spells)
        new_card = create_card(cid, game)
        if new_card:
            new_card.temporary = True
            player.add_to_hand(new_card)
