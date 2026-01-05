"""Effect for Modest Tour (WORK_027t1).

Card Text: Get 2 random cards that can potentially impact the enemy's battlefield.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Get 2 random cards that can potentially impact the enemy's battlefield....
    pass