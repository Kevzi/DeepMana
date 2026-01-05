"""Effect for Tess Greymane (CORE_GIL_598).

Card Text: [x]<b>Battlecry:</b> Replay every card
from another class you've
played this game <i>(targets
chosen randomly)</i>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Replay every card
from another class you've
played this game <i>(targets
chosen...
    pass