"""Effect for Soulbreaker (CORE_RLK_012).

Card Text: After your hero attacks and kills a minion, gain 2 <b>Corpses</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: After your hero attacks and kills a minion, gain 2 <b>Corpses</b>....
    pass