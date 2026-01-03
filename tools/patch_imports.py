import os

def patch_effects():
    effects_dir = "card_effects"
    patched_count = 0
    
    enums_to_add = ["CardType", "Race", "Zone"] # Most common missing ones
    
    for root, dirs, files in os.walk(effects_dir):
        for file in files:
            if file.startswith("effect_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                content = "".join(lines)
                needed = []
                for enum in enums_to_add:
                    if enum in content and f"import {enum}" not in content:
                        needed.append(enum)
                
                if needed:
                    # Insert at the top (after docstring if exists)
                    import_line = f"from simulator.enums import {', '.join(needed)}\n"
                    
                    if lines and lines[0].startswith('"""'):
                        # Find end of docstring
                        idx = 1
                        while idx < len(lines) and not lines[idx-1].strip().endswith('"""'):
                            idx += 1
                        lines.insert(idx, import_line)
                    else:
                        lines.insert(0, import_line)
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                    patched_count += 1
                    print(f"Patched {file_path} with {', '.join(needed)}")

    print(f"\nSuccessfully patched {patched_count} files.")

if __name__ == "__main__":
    patch_effects()
