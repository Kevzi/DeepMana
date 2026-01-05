"""Effect for Mystery Dispense-o-bot (JAM_000t4).

Card Text: [x]<b>Battlecry:</b> Get two
random Mage <b>Secrets</b>.
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Get two
random Mage <b>Secrets</b>.
<i>(Changes each turn.)</i>...
    pass