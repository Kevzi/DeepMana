import secrets
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Simulation d'une DB (User Token -> {expiration, hwid, status})
USER_DB = {
    "TOKEN_TEST_ACTIVE": {
        "status": "ACTIVE",
        "expires_at": datetime.now() + timedelta(days=30),
        "hwid": None # Sera lié au premier login
    },
    "TOKEN_TEST_EXPIRED": {
        "status": "EXPIRED",
        "expires_at": datetime.now() - timedelta(days=1),
        "hwid": None
    }
}

def validate_user(token: str, client_hwid: str) -> bool:
    """ Vérifie si le token est valide et lié au bon HWID. """
    user = USER_DB.get(token)
    if not user:
        logger.warning(f"Connection attempt with invalid token: {token}")
        return False
        
    if user["status"] != "ACTIVE":
        logger.warning(f"User {token} has status {user['status']}")
        return False

    if user["expires_at"] < datetime.now():
        user["status"] = "EXPIRED"
        logger.warning(f"User {token} subscription has expired")
        return False

    # HWID Lock logic
    if user["hwid"] is None:
        user["hwid"] = client_hwid
        logger.info(f"Token {token} locked to HWID {client_hwid}")
        return True
    
    if user["hwid"] != client_hwid:
        logger.error(f"HWID MISMATCH for token {token}!")
        return False

    return True

def handle_stripe_webhook(payload: dict):
    """ Met à jour la DB lors d'un paiement Stripe. """
    event_type = payload.get("type")
    # Simulation: On extrait l'ID client lié au token
    # (En vrai, Stripe Metadata contient le Token ou UserID)
    token = payload.get("data", {}).get("object", {}).get("metadata", {}).get("user_token")
    
    if event_type == "invoice.payment_succeeded" and token:
        if token in USER_DB:
            USER_DB[token]["status"] = "ACTIVE"
            USER_DB[token]["expires_at"] = datetime.now() + timedelta(days=30)
            logger.info(f"Subscription renewed for {token}")
