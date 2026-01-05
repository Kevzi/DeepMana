"""Effect for Tomb Guardians (CORE_RLK_118).

Card Text: Summon two 2/2 Zombies with <b>Taunt</b>. Spend 4 <b>Corpses</b> to
give them <b>Reborn</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "CORE_RLK_118t")
    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2
        target._taunt = True
        target._reborn = True