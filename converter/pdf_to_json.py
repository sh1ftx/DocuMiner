import os
import json
import pdfplumber
from tqdm import tqdm
from rich.console import Console

console = Console()


def extrair_texto(pdf_path: str) -> str:
    texto = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""
    except Exception as e:
        console.print(f"[red]Erro ao processar {pdf_path}: {e}[/]")
    return texto.strip()


def processar_pdfs(input_dir: str = "pdfs", output_dir: str = "data/jsons") -> None:
    if not os.path.exists(input_dir):
        console.print(f"[red]Diretório de entrada não encontrado: {input_dir}[/]")
        return

    os.makedirs(output_dir, exist_ok=True)

    arquivos = sorted([
        f for f in os.listdir(input_dir)
        if f.lower().startswith("pdf_") and f.lower().endswith(".pdf")
    ])

    if not arquivos:
        console.print(f"[yellow]Nenhum arquivo PDF encontrado em {input_dir}.[/]")
        return

    for nome_pdf in tqdm(arquivos, desc="Convertendo PDFs"):
        caminho_pdf = os.path.join(input_dir, nome_pdf)
        texto = extrair_texto(caminho_pdf)

        if not texto:
            console.print(f"[yellow]Aviso: Nenhum texto extraído de {nome_pdf}.[/]")
            continue

        json_data = {
            "arquivo": nome_pdf,
            "conteudo": texto
        }

        nome_json = nome_pdf.replace(".pdf", ".json")
        caminho_json = os.path.join(output_dir, nome_json)

        try:
            with open(caminho_json, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            console.print(f"[red]Erro ao salvar JSON {nome_json}: {e}[/]")


if __name__ == "__main__":
    processar_pdfs()
