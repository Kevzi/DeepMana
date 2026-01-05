"""Effect for Seedling Growth (TOY_801b).

Card Text: Gain <b>Spell Damage +1</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1