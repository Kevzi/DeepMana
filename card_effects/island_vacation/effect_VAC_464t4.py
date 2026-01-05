"""Effect for The Exorcisor (VAC_464t4).

Card Text: <b>Silence</b> any minion attacked by this weapon.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Silence a minion
    if target:
        game.silence(target)