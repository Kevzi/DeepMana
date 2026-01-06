import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QPainter, QPen
import ctypes
from ctypes import wintypes

# Windows Constants for click-through
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080

from PySide6.QtGui import QColor, QPainter, QPen, QFont, QLinearGradient, QRadialGradient, QBrush
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, Property, QEasingCurve, QTimer

class OverlayWindow(QMainWindow):
    """
    Overlay Premium avec animations et effets de lueur (Neon/Gamer style).
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        self.recommendations = []
        self._pulse_anim = 0.0
        
        # Timer pour l'animation de pulsation (60 FPS)
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self._update_pulse)
        self.pulse_timer.start(16)
        
        self.status_text = "HEARTHSTONE ONE - ANALYZING..."
        self.status_color = QColor(0, 255, 127) # Spring Green

    def _update_pulse(self):
        import math
        self._pulse_anim = (math.sin(time.time() * 4) + 1) / 2 # 0.0 to 1.0
        self.update()

    def set_click_through(self):
        hwnd = self.winId()
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        new_style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # 1. Barre de Statut Supérieure (Glassmorphism)
        status_rect = self.rect()
        status_rect.setHeight(40)
        grad = QLinearGradient(0, 0, 0, 40)
        grad.setColorAt(0, QColor(20, 20, 25, 200))
        grad.setColorAt(1, QColor(20, 20, 25, 0))
        painter.fillRect(status_rect, grad)

        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        painter.setPen(self.status_color)
        painter.drawText(20, 28, self.status_text)

        # 2. Dessiner les Recommendations de l'IA
        for rec in self.recommendations:
            pos = rec['pos']
            text = rec['text']
            val = self._pulse_anim
            
            # Effet de Lueur (Glow)
            glow_size = 40 + int(20 * val)
            glow = QRadialGradient(pos, glow_size)
            glow.setColorAt(0, QColor(0, 255, 255, int(150 * val)))
            glow.setColorAt(1, QColor(0, 255, 255, 0))
            painter.setBrush(glow)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(pos, glow_size, glow_size)

            # Cercle Central (Neon)
            painter.setBrush(Qt.NoBrush)
            pen = QPen(QColor(0, 255, 255))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawEllipse(pos, 30, 30)

            # Texte avec Ombre
            painter.setFont(QFont("Segoe UI Black", 14))
            painter.setPen(QColor(0, 0, 0, 200)) # Shadow
            painter.drawText(pos.x() + 42, pos.y() + 7, text)
            painter.setPen(QColor(255, 255, 255)) # White text
            painter.drawText(pos.x() + 40, pos.y() + 5, text)
            
            # Ligne de connexion (Optionnel)
            # painter.drawLine(QPoint(20, 20), pos)

    def update_recommendations(self, recs):
        self.recommendations = recs
        self.status_text = "IA RECOMMENDATION READY"
        self.status_color = QColor(255, 215, 0) # Gold
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()
    
    # Simuler une recommandation après 2 secondes
    from PySide6.QtCore import QTimer
    QTimer.singleShot(2000, lambda: overlay.update_recommendations([
        {'pos': QPoint(500, 700), 'text': "PLAY THIS!"},
        {'pos': QPoint(960, 540), 'text': "ATTACK FACE"}
    ]))
    
    sys.exit(app.exec())
