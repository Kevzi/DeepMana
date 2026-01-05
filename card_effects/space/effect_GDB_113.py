"""Effect for Airlock Breach (GDB_113).

Card Text: [x]Summon a 5/5 Undead
with <b>Taunt</b> and give your
hero +5 Health. Spend
5 <b>Corpses</b> to do it again.
"""

from simulator.enums import CardType

def on_play(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Summon token(s)
    for _ in range(5):
        game.summon_token(player, "GDB_113t")
    # Give +5/+5 and keywords
    if target:
        
target._attack += 5        target._max_health += 5        target._health += 5
        target._taunt = True
    # Restore 5 Health to your hero
    if player.hero:
        game.heal(player.hero, 5, source)