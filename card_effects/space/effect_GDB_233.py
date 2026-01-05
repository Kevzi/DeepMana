"""Effect for Dwarf Planet (GDB_233).

Card Text: Fill your board
with random 2-Cost minions that attack
random enemies.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Fill your board
with random 2-Cost minions that attack
random enemies....
    pass