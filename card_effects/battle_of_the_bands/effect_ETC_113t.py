"""Effect for Fizzle's Snapshot (ETC_113t).

Card Text: [x]Add the snapshotted
cards to your hand.
<i>(Once per game)</i>
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Add the snapshotted
cards to your hand.
<i>(Once per game)</i>...
    pass