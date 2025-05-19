#!/data/data/com.termux/files/usr/bin/bash

# ==============================================================================
# CONFIG_TERMUX.SH - INSTALADOR AUTOMÁTICO DO DOCUMINER PARA TERMUX
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

📱 Instalando via Termux no Android.
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

print_header "Atualizando pacotes do Termux..."
pkg update -y && pkg upgrade -y

print_header "Instalando Python e dependências básicas..."

pkg install -y python clang libjpeg-turbo libjpeg-turbo-dev fftw libpng zlib \
    libffi freetype freetype-dev libxslt libxml2 libjpeg libjpeg-dev \
    build-essential libcrypt libcrypt-dev

print_step "Verificando pip..."
pip install --upgrade pip setuptools wheel

print_header "Criando ambiente virtual..."

if [ ! -d "venv" ]; then
  python -m venv venv
  echo "Ambiente virtual criado."
fi

source venv/bin/activate

print_step "Instalando dependências do projeto..."
pip install -r requirements.txt || print_warn "Algumas dependências podem precisar de ajustes manuais."

print_step "Deseja instalar Whisper (para transcrição de áudio)?"
if ask_user "Instalar Whisper?"; then
  if ! pip install git+https://github.com/openai/whisper.git; then
    print_error "❌ Falha ao instalar Whisper. Abortando."
    exit 1
  fi
else
  print_warn "Pulando instalação do Whisper."
fi

print_header "Criando estrutura de pastas do projeto..."

mkdir -p data/jsons
mkdir -p logs
mkdir -p user

print_header "Executando o DocuMiner..."

if [ -f "main.py" ]; then
  python main.py
else
  print_error "Arquivo 'main.py' não encontrado na raiz do projeto."
  exit 1
fi
