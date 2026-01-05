"""Effect for Questing Deck (TOY_700t8).

Card Text: Your deck has 3 Shaman <b>Quests</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Your deck has 3 Shaman <b>Quests</b>....
    pass