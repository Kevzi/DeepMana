"""Effect for Fire Fly (UNG_809).

Card Text: <b>Battlecry</b>: Add a 1/2 Elemental to your hand.
"""

def battlecry(game, source, target):
    player = source.controller
    # Add 1/2 Flame Elemental (UNG_809t) to hand
    token = create_card("UNG_809t", player)
    if token:
        player.add_to_hand(token)