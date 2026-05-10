from pathlib import Path
import subprocess
import webbrowser
import time
import socket
import sys

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_URL = "http://localhost:8000/dashboard/ALFRED_DASHBOARD_DYNAMIC.html"
PORT = 8000

from datetime import datetime

def log(message: str) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [ALFRED] {message}")


def is_port_used(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex(("localhost", port)) == 0


def run_script(script_name: str) -> None:
    script_path = ROOT / "tools" / "dashboard_tools" / script_name
    log(f"Execution : {script_name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Echec du script : {script_name}")


def start_server() -> subprocess.Popen | None:
    if is_port_used(PORT):
        log(f"Serveur deja actif sur le port {PORT}.")
        return None

    log(f"Lancement du serveur local sur le port {PORT}...")

    return subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=ROOT,
    )


def main() -> None:
    log(f"ROOT = {ROOT}")

    run_script("update_dashboard_data.py")

    server = start_server()

    time.sleep(2)

    log("Ouverture du dashboard...")
    webbrowser.open(DASHBOARD_URL)

    log("Dashboard pret.")
    log(DASHBOARD_URL)

    if server:
        log("Laisse cette fenetre ouverte pour garder le serveur actif.")
        try:
            server.wait()
        except KeyboardInterrupt:
            log("Arret du serveur.")
            server.terminate()


if __name__ == "__main__":
    main()
