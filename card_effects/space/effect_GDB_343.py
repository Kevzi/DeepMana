"""Effect for Perplexing Anomaly (GDB_343).

Card Text: <b>Rush</b>, <b>Taunt</b>,
<b>...<b>Stealth</b>?</b>
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Rush</b>, <b>Taunt</b>,
<b>...<b>Stealth</b>?</b>...
    pass