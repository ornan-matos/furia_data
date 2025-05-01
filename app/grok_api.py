# app/grok_api.py
import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from openai import OpenAI
from app.config import config

def extrair_texto_ocr(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)

        # Pré-processamento: escala de cinza
        imagem = imagem.convert("L")

        # Aumentar contraste
        enhancer = ImageEnhance.Contrast(imagem)
        imagem = enhancer.enhance(2.0)

        # Binarização (threshold)
        imagem = imagem.point(lambda x: 0 if x < 140 else 255, '1')

        # Filtro de nitidez
        imagem = imagem.filter(ImageFilter.SHARPEN)

        # Executar OCR
        texto = pytesseract.image_to_string(imagem, lang='por')
        return texto.strip()

    except Exception as e:
        return f"[ERRO AO EXTRAIR TEXTO]: {str(e)}"

def validar_documento_grok(doc_path: str):
    if config.OFFLINE_MODE:
        print("[Modo Offline] Simulando validação de documento com Grok...")
        return True, gerar_relatorio_simulado(os.path.basename(doc_path))

    if not config.GROK_API_KEY:
        return False, "Chave de API do Grok não configurada"

    if not os.path.exists(doc_path):
        return False, "Arquivo de documento não encontrado"

    try:
        texto_extraido = extrair_texto_ocr(doc_path)

        client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=config.GROK_API_KEY
        )

        prompt = (
            "Você é um especialista em análise de documentos brasileiros.\n"
            "Foi extraído o seguinte conteúdo de um documento de identidade por OCR:\n\n"
            f"{texto_extraido}\n\n"
            "Avalie se o conteúdo parece autêntico e, com base nele, gere um pequeno relatório do perfil desse usuário."
        )

        completion = client.chat.completions.create(
            model="grok-3-beta",
            messages=[
                {"role": "system", "content": "Você é um analista de documentos e perfis de usuários."},
                {"role": "user", "content": prompt},
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
