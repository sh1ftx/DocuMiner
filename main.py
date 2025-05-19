from rich.console import Console
from core import processor, prompt_builder  # para funções relacionadas à base e Gemini
from ui import banner, login, terminal_ui
from converter.pdf_to_json import processar_pdfs  # import correto da função que converte PDFs
import os
import sys

console = Console()

def main():
    banner.show_banner()

    # Autenticação / login do usuário (carregar api_key e user)
    user_data = login.menu_login()
    if not user_data:
        console.print("[bold red]Falha na autenticação. Encerrando.[/]")
        sys.exit(1)

    api_key = user_data.get("api_key")

    # Diretórios
    pasta_pdfs = os.path.join("pdfs")
    pasta_json = os.path.join("data", "jsons")

    # Converte PDFs para JSON (garante dados atualizados)
    if not os.path.exists(pasta_pdfs):
        console.print(f"[bold red]Pasta de PDFs '{pasta_pdfs}' não encontrada. Coloque seus arquivos PDF lá.[/]")
        return

    console.print("[bold cyan]Convertendo PDFs para JSON...[/]")
    processar_pdfs(pasta_pdfs, pasta_json)  # chama a função da pasta converter

    # Carregar base de conhecimento JSON
    if not os.path.exists(pasta_json):
        console.print(f"[bold red]Pasta {pasta_json} não encontrada após conversão. Abortando.[/]")
        return

    console.print("[bold green]Carregando base de conhecimento...[/]")
    base_conhecimento = processor.carregar_base_de_conhecimento(pasta_json)

    console.print("[bold green]Pronto! Você pode fazer perguntas baseadas nos documentos.[/]")
    
    while True:
        pergunta = terminal_ui.input_pergunta()
        if pergunta.lower() in ["sair", "exit", "quit"]:
            console.print("[bold yellow]Saindo... Até a próxima![/]")
            break

        # Monta prompt usando função no processor (ou prompt_builder se preferir)
        prompt = processor.montar_prompt(pergunta, base_conhecimento)

        # Pergunta ao assistente com prompt e api_key
        try:
            resposta = processor.perguntar_ao_assistente(prompt, api_key)
            terminal_ui.print_resposta(resposta)
        except Exception as e:
            console.print(f"[bold red]Erro ao obter resposta do assistente:[/] {e}")

if __name__ == "__main__":
    main()
