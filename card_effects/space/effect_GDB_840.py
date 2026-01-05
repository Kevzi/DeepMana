"""Effect for Extraterrestrial Egg (GDB_840).

Card Text: [x]<b>Deathrattle:</b> Summon a
3/5 Beast that attacks the
lowest Health enemy.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(3):
        game.summon_token(player, "GDB_840t")
    # Restore 3 Health
    if target:
        game.heal(target, 3, source)