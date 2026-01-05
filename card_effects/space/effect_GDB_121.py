"""Effect for Foreboding Flame (GDB_121).

Card Text: [x]<b>Battlecry:</b> Demons that
didn't start in your deck
cost (1) less this game.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Demons that
didn't start in your deck
cost (1) less this game....
    pass