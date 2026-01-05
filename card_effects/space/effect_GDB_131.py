"""Effect for Velen, Leader of the Exiled (GDB_131).

Card Text: [x]<b>Taunt</b>. <b>Deathrattle:</b> Trigger the
<b>Battlecries</b> and <b>Deathrattles</b>
of all other Draenei you
played this game.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Taunt</b>. <b>Deathrattle:</b> Trigger the
<b>Battlecries</b> and <b>Deathrattles</b>
of all o...
    pass