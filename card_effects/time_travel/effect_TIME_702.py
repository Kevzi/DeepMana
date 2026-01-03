
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_draw(game: Game, player: Player, card: Card):
    game.register_trigger("on_minion_played", card, on_minion_played)

def on_minion_played(game: Game, owner_card: Card, played_minion: Card):
    if owner_card.owner == played_minion.owner and owner_card.zone == 3: # Zone.HAND
        # Mark as active for this turn/session
        owner_card._ebb_active = True

def on_play(game: Game, player: Player, card: Card, target=None):
    damage = 3
    if target:
        game.deal_damage(target, damage, source=card)
    
    if getattr(card, '_ebb_active', False):
        player.hero.armor += 5
        card._ebb_active = False # Reset
