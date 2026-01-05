"""Effect for Abduction Ray (GDB_123).

Card Text: Get a random Demon. Reduce its Cost by (2). Repeatable this turn.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Get a random Demon. Reduce its Cost by (2). Repeatable this turn....
    pass