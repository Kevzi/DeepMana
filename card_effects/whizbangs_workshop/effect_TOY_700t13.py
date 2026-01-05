"""Effect for Morphing Card (TOY_700t13).

Card Text: [x]Each turn this is in your
hand, transform it into a
random playable Mage
or Neutral card.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]Each turn this is in your
hand, transform it into a
random playable Mage
or Neutral card....
    pass