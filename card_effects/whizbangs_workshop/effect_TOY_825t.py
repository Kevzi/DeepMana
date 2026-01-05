"""Effect for Spinel Spellstone (TOY_825t).

Card Text: Give Undead in your hand +2/+2. <i>(Gain 5 <b>Corpses</b> to upgrade.)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2