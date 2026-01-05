"""Effect for Ancient Reflections (VAC_464t19).

Card Text: Choose a minion.
Fill your board with 1/1 copies of it.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Choose a minion.
Fill your board with 1/1 copies of it....
    pass