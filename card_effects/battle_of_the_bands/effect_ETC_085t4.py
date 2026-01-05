"""Effect for Movement of Gluttony (ETC_085t4).

Card Text: Give a random minion
in your hand, deck, and
battlefield +6/+6.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +6/+6 and keywords
    if target:
        
target._attack += 6        target._max_health += 6        target._health += 6