"""Effect for Gilneas Brochure (WORK_017t).

Card Text: <b>Silence</b> a minion
and give it -2/-2.
<i>(Flips each turn.)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+2 and keywords
    if target:
        
target._attack += 2        target._max_health += 2        target._health += 2
    # Silence a minion
    if target:
        game.silence(target)