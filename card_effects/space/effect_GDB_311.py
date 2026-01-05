"""Effect for Deep Space Curator (GDB_311).

Card Text: <b><b>Spellburst</b>:</b> Get a random minion of the spell's Cost. Set its Cost to (0).
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b><b>Spellburst</b>:</b> Get a random minion of the spell's Cost. Set its Cost to (0)....
    pass