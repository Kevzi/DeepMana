"""Effect for Undercity Huckster (CORE_OG_330).

Card Text: <b>Deathrattle:</b> Get a
random card <i>(from your
opponent's class)</i>.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Deathrattle:</b> Get a
random card <i>(from your
opponent's class)</i>....
    pass