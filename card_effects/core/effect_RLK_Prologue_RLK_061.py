"""Effect for Battlefield Necromancer (RLK_Prologue_RLK_061).

Card Text: [x]At the end of your turn,
raise a <b>Corpse</b> as a 1/2
  Risen Footman with <b>Taunt</b>.  
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]At the end of your turn,
raise a <b>Corpse</b> as a 1/2
  Risen Footman with <b>Taunt</b>.  ...
    pass