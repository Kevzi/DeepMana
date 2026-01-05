"""Effect for Lorewalker Cho (CORE_EX1_100).

Card Text: Whenever a player casts a spell, put a copy into the other player’s hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Whenever a player casts a spell, put a copy into the other player’s hand....
    pass