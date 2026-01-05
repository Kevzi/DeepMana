"""Effect for Clay Matriarch (TOY_380t).

Card Text: [x]<b>Mini</b>
<b>Taunt</b>. <b>Deathrattle:</b> Summon
a 4/4 Whelp with <b>Elusive</b>.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(4):
        game.summon_token(player, "TOY_380tt")