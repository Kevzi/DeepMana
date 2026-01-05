"""Effect for Poison Breath (CORE_EDR_002).

Card Text: Give a friendly
Undead <b>Poisonous</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +0/+0 and keywords
    if target:
        pass
        target._poisonous = True