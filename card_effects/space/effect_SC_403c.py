"""Effect for Raven (SC_403c).

Card Text: [x]<b>Starship Piece</b>
When this is launched, gain
2 random <b>Bonus Effects</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Starship Piece</b>
When this is launched, gain
2 random <b>Bonus Effects</b>....
    pass