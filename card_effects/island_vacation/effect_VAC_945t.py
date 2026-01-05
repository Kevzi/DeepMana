"""Effect for Ourobos, World Serpent (VAC_945t).

Card Text: [x]<b>Taunt</b>
<b>Deathrattle:</b> Give a minion
 in your hand "<b>Deathrattle:</b>
  Summon Ourobos."
"""

from simulator.enums import CardType

def deathrattle(game, source):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(1):
        game.summon_token(player, "VAC_945tt")
    # Give +0/+0 and keywords
    if target:
        pass
        target._taunt = True