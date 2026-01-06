import os
import time
import logging
import re
from PySide6.QtCore import QThread, Signal

class LogReader(QThread):
    """
    Lit Power.log en temps réel (Tailing) et extrait les événements.
    """
    line_received = Signal(str)
    state_changed = Signal(dict)

    def __init__(self, log_path: str):
        super().__init__()
        self.log_path = log_path
        self._running = True
        
        # Regex basiques pour le prototype
        self.re_tag_change = re.compile(r"TAG_CHANGE Entity=(?P<entity>.*) tag=(?P<tag>.*) value=(?P<value>.*)")

    def run(self):
        if not os.path.exists(self.log_path):
            # Créer un dummy log si absent (en dev)
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'w') as f: f.write("")

        with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Aller à la fin du fichier
            f.seek(0, 2)
            
            while self._running:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                self.process_line(line.strip())

    def process_line(self, line: str):
        # Envoyer la ligne brute pour debug
        self.line_received.emit(line)
        
        # Parser les tags critiques
        match = self.re_tag_change.search(line)
        if match:
            entity = match.group("entity")
            tag = match.group("tag")
            value = match.group("value")
            
            # Notifier d'un changement d'état simplifié
            self.state_changed.emit({
                "type": "tag_change",
                "entity": entity,
                "tag": tag,
                "value": value
            })

    def stop(self):
        self._running = False
