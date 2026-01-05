"""Effect for Good Vibrations (ETC_373b).

Card Text: Give your minions +2/+4 and <b>Taunt</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+4 and keywords
    if target:
        
target._attack += 2        target._max_health += 4        target._health += 4
        target._taunt = True