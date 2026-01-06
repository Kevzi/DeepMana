"""Effect for CS2_222 (Stormwind Champion)"""

def setup(game, card):
    def on_calculate_attack(game, aura_card, target, modifier):
        # "Your other minions have +1/+1"
        if target.zone == 1: # Zone.PLAY
             if target.controller == aura_card.controller and target != aura_card:
                 modifier["amount"] += 1

    def on_calculate_health(game, aura_card, target, modifier):
        if target.zone == 1:
             if target.controller == aura_card.controller and target != aura_card:
                 modifier["amount"] += 1

    game.register_trigger("on_calculate_attack", card, on_calculate_attack)
    game.register_trigger("on_calculate_health", card, on_calculate_health)