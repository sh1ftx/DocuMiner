#!/bin/bash

# ==============================================================================
# CONFIG_MACOS.SH - INSTALADOR AUTOMÁTICO DO DOCUMINER PARA macOS
# ==============================================================================

set -e

LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOGFILE="$LOG_DIR/install.log"
exec > >(tee -i "$LOGFILE")
exec 2>&1

function show_banner() {
cat << "EOF"
 ____                 _       _                   
|  _ \  ___  ___ ___ | | __ _| |_ ___  _ __ ___   
| | | |/ _ \/ __/ _ \| |/ _` | __/ _ \| '_ ` _ \  
| |_| |  __/ (_| (_) | | (_| | || (_) | | | | | | 
|____/ \___|\___\___/|_|\__,_|\__\___/|_| |_| |_| 

DocuMiner - Análise inteligente de documentos com AI.

👨‍💻 Desenvolvido por: Kayki Ivan (Sh1ft)
EOF
}

function print_header() {
  echo -e "\n\033[1;34m================================================================================"
  echo -e "        $1"
  echo -e "================================================================================\033[0m"
}

function print_step() {
  echo -e "\033[1;32m[PASSO] $1\033[0m"
}

function print_warn() {
  echo -e "\033[1;33m[AVISO] $1\033[0m"
}

function print_error() {
  echo -e "\033[1;31m[ERRO] $1\033[0m"
}

function ask_user() {
  read -p "$1 (s/n): " choice
  case "$choice" in
    s|S ) return 0 ;;
    n|N ) return 1 ;;
    * ) echo "Opção inválida." && ask_user "$1" ;;
  esac
}

show_banner

print_header "Detectando Sistema Operacional..."

if [[ "$OSTYPE" == "darwin"* ]]; then
  OS="macos"
  PM="brew"
else
  print_error "Este script é apenas para macOS."
  exit 1
fi

echo "Sistema detectado: $OS"

print_header "Verificando o Python..."

if ! command -v python3 &> /dev/null; then
  print_warn "Python3 não encontrado."
  if ask_user "Deseja instalar o Python3 agora via Homebrew?"; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
  else
    print_error "Instalação do Python cancelada."
    exit 1
  fi
else
  python3 --version
  echo "Python já está instalado."
fi

print_header "Criando ambiente virtual 'venv'..."

if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Ambiente virtual criado."
fi

print_step "Ativando ambiente virtual..."
source venv/bin/activate

print_step "Atualizando pip..."
pip install --upgrade pip

print_step "Instalando dependências do projeto..."
pip install -r requirements.txt || print_warn "Algumas dependências podem precisar ser instaladas manualmente."

print_step "Deseja instalar Whisper (para transcrição de áudio)?"
if ask_user "Instalar Whisper?"; then
  if ! pip install git+https://github.com/openai/whisper.git; then
    print_error "❌ Falha ao instalar Whisper. Abortando."
    exit 1
  fi
else
  print_warn "Pulando instalação do Whisper."
fi

print_header "Garantindo estrutura mínima de diretórios..."

mkdir -p data/jsons
mkdir -p logs
mkdir -p user

print_header "Execução do DocuMiner..."

if [ -f "main.py" ]; then
  python main.py
else
  print_error "Arquivo 'main.py' não encontrado na raiz do projeto. Verifique o projeto."
  exit 1
fi
