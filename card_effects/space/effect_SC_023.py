"""Effect for Spine Crawler (SC_023).

Card Text: [x]<b>Taunt</b>. Can't attack.
Has +3 Attack if you
control a location.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+0 and keywords
    if target:
        
target._attack += 3
        target._taunt = True