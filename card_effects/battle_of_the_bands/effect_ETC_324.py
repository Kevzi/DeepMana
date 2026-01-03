"""Effect for ETC_324 in BATTLE_OF_THE_BANDS"""


def setup(game, source):
    source.divine_shield = True
    def on_lose_ds(game, trig_src, target):
        if target.controller == source.controller:
            source.controller.draw(1)
    
    game.register_trigger('on_divine_shield_lost', source, on_lose_ds)
