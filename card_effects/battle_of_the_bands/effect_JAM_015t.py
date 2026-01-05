"""Effect for Sharpened Tuning Fork (JAM_015t).

Card Text: [x]<b>Battlecry:</b> Gain +2 Attack.
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2