# app/callback_handler.py
import streamlit as st
from app.x_api import trocar_codigo_por_token

def processar_callback():
    params = st.query_params
    if "code" in params:
        code = params["code"][0]
        if trocar_codigo_por_token(code):
            st.success("✅ Conexão com o X realizada com sucesso!")
        else:
            st.error("❌ Erro ao autenticar com o X. Tente novamente.")
