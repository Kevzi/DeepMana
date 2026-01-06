import sys
import json
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PySide6.QtCore import QThread, Signal, Slot
import websockets

from server.hwid import get_hwid

class WebSocketThread(QThread):
    message_received = Signal(str)
    connected = Signal()
    disconnected = Signal()

    def __init__(self, url, token):
        super().__init__()
        self.url = url
        self.token = token
        self._loop = asyncio.new_event_loop()
        self._ws = None
        self._running = True
        self.hwid = get_hwid()

    def run(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._listen())

    async def _listen(self):
        try:
            async with websockets.connect(self.url) as ws:
                self._ws = ws
                
                # Handshake initial avec HWID + TOKEN
                auth_msg = {
                    "type": "init", 
                    "hwid": self.hwid,
                    "token": self.token
                }
                await ws.send(json.dumps(auth_msg))
                
                self.connected.emit()
                while self._running:
                    try:
                        message = await ws.recv()
                        self.message_received.emit(message)
                    except websockets.ConnectionClosed:
                        break
        except Exception as e:
            self.message_received.emit(f"Error: {e}")
        finally:
            self.disconnected.emit()

    def stop(self):
        self._running = False
        if self._ws:
            self._loop.call_soon_threadsafe(self._loop.create_task, self._ws.close())
        self._loop.call_soon_threadsafe(self._loop.stop)

    def send_message(self, data):
        if self._ws:
            asyncio.run_coroutine_threadsafe(self._ws.send(json.dumps(data)), self._loop)

from client.state_manager import StateManager

from client.overlay import OverlayWindow
from PySide6.QtCore import QPoint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HearthstoneOne Coach HUB")
        self.resize(1000, 600)

        # ... (layouts, state_manager, etc.) ...
        # (Restoring layout code for clarity)
        layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        self.send_btn = QPushButton("Force Manual Sync")
        self.send_btn.clicked.connect(self.send_mock_state)
        layout.addWidget(self.send_btn)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.state_manager = StateManager()
        
        # 3. Overlay Window (Transparent)
        self.overlay = OverlayWindow()
        self.overlay.show()

        # 1. WebSocket Thread
        self.ws_thread = WebSocketThread("ws://localhost:8000/ws/user_123", "TOKEN_TEST_ACTIVE")
        self.ws_thread.message_received.connect(self.on_message)
        self.ws_thread.connected.connect(lambda: self.log("<font color='green'>Connection Established...</font>"))
        self.ws_thread.disconnected.connect(lambda: self.log("<font color='red'>Server Disconnected</font>"))
        self.ws_thread.start()

        # 2. Log Reader Thread
        log_path = os.path.join(os.getcwd(), "logs", "Power.log")
        self.log_reader = LogReader(log_path)
        self.log_reader.state_changed.connect(self.on_tag_change)
        self.log_reader.start()

    def on_message(self, message):
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == "auth_success":
                self.log(f"<font color='cyan'>[AUTH] {data.get('message')}</font>")
                self.overlay.status_text = "AUTHENTICATED - READY"
                return
                
            if msg_type == "error":
                self.log(f"<font color='red'><b>[ERROR] {data.get('message')}</b></font>")
                return

            action = data.get('action')
            # Mapping d'action en coordonnées écran (Position bouton Fin de tour par exemple)
            if action == "END_TURN":
                self.overlay.update_recommendations([
                    {'pos': QPoint(1550, 450), 'text': "FIN DU TOUR RECOMMANDÉE"}
                ])
        except Exception as e:
            self.log(f"Error parsing message: {e}")

    def on_tag_change(self, tag_data):
        """Appelé lors d'une ligne TAG_CHANGE détectée."""
        entity = tag_data["entity"]
        tag = tag_data["tag"]
        value = tag_data["value"]
        
        # Mettre à jour le gestionnaire d'état
        self.state_manager.update_tag(entity, tag, value)
        
        # Affichage sélectif dans la GUI
        if tag in ["DAMAGE", "RESOURCES", "STEP", "ZONE"]:
            self.log(f"<i>[STATE] {entity}: {tag} -> {value}</i>")
            
            # Sync avec le serveur
            full_state = self.state_manager.get_game_state_json()
            self.ws_thread.send_message({
                "type": "game_state_update",
                "data": full_state
            })

    def send_mock_state(self):
        full_state = self.state_manager.get_game_state_json()
        self.ws_thread.send_message({
            "type": "game_state_manual_sync",
            "data": full_state
        })
        self.log("<font color='orange'>Manual synchronization sent.</font>")
        mock_data = {
            "type": "game_state",
            "mana": 5,
            "hand_size": 3,
            "my_hp": 30
        }
        self.ws_thread.send_message(mock_data)
        self.log("Sent mock state to server...")

    def closeEvent(self, event):
        self.ws_thread.stop()
        self.ws_thread.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
