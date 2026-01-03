import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QPolygonF
from PyQt6.QtCore import Qt, QTimer, QPointF

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HearthstoneOne Overlay")
        
        # State
        self.arrow_start = None
        self.arrow_end = None
        
        # Window Settings
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        # ... (Geometry resize logic existing)
        if QApplication.primaryScreen():
            screen_geo = QApplication.primaryScreen().geometry()
            self.setGeometry(screen_geo)
        else:
            self.setGeometry(0, 0, 1920, 1080)

        # Layout
        central_widget = QWidget()
        # Important: For painting on top, we might need the widget to handle paint or main window.
        # But QMainWindow paintEvent works if central widget is transparent.
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Labels
        self.status_label = QLabel("🤖 HearthstoneOne AI: Ready")
        self.status_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #00FF00; background-color: rgba(0, 0, 0, 180); padding: 8px; border-radius: 5px;")
        
        self.info_label = QLabel("Waiting for game logs...")
        self.info_label.setFont(QFont("Segoe UI", 14))
        self.info_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); padding: 5px; border-radius: 3px;")
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.info_label)

    def update_info(self, text):
        self.info_label.setText(text)
        
    def set_arrow(self, start, end):
        """Sets arrow coordinates (objects with x, y attributes)."""
        self.arrow_start = start
        self.arrow_end = end
        self.update() # Trigger repaint

    def paintEvent(self, event):
        if self.arrow_start and self.arrow_end:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw Line
            pen = QPen(QColor(0, 255, 0, 200), 6)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            
            start = QPointF(float(self.arrow_start.x), float(self.arrow_start.y))
            end = QPointF(float(self.arrow_end.x), float(self.arrow_end.y))
            
            painter.drawLine(start, end)
            
            # Draw Circle at Target
            painter.setBrush(QColor(0, 255, 0, 100))
            painter.drawEllipse(end, 15, 15)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OverlayWindow()
    window.show()
    print("Overlay started.")
    sys.exit(app.exec())
