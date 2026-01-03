
from simulator.entities import Card, Minion
from simulator.player import Player
from simulator.game import Game
from simulator.factory import create_card

def on_play(game: Game, player: Player, card: Card, target=None):
    if target:
        # We transform by replacing
        # Frog ID is typically EX1_246t
        frog_data = create_card("EX1_246t", game)
        if not frog_data:
            # Fallback if ID is different in this dataset
            frog_data = create_card("hearthstone.entities.Classic.Shaman.Frog", game)
            
        if frog_data:
            frog = Minion(frog_data.data, game)
            frog.owner = target.owner
            
            idx = target.owner.board.index(target)
            target.owner.board[idx] = frog
            
            # Fire event
            game.fire_event("on_minion_transformed", target, frog)
