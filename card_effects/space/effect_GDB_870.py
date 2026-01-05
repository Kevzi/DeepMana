"""Effect for Eredar Skulker (GDB_870).

Card Text: [x]<b>Combo and <b>Spellburst</b>:</b>
Gain +2 Attack and <b>Stealth</b>.
"""

from simulator.enums import CardType

def on_combo(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2
        target._stealth = True