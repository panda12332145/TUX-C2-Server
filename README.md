# 🧭 TUX-C2-Server — Servidor C2 em Python (Lab)
<p align="center">
  <img alt="Tamanho do repositório" src="https://img.shields.io/github/repo-size/panda12332145/TUX-C2-Server">
  <a href="https://github.com/panda12332145/TUX-C2-Server/commits/main"><img alt="Último commit" src="https://img.shields.io/github/last-commit/panda12332145/TUX-C2-Server"></a>
  <a href="https://github.com/panda12332145/TUX-C2-Server"><img alt="Stars" src="https://img.shields.io/github/stars/panda12332145/TUX-C2-Server?style=social"></a>
  <img alt="Linguagem" src="https://img.shields.io/badge/language-Python-blue">
</p>
---
> ⚠️ **Uso educacional/lab:** servidor C2 (command & control) exclusivamente para **ambientes autorizados** e estudo de defesa. Uso sem autorização é crime (Lei 12.737/2012 — Marco Civil / Código Penal art. 154-A).

---
## 🔖 Resumo

**C2 (Command & Control) em Python** composto por um **servidor TCP** com painel de operador em CLI (listagem de máquinas conectadas com país, usuário, SO e IP) e um **beacon** que coleta dados do host de forma *best-effort* e se registra no servidor. Toda configuração (host, porta, buffer) vive em `config/settings.py` — cliente e servidor compartilham o mesmo lugar.

### ✨ Funcionalidades Principais

- ✅ Painel de operador: lista máquinas registradas com país/usuário/SO/IP
- ✅ Beacon com país via `ipapi.co` (best-effort, fallback honesto 'Desconhecido')
- ✅ `config/settings.py` centralizado — sem HOST/PORT duplicados entre arquivos
- ✅ Servidor multi-cliente com `threading` + `SO_REUSEADDR` (restart sem porta presa)
- ✅ Identificador de máquina por MAC (`uuid.getnode()` em hex)
- ✅ Fallback de usuário sem TTY (`os.getlogin` → `getpass.getuser`)

## 📽 Demonstração

```text
$ python main.py
╔════════════════════════════════╗
║   TUX PROJECT - C2 SERVER      ║
╚════════════════════════════════╝
[1] Listar máquinas conectadas
[2] Sair
[C2] Opção: 1

  Identificador : 0x8f3a2b1c4d5e
  País          : Brasil
  Usuário       : aluno
  SO            : Linux_6.9.0
```

## ⚙️ Explicação das Partes Importantes

### Configuração compartilhada (`config/settings.py`)

```python
HOST = "0.0.0.0"
PORT = int(os.environ.get("TUX_PORT", "9999"))
BUFFER_SIZE = 4096
```

> Servidor e beacon importam o MESMO módulo — mudar a porta em um lugar só propaga para os dois lados (antes cada arquivo redefinia HOST/PORT e divergiam).

### Beacon sem quebra em ambiente sem TTY

```python
def _current_user():
    try:
        return os.getlogin()
    except OSError:
        return getpass.getuser()   # container/CI sem terminal de controle
```

> `os.getlogin()` falha em shells sem TTY (containers, CI) — o fallback mantém o beacon funcional.

## 🔄 Fluxo de Trabalho / Arquitetura

```mermaid
graph TD
    C[Operador CLI] -->|opção 1| S[Servidor TCP :9999]
    B[Beacon] -->|JSON: identifier/country/os| S
    S --> T[(clients dict)]
    T --> C
    B -->|ipapi.co (best-effort)| A[País ou 'Desconhecido']
```

## 📂 Estrutura do Projeto

```plaintext
TUX-C2-Server/
├── main.py               # entrada do servidor (painel)
├── beacon.py             # entrada do agente beacon
├── config/settings.py    # HOST/PORT/BUFFER compartilhados
├── src/
│   ├── server.py         # TCP server + menu do operador
│   └── client_beacon.py  # coleta de info + envio
├── tests/test_server.py  # 4 testes (socketpair, sem rede)
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologias

| Ferramenta | Uso |
|---|---|
| **Python 3** | Linguagem |
| **sockets TCP** | Transporte |
| **colorama** | Painel colorido |
| **ipapi.co** | GeoIP best-effort |

## ▶️ Instalação

```bash
git clone https://github.com/panda12332145/TUX-C2-Server.git
cd TUX-C2-Server
pip install -r requirements.txt
```

## 🚀 Execução

```bash
# Terminal 1 — servidor:
python main.py

# Terminal 2 — beacon (registro):
python beacon.py

# Porta alternativa:
TUX_PORT=8888 python main.py

# Testes:
python tests/test_server.py
```

## 🧪 Testes

4 testes automatizados: config como fonte única da verdade, forma do beacon, registro de cliente via socketpair e tolerância a payload inválido (JSON corrompido não derruba o handler).

## ⚠️ Limitações

- Beacon não executa comandos remotos — é só registro/inventário (C2 básico didático)
- Sem criptografia/TLS no canal TCP (adição natural no roadmap)
- País depende de rede externa; offline retorna 'Desconhecido' por desenho

## 🚀 Roadmap

- [ ] Canal TLS (ssl.wrap_socket)
- [ ] Heartbeat periódico do beacon
- [ ] Log de eventos do operador
- [ ] Comandos remotos com allowlist (lab)

## 📄 Licença

Todos os direitos reservados ao autor.

---

## 👾 Autor

<p align="center">
  <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/73090399?v=4" width="100px" alt="Avatar"/>
</p>

<p align="center">Feito por <strong>Panda12332145</strong> 👋🏽</p>

---

## 🧑‍💻 Sobre Mim

Sou apaixonado por **Física Teórica, Cibersegurança e Desenvolvimento de Sistemas**. Tenho grande interesse em programação de baixo nível, engenharia reversa, automação, sistemas Windows, criptografia e segurança ofensiva. Também gosto bastante de música, filosofia e computação avançada.

---

## 🌐 Redes

* **Site:** [https://panda-h0me.netlify.app/](https://panda-h0me.netlify.app/)
* **YouTube:** [https://www.youtube.com/@X86BinaryGhost](https://www.youtube.com/@X86BinaryGhost)
* **Instagram:** [https://www.instagram.com/01pandal10/](https://www.instagram.com/01pandal10/)
* **GitHub:** [https://github.com/panda12332145](https://github.com/panda12332145)
* **LinkedIn:** [linkedin.com/in/athos-da-boanergis](https://www.linkedin.com/in/athos-d%C3%A3-boanergis-5585a4288/)

---

## 🚀 Áreas de Interesse

* **Cibersegurança Avançada** 🔒
* **Hacking & Engenharia Reversa** 💻
* **Computação de Baixo Nível** 🖥️
* **Matemática e Física Teórica** 📐⚛️
* **Desenvolvimento de Ferramentas de Segurança** 🛠️

_"Conhecimento é poder, e domínio técnico vem da compreensão profunda dos sistemas."_

---

## 📞 Contato & Suporte

Para colaborações, dúvidas ou sugestões:

📧 **E-mail:** [athos.cybersec@gmail.com](mailto:athos.cybersec@gmail.com)

🐛 **Reportar Bug:** [Abrir Issue](https://github.com/panda12332145/TUX-C2-Server/issues)

💡 **Sugerir Melhoria:** [Discussions](https://github.com/panda12332145/TUX-C2-Server/discussions)
