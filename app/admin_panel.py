import sqlite3
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from app.config import config

def render():
    st.subheader("👥 Administração de Fãs da FURIA")
    tabs = st.tabs(["📋 Lista de Fãs", "📊 Análise de Dados"])

    with tabs[0]:
        render_tabela_fas()

    with tabs[1]:
        render_graficos()

def render_tabela_fas():
    conn = sqlite3.connect(config.DB_PATH)
    df = pd.read_sql_query("SELECT * FROM fans", conn)
    conn.close()

    filtro_nome = st.text_input("🔍 Filtrar por nome")
    filtro_cpf = st.text_input("🔍 Filtrar por CPF")

    if filtro_nome:
        df = df[df["nome"].str.contains(filtro_nome, case=False, na=False)]
    if filtro_cpf:
        df = df[df["cpf"].str.contains(filtro_cpf, case=False, na=False)]

    if df.empty:
        st.warning("Nenhum fã encontrado.")
        return

    st.dataframe(df.drop(columns=["documento", "dados_x", "relatorio_grok"]))

    for _, row in df.iterrows():
        with st.expander(f"{row['nome']} ({row['cpf']})"):
            st.json(json.loads(row["dados_x"] or "{}"), expanded=False)
            st.text_area("📄 Relatório do Grok", row["relatorio_grok"], height=150)
            if st.button(f"🗑️ Excluir fã {row['cpf']}", key=row["cpf"]):
                excluir_fan_por_cpf(row["cpf"])
                st.success(f"Fã {row['cpf']} removido.")
                st.experimental_rerun()

def excluir_fan_por_cpf(cpf):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM fans WHERE cpf = ?", (cpf,))
    conn.commit()
    conn.close()

def render_graficos():
    conn = sqlite3.connect(config.DB_PATH)
    df = pd.read_sql_query("SELECT * FROM fans", conn)
    conn.close()

    if df.empty:
        st.info("Nenhum dado disponível para análise.")
        return

    st.markdown("### 🎯 Interesses dos fãs")
    interesses = explode_json_column(df, "interesses")
    plot_bar_chart(interesses, "Interesses")

    st.markdown("### 🛒 Produtos comprados")
    produtos = explode_json_column(df, "produtos")
    plot_bar_chart(produtos, "Produtos")

    st.markdown("### 🏁 Atividades mais comuns")
    atividades = explode_json_column(df, "atividades")
    plot_bar_chart(atividades, "Atividades")

    st.markdown("### 🎫 Eventos mencionados")
    eventos = df["eventos"].value_counts()
    plot_bar_chart(eventos, "Eventos")

    st.markdown("### 🌐 Sites de eSports preferidos")
    sites = explode_json_column(df, "sites")
    plot_bar_chart(sites, "Sites")

    st.markdown("### 🔍 Análise de Clusters com TF-IDF dos interesses")
    interesses_texto = [" ".join(json.loads(x)) for x in df["interesses"] if x]
    if len(interesses_texto) >= 2:
        try:
            tfidf = TfidfVectorizer()
            tfidf_matrix = tfidf.fit_transform(interesses_texto)
            st.write("TF-IDF Matrix (amostra):")
            st.dataframe(pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out()))
        except Exception as e:
            st.warning(f"Erro ao calcular TF-IDF: {e}")
    else:
        st.info("Mais dados são necessários para gerar clusters.")

def explode_json_column(df, colname):
    exploded = df[colname].dropna().apply(json.loads).explode()
    return exploded.value_counts()

def plot_bar_chart(series, title):
    if series.empty:
        st.info(f"Nenhum dado para {title}.")
        return
    fig, ax = plt.subplots()
    try:
        series.plot(kind='bar', ax=ax)
        ax.set_title(title)
        st.pyplot(fig)
    except TypeError:
        st.warning(f"Não foi possível gerar o gráfico para '{title}': dados não numéricos.")
