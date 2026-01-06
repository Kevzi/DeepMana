"""Effect for EX1_583 (Priestess of Elune)"""

def setup(game, card):
    def on_play(game, source, minion, target=None):
        if minion == card:
            game.heal(card.controller.hero, 4)

    game.register_trigger("on_minion_played", card, on_play)