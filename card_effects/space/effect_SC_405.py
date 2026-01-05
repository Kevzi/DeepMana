"""Effect for Ultra-Capacitor (SC_405).

Card Text: [x]<b>Starship Piece</b>
<b>Battlecry:</b> Gain +1/+1 for
  each other friendly minion.  
Also triggers on launch.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Give +1/+1 and keywords
    if target:
        
target._attack += 1        target._max_health += 1        target._health += 1