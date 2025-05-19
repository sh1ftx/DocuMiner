import os
import json
from typing import List, Dict
from rich.console import Console

console = Console()

class KnowledgeBase:
    def __init__(self, pasta_json: str):
        self.pasta_json = pasta_json
        self.documentos = []

    def carregar(self) -> None:
        if not os.path.exists(self.pasta_json):
            console.print(f"[red]Erro: Pasta {self.pasta_json} não encontrada.[/]")
            return

        arquivos = sorted(f for f in os.listdir(self.pasta_json) if f.lower().endswith(".json"))
        self.documentos.clear()

        for arquivo in arquivos:
            caminho = os.path.join(self.pasta_json, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dado = json.load(f)
                    self.documentos.append(dado)
            except Exception as e:
                console.print(f"[yellow]Erro ao carregar {arquivo}: {e}[/]")

    def buscar_relevantes(self, termo: str, max_docs: int = 5) -> List[Dict]:
        """
        Busca documentos que contenham o termo na chave 'conteudo'.
        Retorna no máximo max_docs documentos.
        """
        termo_lower = termo.lower()
        resultados = [doc for doc in self.documentos if termo_lower in doc["conteudo"].lower()]
        return resultados[:max_docs]

    def get_documentos(self) -> List[Dict]:
        return self.documentos
