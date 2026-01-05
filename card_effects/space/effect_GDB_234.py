"""Effect for Spore Empress Moldara (GDB_234).

Card Text: <b>Start of Game:</b> Shuffle 7 Replicating Spores into your deck.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Start of Game:</b> Shuffle 7 Replicating Spores into your deck....
    pass