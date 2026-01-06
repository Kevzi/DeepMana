import time
import os

log_path = os.path.join(os.getcwd(), "logs", "Power.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

test_lines = [
    "D 12:00:00.0000000 PowerTaskList.DebugDump() - TAG_CHANGE Entity=GameEntity tag=STEP value=MAIN_ACTION",
    "D 12:00:01.0000000 PowerTaskList.DebugDump() - TAG_CHANGE Entity=Player1 tag=RESOURCES value=5",
    "D 12:00:02.0000000 PowerTaskList.DebugDump() - TAG_CHANGE Entity=Hero1 tag=DAMAGE value=2",
    "D 12:00:03.0000000 PowerTaskList.DebugDump() - TAG_CHANGE Entity=Minion1 tag=DAMAGE value=10",
]

print(f"Simulating logs in {log_path}...")
with open(log_path, 'a', encoding='utf-8') as f:
    for line in test_lines:
        print(f"Writing: {line}")
        f.write(line + "\n")
        f.flush()
        time.sleep(2)

print("Simulation finished.")
