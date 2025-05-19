def montar_prompt(
    pergunta: str,
    documentos: list[dict],
    max_chars_por_doc: int = 3000,
    introducao: str = None,
    estilo_resposta: str = "resposta clara e objetiva"
) -> str:
    """
    Monta o prompt para enviar ao modelo, baseado na pergunta e documentos.

    :param pergunta: Pergunta do usuário.
    :param documentos: Lista de dicts com 'arquivo' e 'conteudo'.
    :param max_chars_por_doc: Limite de caracteres por documento.
    :param introducao: Texto introdutório customizado (padrão explicativo).
    :param estilo_resposta: Como o assistente deve responder (ex: detalhado, resumido).
    :return: String com prompt montado.
    """

    if introducao is None:
        introducao = (
            "Você é um assistente inteligente que responde com base nos documentos abaixo.\n"
            "Use as informações para responder à pergunta do usuário de forma clara e precisa.\n\n"
        )

    prompt = introducao

    for doc in documentos:
        conteudo_cortado = doc['conteudo'][:max_chars_por_doc]
        prompt += f"[Arquivo: {doc['arquivo']}]\n{conteudo_cortado}\n\n"

    prompt += f"Pergunta: {pergunta}\n"
    prompt += f"Por favor, forneça uma {estilo_resposta}.\nResposta:"

    return prompt
