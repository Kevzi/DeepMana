
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    count = getattr(player, 'amirdrassil_uses', 0) + 1
    player.amirdrassil_uses = count
    
    # Summon N 1-cost minions
    for _ in range(count):
        # Pick a random 1-cost minion
        db = game.db # Assuming db is accessible via game
        one_costs = [cid for cid, c in db.cards.items() if c.get("cost") == 1 and c.get("type") == "MINION"]
        if one_costs:
            random_cid = game.random.choice(one_costs)
            game.summon_token(player, random_cid)
            
    # Gain N Armor
    player.hero.armor += count
    
    # Draw N cards
    player.draw(count)
    
    # Refresh N Mana
    player.mana = min(player.mana_crystals, player.mana + count)
