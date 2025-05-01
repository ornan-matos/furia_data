import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env na raiz do projeto
load_dotenv()

class Config:
    # Modo offline desativa conexões com APIs externas
    OFFLINE_MODE = os.getenv("OFFLINE_MODE", "true").lower() == "true"

    # Chave da API do Grok
    GROK_API_KEY = os.getenv("GROK_API_KEY")

    # Configurações da API X (Twitter)
    X_CLIENT_ID = os.getenv("X_CLIENT_ID")
    X_CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
    X_REDIRECT_URI = os.getenv("X_REDIRECT_URI", "http://localhost:8501")

    # Senha da área administrativa
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # Caminho do banco de dados SQLite
    DB_PATH = os.getenv("DB_PATH", "database/fan_profiles.db")

    # Diretório onde os uploads são armazenados
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

config = Config()
