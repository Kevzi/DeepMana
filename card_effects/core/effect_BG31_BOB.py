
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    # Mock choices for Battlegrounds action
    # Choice 1: Get a random Tier 6 minion (6-cost)
    # Choice 2: Add 3 coins (Temporary mana)
    # Choice 3: Give your minions +2/+2 (Battlegrounds blood gem style)
    
    # We create temporary "Choice" cards for discovery
    choices = [
        {"id": "BOB_CHOICE_1", "name": "Hire a Champion", "text": "Get a random 6-Cost minion."}
        {"id": "BOB_CHOICE_2", "name": "Refresh Drinks", "text": "Gain 3 Temporary Mana."}
        {"id": "BOB_CHOICE_3", "name": "Strong Arms", "text": "Give your minions +2/+2."}
    ]
    
    # Custom discover logic
    options = []
    for c in choices:
        mock = create_card("CS2_022", game) # Dummy card base (Coin or similar)
        mock.name = c["name"]
        mock.text = c["text"]
        mock.card_id = c["id"]
        options.append(mock)
        
    def callback(game, choice):
        if choice.card_id == "BOB_CHOICE_1":
            six_costs = [cid for cid, c in game.db.cards.items() if c.get("cost") == 6 and c.get("type") == "MINION"]
            if six_costs:
                player.add_to_hand(create_card(game.random.choice(six_costs), game))
        elif choice.card_id == "BOB_CHOICE_2":
            player.temp_mana += 3
        elif choice.card_id == "BOB_CHOICE_3":
            for m in player.board:
                m._attack += 2
                m._health += 2
                m._max_health += 2
                
    game.discover(player, options, callback)
