import sys
import os

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from simulator import CardDatabase, create_card, Player, Game

CardDatabase.get_instance().load()
db = CardDatabase.get_instance()

def check_card(card_id):
    data = db._cards.get(card_id)
    if data:
        print(f"Card {card_id}: {data.name}, {data.attack}/{data.health}, Set: {data.card_set}, Type: {data.card_type.name}, Race: {data.race.name}")
    else:
        print(f"Card {card_id} NOT FOUND in database.")

check_card("BOT_031") # Faithful Lumi
check_card("BOT_033") # Wargear
check_card("EX1_583") # Stormwind Champion
