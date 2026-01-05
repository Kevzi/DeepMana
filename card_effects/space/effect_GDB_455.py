"""Effect for Askara (GDB_455).

Card Text: <b>Battlecry:</b> The next Draenei you play summons a copy of itself.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_455t")