import os
import streamlit as st
from app.config import config
from app.utils import validar_cpf, salvar_fan_data
from app.grok_api import validar_documento_grok
from app.x_api import coletar_dados_x, iniciar_login
import uuid

def render():
    st.subheader("📋 Cadastro de Fã da FURIA")

    if not st.session_state.get("x_autenticado"):
        st.warning("⚠️ Para enviar o cadastro, conecte sua conta do X (Twitter) abaixo:")
        iniciar_login()
        return

    with st.form("form_fan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo")
            email = st.text_input("Email")
            cpf = st.text_input("CPF")
            endereco = st.text_input("Endereço")

        with col2:
            interesses = st.multiselect("Interesses em eSports", [
                "CS:GO", "Valorant", "LoL", "Dota 2", "PUBG", "Free Fire", "FIFA", "Outros"
            ])

            atividades = st.multiselect("Atividades de engajamento", [
                "Comentando jogos", "Postando memes", "Participando de sorteios", "Criando conteúdo", "Outros"
            ])

            eventos = st.selectbox("Participou de eventos da FURIA?", [
                "Nenhum", "Presencial", "Online (Twitter/Twitch/YouTube)", "Ambos"
            ])

            produtos = st.multiselect("Produtos adquiridos no site furia.gg", [
                "Camisas", "Bonés", "Moletons", "Posters", "Outros"
            ])

            sites = st.multiselect("Sites onde acompanha notícias de eSports", [
                "HLTV.org", "GE.globo", "The Enemy", "Mais Esports", "Reddit", "Twitter", "Outros"
            ])

        redes_sociais = st.text_input("Links de redes sociais (X, Instagram, etc.)")

        st.markdown("**📤 Upload de Documento (PNG, JPG ou PDF)**")
        doc = st.file_uploader("Selecione o documento", type=["png", "jpg", "jpeg", "pdf"])

        submit = st.form_submit_button("Enviar Cadastro")

    if submit:
        if not validar_cpf(cpf):
            st.error("CPF inválido.")
            return
        if not nome or not email or not doc:
            st.warning("Por favor, preencha todos os campos obrigatórios.")
            return

        # Salva o documento em pasta do CPF
        cpf_dir = os.path.join(config.UPLOAD_DIR, cpf)
        os.makedirs(cpf_dir, exist_ok=True)
        doc_path = os.path.join(cpf_dir, f"{uuid.uuid4()}_{doc.name}")
        with open(doc_path, "wb") as f:
            f.write(doc.read())

        # Validação com o Grok
        doc_valido, relatorio_grok = validar_documento_grok(doc_path)
        if not doc_valido:
            st.error(f"Documento inválido: {relatorio_grok}")
            return

        # Dados da conta X (obrigatório)
        dados_x = coletar_dados_x()

        # Monta o dicionário final para salvar
        fan_data = {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "endereco": endereco,
            "interesses": interesses,
            "atividades": atividades,
            "eventos": eventos,
            "produtos": produtos,
            "sites": sites,
            "redes_sociais": redes_sociais,
            "documento": doc_path,
            "relatorio_grok": relatorio_grok,
            "dados_x": dados_x
        }

        salvar_fan_data(fan_data)
        st.success("✅ Cadastro enviado com sucesso!")

        # Preserva o code_verifier do X para não quebrar o fluxo OAuth após o redirect
        x_code_verifier = st.session_state.get("x_code_verifier")
        st.session_state.clear()
        if x_code_verifier:
            st.session_state["x_code_verifier"] = x_code_verifier
