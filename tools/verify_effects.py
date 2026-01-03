import os
import sys
import importlib.util
import inspect
from unittest.mock import MagicMock

# Path hack
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulator.enums import CardType, Race, Zone

def verify_all_effects():
    effects_dir = "card_effects"
    print(f"Scanning {effects_dir} for potential errors...")
    
    error_count = 0
    success_count = 0
    
    # Mock game environment
    mock_game = MagicMock()
    # Ensure register_trigger exists
    mock_game.register_trigger = MagicMock()
    
    for root, dirs, files in os.walk(effects_dir):
        for file in files:
            if file.startswith("effect_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                card_id = file.replace("effect_", "").replace(".py", "")
                
                try:
                    # 1. Try to import the module (catches syntax and top-level import errors)
                    spec = importlib.util.spec_from_file_location("module.name", file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 2. Try to run setup (catches attribution and signature errors)
                    if hasattr(module, "setup"):
                        mock_source = MagicMock()
                        # Setup might access source.controller.hero
                        mock_source.controller = MagicMock()
                        mock_source.controller.hero = MagicMock()
                        mock_source.card_id = card_id
                        
                        # Inspect the setup function to see if it registers triggers
                        # We intercept register_trigger to check the callback signatures
                        def mock_register(trigger_name, source, callback):
                            expected_args = {
                                'on_turn_end': 3,    # (game, trig_src, turn_count)
                                'on_turn_start': 3,  # (game, trig_src, turn_count)
                                'on_card_played': 4, # (game, trig_src, card, target)
                                'on_minion_died': 3, # (game, trig_src, minion)
                                'on_damage': 4,      # (game, trig_src, target, amount)
                            }
                            
                            if trigger_name in expected_args:
                                sig = inspect.signature(callback)
                                if len(sig.parameters) != expected_args[trigger_name]:
                                    raise TypeError(f"Trigger '{trigger_name}' handler '{callback.__name__}' expects {len(sig.parameters)} args, but simulator sends {expected_args[trigger_name]}")

                        mock_game.register_trigger.side_effect = mock_register
                        module.setup(mock_game, mock_source)
                    
                    success_count += 1
                except Exception as e:
                    print(f"ERROR in {file_path}:")
                    print(f"   -> {type(e).__name__}: {e}")
                    error_count += 1

    print("\n--- Verification Result ---")
    print(f"Verified: {success_count} cards")
    print(f"Failed:   {error_count} cards")
    
    if error_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    verify_all_effects()
