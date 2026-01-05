"""Effect for Spawning Pool (SC_000).

Card Text: [x]Get a 1/1 Zergling.
<b>Deathrattle:</b> Your Zerg
minions have <b>Rush</b>
this turn.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Get a 1/1 Zergling.
<b>Deathrattle:</b> Your Zerg
minions have <b>Rush</b>
this turn....
    pass