"""Effect for The Replicator-inator (MIS_025t).

Card Text: [x]<b>Mini</b>
After you play a minion with
the same Attack as this,
summon a copy of it.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon a copy of this minion
    if source.card_id:
        game.summon_token(player, source.card_id)