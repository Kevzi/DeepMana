import os
import sys
import subprocess

def run_build():
    """
    Compile le client HearthstoneOne en un exécutable autonome (.exe sur Windows).
    Utilise Nuitka pour la compilation en code natif et l'obfuscation.
    """
    entry_point = os.path.join("client", "main.py")
    output_name = "HearthstoneOne_Coach"
    
    print(f"🚀 Starting compilation of {entry_point}...")
    
    # Commande Nuitka avec les flags optimisés pour un SaaS
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",                # Créer un dossier autonome
        "--onefile",                   # Empaqueter le tout dans un seul .exe
        "--enable-plugin=pyside6",     # Support natif pour PySide6 (Qt)
        "--windows-disable-console",   # Ne pas ouvrir de console CMD au lancement
        "--plugin-enable=upx",         # Compresser l'exécutable final (si UPX est présent)
        "--follow-imports",            # Suivre les imports internes (client, server, auth...)
        f"--output-filename={output_name}",
        entry_point
    ]
    
    # Note: On doit s'assurer que 'server.hwid' est accessible car il est importé par le client
    # On ajoute le dossier racine au PYTHONPATH interne de Nuitka
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.getcwd())

    try:
        subprocess.run(cmd, check=True, env=env)
        print(f"✅ Compilation finished! Executable available as {output_name}.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during compilation: {e}")
    except FileNotFoundError:
        print("❌ Nuitka not found. Please run: pip install nuitka")

if __name__ == "__main__":
    run_build()
