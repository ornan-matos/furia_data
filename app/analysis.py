import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

def agrupar_fas_por_interesse(df: pd.DataFrame, n_clusters=3):
    textos = [" ".join(json.loads(x)) for x in df["interesses"].dropna()]
    if len(textos) < n_clusters:
        return None, "Poucos dados para clustering"

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(textos)
    modelo = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = modelo.fit_predict(tfidf_matrix)

    return df, None

def recomendar_conteudo_para_fan(cpf: str, df: pd.DataFrame) -> str:
    fan_row = df[df["cpf"] == cpf]
    if fan_row.empty:
        return "Fã não encontrado."

    interesses_fan = json.loads(fan_row.iloc[0]["interesses"])
    texto_base = [" ".join(json.loads(x)) for x in df["interesses"].dropna()]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texto_base)

    idx = df.index[df["cpf"] == cpf][0]
    similaridades = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    similares = df.iloc[similaridades.argsort()[-4:-1]]

    recomendacoes = set()
    for _, row in similares.iterrows():
        recomendacoes.update(json.loads(row["interesses"]))

    recomendacoes -= set(interesses_fan)
    if not recomendacoes:
        return "Você já está bem alinhado com os interesses mais comuns da comunidade FURIA!"

    return (
        f"Baseado em fãs com perfil semelhante, sugerimos que você explore também: "
        + ", ".join(sorted(recomendacoes)) + "."
    )

def gerar_resumo_do_fan(fan: dict) -> str:
    resumo = f"{fan['nome']} é um fã da FURIA localizado em {fan.get('endereco', 'local desconhecido')}.\n"
    resumo += f"Participou de eventos do tipo: {fan.get('eventos', 'Nenhum')}.\n"
    resumo += f"Está engajado com atividades como: {', '.join(fan.get('atividades', []))}.\n"
    resumo += f"Já adquiriu produtos: {', '.join(fan.get('produtos', []))}.\n"
    if fan.get("dados_x"):
        x = fan["dados_x"]
        resumo += f"Nas redes sociais, tem @{x.get('username')} com {x.get('seguidores')} seguidores.\n"
    return resumo
