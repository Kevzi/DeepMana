
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    if target:
        game.destroy(target)
        
    # Combo: Summon random 8-cost
    if player.combo_cards_played > 1:
        eight_costs = [cid for cid, c in game.db.cards.items() 
                       if c.get("cost") == 8 and c.get("type") == "MINION"]
        if eight_costs:
            random_cid = game.random.choice(eight_costs)
            game.summon_token(player, random_cid)
