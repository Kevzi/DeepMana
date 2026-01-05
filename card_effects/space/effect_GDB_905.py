"""Effect for Launch Starship (GDB_905).

Card Text: Launch your <b>Starship</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Launch your <b>Starship</b>....
    pass