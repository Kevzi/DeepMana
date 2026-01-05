"""Effect for Malignant Horror (CORE_RLK_745).

Card Text: [x]<b>Reborn</b>
At the end of your turn,
spend 4 <b>Corpses</b> to summon
a copy of this minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon a copy of this minion
    if source.card_id:
        game.summon_token(player, source.card_id)