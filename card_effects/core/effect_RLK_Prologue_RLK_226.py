"""Effect for Ymirjar Deathbringer (RLK_Prologue_RLK_226).

Card Text: [x]<b>Taunt</b>. <b>Deathrattle:</b> Spend 3
<b>Corpses</b> to summon a 3/3
Risen Ymirjar with <b>Taunt</b>.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(3):
        game.summon_token(player, "RLK_Prologue_RLK_226t")