import os
import shutil
import json

def reset_training():
    print("=== Training Reset & Turbo Utility ===")
    
    # 1. Clean Models
    if os.path.exists("models"):
        print("Cleaning models directory...")
        shutil.rmtree("models")
    os.makedirs("models", exist_ok=True)
    
    # 2. Clean Analytics History
    history_paths = ["training_history.json", "gui/training_history.json"]
    for path in history_paths:
        if os.path.exists(path):
            print(f"Cleaning {path}...")
            os.remove(path)
        
    # 3. Clean TensorBoard runs
    if os.path.exists("runs"):
        print("Cleaning runs directory...")
        shutil.rmtree("runs")
    os.makedirs("runs", exist_ok=True)
    # Assuming user has a decent CPU since 8 workers = 50%
    config = {
        "workers": 12, # Turbo!
        "batch_size": 128, # Larger batches for more stability
        "mcts_sims": 40 # Slightly better quality search
    }
    
    with open("training_config.json", 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Turbo configuration created: {config}")
    
    print("\n[OK] Reset complete. Restart the GUI to start fresh with high performance!")

if __name__ == "__main__":
    reset_training()
