# 📋 HearthstoneOne — Roadmap

> Last updated: 2026-01-03

---

## ✅ Phase 0: Universal Simulator

| Task | Status |
|------|--------|
| Simulator Architecture | ✅ |
| Base Game Engine | ✅ |
| Triggers & Events System | ✅ |
| LLM Effect Generation | ✅ |
| History Trackers | ✅ |
| Complex Card Validation (Rewind) | ✅ |
| RL Wrapper | ✅ |

---

## ✅ Phase 1: Data Structures

| Task | Status |
|------|--------|
| `game_wrapper.py` | ✅ |
| `game_state.py` | ✅ |
| `actions.py` | ✅ |
| Unit Tests | ✅ |

---

## ✅ Phase 2: Self-Play Engine

| Task | Status |
|------|--------|
| `self_play.py` | ✅ |
| Self-play Tests | ✅ |

---

## ✅ Phase 3: Core AI (MCTS + Neural Network)

| Task | Status |
|------|--------|
| `model.py` — Actor-Critic Network | ✅ |
| `encoder.py` — State/Action Encoding | ✅ |
| `mcts.py` — Monte Carlo Tree Search | ✅ |
| Game State Cloning | ✅ |
| AI Core Tests | ✅ |

---

## ✅ Phase 4: Training Loop

| Task | Status |
|------|--------|
| `replay_buffer.py` — Trajectory Storage | ✅ |
| `data_collector.py` — Parallel Self-Play (8 workers) | ✅ |
| `trainer.py` — PyTorch Loop | ✅ |
| TensorBoard & Resume Functionality | ✅ |
| Proof of Life (Decreasing Loss) | ✅ |

---

## ✅ Phase 5: Evaluation & Optimization

| Task | Status |
|------|--------|
| `evaluation.py` Script | ✅ |
| Meta Decks Integration (HSGuru) | ✅ |
| Auto-Validation of Cards (`verify_effects.py`) | ✅ |
| Custom Meta Decks JSON Support | ✅ |
| MCTS Optimization | ✅ |
| Hyperparameter Tuning | 🚧 |

---

## ✅ Phase 6: Graphical User Interface (GUI)

| Task | Status |
|------|--------|
| `gui/main_window.py` — Dashboard | ✅ |
| Real-time Training Statistics | ✅ |
| Meta Decks Library | ✅ |
| Training Controls (Start/Stop) | ✅ |
| Integrated Log Terminal | ✅ |

---

## ✅ Phase 7: Runtime (Logs & Parser)

| Task | Status |
|------|--------|
| `runtime/log_watcher.py` — Watch Power.log | ✅ |
| Auto-reconnection (Poll) | ✅ |
| `runtime/parser.py` — Parse TAG_CHANGE | ✅ |
| `runtime/parser.py` — Parse FULL_ENTITY | ✅ |
| Extract ZONE, DAMAGE, CONTROLLER | ✅ |
| Extract zonePos | ✅ |
| Handle SETASIDE (Discover) | ✅ |
| Parser Tests | ✅ |

---

## ✅ Phase 8: Graphical Overlay

| Task | Status |
|------|--------|
| `overlay/overlay_window.py` — Premium Design | ✅ |
| Glassmorphism & Animations | ✅ |
| `overlay/geometry.py` — Screen Coordinates | ✅ |
| Neon Arrows (Targeted Cards) | ✅ |
| Golden Circles (Untargeted Cards) | ✅ |
| `runtime/live_assistant.py` — Orchestrator | ✅ |
| Card & Attack Suggestions | ✅ |
| Win Probability Display (%) | ✅ |
| Spy Mode Configuration Tab | ✅ |

---

## ✅ Phase 10: Trained AI Integration

| Task | Status |
|------|--------|
| Connect `model.py` to `live_assistant.py` | ✅ |
| Real-time MCTS (Inference) | ✅ |
| Optimized GPU Inference | ✅ |

---

## ⏳ Phase 11: Export & Future

| Task | Status |
|------|--------|
| Export ONNX | ⏳ |
| Mobile Version / Lightweight Inference | ⏳ |
| Opponent Archetype Analysis (Spy Mode) | ⏳ |

---

## 📊 Summary

| Phase | Status |
|-------|--------|
| Phase 0 — Simulator | ✅ Complete |
| Phase 1 — Structures | ✅ Complete |
| Phase 2 — Self-Play | ✅ Complete |
| Phase 3 — Core AI | ✅ Complete |
| Phase 4 — Training | ✅ Complete |
| Phase 5 — Evaluation | ✅ Complete |
| Phase 6 — GUI | ✅ Complete |
| Phase 7 — Runtime | ✅ Complete |
| Phase 8 — Overlay | ✅ Complete |
| Phase 10 — Integration | ✅ Complete |
| Phase 11 — Future | ⏳ Pending |
