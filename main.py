import streamlit as st
from app.callback_handler import processar_callback
from app.database import inicializar_banco
from app import fan_form, admin_panel
from app.config import config

# Deve ser o primeiro comando Streamlit
st.set_page_config(page_title="FURIA Fan Data", layout="wide")

processar_callback()
inicializar_banco()

with st.sidebar:
    st.image("static/logo_furia.png", width=180)
    st.title("FURIA Fan Data")
    menu = st.radio("Navegar", ["Cadastro de Fã", "Administração"])

if menu == "Cadastro de Fã":
    fan_form.render()
elif menu == "Administração":
    if not st.session_state.get("admin_autenticado"):
        senha_input = st.text_input("Senha do Administrador", type="password", key="admin_password")
        if senha_input == config.ADMIN_PASSWORD:
            st.session_state["admin_autenticado"] = True
            st.experimental_rerun()
        elif senha_input:
            st.error("Senha incorreta.")
    else:
        admin_panel.render()
