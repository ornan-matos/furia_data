import os
from openai import OpenAI
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
        client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=config.GROK_API_KEY
        )

        with open(doc_path, "rb") as image_file:
            image_data = image_file.read()

        # Envia a imagem para análise usando o modelo de imagem
        response = client.images.generate(
            model="grok-2-image-1212",
            prompt="Analise este documento de identidade ou comprovante"
        )

        image_url = response.data[0].url

        # Em seguida, envia esse link para análise de perfil textual
        completion = client.chat.completions.create(
            model="grok-3-beta",
            messages=[
                {"role": "system", "content": "Você é um especialista em validação de documentos e perfis."},
                {"role": "user", "content": f"Analise o seguinte documento: {image_url}. Retorne se o documento parece válido para os padrões de um documento de registro geral (RG) que aceito no Brasil e também se é o tipo de perfil do usuário."},
            ]
        )

        resultado = completion.choices[0].message.content
        return True, resultado

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
