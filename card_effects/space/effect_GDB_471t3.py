"""Effect for Gunner Crewmate (GDB_471t3).

Card Text: [x]<b>Rush</b>
<b>Battlecry:</b> Summon every
adjoining Crewmate.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_471t3t")