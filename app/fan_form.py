import os
import streamlit as st
from app.config import config
from app.utils import validar_cpf, salvar_fan_data
from app.grok_api import validar_documento_grok
from app.x_api import coletar_dados_x, iniciar_login
import uuid

def render():
    # ✅ Cabeçalho com imagem personalizada
    st.image("static/banner_furia_cadastro.png", use_column_width=True)

    if not st.session_state.get("x_autenticado"):
        st.markdown("""
            <div style="background-color:#0e0e0e;padding:1.5em;border-radius:10px;margin-bottom:1em;">
                <h3 style="color:white;">Seja bem-vindo ao FURIA Fan Data!</h3>
                <p style="color:white;font-size:15px;">
                Conecte sua conta do <strong>X (Twitter)</strong> para começarmos seu cadastro como fã oficial da FURIA.<br>
                Essa conexão nos ajuda a entender melhor sua relação com o time e personalizar sua experiência!
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Gera URL para login
        auth_url = iniciar_login(return_url=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <a href="{auth_url}" target="_self" style="text-decoration: none;">
                    <button style="display: flex; align-items: center; gap: 8px; background-color: #000; color: white; border: none; padding: 12px 20px; border-radius: 6px; font-size: 15px; cursor: pointer;">
                        <img src="https://abs.twimg.com/favicons/twitter.2.ico" width="20" height="20">
                        Conectar com X
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )

        with col2:
            with st.popover("Termos de Privacidade", use_container_width=True):
                # Estilo CSS para limitar a largura
                st.markdown(
                """
                <style>
                .stPopover { width: 100px !important; }
                </style>
                """,
                unsafe_allow_html=True
                )

                # Conteúdo dos termos
                st.markdown("""
                **Termos de Privacidade - FURIA Fan Data**

                - Seus dados serão utilizados exclusivamente para fins analíticos e de interação com a comunidade da FURIA.  
                - O documento enviado será analisado por IA apenas para verificação de identidade.  
                - Os dados da sua conta X (nome, bio, seguidores) são utilizados apenas para personalizar a experiência.  
                - Você pode solicitar a exclusão dos dados a qualquer momento via suporte oficial.

                Acesse: [https://furiadata-production-dba8.up.railway.app/](https://furiadata-production-dba8.up.railway.app/)
                """)

        return


    # 🔓 Conectado: exibe formulário completo
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
                "Comentando jogos", "Postando memes", "Participando de sorteios",
                "Criando conteúdo", "Consumindo streams", "Outros"
            ])

            st.markdown("**🎫 Eventos da FURIA que participou**")
            eventos_real = st.multiselect("Selecione os eventos:", [
                "IEM Rio Major 2022",
                "CBLOL Arena (RJ)",
                "FURIA Fan Fest 2023",
                "BLAST.tv Paris Major Viewing Party",
                "Outros eventos presenciais"
            ])
            eventos_formato = st.selectbox("Formato do evento", ["Presencial", "Online", "Ambos"])

            produtos = st.multiselect("Produtos oficiais da FURIA adquiridos:", [
                "Camisa Oficial 2023",
                "Camisa Retrô CS",
                "Jaqueta FURIA Blackout",
                "Boné Snapback",
                "Mochila personalizada",
                "Chaveiro Pantera",
                "Copo térmico",
                "Outros"
            ])

            sites = st.multiselect("Sites onde acompanha notícias de eSports", [
                "HLTV.org", "GE.globo", "The Enemy", "Mais Esports", "Reddit", "Twitter", "Outros"
            ])

        redes_sociais = st.text_input("Links de redes sociais (X, Instagram, etc.)")

        st.markdown("**📤 Upload de Documento (PNG, JPG ou PDF)**")
        doc = st.file_uploader("Selecione o documento", type=["png", "jpg", "jpeg", "pdf"])

        submit = st.form_submit_button("Enviar Cadastro")

    if submit:
        if not nome or not email or not cpf:
            st.warning("⚠️ Nome, Email e CPF são obrigatórios.")
            return
        if not validar_cpf(cpf):
            st.error("CPF inválido.")
            return
        if not doc:
            st.warning("Por favor, envie um documento.")
            return

        # Salva o documento
        cpf_dir = os.path.join(config.UPLOAD_DIR, cpf)
        os.makedirs(cpf_dir, exist_ok=True)
        doc_path = os.path.join(cpf_dir, f"{uuid.uuid4()}_{doc.name}")
        with open(doc_path, "wb") as f:
            f.write(doc.read())

        # Validação do documento
        doc_valido, relatorio_grok = validar_documento_grok(doc_path)
        if not doc_valido:
            st.error(f"Documento inválido: {relatorio_grok}")
            return

        # Dados do X (já autenticado)
        dados_x = coletar_dados_x()

        fan_data = {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "endereco": endereco,
            "interesses": interesses,
            "atividades": atividades,
            "eventos": {
                "lista": eventos_real,
                "formato": eventos_formato
            },
            "produtos": produtos,
            "sites": sites,
            "redes_sociais": redes_sociais,
            "documento": doc_path,
            "relatorio_grok": relatorio_grok,
            "dados_x": dados_x
        }

        salvar_fan_data(fan_data)
        st.success("✅ Cadastro enviado com sucesso!")

        # Mantém o code_verifier se necessário
        x_code_verifier = st.session_state.get("x_code_verifier")
        st.session_state.clear()
        if x_code_verifier:
            st.session_state["x_code_verifier"] = x_code_verifier
