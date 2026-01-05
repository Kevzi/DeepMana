"""Effect for Tirion Fordring (CORE_EX1_383).

Card Text: <b>Divine Shield</b>, <b>Taunt</b> <b>Deathrattle:</b> Equip a 5/3 Ashbringer.
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Effect: <b>Divine Shield</b>, <b>Taunt</b> <b>Deathrattle:</b> Equip a 5/3 Ashbringer....
    pass