"""Effect for Kerrigan, Queen of Blades (SC_004).

Card Text: [x]<b>Battlecry:</b> Summon two
2/5 Hive Queens. Deal 3
damage to all enemies.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Deal 2 damage to all characters
    for m in list(player.board) + list(opponent.board):
        game.deal_damage(m, 2, source)
    if player.hero:
        game.deal_damage(player.hero, 2, source)
    if opponent.hero:
        game.deal_damage(opponent.hero, 2, source)
    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "SC_004t")