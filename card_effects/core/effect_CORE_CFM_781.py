"""Effect for Shaku, the Collector (CORE_CFM_781).

Card Text: [x]<b>Stealth</b>. Whenever this
attacks, add a random card
to your hand <i>(from your
opponent's class).</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Stealth</b>. Whenever this
attacks, add a random card
to your hand <i>(from your
opponent's cl...
    pass