"""Effect for Instrument Case (ETC_098t).

Card Text: <b>Deathrattle:</b> Add a
random weapon to your opponent's hand.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Deathrattle:</b> Add a
random weapon to your opponent's hand....
    pass