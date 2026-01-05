"""Effect for Lightfused Manasaber (GDB_322).

Card Text: <b>Rush</b>
<b><b>Spellburst</b>:</b> Gain
<b>Divine Shield</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Rush</b>
<b><b>Spellburst</b>:</b> Gain
<b>Divine Shield</b>....
    pass