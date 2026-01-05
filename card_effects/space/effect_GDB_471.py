"""Effect for Voronei Recruiter (GDB_471).

Card Text: [x]At the end of your turn,
get a 4/4 Crewmate with
a random <b>Bonus Effect</b>.
"""

from simulator.enums import CardType

def battlecry(game, source, target):
    player = source.controller
    opponent = player.opponent

    # Effect: [x]At the end of your turn,
get a 4/4 Crewmate with
a random <b>Bonus Effect</b>....
    pass