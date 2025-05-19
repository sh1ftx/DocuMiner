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
  # Tenta instalar Whisper com resume retries para evitar erro por conexão intermitente
  if ! pip install --upgrade --force-reinstall --no-cache-dir --resume-retries 5 git+https://github.com/openai/whisper.git; then
    print_warn "Falha na instalação automática do Whisper. Tentando instalar triton manualmente..."

    TRITON_URL="https://files.pythonhosted.org/packages/7d/74/4bf2702b65e93accaa20397b74da46fb7a0356452c1bb94dbabaf0582930/triton-3.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl"
    TRITON_WHL="triton-3.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl"

    # Faz download com curl ou wget (priorizando curl)
    if command -v curl &> /dev/null; then
      curl -C - -L -o "$TRITON_WHL" "$TRITON_URL" || true
    elif command -v wget &> /dev/null; then
      wget -c -O "$TRITON_WHL" "$TRITON_URL" || true
    else
      print_error "Nem curl nem wget encontrados para baixar triton manualmente."
      exit 1
    fi

    if [ -f "$TRITON_WHL" ]; then
      pip install "$TRITON_WHL" || {
        print_error "Falha ao instalar o arquivo triton manualmente."
        exit 1
      }
      rm -f "$TRITON_WHL"

      print_step "Tentando novamente instalar Whisper..."
      if ! pip install --upgrade --force-reinstall --no-cache-dir git+https://github.com/openai/whisper.git; then
        print_error "❌ Falha ao instalar Whisper após tentativa manual. Abortando."
        exit 1
      fi
    else
      print_error "Arquivo triton não baixado. Abortando."
      exit 1
    fi
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
