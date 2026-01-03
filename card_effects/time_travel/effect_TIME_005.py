"""Effect for TIME_005 in TIME_TRAVEL"""


def battlecry(game, source, target):
    player = source.controller
    # Track played Rafaams
    played = getattr(player, 'rafaams_played', set())
    # The 'rest' means the 9 others
    others = {
        'TIME_005t1', 'TIME_005t2', 'TIME_005t3'
        'TIME_005t4', 'TIME_005t5', 'TIME_005t6'
        'TIME_005t7', 'TIME_005t8', 'TIME_005t9'
    }
    if others.issubset(played):
        game.deal_damage(player.opponent.hero, 100, source) # Exodia!

def setup(game, source):
    # Register that a Rafaam was played
    def on_play(game, trig_src, card, target):
        if card.controller == trig_src.controller and card.card_id.startswith('TIME_005'):
             played = getattr(trig_src.controller, 'rafaams_played', set())
             played.add(card.card_id)
             trig_src.controller.rafaams_played = played
    game.register_trigger('on_card_played', source, on_play)
