"""Effect for Holy Book (VAC_464t7).

Card Text: <b>Silence</b> and destroy a minion. Summon a 10/10 copy of it.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_464t7t")
    # Destroy a minion
    if target:
        target.destroy()
    # Silence a minion
    if target:
        game.silence(target)