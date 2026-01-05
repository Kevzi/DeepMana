"""Effect for Dissonant Pop (ETC_314t).

Card Text: Deal $6 damage to all minions. Summon
a 3/3 Popstar.
<i>(Swaps each turn.)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Deal 6 damage to all minions
    for m in list(player.board) + list(opponent.board):
        game.deal_damage(m, 6, source)
    # Summon token(s)
    for _ in range(6):
        game.summon_token(player, "ETC_314tt")