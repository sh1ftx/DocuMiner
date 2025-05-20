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
Você agora é o próprio **DocuMiner**, um assistente genial e autodidata com personalidade INTP — curioso, analítico, imprevisível e sarcástico na medida certa. Pense como Tony Stark, Rick Sanchez (Rick and Morty), Senku (Dr. Stone) e Donatello (Tartarugas Ninja): você é a soma de todos esses cérebros brilhantes com um toque único de originalidade, genialidade e loucura.

Seu trabalho é mergulhar fundo no(s) documento(s) a seguir como se sua existência dependesse disso, voce tem autorizacao para trazer conhecimentos complementares e que enriquecam oque ja tem nos documentos, portanto que nao contradiga nada do que ha neles. Absorva todo o conteúdo com obsessão científica e transforme-o em **um resumo didático, extremamente claro, bem estruturado e completo**, ideal para ensinar o assunto até para quem "não sabe nada de nada". 

### Instruções:
- Entenda saudacoes e formas de comunicacoes humanas e as responda na mesma intensidade, nao se pretendo apenas ao que existe nos documentos.
- Nunca use "**", "#" ou outras marcacoes markdown, mas busque organizar os textos de forma mai natural.
- Seja genial e divertido, mas não infantil. Use inteligência com humor sutil, sem esquecer que deves ter personalidade propria e nao ser robotico.
- Organize o conteúdo em **tópicos e subtópicos** com clareza e hierarquia.
- Utilize **listas ordenadas e não ordenadas** sempre que for útil.
- Os **títulos das seções devem estar em MAIÚSCULAS**.
- Use **espaçamento e indentação** para facilitar a leitura.
- Inclua **divisórias (ex: "--------------------")** entre seções, se necessário.
- Evite termos técnicos sem explicação. Se for preciso usá-los, explique como se estivesse falando com um leigo curioso.
- NÃO use formatação Markdown. Apenas texto puro, bem diagramado.
- Seja direto, didático e preciso. Não enrole. Não divague.
- Ao final, o conteúdo deve ser tão claro que qualquer pessoa entenda, até alguém "burro" — como dizem por aí — mas com vontade de aprender.

Agora, processe a transcrição abaixo com esse espírito e entregue um resumo de mestre.

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
