
from simulator.entities import Card, Minion
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_draw(game: Game, player: Player, card: Card):
    # Register trigger in hand
    game.register_trigger("on_minion_played", card, on_opponent_minion_played)

def on_opponent_minion_played(game: Game, owner_card: Card, played_minion: Card):
    # owner_card is Mirrex. Check if it's in hand of its owner
    if owner_card.zone != 3: # Zone.HAND
        return
        
    # Check if opponent played it
    if played_minion.owner != owner_card.owner:
        # Transform Mirrex into a copy but 3/4
        # We need a way to transform a card in hand
        # Simplest: update attributes of owner_card
        owner_card.card_id = played_minion.card_id
        owner_card.name = played_minion.name
        owner_card._attack = 3
        owner_card._health = 4
        owner_card._max_health = 4
        # Copy effects? mirrex usually copies everything
        owner_card.data = played_minion.data
        # Note: card_id and data are now the target minion's.
        # Mirrex text says "While in your hand, this IS a 3/4 copy"
