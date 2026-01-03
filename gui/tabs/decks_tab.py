from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QListWidget, QListWidgetItem, QTextEdit, QMessageBox, QDialog,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer
import sys
import os

from simulator.deck_generator import DeckGenerator
from simulator.card_loader import CardDatabase

class DecksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Left: List of Decks
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        
        title = QLabel("Meta Decks (Standard)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #cbd5e1;")
        left_layout.addWidget(title)
        
        self.deck_list = QListWidget()
        self.deck_list.setStyleSheet("""
            QListWidget {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #334155;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
            }
        """)
        left_layout.addWidget(self.deck_list)
        
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.clicked.connect(self.load_decks)
        view_btn = QPushButton("View Deck List")
        view_btn.clicked.connect(self.view_selected_deck)
        
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(view_btn)
        left_layout.addLayout(btn_layout)
        
        layout.addWidget(left_panel, 1) # Stretch 1
        
        # Load decks on start
        self.meta_decks = {} # Store loaded decks locally: name -> code
        self.load_decks()
        
    def load_decks(self):
        self.deck_list.clear()
        self.meta_decks = {}
        
        # Load from JSON via Generator
        try:
            decks_map = DeckGenerator._load_meta_decks()
        except Exception:
            self.deck_list.addItem("Error loading deck generator.")
            return
        
        if not decks_map:
            self.deck_list.addItem("No decks found or error loading JSON.")
            return

        # Group by Class for nicer display
        grouped = {}
        for code, (cls_name, deck_name) in decks_map.items():
            if cls_name not in grouped: grouped[cls_name] = []
            grouped[cls_name].append((deck_name, code))
            
        for cls_name in sorted(grouped.keys()):
            for deck_name, code in grouped[cls_name]:
                display_name = f"[{cls_name}] {deck_name}"
                item = QListWidgetItem(display_name)
                # Map display name to code
                self.meta_decks[display_name] = code
                self.deck_list.addItem(item)
                
    def view_selected_deck(self):
        current_item = self.deck_list.currentItem()
        if not current_item:
            return
            
        display_name = current_item.text()
        code = self.meta_decks.get(display_name)
        
        if code:
            self.show_deck_list(display_name, code)
            
    def show_deck_list(self, name, code):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Deck List: {name}")
        dialog.resize(400, 600)
        dialog.setStyleSheet("background-color: #0f172a; color: white;")
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel(name)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setStyleSheet("background-color: #1e293b; color: #94a3b8; border: none; font-size: 14px;")
        
        card_ids = None
        error_msg = "Unknown error"
        try:
            card_ids = DeckGenerator.decode_deck_string(code)
        except Exception as e:
            card_ids = None
            error_msg = str(e)
            print(f"Error decoding deck: {e}")
            
        if card_ids:
            # Count cards
            counts = {}
            for cid in card_ids:
                counts[cid] = counts.get(cid, 0) + 1
                
            # Get card details
            db = CardDatabase.get_instance()
            if not db._loaded: db.load()
            
            cards_info = []
            unknown_count = 0
            
            for cid, count in counts.items():
                if cid.startswith("DBF:"):
                     unknown_count += 1
                     cards_info.append((0, f"Unknown Card ({cid})", count))
                     continue
                     
                card = db.get_card(cid)
                if card:
                    cards_info.append((card.cost, card.name, count))
                else:
                    cards_info.append((0, f"Unknown ID: {cid}", count))
            
            # Sort by cost
            cards_info.sort(key=lambda x: x[0])
            
            # Format text
            content = f"**Total Cards:** {len(card_ids)}\n\n"
            for cost, cname, count in cards_info:
                content += f"[{cost}] {cname}"
                if count > 1:
                    content += f"  x{count}"
                content += "\n\n" # Double newline for markdown spacing
                
            text_area.setMarkdown(content)
        elif card_ids is not None:
             text_area.setText("Deck decoded but no cards found (Empty List).")
        else:
             text_area.setText(f"Error decoding deck.\nDetails: {error_msg}")
        
        layout.addWidget(text_area)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setStyleSheet("background-color: #3b82f6; padding: 8px; border-radius: 4px;")
        layout.addWidget(close_btn)
        
        dialog.exec()
