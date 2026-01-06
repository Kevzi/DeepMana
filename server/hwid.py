import subprocess
import hashlib
import platform

def get_hwid():
    """
    Génère un identifiant unique pour la machine (HWID) basé sur le matériel.
    """
    system = platform.system()
    try:
        if system == "Windows":
            # Utilisation de l'UUID du bios sur Windows
            cmd = "wmic csproduct get uuid"
            uuid = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        elif system == "Linux":
            # Utilisation de l'id machine sur Linux
            with open("/etc/machine-id", "r") as f:
                uuid = f.read().strip()
        else:
            uuid = platform.node()
    except Exception:
        # Fallback sur le nom de l'ordinateur + processeur si wmic échoue
        uuid = f"{platform.node()}-{platform.processor()}"

    # Hachage pour l'anonymisation et l'uniformisation
    return hashlib.sha256(uuid.encode()).hexdigest()
