"""Effect for Graveyard Shift (RLK_Prologue_RLK_705).

Card Text: [x]Summon two 1/1
Zombies with <b>Reborn</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "RLK_Prologue_RLK_705t")