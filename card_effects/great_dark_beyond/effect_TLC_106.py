"""Effect for Spiritsinger Umbra (TLC_106)"""
# Assuming TLC_106 is Umbra or similar effect (trigger Deathrattles on summon)

def on_summon_friendly(game, source, minion):
    """After you summon a minion, trigger its Deathrattle."""
    if minion is not source and minion.deathrattle:
         # Trigger DR
         game.trigger_deathrattle(minion)

def setup(game, source):
    # Register trigger
    # game.register_trigger(Trigger.ON_SUMMON, on_summon_friendly, owner=source)
    pass
