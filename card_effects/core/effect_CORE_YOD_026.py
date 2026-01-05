"""Effect for Fiendish Servant (CORE_YOD_026).

Card Text: [x]<b>Deathrattle:</b> Give this
minion's Attack to a random
friendly minion.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Give +0/+0 and keywords
    if target:
        pass