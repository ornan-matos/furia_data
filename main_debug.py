import streamlit as st
from app import fan_form, admin_panel
from app.config import config
from app.database import inicializar_banco
from app.callback_handler import processar_callback

st.set_page_config(page_title="FURIA Fan Data", layout="wide")

processar_callback()
inicializar_banco()

# Depuração visual no sidebar
with st.sidebar:
    st.image("static/logo_furia.png", width=200)
    st.title("FURIA Fan Data")
    st.markdown(f"🛡️ `ADMIN_PASSWORD`: `{config.ADMIN_PASSWORD}`")  # Mostra valor da senha carregada
    menu = st.radio("Navegar", ["Cadastro de Fã", "Administração"])

if menu == "Cadastro de Fã":
    fan_form.render()

elif menu == "Administração":
    senha_input = st.text_input("Senha do Administrador", type="password")

    # Debug visual
    st.write(f"🔍 Senha digitada: `{senha_input}`")
    st.write(f"🔒 Senha esperada: `{config.ADMIN_PASSWORD}`")

    # Debug no log do Railway
    if senha_input:
        print(f"[DEBUG] Senha digitada: {senha_input}")
        print(f"[DEBUG] Senha esperada: {config.ADMIN_PASSWORD}")

    if senha_input == config.ADMIN_PASSWORD:
        st.success("✅ Acesso liberado.")
        admin_panel.render()
    elif senha_input:
        st.error("❌ Senha incorreta.")
    else:
        st.warning("Acesso restrito à administração.")
