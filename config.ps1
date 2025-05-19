# ================================
# CONFIG.PS1 - DOCUMINER INSTALLER
# ================================

$ErrorActionPreference = "Stop"

function Show-Banner {
@"
 ____                 _       _                   
|  _ \  ___  ___ ___ | | __ _| |_ ___  _ __ ___   
| | | |/ _ \/ __/ _ \| |/ _` | __/ _ \| '_ ` _ \  
| |_| |  __/ (_| (_) | | (_| | || (_) | | | | | | 
|____/ \___|\___\___/|_|\__,_|\__\___/|_| |_| |_| 

DocuMiner - Análise inteligente de documentos com AI.

👨‍💻 Desenvolvido por: Kayki Ivan (Sh1ft)
"@
}

function Print-Header($msg) {
    Write-Host "`n============================== $msg ==============================" -ForegroundColor Cyan
}

function Print-Step($msg) {
    Write-Host "[PASSO] $msg" -ForegroundColor Green
}

function Print-Warn($msg) {
    Write-Host "[AVISO] $msg" -ForegroundColor Yellow
}

function Print-Error($msg) {
    Write-Host "[ERRO] $msg" -ForegroundColor Red
    exit 1
}

function Ask-User($question) {
    do {
        $response = Read-Host "$question (s/n)"
    } while ($response -notin @("s", "S", "n", "N"))
    return $response -in @("s", "S")
}

Show-Banner

Print-Header "Verificando o Python..."

if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Print-Warn "Python não encontrado."
    if (Ask-User "Deseja instalar Python via Chocolatey?") {
        if (-not (Get-Command "choco" -ErrorAction SilentlyContinue)) {
            Print-Error "Chocolatey não está instalado. Instale manualmente ou baixe o Python do site oficial."
        }
        choco install python -y
    } else {
        Print-Error "Instalação do Python cancelada."
    }
} else {
    python --version
    Write-Host "Python já instalado."
}

Print-Header "Criando ambiente virtual 'venv'..."

if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "Ambiente virtual criado com sucesso."
}

Print-Step "Ativando o ambiente virtual..."
. .\venv\Scripts\Activate.ps1

Print-Step "Atualizando pip..."
pip install --upgrade pip

Print-Step "Instalando dependências do projeto..."
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Print-Warn "Arquivo requirements.txt não encontrado!"
}

Print-Step "Deseja instalar Whisper (para transcrição de áudio)?"
if (Ask-User "Instalar Whisper?") {
    try {
        pip install git+https://github.com/openai/whisper.git
    } catch {
        Print-Error "❌ Falha ao instalar Whisper. Abortando."
    }
} else {
    Print-Warn "Pulando instalação do Whisper."
}

Print-Header "Garantindo estrutura mínima de diretórios..."
New-Item -ItemType Directory -Force -Path "data/jsons" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "user" | Out-Null

Print-Header "Executando DocuMiner..."
if (Test-Path "main.py") {
    python main.py
} else {
    Print-Error "Arquivo 'main.py' não encontrado. Verifique a estrutura do projeto."
}
