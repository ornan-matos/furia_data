import streamlit as st

def input_dados_pessoais():
    st.markdown("### 📇 Dados Pessoais")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        cpf = st.text_input("CPF")
        endereco = st.text_input("Endereço")
    return nome, email, cpf, endereco

def selecao_interesses():
    return st.multiselect("🎮 Interesses em eSports", [
        "CS:GO", "Valorant", "LoL", "Dota 2", "PUBG", "Free Fire", "FIFA", "Outros"
    ])

def selecao_atividades():
    return st.multiselect("🧩 Atividades de engajamento", [
        "Comentando jogos", "Postando memes", "Participando de sorteios", "Criando conteúdo", "Outros"
    ])

def selecao_eventos():
    return st.selectbox("🎟️ Participou de eventos da FURIA?", [
        "Nenhum", "Presencial", "Online (Twitter/Twitch/YouTube)", "Ambos"
    ])

def selecao_produtos():
    return st.multiselect("🛍️ Produtos adquiridos no site furia.gg", [
        "Camisas", "Bonés", "Moletons", "Posters", "Outros"
    ])

def selecao_sites():
    return st.multiselect("🌐 Sites onde acompanha notícias de eSports", [
        "HLTV.org", "GE.globo", "The Enemy", "Mais Esports", "Reddit", "Twitter", "Outros"
    ])

def input_redes_sociais():
    return st.text_input("🔗 Links de redes sociais (X, Instagram, etc.)")

def upload_documento():
    st.markdown("**📤 Upload de Documento (PNG, JPG ou PDF)**")
    return st.file_uploader("Selecione o documento", type=["png", "jpg", "jpeg", "pdf"])
