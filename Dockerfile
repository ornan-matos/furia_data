# Etapa base: Python leve
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expondo a porta padrão do Streamlit
EXPOSE 8501

# Define variável de ambiente padrão para modo offline
ENV OFFLINE_MODE=true

# Instalação OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-por libtesseract-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Comando de entrada
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
