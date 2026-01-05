"""Effect for Archimonde (GDB_128).

Card Text: [x]<b>Battlecry:</b> Summon every
Demon you played this
game that didn't start
in your deck.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_128t")