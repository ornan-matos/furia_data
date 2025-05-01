import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from app.config import config

def processar_callback():
    params = st.query_params
    code = params.get("code", None)

    if code and "x_token" not in st.session_state:
        print(f"[DEBUG] Código de autorização recebido: {code}")

        try:
            token = trocar_codigo_por_token(code)
            st.session_state["x_token"] = token
            st.success("✅ Conexão com o X realizada com sucesso!")
            print(f"[DEBUG] Token de acesso obtido: {token}")
        except Exception as e:
            st.error("Erro ao autenticar com o X. Tente novamente.")
            print(f"[ERRO] Falha ao trocar código por token: {str(e)}")

def trocar_codigo_por_token(code):
    code_verifier = st.session_state.get("x_code_verifier")
    if not code_verifier:
        raise Exception("code_verifier não encontrado na sessão (perdido no redirect?)")

    client = OAuth2Session(
        client_id=config.X_CLIENT_ID,
        client_secret=config.X_CLIENT_SECRET,
        redirect_uri=config.X_REDIRECT_URI,
        code_verifier=code_verifier,
    )

    token = client.fetch_token(
        url="https://api.twitter.com/2/oauth2/token",
        grant_type="authorization_code",
        code=code,
    )

    return token["access_token"]
