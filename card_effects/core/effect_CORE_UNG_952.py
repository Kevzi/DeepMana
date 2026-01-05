"""Effect for Spikeridged Steed (CORE_UNG_952).

Card Text: Give a minion +2/+6 and <b>Taunt</b>. When it dies, summon a Stegodon.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "CORE_UNG_952t")
    # Give +2/+6 and keywords
    if target:
        
target._attack += 2        target._max_health += 6        target._health += 6
        target._taunt = True