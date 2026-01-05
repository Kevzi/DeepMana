"""Effect for Sha'tari Cloakfield (GDB_103).

Card Text: <b>Elusive</b>. Your first spell each turn costs (1) less. <b>Starship Piece</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Elusive</b>. Your first spell each turn costs (1) less. <b>Starship Piece</b>...
    pass