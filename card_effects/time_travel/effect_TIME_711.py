
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    # Find all 1-cost minions
    one_costs = [cid for cid, c in game.db.cards.items() 
                 if c.get("cost") == 1 and c.get("type") == "MINION" and c.get("set") != "CORE"]
    
    if not one_costs:
        return
        
    for _ in range(2):
        if len(player.board) >= 7:
            break
        random_cid = game.random.choice(one_costs)
        minion = game.summon_token(player, random_cid)
        
        # Combo effect: +1 Attack
        if minion and player.combo_cards_played > 1:
            minion._attack += 1
