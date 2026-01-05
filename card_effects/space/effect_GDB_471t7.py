"""Effect for Medical Crewmate (GDB_471t7).

Card Text: [x]<b>Lifesteal</b>
<b>Battlecry:</b> Summon every
adjoining Crewmate.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "GDB_471t7t")