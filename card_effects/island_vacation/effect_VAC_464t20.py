"""Effect for Banana Split (VAC_464t20).

Card Text: Give a friendly minion +2/+2. Summon two copies of it.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(2):
        game.summon_token(player, "VAC_464t20t")
    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2