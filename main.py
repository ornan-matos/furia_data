import streamlit as st
from app import fan_form, admin_panel
from app.config import config
from app.database import inicializar_banco
from app.callback_handler import processar_callback

st.set_page_config(page_title="FURIA Fan Data", layout="wide")

with st.sidebar:
    st.image("static/logo_furia.png", width=180)
    st.title("FURIA Fan Data")
    menu = st.radio("Navegar", ["Cadastro de Fã", "Administração"])

if menu == "Cadastro de Fã":
    fan_form.render()
elif menu == "Administração":
    if st.text_input("Senha do Administrador", type="password") == config.ADMIN_PASSWORD:
        admin_panel.render()
    else:
        st.warning("Acesso restrito à administração.")

processar_callback()

inicializar_banco()