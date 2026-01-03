# 📜 Changelog

Toutes les modifications notables du projet HearthstoneOne.

---

## [2026-01-03] — High-Speed Training & Premium Overlay

### ✨ Ajouté
- **Multiprocessing Support** — `training/data_collector.py` utilise désormais 8 workers parallèles.
- **Premium Overlay** — Nouveau design Glassmorphism avec néons et animations de pulsation.
- **Win Probability** — Affichage dynamique des probabilités de victoire (IA Value Head).
- **TensorBoard** — Suivi en direct des metrics d'entraînement (Loss, Winners, Buffer).
- **Meta Decks Support** — Intégration de 120+ decks meta (HSGuru Janvier 2026).
- **Auto-Validator** — `tools/verify_effects.py` pour valider 1800+ scripts d'effets.
- **Resume System** — Sauvegarde et chargement automatique des checkpoints (poids + optimizer).

### 🔧 Modifié
- **`training/data_collector.py`** — Refonte complète pour le parallélisme.
- **`runtime/live_assistant.py`** — Intégration complète de l'IA AlphaZero pour les suggestions.
- **`overlay/overlay_window.py`** — Améliorations esthétiques majeures.
- **Card Fixes** — Correction massive des signatures de triggers (on_turn_end, etc.).

---

## [2026-01-03] — Live Assistant & Overlay (V1)

### 🔧 Modifié
- **`runtime/log_watcher.py`** — Auto-reconnexion si lancé avant Hearthstone
- **`runtime/parser.py`** — Parsing robuste avec regex flexibles
- **`simulator/player.py`** — Ajout de `setaside` et `choices`
- **`simulator/factory.py`** — Correction assignation contrôleur

### 📚 Documenté
- `README.md` entièrement réécrit avec diagrammes Mermaid
- `docs/TASKS.md` mis à jour avec toutes les phases

---

## [2026-01-02] — Training Pipeline

### ✨ Ajouté
- **`training/trainer.py`** — Boucle d'entraînement PyTorch
- **`training/data_collector.py`** — Collecte de trajectoires via self-play
- **`ai/replay_buffer.py`** — Stockage optimisé des données

### 🧪 Testé
- Proof of Life : Loss qui descend après quelques itérations

---

## [2026-01-01] — Core AI

### ✨ Ajouté
- **`ai/model.py`** — Réseau Actor-Critic (Policy + Value heads)
- **`ai/mcts.py`** — Monte Carlo Tree Search avec UCB
- **`ai/encoder.py`** — Encodage état de jeu en tenseur (690 dimensions)
- **`evaluation.py`** — Script d'évaluation basique

---

## [2025-12-31] — Simulateur Universel

### ✨ Ajouté
- **`simulator/game.py`** — Moteur de jeu complet
- **`simulator/player.py`** — Gestion joueur (main, board, deck)
- **`simulator/entities.py`** — Cartes, Serviteurs, Héros, Pouvoirs
- **`simulator/card_loader.py`** — Chargement depuis hearthstone_data
- **`simulator/enums.py`** — Énumérations (Zone, CardType, etc.)

### 🔧 Modifié
- Migration complète depuis Fireplace vers simulateur custom

---

## [2025-12-30] — Setup Initial

### ✨ Ajouté
- Structure du projet
- `requirements.txt`
- Architecture de base
