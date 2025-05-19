from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def print_status(msg: str):
    console.print(f"🟡 {msg}", style="bold yellow")

def print_success(msg: str):
    console.print(f"✅ {msg}", style="bold green")

def print_error(msg: str):
    console.print(f"❌ {msg}", style="bold red")

def input_pergunta() -> str:
    return Prompt.ask("\n🤖 [bold cyan]Pergunte algo com base nos documentos[/]")

def print_resposta(texto: str):
    painel = Panel.fit(
        texto,
        title="🤖 [bold green]Resposta do DocuMiner[/]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(painel)

def mostrar_progresso(tarefa: str, duracao_segundos: float):
    """
    Exibe uma barra/spinner de progresso simulada para tarefas que demoram um pouco.
    Exemplo de uso: mostrar_progresso("Carregando documentos...", 2.5)
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(tarefa, total=None)
        import time
        time.sleep(duracao_segundos)
        progress.remove_task(task)
