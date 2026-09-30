"""Testes do TUX-C2-Server (sem interatividade)."""
import json
import os
import socket
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from src import server
from src.client_beacon import collect_system_info


def test_config_is_source_of_truth():
    assert server.HOST == settings.HOST
    assert server.PORT == settings.PORT
    assert settings.BUFFER_SIZE == 4096


def test_collect_system_info_shape():
    info = collect_system_info()
    for key in ("identifier", "country", "status", "username", "os", "ram", "signal"):
        assert key in info, f"faltando {key}"
    assert info["identifier"].startswith("0x")
    assert info["status"] == "online"
    assert "_" in info["os"]  # Sistema_Release


def test_handle_client_registers_beacon():
    server.clients.clear()
    srv, cli = socket.socketpair()
    payload = {
        "identifier": "0xtest123",
        "country": "Brasil",
        "status": "online",
        "username": "lab",
        "os": "Linux_6.9",
        "ram": "8GB",
        "signal": "Boa",
    }
    def send():
        cli.sendall(json.dumps(payload).encode())
        cli.shutdown(socket.SHUT_WR)
    threading.Thread(target=send, daemon=True).start()
    server.handle_client(srv, ("10.0.0.5", 4242))
    assert "0xtest123" in server.clients
    assert server.clients["0xtest123"]["ip"] == "10.0.0.5"
    assert server.clients["0xtest123"]["username"] == "lab"


def test_handle_client_bad_payload():
    server.clients.clear()
    srv, cli = socket.socketpair()
    def send():
        cli.sendall(b"not-json{{{")
        cli.shutdown(socket.SHUT_WR)
    threading.Thread(target=send, daemon=True).start()
    server.handle_client(srv, ("10.0.0.6", 1))   # não deve levantar
    assert not server.clients


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✅ {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")
