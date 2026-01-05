"""Effect for Jim Raynor (SC_400).

Card Text: [x]<b>Battlecry:</b> Relaunch
every <b>Starship</b> that you
launched this game.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]<b>Battlecry:</b> Relaunch
every <b>Starship</b> that you
launched this game....
    pass