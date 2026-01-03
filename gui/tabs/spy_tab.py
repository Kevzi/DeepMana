from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
import qtawesome as qta

class SpyTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # 1. Main Overlay Control
        master_card = QFrame()
        master_card.setProperty("class", "card")
        master_layout = QVBoxLayout(master_card)
        
        title = QLabel("LIVE ASSISTANT")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        master_layout.addWidget(title)
        
        desc = QLabel("The AI analyzes your game live and overlays the best actions on top of Hearthstone.")
        desc.setStyleSheet("color: #94a3b8;")
        master_layout.addWidget(desc)
        
        self.btn_toggle = QPushButton("START ASSISTANT")
        self.btn_toggle.setObjectName("start_btn")
        self.btn_toggle.setFixedHeight(60)
        self.btn_toggle.setIcon(qta.icon("fa5s.play-circle", color="white"))
        master_layout.addWidget(self.btn_toggle)
        
        self.layout.addWidget(master_card)
        
        # 2. Options
        options_layout = QHBoxLayout()
        
        # Display Options
        opt_card = QFrame()
        opt_card.setProperty("class", "card")
        opt_layout = QVBoxLayout(opt_card)
        opt_layout.addWidget(QLabel("DISPLAY SETTINGS"))
        
        self.chk_winrate = QCheckBox("Show Winrate %")
        self.chk_winrate.setChecked(True)
        self.chk_arrows = QCheckBox("Targeting Arrows")
        self.chk_arrows.setChecked(True)
        self.chk_hand = QCheckBox("Hand Analysis")
        self.chk_hand.setChecked(True)
        
        opt_layout.addWidget(self.chk_winrate)
        opt_layout.addWidget(self.chk_arrows)
        opt_layout.addWidget(self.chk_hand)
        options_layout.addWidget(opt_card)
        
        # Engine Options
        eng_card = QFrame()
        eng_card.setProperty("class", "card")
        eng_layout = QVBoxLayout(eng_card)
        eng_layout.addWidget(QLabel("INFERENCE ENGINE"))
        
        self.combo_model = QComboBox()
        self.combo_model.addItem("AlphaZero Model (Latest)")
        self.combo_model.addItem("AlphaZero Model (Best)")
        eng_layout.addWidget(self.combo_model)
        
        eng_layout.addWidget(QLabel("MCTS Simulations:"))
        self.combo_sims = QComboBox()
        self.combo_sims.addItems(["40", "100", "400 (Ultra)"])
        eng_layout.addWidget(self.combo_sims)
        
        options_layout.addWidget(eng_card)
        
        self.layout.addLayout(options_layout)
        self.layout.addStretch()
