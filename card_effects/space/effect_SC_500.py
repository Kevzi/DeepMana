"""Effect for Wayward Probe (SC_500).

Card Text: [x]<b>Battlecry and Deathrattle:</b>
Get a random
<b>Starship Piece</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry and Deathrattle:</b>
Get a random
<b>Starship Piece</b>....
    pass


def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent
    # Deathrattle effect
    pass  # TODO: Implement deathrattle portion