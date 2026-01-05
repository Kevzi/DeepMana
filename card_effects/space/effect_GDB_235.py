"""Effect for Exarch Akama (GDB_235).

Card Text: [x]After this attacks,
all other friendly minions
can attack again <i>(except
Exarch Akama)</i>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]After this attacks,
all other friendly minions
can attack again <i>(except
Exarch Akama)</i>....
    pass