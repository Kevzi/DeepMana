
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    damage = 2
    if target:
        game.deal_damage(target, damage, source=card)
        
    # Discover a Warrior minion
    warrior_minions = [cid for cid, c in game.db.cards.items() 
                       if c.get("cardClass") == "WARRIOR" and c.get("type") == "MINION"]
    
    if warrior_minions:
        options_ids = game.random.sample(warrior_minions, 3)
        options = [create_card(cid, game) for cid in options_ids]
        
        def callback(game, choice):
            # Apply Dark Gift
            game._apply_dark_gift(choice)
            player.add_to_hand(choice)
            
        game.discover(player, options, callback)
