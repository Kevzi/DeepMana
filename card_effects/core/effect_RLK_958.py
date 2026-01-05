"""Effect for Skeletal Sidekick (RLK_958).

Card Text: <b>Battlecry:</b> Give a friendly Undead +2 Attack.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +2/+0 and keywords
    if target:
        
target._attack += 2