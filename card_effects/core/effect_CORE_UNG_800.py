"""Effect for Terrorscale Stalker (CORE_UNG_800).

Card Text: <b>Battlecry:</b> Trigger a friendly minion's <b>Deathrattle</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Battlecry:</b> Trigger a friendly minion's <b>Deathrattle</b>....
    pass


def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent
    # Deathrattle effect
    pass  # TODO: Implement deathrattle portion