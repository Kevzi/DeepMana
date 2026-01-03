"""Effect for Mothership (SC_762)"""

def battlecry(game, source, target):
    """Battlecry: Cloak all other friendly minions. (Give them Stealth)"""
    for minion in source.controller.board:
        if minion is not source:
            minion.stealth = True
            
def end_turn(game, source):
    """End of Turn: Summon a random Protoss unit."""
    # Simplified
    protoss_units = ["SC_753", "SC_755"] # Zealot/Dragoon/Cannon
    import random
    unit = random.choice(protoss_units)
    game.summon(source.controller, unit)
