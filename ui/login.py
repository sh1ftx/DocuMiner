from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
import json
import os
import sys

console = Console()
USER_FILE = "user/config.json"

def validar_api_key() -> str:
    console.print(
        Panel(
            Text(
                "🔑 Insira sua API Key válida para o Google Gemini.\n"
                "👉 Caso não tenha, crie uma no portal do Google Cloud:\n"
                "https://aistudio.google.com/app/apikey?hl=pt-br",
                style="bold white",
                justify="center"
            ),
            border_style="bright_blue",
            title="[bold bright_cyan]API Key Gemini[/]"
        )
    )
    while True:
        api_key = Prompt.ask("[bright_magenta]> [/]", password=True).strip()
        if api_key and len(api_key) > 10:
            return api_key
        else:
            console.print("[bold red]API Key inválida ou muito curta. Tente novamente.[/]\n")

def carregar_credenciais() -> dict | None:
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("username") and data.get("api_key"):
                    return data
        except Exception as e:
            console.print(f"[bold red]Erro ao ler config.json:[/] {e}")
    return None

def salvar_credenciais(username: str, senha: str, api_key: str):
    os.makedirs("user", exist_ok=True)
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "username": username,
            "senha": senha,
            "api_key": api_key
        }, f, indent=2, ensure_ascii=False)

def mostrar_usuario(data: dict):
    table = Table(title="Usuário Atual", box=None)
    table.add_column("Campo", style="cyan", no_wrap=True)
    table.add_column("Valor", style="green")

    table.add_row("Nome de usuário", data.get("username", "N/A"))
    table.add_row("API Key", "[bold yellow]Oculta por segurança[/]")
    table.add_row("Senha", "[bold yellow]Simulada / Oculta[/]")
    console.print(table)

def cadastro_usuario():
    console.rule("[bold blue] Cadastro de Novo Usuário [/]", style="blue")
    username = Prompt.ask("[bold bright_cyan]👤 Nome de usuário[/]").strip()
    senha = Prompt.ask("[bold bright_yellow]🔒 Senha (simulada)[/]", password=True)
    api_key = validar_api_key()
    salvar_credenciais(username, senha, api_key)
    console.print(Panel(f"✅ Cadastro concluído para [bold green]{username}[/]", style="green"))
    return {"username": username, "senha": senha, "api_key": api_key}

def alterar_api_key(data: dict):
    console.rule("[bold blue] Alterar API Key [/]", style="blue")
    nova_key = validar_api_key()
    data["api_key"] = nova_key
    salvar_credenciais(data["username"], data.get("senha", ""), nova_key)
    console.print(Panel("[bold green]API Key atualizada com sucesso![/]", style="green"))

def logout():
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)
        console.print(Panel("[bold red]Logout efetuado. Credenciais apagadas.[/]", style="red"))
    else:
        console.print("[bold yellow]Nenhuma credencial encontrada para apagar.[/]")

def menu_login():
    console.rule("[bold cyan] Bem-vindo ao DocuMiner - Login [/]", style="cyan")

    dados = carregar_credenciais()
    if dados:
        console.print(Panel(f"👤 Usuário logado: [bold green]{dados['username']}[/]", style="green"))
    else:
        console.print(Panel("[bold yellow]Nenhum usuário logado.[/]\nFaça cadastro para começar.", style="yellow"))

    while True:
        table = Table(title="Menu de Login", show_header=False, box=None)
        table.add_row("[1] Login com usuário salvo")
        table.add_row("[2] Cadastro de novo usuário")
        table.add_row("[3] Mostrar usuário atual")
        table.add_row("[4] Alterar API Key")
        table.add_row("[5] Logout")
        table.add_row("[0] Sair")
        console.print(table)

        escolha = IntPrompt.ask("Escolha uma opção", default=0)

        if escolha == 1:
            if dados:
                console.print(Panel(f"✅ Login confirmado para [bold green]{dados['username']}[/]", style="green"))
                return {"username": dados["username"], "api_key": dados["api_key"]}
            else:
                console.print("[bold red]Nenhum usuário salvo. Faça cadastro primeiro.[/]\n")
        elif escolha == 2:
            dados = cadastro_usuario()
        elif escolha == 3:
            if dados:
                mostrar_usuario(dados)
            else:
                console.print("[bold yellow]Nenhum usuário salvo para mostrar.[/]\n")
        elif escolha == 4:
            if dados:
                alterar_api_key(dados)
            else:
                console.print("[bold red]Nenhum usuário salvo para alterar API Key.[/]\n")
        elif escolha == 5:
            logout()
            dados = None
        elif escolha == 0:
            console.print("👋 Saindo do DocuMiner. Até logo!")
            sys.exit(0)
        else:
            console.print("[bold red]Opção inválida. Tente novamente.[/]\n")
