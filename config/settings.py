import os

# === Diretórios ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(ROOT_DIR, "data")
JSONS_DIR = os.path.join(DATA_DIR, "jsons")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
USER_DIR = os.path.join(ROOT_DIR, "user")

# === API Google Gemini ===
GEMINI_API_BASE_URL = "https://api.generativeai.googleapis.com/v1beta2"  # exemplo
GEMINI_DEFAULT_MODEL = "gemini-1"  # ajuste conforme disponível

# === Prompt ===
MAX_CHARS_PER_DOCUMENT = 3000  # limite padrão para texto em prompt

# === Outros ===
LANGUAGE_DEFAULT = "pt-br"  # idioma padrão
DEBUG = False  # ativa logs/debug extras se True

# === Configurações de timeout / retry para chamadas API, etc ===
API_TIMEOUT_SECONDS = 30
API_MAX_RETRIES = 3
