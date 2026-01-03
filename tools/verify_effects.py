import os
import sys
import ast

# Path hack
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def verify_all_effects():
    effects_dir = "card_effects"
    print(f"Scanning {effects_dir} for missing imports and signature errors...")
    
    error_count = 0
    success_count = 0
    
    # Enums we expect to be imported if used
    REQUIRED_ENUMS = {'CardType', 'Race', 'Zone', 'PlayState', 'Mulligan', 'GameTag', 'SpellSchool', 'Rarity', 'CardClass'}
    
    for root, dirs, files in os.walk(effects_dir):
        for file in files:
            if file.startswith("effect_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                    
                    found_names = set()
                    defined_names = {'print', 'len', 'range', 'getattr', 'hasattr', 'setattr', 'list', 'dict', 'set', 'int', 'str', 'bool', 'float', 'type', 'isinstance', 'enumerate', 'abs', 'min', 'max', 'sum', 'any', 'all', 'open', 'round', 'None', 'True', 'False'}
                    
                    # Track imports
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                defined_names.add(alias.asname or alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            for alias in node.names:
                                defined_names.add(alias.asname or alias.name)
                        elif isinstance(node, ast.FunctionDef):
                            defined_names.add(node.name)
                        elif isinstance(node, ast.ClassDef):
                            defined_names.add(node.name)
                    
                    # Collect used Names (in Attributes or raw Name)
                    class NameVisitor(ast.NodeVisitor):
                        def __init__(self):
                            self.used = set()
                            self.defined_in_scope = set()
                        
                        def visit_Name(self, node):
                            if isinstance(node.ctx, ast.Load):
                                self.used.add(node.id)
                            elif isinstance(node.ctx, (ast.Store, ast.Param)):
                                self.defined_in_scope.add(node.id)
                            self.generic_visit(node)
                            
                        def visit_FunctionDef(self, node):
                            # Function names are defined in parent scope
                            # But arguments are defined in this scope
                            old_defined = self.defined_in_scope.copy()
                            for arg in node.args.args:
                                self.defined_in_scope.add(arg.arg)
                            self.generic_visit(node)
                            self.defined_in_scope = old_defined

                    visitor = NameVisitor()
                    visitor.visit(tree)
                    
                    missing = (visitor.used - defined_names - visitor.defined_in_scope)
                    critical_missing = missing.intersection(REQUIRED_ENUMS)
                    
                    if critical_missing:
                        print(f"ERROR in {file_path}:")
                        print(f"   -> Missing imports for: {', '.join(critical_missing)}")
                        error_count += 1
                        continue

                    # Verify setup function signature if exists
                    for node in tree.body:
                        if isinstance(node, ast.FunctionDef) and node.name == 'setup':
                            if len(node.args.args) != 2:
                                print(f"ERROR in {file_path}:")
                                print(f"   -> 'setup' function has {len(node.args.args)} args, expected 2 (game, source)")
                                error_count += 1
                                break
                    else:
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
