"""Effect for Resistance Aura (TTN_851).

Card Text: Your opponent's
spells cost (1) more.
Lasts 2 enemy turns.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Your opponent's
spells cost (1) more.
Lasts 2 enemy turns....
    pass