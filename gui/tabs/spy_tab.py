from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QComboBox, QCheckBox, QApplication)
from PyQt6.QtCore import Qt
import qtawesome as qta
from runtime.live_assistant import AssistantWorker
from overlay.overlay_window import OverlayWindow

class SpyTab(QWidget):
    def __init__(self):
        super().__init__()
        self.assistant_worker = None
        self.overlay_window = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # 1. Main Overlay Control
        master_card = QFrame()
        master_card.setObjectName("dash_card")
        master_layout = QVBoxLayout(master_card)
        master_layout.setContentsMargins(24, 24, 24, 24)
        master_layout.setSpacing(12)
        
        title = QLabel("LIVE ASSISTANT")
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: white;")
        master_layout.addWidget(title)
        
        desc = QLabel("Real-time game state analysis using the trained AlphaZero neural network.")
        desc.setStyleSheet("color: #8a8a8a; font-size: 13px;")
        master_layout.addWidget(desc)
        
        self.btn_toggle = QPushButton("START ASSISTANT")
        self.btn_toggle.setObjectName("neural-btn")
        self.btn_toggle.setFixedHeight(44)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setIcon(qta.icon("fa5s.play", color="white"))
        self.btn_toggle.clicked.connect(self.toggle_assistant)
        master_layout.addWidget(self.btn_toggle)
        
        self.layout.addWidget(master_card)
        self.layout.addSpacing(20)
        
        # 2. Options
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)
        
        # Display Options
        opt_card = QFrame()
        opt_card.setObjectName("dash_card")
        opt_layout = QVBoxLayout(opt_card)
        opt_layout.setContentsMargins(20, 20, 20, 20)
        opt_layout.setSpacing(15)
        
        opt_title = QLabel("DISPLAY SETTINGS")
        opt_title.setStyleSheet("color: #8a8a8a; font-size: 11px; font-weight: 600; letter-spacing: 0.5px;")
        opt_layout.addWidget(opt_title)
        
        self.chk_winrate = QCheckBox("Show Winrate %")
        self.chk_winrate.setChecked(True)
        self.chk_arrows = QCheckBox("Targeting Arrows")
        self.chk_arrows.setChecked(True)
        self.chk_hand = QCheckBox("Hand Analysis")
        self.chk_hand.setChecked(True)
        
        opt_layout.addWidget(self.chk_winrate)
        opt_layout.addWidget(self.chk_arrows)
        opt_layout.addWidget(self.chk_hand)
        opt_layout.addStretch()
        options_layout.addWidget(opt_card)
        
        # Engine Options
        eng_card = QFrame()
        eng_card.setObjectName("dash_card")
        eng_layout = QVBoxLayout(eng_card)
        eng_layout.setContentsMargins(20, 20, 20, 20)
        eng_layout.setSpacing(15)
        
        eng_title = QLabel("INFERENCE ENGINE")
        eng_title.setStyleSheet("color: #8a8a8a; font-size: 11px; font-weight: 600; letter-spacing: 0.5px;")
        eng_layout.addWidget(eng_title)
        
        eng_layout.addWidget(QLabel("Neural Model Selection:"))
        self.combo_model = QComboBox()
        self.combo_model.addItem("AlphaZero (Auto-Latest)")
        eng_layout.addWidget(self.combo_model)
        
        eng_layout.addWidget(QLabel("MCTS Simulations:"))
        self.combo_sims = QComboBox()
        self.combo_sims.addItems(["40", "100", "400 (High Precision)"])
        eng_layout.addWidget(self.combo_sims)
        eng_layout.addStretch()
        
        options_layout.addWidget(eng_card)
        self.layout.addLayout(options_layout)
        self.layout.addStretch()

    def toggle_assistant(self):
        if self.assistant_worker and self.assistant_worker.isRunning():
            self.stop_assistant()
        else:
            self.start_assistant()

    def start_assistant(self):
        # 1. Create Overlay (Main Thread)
        self.overlay_window = OverlayWindow()
        self.overlay_window.show()
        
        # 2. Create Worker (Background Thread)
        self.assistant_worker = AssistantWorker(use_model=True)
        
        # Get screen geometry for accurate arrow placement
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.geometry()
            self.assistant_worker.geometry.resize(geo.width(), geo.height())
        
        # 3. Connect Signals
        self.assistant_worker.status_signal.connect(self.overlay_window.update_status)
        self.assistant_worker.info_signal.connect(self.overlay_window.update_info)
        self.assistant_worker.winrate_signal.connect(self.overlay_window.update_winrate)
        self.assistant_worker.arrow_signal.connect(self.overlay_window.set_arrow)
        self.assistant_worker.highlight_signal.connect(self.overlay_window.set_highlight)
        
        self.assistant_worker.start()
        
        self.btn_toggle.setText("STOP ASSISTANT")
        self.btn_toggle.setObjectName("stop-btn") # Switch to stop style
        self.btn_toggle.setIcon(qta.icon("fa5s.stop", color="white"))
        self.btn_toggle.setStyle(self.btn_toggle.style()) # Refresh style

    def stop_assistant(self):
        if self.assistant_worker:
            self.assistant_worker.stop()
            self.assistant_worker.wait(2000) # Wait up to 2 seconds
            if self.assistant_worker.isRunning():
                self.assistant_worker.terminate()
            self.assistant_worker = None
        
        if self.overlay_window:
            self.overlay_window.close()
            self.overlay_window = None
            
        self.btn_toggle.setText("START ASSISTANT")
        self.btn_toggle.setObjectName("neural-btn")
        self.btn_toggle.setIcon(qta.icon("fa5s.play", color="white"))
        self.btn_toggle.setStyle(self.btn_toggle.style())

