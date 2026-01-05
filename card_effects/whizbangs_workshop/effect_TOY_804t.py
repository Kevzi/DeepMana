"""Effect for Grove Beetle (TOY_804t).

Card Text: <b>Taunt</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Taunt</b>...
    pass