# FURIA Fan Data

Sistema completo de coleta de dados de fãs da equipe de eSports FURIA, com integração a redes sociais, análise de perfis, gráficos interativos e validação documental com IA (Grok).

---

## 🚀 Funcionalidades

- Formulário com validação de CPF, email e upload de documento
- Análise de engajamento, eventos e produtos adquiridos
- Validação de documentos com Grok (modo online ou offline)
- Conexão com conta do X (Twitter) via OAuth 2.0 + PKCE
- Armazenamento em SQLite com campos dinâmicos
- Área administrativa com filtros, exclusão e gráficos
- Análise de texto com TF-IDF

---

## 📁 Estrutura do Projeto

```
furia_fan_data/
├── app/
│   ├── admin_panel.py
│   ├── analysis.py
│   ├── callback_handler.py
│   ├── config.py
│   ├── database.py
│   ├── fan_form.py
│   ├── forms.py
│   ├── grok_api.py
│   ├── utils.py
│   └── x_api.py
├── database/
│   └── fan_profiles.db
├── static/
│   └── logo_furia.png
├── uploads/
│   └── (gerado dinamicamente por CPF)
├── .env
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── main.py
```

---

## ⚙️ Requisitos

- Python 3.11+
- Docker (opcional)
- Conta no [Twitter Developer Portal](https://developer.twitter.com/) (para integração com X)

---

## 🔐 Configuração `.env`

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
OFFLINE_MODE=false
GROK_API_KEY=sua_chave_grok_aqui

X_CLIENT_ID=seu_client_id_do_X
X_CLIENT_SECRET=seu_client_secret_do_X
X_REDIRECT_URI=http://localhost:8501

ADMIN_PASSWORD=admin123
DB_PATH=database/fan_profiles.db
UPLOAD_DIR=uploads
```

Se quiser rodar **em modo offline** (sem Grok nem X):
```env
OFFLINE_MODE=true
```

---

## ▶️ Executar Localmente

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar app
```bash
streamlit run main.py
```

---

## 🐳 Usando Docker

### 1. Build da imagem
```bash
docker build -t furia-fan-data .
```

### 2. Rodar com variáveis de ambiente
```bash
docker run -p 8501:8501 --env-file .env furia-fan-data
```

---

## 📊 Acesso à Área Administrativa

Acesse via menu lateral > "Administração" e informe a senha definida em `ADMIN_PASSWORD`.

---

## 🧠 Modo Offline

Para testes locais e simulações sem API externa:
```env
OFFLINE_MODE=true
```
- Dados do X e validação de documento serão simulados.

---

## 📦 Deploy (exemplo: Railway)

- Use o `Dockerfile` fornecido
- Adicione as variáveis do `.env` no painel da Railway
- Certifique-se de expor a porta `8501`

---

## ✍️ Autor

Desenvolvido por Ornan Matos, 2025.
