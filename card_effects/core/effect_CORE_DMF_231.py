"""Effect for Zai, the Incredible (CORE_DMF_231).

Card Text: <b>Battlecry:</b> Copy the left- and right-most cards in your hand.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Copy the left- and right-most cards in your hand....
    pass