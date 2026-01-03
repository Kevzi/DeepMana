# 📜 Changelog

All notable changes to the HearthstoneOne project.

---

## [2026-01-03] — Meta Decks JSON & Starcraft Support

### ✨ Added
- **`data/meta_decks.json`** — Externalized deck definitions for easier management.
- **Starcraft Custom Set** — Implemented effects for Photon Cannon, Artanis, Mothership.
- **Custom User Decks** — Added support for user-provided "New Priest" and "New Warlock" archetypes.
- **Data Improver** — `CardDatabase` now prioritizes `data/cards.json` and applies patches from `data/manual_cards.json` to fix missing 2026 cards.

### 🔧 Changed
- **`simulator/deck_generator.py`** — Major refactor to load decks from JSON files dynamically.
- **`gui/tabs/decks_tab.py`** — Updated to consume the new JSON-based deck generator.
- **Model Reset** — Purged old checkpoints to allow fresh training on the fully corrected dataset.

### 🧪 Fixed
- **"Unknown Card" Bug** — Resolved issues with missing DBF IDs by utilizing `manual_cards.json` patches and verifying against HSGuru codes.

---

## [2026-01-03] — Dashboard v1.0 & Fixes

### ✨ Added
- **Dashboard GUI** — Complete training control center with Real-time Stats (Winrate, Loss).
- **Meta Decks Library** — GUI tab to browse 120+ top-tier decks with "View List" popup.
- **Deck Decoder** — Integrated logic to decode DeckStrings into readable card lists (Name, Mana, Count).
- **Stop Button** — Safe training interruption mechanism in `trainer.py`.

### 🔧 Fixed
- **Nozdormu Crash** — Implemented native `dormant` mechanic to prevent simulated crashes.
- **Dynamic Cloning** — Fixed `entities.py` to recursively copy custom attributes (preventing future crashes).
- **Empty Deck List** — Added error handling and visual feedback when decoding decks.
- **Localization** — Full translation of the Interface and Documentation to **English**.

---

## [2026-01-03] — High-Speed Training & Premium Overlay

### ✨ Added
- **Multiprocessing Support** — `training/data_collector.py` now uses 8 parallel workers.
- **Premium Overlay** — New Glassmorphism design with neon effects and pulsating animations.
- **Win Probability** — Dynamic display of win probability (AI Value Head).
- **TensorBoard** — Live tracking of training metrics (Loss, Winners, Buffer).
- **Meta Decks Support** — Integration of 120+ meta decks (HSGuru January 2026).
- **Auto-Validator** — `tools/verify_effects.py` to validate 1800+ effect scripts.
- **Resume System** — Automatic saving and loading of checkpoints (weights + optimizer).

### 🔧 Changed
- **`training/data_collector.py`** — Complete refactor for parallelism.
- **`runtime/live_assistant.py`** — Full AlphaZero AI integration for suggestions.
- **`overlay/overlay_window.py`** — Major aesthetic improvements.
- **Card Fixes** — Massive validation of trigger signatures (on_turn_end, etc.).

---

## [2026-01-03] — Live Assistant & Overlay (V1)

### 🔧 Changed
- **`runtime/log_watcher.py`** — Auto-reconnection if launched before Hearthstone.
- **`runtime/parser.py`** — Robust parsing with flexible regex.
- **`simulator/player.py`** — Added `setaside` and `choices`.
- **`simulator/factory.py`** — Fixed controller assignment.

### 📚 Documented
- `README.md` completely rewritten with Mermaid diagrams.
- `docs/TASKS.md` updated with all phases.

---

## [2026-01-02] — Training Pipeline

### ✨ Added
- **`training/trainer.py`** — PyTorch Training Loop.
- **`training/data_collector.py`** — Trajectory collection via self-play.
- **`ai/replay_buffer.py`** — Optimized data storage.

### 🧪 Tested
- Proof of Life: Decreasing Loss after a few iterations.

---

## [2026-01-01] — Core AI

### ✨ Added
- **`ai/model.py`** — Actor-Critic Network (Policy + Value heads).
- **`ai/mcts.py`** — Monte Carlo Tree Search with UCB.
- **`ai/encoder.py`** — Game state encoding to tensor (690 dimensions).
- **`evaluation.py`** — Basic evaluation script.

---

## [2025-12-31] — Universal Simulator

### ✨ Added
- **`simulator/game.py`** — Complete Game Engine.
- **`simulator/player.py`** — Player management (hand, board, deck).
- **`simulator/entities.py`** — Cards, Minions, Heroes, Powers.
- **`simulator/card_loader.py`** — Loading from hearthstone_data.
- **`simulator/enums.py`** — Enumerations (Zone, CardType, etc.).

### 🔧 Changed
- Complete migration from Fireplace to custom simulator.

---

## [2025-12-30] — Initial Setup

### ✨ Added
- Project structure.
- `requirements.txt`.
- Base architecture.
