```
 ____  ____  ____  _     _      _  _      _____ ____ 
/  _ \/  _ \/   _\/ \ /\/ \__/|/ \/ \  /|/  __//  __\
| | \|| / \||  /  | | ||| |\/||| || |\ |||  \  |  \/|
| |_/|| \_/||  \_ | \_/|| |  ||| || | \|||  /_ |    /
\____/\____/\____/\____/\_/  \|\_/\_/  \|\____\\_/\_\
```

DocuMiner — Análise inteligente de documentos com IA.

👨‍💻 Desenvolvido por: Kayki Ivan (Sh1ft)


## Índice

- [1. Introdução](#1-introdução)
- [2. Objetivos](#2-objetivos)
- [3. Arquitetura do Projeto](#3-arquitetura-do-projeto)
- [4. Tecnologias Utilizadas](#4-tecnologias-utilizadas)
- [5. Instalação e Execução](#5-instalação-e-execução)
  - [Linux](#linux)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Android (Termux)](#android-termux)
- [6. Funcionalidades](#6-funcionalidades)
- [7. Considerações Finais](#7-considerações-finais)
- [8. Referências](#8-referências)

## 1. Introdução

O **DocuMiner** é uma ferramenta de linha de comando que utiliza inteligência artificial para analisar, resumir e responder perguntas sobre documentos em PDF. Ideal para estudantes, pesquisadores e profissionais que lidam com grandes volumes de informação, o DocuMiner transforma documentos complexos em insights acessíveis.

---

## 2. Objetivos

### Geral

- Facilitar a análise e compreensão de documentos extensos por meio de IA.

### Específicos

- Automatizar a conversão de PDFs para JSON.
- Permitir consultas interativas sobre o conteúdo dos documentos.
- Suportar múltiplos sistemas operacionais.
- Oferecer uma interface de terminal intuitiva.

## 3. Arquitetura do Projeto

```
DocuMiner/
├── main.py
├── core/
│ ├── processor.py
│ └── prompt_builder.py
├── converter/
│ └── pdf_to_json.py
├── ui/
│ ├── banner.py
│ ├── login.py
│ └── terminal_ui.py
├── data/
│ └── jsons/
├── pdfs/
├── logs/
├── user/
├── requirements.txt
├── config.sh
├── config.ps1
├── config_macos.sh
├── config_termux.sh
└── README.md
```

## 4. Tecnologias Utilizadas

- **Python 3.11+**
- **Google Generative AI (gemini-1.5-flash)**
- **Rich**: Para interfaces de terminal aprimoradas.
- **PDFMiner**: Extração de texto de PDFs.
- **OpenAI Whisper**: Transcrição de áudio (opcional).
- **Tqdm**: Barra de progresso.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.

## 5. Instalação e Execução

### Linux (Debian, Arch e derivados)

```bash
git clone https://github.com/sh1ftx/DocuMiner.git
cd DocuMiner
chmod +x config.sh
./config.sh
```

### No Windows: 

```
git clone https://github.com/sh1ftx/DocuMiner.git
cd DocuMiner
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\config.ps1
```

### No MacOS: 

```
git clone https://github.com/sh1ftx/DocuMiner.git
cd DocuMiner
chmod +x config_macos.sh
./config_macos.sh
```

### No Android (Termux):

```
pkg update && pkg upgrade
pkg install git python ffmpeg
git clone https://github.com/sh1ftx/DocuMiner.git
cd DocuMiner
chmod +x config_termux.sh
./config_termux.sh
```
## 6. Funcionalidades

- Conversão de PDFs para JSON: Automatizada para facilitar o processamento.
- Consulta Interativa: Faça perguntas sobre o conteúdo dos documentos.
- Resumos Inteligentes: Geração de resumos concisos dos documentos.
- Suporte Multiplataforma: Compatível com Linux, Windows, macOS e Termux.
- Interface de Terminal Aprimorada: Utiliza a biblioteca Rich para uma melhor experiência.

## 7. Considerações Finais

O DocuMiner é uma solução poderosa para quem precisa extrair informações de grandes volumes de documentos. Com suporte a múltiplas plataformas e uma interface intuitiva, torna a análise de documentos mais eficiente e acessível.

## 8. Referências

- Python Docs: https://docs.python.org/3/
- Gemini API: https://ai.google.dev/
- PyMuPDF: https://pymupdf.readthedocs.io
- Whisper (OpenAI): https://github.com/openai/whisper
- Projeto Termux: https://termux.dev

Desenvolvido com 💡 por Kayki Ivan (Sh1ft)

