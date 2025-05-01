import os
import requests
from app.config import config

def validar_documento_grok(doc_path: str):
    if config.OFFLINE_MODE:
        print("[Modo Offline] Simulando validação de documento com Grok...")
        return True, gerar_relatorio_simulado(os.path.basename(doc_path))

    if not config.GROK_API_KEY:
        return False, "Chave de API do Grok não configurada"

    if not os.path.exists(doc_path):
        return False, "Arquivo de documento não encontrado"

    try:
        with open(doc_path, 'rb') as file:
            files = {'file': file}
            headers = {"Authorization": f"Bearer {config.GROK_API_KEY}"}
            response = requests.post(
                "https://api.grok.example.com/validate_document",
                files=files,
                headers=headers
            )

        if response.status_code == 200:
            resultado = response.json()
            if resultado.get("valid", False):
                return True, resultado.get("report", "Documento validado com sucesso.")
            else:
                return False, resultado.get("message", "Documento inválido.")
        else:
            return False, f"Erro na API do Grok: {response.status_code}"
    except Exception as e:
        return False, f"Erro na requisição: {str(e)}"

def gerar_relatorio_simulado(nome_arquivo: str) -> str:
    return (
        f"Relatório simulado para o documento '{nome_arquivo}':\n"
        "- Documento legível\n"
        "- Dados consistentes com perfil informado\n"
        "- Nenhum indício de fraude\n"
        "- Recomendado para análise de perfil FURIA"
    )
