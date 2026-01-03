"""Effect for Headhunt (GDB_473)"""

def play(game, source, target):
    """Deal 3 damage to a minion. If it dies, draw a card."""
    if target:
        died = game.deal_damage(target, 3, source)
        # Note: deal_damage usually returns bool (true if fatal) or int damage dealt.
        # Checking if target is in graveyard is safer.
        if target.is_dead or target.zone.name == 'GRAVEYARD':
            source.controller.draw(1)
