"""Effect for Grimmer Patron (VAC_464t26).

Card Text: At the end of your turn, summon a copy of this minion.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon a copy of this minion
    if source.card_id:
        game.summon_token(player, source.card_id)