"""Effect for Infested Breath (EDR_814)"""

def play(game, source, target):
    """Deal 3 damage to all minions. If you have a Corpse, deal 4 instead."""
    damage = 3
    player = source.controller
    
    # Check for corpse
    if hasattr(player, 'corpses') and player.corpses > 0:
        damage = 4
        # Does it consume a corpse? Usually "Spend a Corpse" text is explicit.
        # "If you have a Corpse" usually implies check only. # But commonly DK spells consume.
        # Let's assume Consume for balance if not specified 'check'.
        # Actually, standard phrasing "Spend a Corpse to deal X" -> Consume.
        # "If you have X corpses" -> Check.
        # Let's assume Check based on "If you have".
    
    targets = game.board
    for minion in targets:
        game.deal_damage(minion, damage, source)
