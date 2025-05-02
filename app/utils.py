import re
import json
import sqlite3
from app.config import config

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i+1) - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True

def salvar_fan_data(data: dict):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()

    # Cria a tabela se não existir
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

    # Serializa campos complexos (listas e dicionários) como JSON
    valores = (
        data["nome"],
        data["email"],
        data["cpf"],
        data["endereco"],
        json.dumps(data["interesses"]),
        json.dumps(data["atividades"]),
        json.dumps(data["eventos"]),            # ✅ corrigido aqui
        json.dumps(data["produtos"]),
        json.dumps(data["sites"]),
        data["redes_sociais"],
        data["documento"],
        data["relatorio_grok"],
        json.dumps(data.get("dados_x", {}))
    )

    # Atualiza se já existir CPF
    c.execute('''
        INSERT OR REPLACE INTO fans (
            nome, email, cpf, endereco, interesses, atividades, eventos,
            produtos, sites, redes_sociais, documento, relatorio_grok, dados_x
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', valores)

    conn.commit()
    conn.close()

def limpar_formulario():
    # Streamlit já limpa automaticamente com clear_on_submit=True
    pass

