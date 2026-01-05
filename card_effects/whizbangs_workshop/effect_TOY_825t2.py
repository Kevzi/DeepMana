"""Effect for Greater Spinel Spellstone (TOY_825t2).

Card Text: Give Undead in your hand +3/+3.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+3 and keywords
    if target:
        
target._attack += 3        target._max_health += 3        target._health += 3