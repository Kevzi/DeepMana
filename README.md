<p align="center">
  <img src="client/assets/logo.png" width="250" alt="HearthstoneOne Logo" onerror="this.src='https://raw.githubusercontent.com/Kevzi/HearthstoneOne/main/docs/logo_placeholder.png'">
</p>

# 💠 HearthstoneOne
> **The Ultimate SaaS AI Coaching Platform for Hearthstone** — Real-time Intelligence via Cloud-Inference

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SaaS](https://img.shields.io/badge/Business-SaaS_Architecture-blue?style=for-the-badge)

---

## ✨ What is HearthstoneOne?

HearthstoneOne is a professional-grade AI ecosystem designed for both players and researchers. Unlike traditional local trackers, it uses a **Thick Server / Thin Client** architecture to provide state-of-the-art decision making while protecting intellectual property.

- 🧠 **PPO + Set Transformer** — Uses Proximal Policy Optimization and permutation-invariant attention networks to capture complex card synergies.
- ☁️ **Cloud Inference** — The AI "Brain" lives on high-performance servers, ensuring low latency and high security.
- 👁️ **Premium Animated Overlay** — Neon-style, pulsating visual guides drawn directly over the game using a high-performance Win32 transparent layer.
- 🛡️ **HWID Security** — Enterprise-grade hardware locking and token-based authentication (Ready for Stripe).
- 🏎️ **Universal Simulator** — Custom high-performance engine supporting 7000+ cards with lazy-evaluation optimizations.

---

## 🏗️ SaaS Architecture

HearthstoneOne is split into two optimized components:

```mermaid
flowchart TD
    subgraph LOCAL["💻 USER MACHINE (Client)"]
        HS[Hearthstone Game]
        LOG[Power.log]
        HUB[HearthstoneOne HUB - PySide6]
        OVERLAY[Neon Overlay - Transparent]
        
        HS --> LOG
        LOG -- Tailing --> HUB
        HUB -- Draw --> OVERLAY
    end

    subgraph CLOUD["☁️ AI INFRASTRUCTURE (Server)"]
        FAST[FastAPI Gateway]
        AUTH[HWID & Stripe Shield]
        PPO[PPO Engine]
        TRANS[Set Transformer Model]
        
        FAST --> AUTH
        AUTH --> PPO
        PPO --> TRANS
    end

    HUB -- Secure WebSocket (TLS) --> FAST
    FAST -- Real-time Suggestions --> HUB
```

---

## 🚀 Getting Started

### 1. Server Setup (Backend)
Requires a CUDA-capable GPU for production-ready inference.
```bash
# Install dependencies
pip install -r requirements.txt

# Start the AI Gateway
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### 2. Client Setup (Frontend / HUB)
```bash
# Run the Client HUB
python client/main.py
```

### 3. Training the AI
```bash
# Start the League Training pipeline
python training/ppo_trainer.py
```

---

## 🛡️ Security & Distribution

HearthstoneOne is designed with commercial distribution in mind:
- **HWID Locking**: Prevents account sharing by binding the license to a single motherboard UUID.
- **Binaire Compilation**: The client can be compiled using **Nuitka** to protect source code.
```bash
python tools/build_client.py
```

---

## 🔧 Technical Stack
- **AI**: PyTorch, PPO, Multi-Head Attention (Set Transformer).
- **Backend**: FastAPI, Websockets, Python 3.13.
- **Frontend**: PySide6 (Qt), Win32 API (ctypes), watchdog.
- **Optimization**: Lazy Stat Evaluation, O(1) Snapshotting, GPU Inference.

---

<p align="center">
  <b>HearthstoneOne</b> — Advanced AI Coaching for Strategy Games.
</p>
