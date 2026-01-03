
from simulator.entities import Card
from simulator.player import Player
from simulator.game import Game

def on_play(game: Game, player: Player, card: Card, target=None):
    # Find all minions in deck
    minions_in_deck = [c for c in player.deck if c.card_type == 1] # CardType.MINION
    
    if not minions_in_deck:
        return
        
    drawn = []
    races_drawn = set()
    
    # Try to find two different races
    # This is a simplified search
    for m in list(minions_in_deck):
        m_races = set(m.races) if m.races else {"NONE"}
        if not drawn:
            drawn.append(m)
            races_drawn.update(m_races)
            player.deck.remove(m)
        else:
            # Check if this minion has any race NOT in races_drawn
            if not (m_races & races_drawn):
                drawn.append(m)
                player.deck.remove(m)
                break
        if len(drawn) >= 2:
            break
            
    for m in drawn:
        m._attack += 2
        m._health += 2
        m._max_health += 2
        player.add_to_hand(m)
