# app/x_api.py
import os
import streamlit as st
import requests
import base64
import hashlib
import secrets
from urllib.parse import urlencode
from app.config import config

X_AUTH_URL = "https://twitter.com/i/oauth2/authorize"
X_TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
X_USERINFO_URL = "https://api.twitter.com/2/users/me?user.fields=description,location,public_metrics"

def gerar_pkce():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("utf-8")
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode("utf-8")
    return code_verifier, code_challenge

def iniciar_login():
    code_verifier, code_challenge = gerar_pkce()

    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/code_verifier.txt", "w") as f:
        f.write(code_verifier)

    params = {
        "response_type": "code",
        "client_id": config.X_CLIENT_ID,
        "redirect_uri": config.X_REDIRECT_URI,
        "scope": "tweet.read users.read offline.access",
        "state": secrets.token_urlsafe(16),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    auth_url = f"{X_AUTH_URL}?{urlencode(params)}"

    # Ícone de login com X
    st.markdown(
        f'<a href="{auth_url}" target="_self">'
        f'<img src="https://abs.twimg.com/favicons/twitter.2.ico" width="32" title="Conectar com X" style="margin:5px;"></a>',
        unsafe_allow_html=True
    )

def trocar_codigo_por_token(code):
    try:
        with open(".tmp/code_verifier.txt") as f:
            code_verifier = f.read().strip()
    except FileNotFoundError:
        print("[ERRO] Arquivo de code_verifier não encontrado")
        return False

    data = {
        "client_id": config.X_CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.X_REDIRECT_URI,
        "code_verifier": code_verifier
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print(f"[DEBUG] Enviando dados para token exchange:\n{data}")

    resp = requests.post(X_TOKEN_URL, data=data, headers=headers)

    print(f"[DEBUG] Status da resposta do X: {resp.status_code}")
    print(f"[DEBUG] Corpo da resposta: {resp.text}")

    if resp.status_code == 200:
        token = resp.json()["access_token"]
        st.session_state["x_token"] = token
        st.session_state["x_autenticado"] = True
        print("[DEBUG] Token de acesso salvo em session_state.")
        return True

    print(f"[ERRO] Falha ao trocar código por token. Status: {resp.status_code}")
    return False

def coletar_dados_x():
    if config.OFFLINE_MODE:
        return {
            "nome": "Fã Simulado",
            "username": "furia_fan123",
            "bio": "Acompanho todos os jogos da FURIA!",
            "localizacao": "Brasil",
            "seguidores": 1024,
            "seguindo": 300
        }

    token = st.session_state.get("x_token")
    if not token:
        iniciar_login()
        return {}

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(X_USERINFO_URL, headers=headers)
    if resp.status_code != 200:
        st.error("Erro ao obter dados da conta do X.")
        print(f"[ERRO] Falha ao buscar dados do X: {resp.status_code} - {resp.text}")
        return {}

    user = resp.json().get("data", {})
    return {
        "nome": user.get("name"),
        "username": user.get("username"),
        "bio": user.get("description"),
        "localizacao": user.get("location"),
        "seguidores": user.get("public_metrics", {}).get("followers_count", 0),
        "seguindo": user.get("public_metrics", {}).get("following_count", 0),
    }
