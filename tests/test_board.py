"""Test script for Board Arena visualization."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
import qdarktheme

from simulator import Game, Player, create_card, CardDatabase
from simulator.enums import GamePhase
from gui.tabs.board_tab import InteractiveBoardTab


def setup_demo_game():
    """Create a demo game with some cards on the board."""
    CardDatabase.get_instance().load()
    
    p1 = Player("You")
    p2 = Player("Opponent")
    
    game = Game()
    game.setup(p1, p2)
    game.phase = GamePhase.MAIN_ACTION
    game.turn = 5
    
    # Give mana
    p1.mana_crystals = 5
    p1.mana = 5
    p2.mana_crystals = 4
    p2.mana = 4
    
    # Add some minions to P1's board
    minions_p1 = ["CS2_222", "CS2_120", "BOT_079"]  # Stormwind Champion, River Croc, Faithful Lumi
    for card_id in minions_p1:
        card = create_card(card_id, game)
        if card:
            card.controller = p1
            p1.summon(card)
    
    # Add some minions to P2's board
    minions_p2 = ["NEW1_023", "CS2_172"]  # Faerie Dragon, Bloodfen Raptor
    for card_id in minions_p2:
        card = create_card(card_id, game)
        if card:
            card.controller = p2
            p2.summon(card)
    
    # Add cards to P1's hand
    hand_cards = ["CS2_029", "BOT_563"]  # Fireball, Wargear
    for card_id in hand_cards:
        card = create_card(card_id, game)
        if card:
            card.controller = p1
            p1.add_to_hand(card)
    
    return game


def main():
    app = QApplication(sys.argv)
    
    # Apply dark theme (handle different qdarktheme versions)
    try:
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    except AttributeError:
        try:
            qdarktheme.setup_theme("dark")
        except:
            pass  # No theme if unavailable
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Board Arena - Interactive Test")
    window.resize(1000, 750)
    
    # Create interactive board tab
    board = InteractiveBoardTab()
    
    # Setup demo game
    game = setup_demo_game()
    board.set_game(game)
    
    window.setCentralWidget(board)
    window.show()
    
    print("=" * 50)
    print("INTERACTIVE BOARD ARENA")
    print("=" * 50)
    print("Drag from YOUR minion to ENEMY minion/hero to attack!")
    print(f"Your board: {[m.name for m in game.current_player.board]}")
    print(f"Enemy board: {[m.name for m in game.opponent.board]}")
    print(f"Your hand: {[c.name for c in game.current_player.hand]}")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
