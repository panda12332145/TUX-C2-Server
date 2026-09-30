"""Configuração central do TUX-C2-Server (usada por servidor e beacon)."""
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("TUX_PORT", "9999"))
BEACON_HOST = os.environ.get("TUX_BEACON_HOST", "127.0.0.1")
MAX_CONNECTIONS = 10
BUFFER_SIZE = 4096
