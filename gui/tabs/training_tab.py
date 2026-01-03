from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QLabel, QPushButton, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
import pyqtgraph as pg

class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # History for plots
        self.loss_history = []
        self.wr_history = []
        self.iterations = []
        
        # 1. Stats Row
        stats_layout = QHBoxLayout()
        self.card_iter = self.create_stat_card("ITERATION", "0 / 100")
        self.card_winrate = self.create_stat_card("P2 WINRATE", "0.0 %")
        self.card_loss = self.create_stat_card("LOSS", "0.000")
        
        stats_layout.addWidget(self.card_iter)
        stats_layout.addWidget(self.card_winrate)
        stats_layout.addWidget(self.card_loss)
        self.layout.addLayout(stats_layout)
        
        # 2. Charts Row
        charts_layout = QHBoxLayout()
        
        # Loss Plot
        self.loss_plot_wid = QFrame()
        self.loss_plot_wid.setProperty("class", "card")
        lp_layout = QVBoxLayout(self.loss_plot_wid)
        lp_layout.addWidget(QLabel("Loss History"))
        self.loss_plot = pg.PlotWidget()
        self.loss_plot.setBackground('transparent')
        self.loss_plot.showGrid(x=True, y=True, alpha=0.3)
        self.loss_plot.setLabel('left', 'Loss')
        self.loss_plot.setLabel('bottom', 'Iteration')
        self.loss_curve = self.loss_plot.plot(pen=pg.mkPen(color='#3b82f6', width=3))
        lp_layout.addWidget(self.loss_plot)
        charts_layout.addWidget(self.loss_plot_wid)
        
        # Winrate Plot
        self.wr_plot_wid = QFrame()
        self.wr_plot_wid.setProperty("class", "card")
        wrp_layout = QVBoxLayout(self.wr_plot_wid)
        wrp_layout.addWidget(QLabel("Player 2 Winrate"))
        self.wr_plot = pg.PlotWidget()
        self.wr_plot.setBackground('transparent')
        self.wr_plot.showGrid(x=True, y=True, alpha=0.3)
        self.wr_plot.setLabel('left', 'Winrate %')
        self.wr_plot.setLabel('bottom', 'Iteration')
        self.wr_plot.setYRange(0, 100)
        self.wr_curve = self.wr_plot.plot(pen=pg.mkPen(color='#10b981', width=3))
        wrp_layout.addWidget(self.wr_plot)
        charts_layout.addWidget(self.wr_plot_wid)
        
        self.layout.addLayout(charts_layout)
        
        # 3. Controls & Progress
        control_card = QFrame()
        control_card.setProperty("class", "card")
        cc_layout = QVBoxLayout(control_card)
        
        top_cc = QHBoxLayout()
        top_cc.addWidget(QLabel("Self-Play Data Collection"))
        self.progress = QProgressBar()
        self.progress.setValue(0)
        top_cc.addWidget(self.progress)
        cc_layout.addLayout(top_cc)
        
        bot_cc = QHBoxLayout()
        self.btn_start = QPushButton("START ENGINE")
        self.btn_start.setObjectName("start_btn")
        self.btn_start.setFixedHeight(45)
        
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setObjectName("stop_btn")
        self.btn_stop.setFixedHeight(45)
        self.btn_stop.setEnabled(False)
        
        bot_cc.addWidget(self.btn_start)
        bot_cc.addWidget(self.btn_stop)
        cc_layout.addLayout(bot_cc)
        
        self.layout.addWidget(control_card)

    def update_data(self, stats):
        """Update the UI with real training statistics."""
        iteration = stats.get("iteration", 0)
        winners = stats.get("winners", {})
        loss = stats.get("avg_loss", 0.0)
        
        # Calculate winrate for P2
        total_games = sum(winners.values())
        wr_p2 = (winners.get(2, 0) / total_games * 100) if total_games > 0 else 0
        
        # Update Cards
        self.card_iter.value_label.setText(f"{iteration} / 100")
        self.card_winrate.value_label.setText(f"{wr_p2:.1f} %")
        self.card_loss.value_label.setText(f"{loss:.3f}")
        
        # Update Plots
        self.iterations.append(iteration)
        self.loss_history.append(loss)
        self.wr_history.append(wr_p2)
        
        self.loss_curve.setData(self.iterations, self.loss_history)
        self.wr_curve.setData(self.iterations, self.wr_history)
        
        # Progress Bar logic (Simplified for now)
        self.progress.setValue(100)

    def create_stat_card(self, title, value):
        card = QFrame()
        card.setProperty("class", "card")
        card_layout = QVBoxLayout(card)
        
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        v_label = QLabel(value)
        v_label.setStyleSheet("color: #f8fafc; font-size: 24px; font-weight: 800;")
        
        card_layout.addWidget(t_label)
        card_layout.addWidget(v_label)
        
        # Store ref to value label to update it later
        card.value_label = v_label
        return card
