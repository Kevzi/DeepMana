import sys
import os

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from simulator import Game, Player, create_card, CardDatabase
from simulator.enums import GamePhase

def setup_game():
    CardDatabase.get_instance().load()
    p1 = Player("Player 1")
    p2 = Player("Player 2")
    game = Game()
    game.setup(p1, p2)
    game.phase = GamePhase.MAIN_ACTION
    game.turn = 1
    p1.mana_crystals = 10
    p1.mana = 10
    return game, p1, p2

def test_aura_stacking():
    print("\n--- Testing Aura Stacking ---")
    game, p1, p2 = setup_game()
    
    # Use IDs for Stormwind Champion (EX1_583) if available, or manually simulate
    # Since I don't want to rely on DB for this logic test, I'll check if handlers exist
    # For now, let's try to create real cards
    try:
        champ1 = create_card("CS2_222", game) # Stormwind Champion
        champ1.controller = p1
        champ2 = create_card("CS2_222", game) 
        champ2.controller = p1
        minion = create_card("CS2_120", game) # River Crocolisk (2/3)
        minion.controller = p1
        
        p1.summon(minion)
        print(f"Base Minion: {minion.name} {minion.attack}/{minion.health}")
        print(f"DEBUG: Minion game set: {minion.game is not None}, Zone: {minion.zone}")
        
        p1.summon(champ1)
        print(f"DEBUG: Champion game set: {champ1.game is not None}, Zone: {champ1.zone}")
        print(f"DEBUG: Game triggers: {len(game._triggers.get('on_calculate_attack', []))}")
        print(f"After 1 Champion: {minion.name} {minion.attack}/{minion.health}")
        
        p1.summon(champ2)
        print(f"After 2 Champions: {minion.name} {minion.attack}/{minion.health}")
        
        if minion.attack != 4 or minion.health != 5: # 2/3 + 1/1 + 1/1
            print("FAIL: Aura didn't update correctly!")
            print(f"Got {minion.attack}/{minion.health}, expected 4/5")
        else:
            print("PASS: Aura updated correctly.")
        
        # Killing one champion should reduce stats
        game.destroy(champ1)
        game.process_deaths()
        print(f"After losing 1 Champion: {minion.name} {minion.attack}/{minion.health}")
        
        if minion.attack != 3 or minion.health != 4:
            print("FAIL: Aura didn't update correctly after death!")
        else:
            print("PASS: Aura updated correctly after death.")
    except Exception as e:
        print(f"ERROR: {e}")

def test_targeting_matrix():
    print("\n--- Testing Targeting Matrix ---")
    game, p1, p2 = setup_game()
    
    # Test Elusive (inciblable)
    try:
        elusive = create_card("NEW1_023", game)
        elusive.controller = p2
        p2.summon(elusive)
        
        # Try to target with a spell
        fireball = create_card("CS2_029", game)
        fireball.controller = p1
        p1.add_to_hand(fireball)
        
        targets = p1.get_valid_targets(fireball)
        is_elusive_targetable = any(t == elusive for t in targets)
        
        if is_elusive_targetable:
            print("FAIL: Elusive minion is targetable by spell!")
        else:
            print("PASS: Elusive minion correctly ignored by spell.")
    except Exception as e:
        print(f"ERROR: {e}")

def test_magnetic_fusion():
    print("\n--- Testing Magnetic Fusion ---")
    game, p1, p2 = setup_game()
    
    try:
        mech = create_card("BOT_079", game) # Faithful Lumi (1/1 Mech)
        mech.controller = p1
        p1.summon(mech)
        
        magnetic_minion = create_card("BOT_563", game) # Wargear (5/5 Magnetic)
        magnetic_minion.controller = p1
        print(f"DEBUG: Magnetic minion: {magnetic_minion.name}, Magnetic flag: {magnetic_minion.magnetic}")
        
        # Card must be in hand to be played!
        p1.add_to_hand(magnetic_minion)
        
        # Playing magnetic to the left of a mech
        game.play_card(magnetic_minion, position=0)
        
        print(f"Fused Mech Attack: {mech.attack}")
        if mech.attack >= 6: # 1 base + 5 wargear
             print("PASS: Magnetic fusion successful.")
        else:
             print("FAIL: Magnetic fusion failed or didn't add stats.")
             print(f"Got {mech.attack}, expected >= 6")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_aura_stacking()
    test_targeting_matrix()
    test_magnetic_fusion()
