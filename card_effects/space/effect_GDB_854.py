"""Effect for Uluu, the Everdrifter (GDB_854).

Card Text: [x]Each turn this is in your
hand, gain two random
<b>Choose One</b> choices.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Each turn this is in your
hand, gain two random
<b>Choose One</b> choices....
    pass