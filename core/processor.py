import os
import json
from rich.console import Console
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

console = Console()


def configurar_api_key(api_key: str):
    genai.configure(api_key=api_key)


def carregar_base_de_conhecimento(pasta_json: str) -> list:
    """
    Carrega todos os arquivos JSON da pasta como base de conhecimento.
    """
    base_conhecimento = []

    if not os.path.exists(pasta_json):
        console.print(f"[red]Erro: Pasta {pasta_json} não encontrada.[/]")
        return base_conhecimento

    arquivos_json = sorted(f for f in os.listdir(pasta_json) if f.lower().endswith(".json"))

    for arquivo in arquivos_json:
        caminho = os.path.join(pasta_json, arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dado = json.load(f)
                base_conhecimento.append(dado)
        except Exception as e:
            console.print(f"[yellow]Aviso: erro ao carregar {arquivo}: {e}[/]")

    return base_conhecimento


def montar_prompt(pergunta: str, documentos: list[dict], max_chars_por_doc: int = 3000) -> str:
    """
    Monta o prompt combinando a pergunta do usuário com trechos dos documentos.
    """
    prompt = "Você é um assistente que responde com base nos documentos abaixo:\n\n"

    for doc in documentos:
        conteudo_cortado = doc["conteudo"][:max_chars_por_doc]
        prompt += f"[Arquivo: {doc['arquivo']}]\n{conteudo_cortado}\n\n"

    prompt += f"Pergunta: {pergunta}\nResposta:"
    return prompt


def perguntar_ao_assistente(prompt: str, api_key: str, model_name: str = "gemini-1.5-flash") -> str:
    """
    Envia o prompt para o modelo da Google e retorna a resposta.
    """
    configurar_api_key(api_key)

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except GoogleAPIError as e:
        console.print(f"[bold red]Erro na API do Gemini:[/] {e}")
        return "Erro ao acessar a API do Gemini."
    except Exception as e:
        console.print(f"[bold red]Erro inesperado:[/] {e}")
        return "Erro interno ao tentar responder à pergunta."
