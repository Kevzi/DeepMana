from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HearthstoneOne AI Server")

import torch
import os
import sys

# Path adjustment for internal modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.transformer_model import HearthstoneTransformer
from ai.encoder import FeatureEncoder
from ai.actions import Action

# Configuration IA
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "models/ppo_checkpoint_0.pt"

# Initialisation Singleton
model = None
encoder = FeatureEncoder()

def get_model():
    global model
    if model is None:
        model = HearthstoneTransformer(action_dim=300).to(DEVICE)
        if os.path.exists(MODEL_PATH):
            logger.info(f"Loading checkpoint {MODEL_PATH}")
            model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
        model.eval()
    return model

from server.auth import validate_user, handle_stripe_webhook, USER_DB
from fastapi import Request

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.json()
    handle_stripe_webhook(payload)
    return {"status": "success"}

from server.hwid import get_hwid

# Mock Base de données abonnés (User ID -> HWID registered)
# En production, cela viendrait d'une DB PostgreSQL/Redis
REGISTERED_CLIENTS = {
    "user_123": None # Sera rempli au premier login
}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    # 1. Handshake de sécurité obligatoire
    try:
        init_data = await websocket.receive_text()
        init_message = json.loads(init_data)
        client_hwid = init_message.get("hwid")
        user_token = init_message.get("token") # Nouveau : Token d'abonnement
        
        logger.info(f"Auth attempt: Client={client_id}, Token={user_token}")

        if not validate_user(user_token, client_hwid):
            await websocket.send_text(json.dumps({
                "type": "error", 
                "message": "Authentication failed: Invalid token, expired subscription or HWID mismatch."
            }))
            await websocket.close(code=4003) # Policy Violation
            return
            
        logger.info(f"Success! Session started for {client_id}")
        await websocket.send_text(json.dumps({"type": "auth_success", "message": "Subscription Verified"}))

    except Exception as e:
        logger.error(f"Handshake error: {e}")
        await websocket.close()
        return

    ai_model = get_model()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "game_state_update":
                # Phase Prototype : On fait une inférence bidon ou basée sur le state partiel
                # Dans une version finale, on utiliserait structured_encode ici
                
                # Simulation d'une action via le modèle
                # (Ici on utiliserait un état converti pour faire model.forward)
                action_idx = 299 # End Turn par défaut
                
                response = {
                    "type": "recommendation",
                    "action": "END_TURN" if action_idx == 299 else f"ACTION_{action_idx}",
                    "reason": "AI Inference calculated (Prototype)",
                    "confidence": 0.85
                }
                await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Error in websocket for {client_id}: {e}")
