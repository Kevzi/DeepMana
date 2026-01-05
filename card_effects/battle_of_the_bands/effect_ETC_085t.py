"""Effect for Movement of Envy (ETC_085t).

Card Text: Remove the top 6
cards from your opponent's deck.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Remove the top 6
cards from your opponent's deck....
    pass