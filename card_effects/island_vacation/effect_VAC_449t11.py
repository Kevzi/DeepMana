"""Effect for Carress, Cabaret Star (VAC_449t11).

Card Text: [x]<b>Battlecry:</b> Gain +2/+2
and <b>Taunt</b>. <b>Freeze</b> three
random enemy minions.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2
        target._taunt = True
    # Freeze a character
    if target:
        target.frozen = True