from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QProgressBar, QApplication)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor, QFont
import os
import json
from training.trainer import Trainer

class TrainingWorker(QThread):
    stats_signal = pyqtSignal(dict)
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.trainer = Trainer()
        
    def run(self):
        try:
            # Override iteration_callback to send signals
            def iteration_callback(stats):
                self.stats_signal.emit(stats)
                
            self.trainer.train(iteration_callback=iteration_callback)
        except Exception as e:
            self.log_signal.emit(f"Error: {e}")

class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        # ... (keep existing layout code but connect buttons)
        
        # (Inside __init__ after button creation)
        # ... (rest of the code will be replaced by the full content below for consistency)

    # I will rewrite the whole class to ensure all connections are there
    def __init__(self):
        super().__init__()
        self.worker = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(0)
        
        # 1. Branding
        branding_layout = QVBoxLayout()
        branding_layout.setContentsMargins(0, 0, 0, 40)
        self.logo_label = QLabel()
        logo_path = os.path.join("gui", "assets", "logo.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pix)
        else:
            self.logo_label.setText("💠")
            self.logo_label.setStyleSheet("font-size: 80px; color: #0078d4;")
        branding_layout.addWidget(self.logo_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.title_label = QLabel("DeepMana Hub")
        self.title_label.setStyleSheet("font-size: 32px; color: #ffffff; font-weight: 600; margin-top: 10px;")
        branding_layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.version_label = QLabel("REINFORCEMENT LEARNING ENGINE")
        self.version_label.setStyleSheet("font-size: 11px; color: #8a8a8a; font-weight: 500; letter-spacing: 1px;")
        branding_layout.addWidget(self.version_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(branding_layout)
        
        # 2. Main Dashboard Card
        self.dash_card = QFrame()
        self.dash_card.setObjectName("dash_card")
        self.dash_card.setMinimumHeight(280)
        self.dash_layout = QVBoxLayout(self.dash_card)
        self.dash_layout.setContentsMargins(40, 40, 40, 40)
        self.dash_layout.setSpacing(40)
        
        stats_row = QHBoxLayout()
        self.stat_iter = self.create_mini_stat("ITERATION", "0")
        self.stat_status = self.create_mini_stat("STATUS", "READY")
        self.stat_wr = self.create_mini_stat("WIN RATE (P2)", "--%")
        stats_row.addWidget(self.stat_iter)
        stats_row.addStretch()
        stats_row.addWidget(self.stat_status)
        stats_row.addStretch()
        stats_row.addWidget(self.stat_wr)
        self.dash_layout.addLayout(stats_row)
        
        action_layout = QHBoxLayout()
        self.btn_start = QPushButton("START TRAINING")
        self.btn_start.setObjectName("neural-btn")
        self.btn_start.setFixedSize(200, 44)
        self.btn_start.clicked.connect(self.start_training)
        
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setObjectName("stop-btn")
        self.btn_stop.setFixedSize(120, 44)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_training)
        
        action_layout.addStretch()
        action_layout.addWidget(self.btn_start)
        action_layout.addWidget(self.btn_stop)
        action_layout.addStretch()
        self.dash_layout.addLayout(action_layout)
        self.layout.addWidget(self.dash_card)
        self.layout.addStretch()

    def create_mini_stat(self, label, value):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #8a8a8a; font-size: 11px; font-weight: 600;")
        val = QLabel(value)
        val.setStyleSheet("color: #ffffff; font-size: 28px; font-weight: 600;")
        l.addWidget(lbl)
        l.addWidget(val)
        w.val_label = val
        return w

    def start_training(self):
        self.worker = TrainingWorker()
        self.worker.stats_signal.connect(self.update_data)
        self.worker.start()
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.stat_status.val_label.setText("INITIALIZING")
        self.stat_status.val_label.setStyleSheet("color: #0078d4; font-size: 28px; font-weight: 600;")

    def stop_training(self):
        if self.worker:
            self.worker.trainer.stop_flag = True
            self.stat_status.val_label.setText("STOPPING...")
            self.btn_stop.setEnabled(False)

    def update_data(self, stats):
        iteration = stats.get("iteration", 0)
        winners = stats.get("winners", {})
        total = sum(winners.values())
        wr = (winners.get(2, 0) / total * 100) if total > 0 else 0
        
        self.stat_iter.val_label.setText(str(iteration))
        self.stat_status.val_label.setText("LEARNING")
        self.stat_status.val_label.setStyleSheet("color: #0078d4; font-size: 28px; font-weight: 600;")
        self.stat_wr.val_label.setText(f"{wr:.1f}%")
        self.version_label.setText(f"PROCESSING ITERATION {iteration}")

