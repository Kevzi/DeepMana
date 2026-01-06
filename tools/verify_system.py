import asyncio
import websockets
import json
import subprocess
import time
import os

async def verify_system():
    # 1. Start Server in background
    server_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "server.main:app", "--port", "8008"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3) # Wait for server to start

    try:
        url = "ws://localhost:8008/ws/test_client"
        async with websockets.connect(url) as ws:
            # Step 1: Handshake
            handshake = {
                "type": "init",
                "hwid": "MOCK_HWID_123",
                "token": "TOKEN_TEST_ACTIVE"
            }
            await ws.send(json.dumps(handshake))
            
            resp = json.loads(await ws.recv())
            print(f"Auth Response: {resp}")
            if resp.get("type") != "auth_success":
                raise Exception("Auth Failed!")

            # Step 2: Send Game State
            game_state = {
                "type": "game_state_update",
                "data": {"step": "MAIN_ACTION", "mana": 10}
            }
            await ws.send(json.dumps(game_state))
            
            reco = json.loads(await ws.recv())
            print(f"AI Recommendation: {reco}")
            if reco.get("type") != "recommendation":
                raise Exception("Recommendation Failed!")

        print("\n✅ SYSTEM VERIFICATION SUCCESSFUL")

    except Exception as e:
        print(f"\n❌ SYSTEM VERIFICATION FAILED: {e}")
    finally:
        server_process.terminate()

if __name__ == "__main__":
    asyncio.run(verify_system())
