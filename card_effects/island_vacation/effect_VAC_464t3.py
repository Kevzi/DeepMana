"""Effect for Mutating Injection (VAC_464t3).

Card Text: Give a minion +4/+4 and <b>Taunt</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +4/+4 and keywords
    if target:
        
target._attack += 4        target._max_health += 4        target._health += 4
        target._taunt = True