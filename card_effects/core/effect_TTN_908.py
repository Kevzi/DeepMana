
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    # This card needs to stay active for 3 turns.
    # We use the 'dormant' or a custom counter.
    # Let's use a hidden trigger source.
    card.duration = 3
    game.register_trigger("on_minion_attack", card, on_attack_trigger)
    game.register_trigger("on_turn_start", card, on_turn_start_trigger)

def on_attack_trigger(game: Game, aura_card: Card, attacker: Card):
    if attacker.owner == aura_card.owner:
        attacker._attack += 2
        attacker._health += 1
        attacker._max_health += 1

def on_turn_start_trigger(game: Game, aura_card: Card, active_player: Player):
    if active_player == aura_card.owner:
        aura_card.duration -= 1
        if aura_card.duration <= 0:
            game.unregister_triggers(aura_card)
