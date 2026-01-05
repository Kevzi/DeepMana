"""Effect for Felfused Battery (GDB_110).

Card Text: After this attacks, give your other minions +1 Attack. <b>Starship Piece</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+0 and keywords
    if target:
        
target._attack += 1