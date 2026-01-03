"""Effect for CORE_WC_042 in CORE"""
from simulator.enums import Race
from simulator.enums import CardType, Race

def setup(game, source):
    def on_play_c(game, trig_src, card, target):
        if card.controller == trig_src.controller and card.card_type == CardType.MINION and hasattr(card.data, 'race') and card.data.race == Race.ELEMENTAL:
            trig_src.attack += 1
            trig_src.health += 1 # Wailing Vapor is +1/+1
    game.register_trigger('on_card_played', source, on_play_c)