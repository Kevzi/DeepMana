"""Effect for Libram of Divinity (GDB_138).

Card Text: Give a minion +3/+3. If this costs (0), return this to your hand
at the end of your turn.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +3/+3 and keywords
    if target:
        
target._attack += 3        target._max_health += 3        target._health += 3