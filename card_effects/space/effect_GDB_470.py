"""Effect for Exarch Maladaar (GDB_470).

Card Text: <b>Battlecry:</b> The next card you play this turn costs <b>Corpses</b> instead of Mana.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> The next card you play this turn costs <b>Corpses</b> instead of Mana....
    pass