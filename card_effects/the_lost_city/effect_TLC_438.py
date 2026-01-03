
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    # This is a battlecry effect
    # Search for eligible spells in deck
    spells = [c for c in player.deck if c.card_type == 2 and game.get_card_cost(player, c) <= 2] # 2 = SPELL
    
    if spells:
        spell = game.random.choice(spells)
        player.deck.remove(spell)
        
        # Cast it. The text says "targets this if possible"
        # We need to check if the spell needs a target
        # For now, we manually trigger the effect of the spell
        handler = game._get_effect_handler(spell.card_id, "on_play")
        if handler:
            # Try to target 'card' (the Treasuregill minion)
            handler(game, player, spell, target=card)
        
        # Move spell to graveyard
        game.fire_event("on_spell_played", spell)
        spell.zone = 4 # Zone.GRAVEYARD
        player.graveyard.append(spell)
