import sqlite3
import os
from app.config import config

def inicializar_banco():
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()

    # Cria a tabela principal com colunas dinâmicas serializadas
    c.execute('''
        CREATE TABLE IF NOT EXISTS fans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            cpf TEXT UNIQUE,
            endereco TEXT,
            interesses TEXT,
            atividades TEXT,
            eventos TEXT,
            produtos TEXT,
            sites TEXT,
            redes_sociais TEXT,
            documento TEXT,
            relatorio_grok TEXT,
            dados_x TEXT
        )
    ''')

    conn.commit()
    conn.close()
