"""Effect for Army of the Dead (RLK_060).

Card Text: Raise up to 5 <b>Corpses</b> as 2/2 Risen Ghouls with <b>Rush</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: Raise up to 5 <b>Corpses</b> as 2/2 Risen Ghouls with <b>Rush</b>....
    pass