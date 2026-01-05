"""Effect for Orbital Moon (GDB_475).

Card Text: Give a minion <b>Taunt</b> and <b>Lifesteal</b>. If you played an adjacent card this turn, also give it <b>Reborn</b>.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +0/+0 and keywords
    if target:
        pass
        target._taunt = True
        target._lifesteal = True
        target._reborn = True