"""Effect for Emergency Meeting (GDB_119).

Card Text: [x]Get two 4/4 Crewmates.
Put a random Demon
that costs (3) or less
between them.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Get two 4/4 Crewmates.
Put a random Demon
that costs (3) or less
between them....
    pass