"""Effect for YOG_525 in TITANS"""
from simulator.enums import CardType


def battlecry(game, source, target):
    for c in source.controller.hand:
        if c.card_type == CardType.MINION:
            c.attack += 1; c.health += 1; c.max_health += 1
