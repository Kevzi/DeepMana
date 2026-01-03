
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    # Rewind logic (if any specific handler exists)
    # Battlecry
    opponent = game.get_opponent(player)
    
    # Get all weapons
    weapons = [cid for cid, c in game.db.cards.items() if c.get("type") == "WEAPON" and c.get("rarity") != "LEGENDARY"]
    
    if weapons:
        # Player
        p_weapon_id = game.random.choice(weapons)
        p_weapon = create_card(p_weapon_id, game)
        if p_weapon:
            game._play_weapon(p_weapon)
            # Give +1/+1
            p_weapon._attack += 1
            p_weapon._health += 1 # Durability
            
        # Opponent
        o_weapon_id = game.random.choice(weapons)
        o_weapon = create_card(o_weapon_id, game)
        if o_weapon:
            game._play_weapon(o_weapon)
            # Opponent weapon doesn't get +1/+1 (only "yours")
