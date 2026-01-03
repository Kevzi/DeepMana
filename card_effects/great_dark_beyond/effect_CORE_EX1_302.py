"""Effect for Mortal Coil (CORE_EX1_302)"""

def play(game, source, target):
    """Deal 1 damage to a minion. If it dies, draw a card."""
    if target:
        died = game.deal_damage(target, 1, source)
        # Check death (deal_damage logic varies, checking zone or is_dead flag is safest)
        if target.is_dead or target.zone.name == 'GRAVEYARD':
            source.controller.draw(1)
