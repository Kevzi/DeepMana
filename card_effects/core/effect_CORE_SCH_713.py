"""Effect for Cult Neophyte (CORE_SCH_713).

Card Text: <b>Battlecry:</b> Your opponent's spells cost (1) more next turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Your opponent's spells cost (1) more next turn....
    pass