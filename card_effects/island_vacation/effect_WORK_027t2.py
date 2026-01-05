"""Effect for Extravagant Tour (WORK_027t2).

Card Text: Get 2 random cards that can potentially spend a lot of Mana.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Get 2 random cards that can potentially spend a lot of Mana....
    pass