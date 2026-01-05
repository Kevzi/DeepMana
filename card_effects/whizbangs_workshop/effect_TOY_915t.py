"""Effect for Tabletop Roleplayer (TOY_915t).

Card Text: [x]<b>Mini</b>
<b>Battlecry:</b> Give a friendly
Demon +2 Attack and
<b>Immune</b> this turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2