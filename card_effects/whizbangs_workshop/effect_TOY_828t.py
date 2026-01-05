"""Effect for Amateur Puppeteer (TOY_828t).

Card Text: [x]<b>Mini</b>, <b>Taunt</b>
<b>Deathrattle:</b> Give Undead
in your hand +2/+2.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2
        target._taunt = True