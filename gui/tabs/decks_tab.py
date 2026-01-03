from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QScrollArea, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt
import qtawesome as qta
from simulator.deck_generator import META_DECK_CODES

class DecksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("META DECKS LIBRARY")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header.addWidget(title)
        header.addStretch()
        
        btn_refresh = QPushButton(" Refresh")
        btn_refresh.setIcon(qta.icon("fa5s.sync", color="white"))
        btn_refresh.setStyleSheet("background-color: #334155; padding: 5px 15px; border-radius: 5px;")
        header.addWidget(btn_refresh)
        
        self.layout.addLayout(header)
        
        # Description
        desc = QLabel("Here are the decks used by the AI for training. Lists sourced from HSGuru (January 2026).")
        desc.setStyleSheet("color: #94a3b8; margin-bottom: 10px;")
        self.layout.addWidget(desc)
        
        # Scroll Area for Decks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        self.grid_layout = QVBoxLayout(container)
        self.grid_layout.setSpacing(10)
        
        scroll.setWidget(container)
        self.layout.addWidget(scroll)
        
        # Initial load
        self.refresh_decks()
        print(f"DEBUG: DecksTab initialized with {len(META_DECK_CODES)} decks.")

    def refresh_decks(self):
        # Clear existing
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Group by class
        by_class = {}
        for code, (cls, name) in META_DECK_CODES.items():
            if cls not in by_class:
                by_class[cls] = []
            by_class[cls].append((name, code))
            
        for cls in sorted(by_class.keys()):
            # Class Header
            cls_label = QLabel(cls)
            cls_label.setStyleSheet(f"font-weight: bold; color: {self.get_class_color(cls)}; font-size: 14px; margin-top: 10px;")
            self.grid_layout.addWidget(cls_label)
            
            for name, code in by_class[cls]:
                card = QFrame()
                card.setProperty("class", "card")
                card.setFixedHeight(60)
                card_layout = QHBoxLayout(card)
                card_layout.setContentsMargins(15, 0, 15, 0)
                
                # Icon
                icon_label = QLabel()
                icon_label.setPixmap(qta.icon("fa5s.bookmark", color=self.get_class_color(cls)).pixmap(24, 24))
                card_layout.addWidget(icon_label)
                
                # Name
                name_label = QLabel(name)
                name_label.setStyleSheet("font-weight: 600; font-size: 13px;")
                card_layout.addWidget(name_label)
                
                card_layout.addStretch()
                
                # Actions
                btn_view = QPushButton("View List")
                btn_view.setStyleSheet("background-color: #334155; border-radius: 4px; padding: 4px 10px; font-size: 11px;")
                # Capture code in lambda properly
                btn_view.clicked.connect(lambda checked, c=code, n=name: self.show_deck_list(n, c))
                card_layout.addWidget(btn_view)
                
                self.grid_layout.addWidget(card)
        
        self.grid_layout.addStretch()

    def show_deck_list(self, name, code):
        from PyQt6.QtWidgets import QDialog, QTextEdit
        from simulator.deck_generator import DeckGenerator
        from simulator.card_loader import CardDatabase
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"List: {name}")
        dialog.resize(400, 600)
        layout = QVBoxLayout(dialog)
        
        # Decode deck
        try:
            card_ids = DeckGenerator.decode_deck_string(code)
        except Exception as e:
            card_ids = None
            print(f"Error decoding deck: {e}")
            
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        
        if card_ids:
            # Load DB names
            db = CardDatabase.get_instance()
            if not db._loaded:
                db.load()
                
            # Format text
            content = f"### {name}\n\n"
            
            # Count cards
            from collections import Counter
            counts = Counter(card_ids)
            
            # Sort by cost
            cards_info = []
            for cid, count in counts.items():
                card_def = db.get_card(cid)
                if card_def:
                    cards_info.append((card_def.cost, card_def.name, count))
                else:
                    cards_info.append((0, cid, count))
                    
            cards_info.sort(key=lambda x: x[0]) # Sort by cost
            
            for cost, cname, count in cards_info:
                prefix = f"[{cost}]"
                count_str = " x2" if count > 1 else "   "
                content += f"{prefix} {cname} {count_str}\n"

            text_area.setMarkdown(content)
        else:
             text_area.setText("Error: Could not decode deck string. Ensure 'hearthstone-deckstrings' is installed and card database is loaded.")

        layout.addWidget(text_area)
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.exec()

    def get_class_color(self, cls):
        colors = {
            "MAGE": "#3b82f6",
            "WARRIOR": "#ef4444",
            "ROGUE": "#f59e0b",
            "DRUID": "#10b981",
            "PALADIN": "#fbbf24",
            "PRIEST": "#f1f5f9",
            "HUNTER": "#22c55e",
            "WARLOCK": "#a855f7",
            "SHAMAN": "#2563eb",
            "DEMONHUNTER": "#8b5cf6",
            "DEATHKNIGHT": "#14b8a6"
        }
        return colors.get(cls.upper(), "#94a3b8")
