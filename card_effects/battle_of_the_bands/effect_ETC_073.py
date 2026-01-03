"""Effect for ETC_073 in BATTLE_OF_THE_BANDS"""


def setup(game, source):
    if not source.controller:
        return
    count = getattr(source.controller, 'combo_cards_played', 0)
    source.attack += count; source.max_health += count; source.health += count
