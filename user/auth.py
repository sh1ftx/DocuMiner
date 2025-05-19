from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import google.generativeai as genai

console = Console()

def validar_api_key(max_tentativas: int = 3) -> str:
    """
    Solicita que o usuário insira uma API key válida para o Google Gemini.
    Valida a chave tentando configurar e listar os modelos.
    Limita tentativas para evitar loop infinito.
    Retorna a chave válida ou encerra o programa após falhas.
    """
    tentativa = 0

    while tentativa < max_tentativas:
        console.print(Panel(
            "[bold cyan]🔑 Insira sua API KEY do Google Gemini[/]\n"
            "[italic]👉 Disponível em: https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br[/italic]",
            border_style="bright_blue",
            title="Autenticação API Key"
        ))
        
        api_key = Prompt.ask("[bold magenta]>[/]").strip()

        if not api_key:
            console.print("[bold red]❌ Nenhuma chave foi inserida. Tente novamente.[/]\n")
            tentativa += 1
            continue

        try:
            genai.configure(api_key=api_key)
            # Testa a chave listando modelos
            genai.list_models()
            console.print("[bold green]✅ API Key validada com sucesso![/]")
            return api_key
        except Exception as e:
            console.print(f"[bold red]❌ Chave inválida ou erro de conexão:[/] {e}\n[bold yellow]🔁 Tente novamente.[/]\n")
            tentativa += 1

    console.print("[bold red]🚫 Número máximo de tentativas atingido. Abortando...[/]")
    raise SystemExit(1)
