"""Effect for Twin Module (TOY_330t97).

Card Text: [x]<b>Battlecry:</b> Summon a
copy of this.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon a copy of this minion
    if source.card_id:
        game.summon_token(player, source.card_id)