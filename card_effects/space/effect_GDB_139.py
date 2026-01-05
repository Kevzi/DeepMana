"""Effect for Libram of Faith (GDB_139).

Card Text: Summon three
3/3 Draenei with <b>Divine Shield</b>. If this costs (0), give them <b>Rush</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(3):
        game.summon_token(player, "GDB_139t")
    # Give +3/+3 and keywords
    if target:
        
target._attack += 3        target._max_health += 3        target._health += 3
        target._rush = True
        target._divine_shield = True