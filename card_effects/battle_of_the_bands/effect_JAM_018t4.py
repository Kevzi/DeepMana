"""Effect for Wailing Rhapsody (JAM_018t4).

Card Text: Deal $3 damage to all minions. Summon
a 5/5 Demon.
<i>(Changes each turn.)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Deal 3 damage to all minions
    for m in list(player.board) + list(opponent.board):
        game.deal_damage(m, 3, source)
    # Summon token(s)
    for _ in range(3):
        game.summon_token(player, "JAM_018t4t")