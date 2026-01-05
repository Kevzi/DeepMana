"""Effect for Tar Creeper (CORE_UNG_928).

Card Text: <b>Taunt</b>
Has +2 Attack during your opponent's turn.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2
        target._taunt = True