import streamlit as st
from app.x_api import trocar_codigo_por_token

def processar_callback():
    params = st.query_params
    code = params.get("code", None)

    if code and "x_token" not in st.session_state:
        print(f"[DEBUG] Código de autorização recebido: {code}")

        try:
            sucesso = trocar_codigo_por_token(code)
            if sucesso:
                st.success("✅ Conectado com o X com sucesso!")
                st.session_state["x_autenticado"] = True
                st.experimental_rerun()
            else:
                st.error("Erro ao trocar código por token do X.")
        except Exception as e:
            st.error("Erro ao autenticar com o X. Tente novamente.")
            print(f"[ERRO] Falha ao trocar código por token: {str(e)}")
