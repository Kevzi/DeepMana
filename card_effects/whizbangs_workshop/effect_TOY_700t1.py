"""Effect for Nonuplet Deck (TOY_700t1).

Card Text: This deck has 9 copies of Astral Automaton.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: This deck has 9 copies of Astral Automaton....
    pass