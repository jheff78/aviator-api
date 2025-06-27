import streamlit as st
import requests
import pandas as pd
import altair as alt

# URL da sua API (substitua pelo endpoint real se necessário)
API_URL = "https://aviator-api-abcdefg.onrender.com/velas"

st.set_page_config(page_title="Aviator - Analisador de Velas", layout="centered")

st.title("📊 Aviator - Analisador de Velas")

# Função para carregar dados da API
def carregar_dados():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Verificação de formato
        if isinstance(data, list) and all("value" in item for item in data):
            return data
        else:
            st.error("Erro: formato dos dados inválido.")
            return None
    except Exception as e:
        st.error("Erro ao buscar dados da API")
        st.error(str(e))
        return None

# Carregar dados
dados = carregar_dados()

if dados:
    df = pd.DataFrame(dados)
    
    # Gráfico de barras
    st.subheader("📈 Gráfico de Velas")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("id:O", title="ID"),
        y=alt.Y("value:Q", title="Valor"),
        color=alt.condition(
            alt.datum.value >= 10,
            alt.value("red"),
            alt.value("steelblue")
        )
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

    # Alerta para valores > 10x
    alertas = df[df["value"] >= 10]
    if not alertas.empty:
        st.warning("⚠️ Velas acima de 10x detectadas!")
        st.dataframe(alertas)

    # Estatísticas
    st.subheader("📊 Estatísticas")
    media = df["value"].mean()
    st.write(f"📌 Média dos valores: **{media:.2f}x**")
    st.write(f"🔢 Total de velas: {len(df)}")
