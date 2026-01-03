"""Effect for Sanguine Depths (CORE_REV_990)"""

def activate(game, source, target):
    """Location: Deal 1 damage to a minion and give it +2 Attack."""
    if target:
        game.deal_damage(target, 1, source)
        target.buff(2, 0)
