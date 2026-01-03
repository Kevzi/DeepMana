
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    damage = 4
    
    # If elemental was played last turn, we can choose target.
    # If no target provided (e.g. random play by AI or manual choice)
    # we use the provided target.
    # Actually, the 'target' is passed by Game.play_card if the card requires it.
    
    if player.elementals_played_last_turn > 0 and target:
        game.deal_damage(target, damage, source=card)
    else:
        # Random enemy
        enemies = game.get_enemy_targets(player)
        if enemies:
            random_target = game.random.choice(enemies)
            game.deal_damage(random_target, damage, source=card)
