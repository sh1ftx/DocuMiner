#!/bin/bash

# ==============================================================================
# CONFIG.SH - INSTALADOR AUTOMÁTICO E ROBUSTO DO PROJETO: DOCUMINER
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

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  if [ -f /etc/debian_version ]; then
    OS="debian"
    PM="sudo apt"
  elif [ -f /etc/arch-release ]; then
    OS="arch"
    PM="sudo pacman -Sy"
  else
    print_error "Distribuição Linux não suportada automaticamente."
    exit 1
  fi
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
  OS="windows"
  PM="choco"
else
  print_error "Sistema operacional não reconhecido: $OSTYPE"
  exit 1
fi

echo "Sistema detectado: $OS"

print_header "Verificando o Python..."

if ! command -v python3 &> /dev/null; then
  print_warn "Python3 não encontrado."
  if ask_user "Deseja instalar o Python3 agora?"; then
    if [ "$OS" = "debian" ]; then
      $PM update
      $PM install python3 python3-pip python3-venv -y
    elif [ "$OS" = "arch" ]; then
      $PM python python-pip python-virtualenv --noconfirm
    elif [ "$OS" = "windows" ]; then
      $PM install python -y
    fi
  else
    print_error "Instalação do Python cancelada."
    exit 1
  fi
else
  echo "Python já está instalado."
fi

print_header "Criando ambiente virtual 'venv'..."

if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Ambiente virtual criado."
fi

# Ativa o ambiente virtual (suporte Windows e Linux)
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
else
  print_error "Ambiente virtual não encontrado."
  exit 1
fi

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
