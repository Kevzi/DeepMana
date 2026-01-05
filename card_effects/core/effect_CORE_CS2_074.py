"""Effect for Deadly Poison (CORE_CS2_074).

Card Text: Give your weapon +2 Attack.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2