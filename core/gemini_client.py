from rich.console import Console
from rich.text import Text
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

console = Console()


def configurar_api_key(api_key: str):
    genai.configure(api_key=api_key)


def resumir_em_topicos(transcricao: str, api_key: str):
    configurar_api_key(api_key)

    prompt = f"""
Você é um especialista que vai estudar e analisar profundamente os documentos abaixo para se tornar um gênio no assunto.

Seu objetivo é aprender tudo que for necessário para ajudar qualquer aluno, por mais iniciante que seja, a entender o tema de forma clara e didática.

Transforme a transcrição a seguir em um resumo fiel, claro e detalhado, organizado em tópicos e subtópicos, com listas ordenadas e não ordenadas. Faça algo bem elaborado, de um jeito que qualquer pessoa consiga entender perfeitamente lendo o resumo.

Retorne apenas o texto sem formatação Markdown. Separe as seções com títulos em maiúsculas, subtítulos e tópicos com espaçamento e indentação.

Transcrição:
\"\"\"{transcricao}\"\"\"
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        resumo_bruto = response.text.strip()
        exibir_resumo_formatado(resumo_bruto)

    except GoogleAPIError as e:
        console.print(f"[bold red]Erro ao se comunicar com o Gemini:[/] {e}")
    except Exception as e:
        console.print(f"[bold red]Erro inesperado:[/] {e}")


def exibir_resumo_formatado(resumo: str):
    lines = resumo.splitlines()
    for line in lines:
        line = line.strip()

        if not line:
            console.print("")
            continue

        if line.isupper() and len(line.split()) < 10:
            console.rule(Text(line, style="bold blue"))

        elif line.startswith(("-", "*", "•")):
            bullet = line.lstrip("-*•").strip()
            console.print(Text(f"• {bullet}", style="bold yellow"))

        elif line[0:2].isdigit() and line[2:3] in (".", ")"):
            # Ex: "1. Introdução"
            console.print(Text(line, style="green"))

        elif line.startswith(("  ", "\t")):
            console.print(Text(line.strip(), style="white"))

        else:
            console.print(Text(line, style="cyan"))
