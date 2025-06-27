import streamlit as st
import requests
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Aviator - Analisador de Velas", layout="centered")

st.title("📊 Aviator - Analisador de Velas")

# URL da sua API (substitua se necessário)
API_URL = "https://aviator-api-xxxxx.onrender.com/velas"

# 🔄 Função para carregar dados
@st.cache_data(ttl=60)
def carregar_dados():
    try:
        resposta = requests.get(API_URL)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            st.error("Erro ao buscar dados da API")
            return []
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return []

# Carregar dados da API
dados = carregar_dados()

# ⚠️ Verificação de estrutura
if not dados or not isinstance(dados, list) or 'value' not in dados[0]:
    st.error("Erro: formato dos dados inválido.")
    st.stop()

# Extrair apenas os valores
valores = [item['value'] for item in dados]

# ================================
# 1. Gráfico de barras
# ================================
st.subheader("📊 Gráfico de Velas (Últimas 20)")
fig, ax = plt.subplots()
ax.bar(range(len(valores)), valores, color='skyblue')
ax.set_xlabel("Index")
ax.set_ylabel("Valor da Vela")
ax.set_title("Distribuição das Últimas 20 Velas")
st.pyplot(fig)

# ================================
# 2. Alerta de valores altos
# ================================
st.subheader("🚨 Velas Acima de 10x")
acima_10 = [v for v in dados if v['value'] >= 10]
if acima_10:
    st.warning(f"{len(acima_10)} valor(es) acima de 10x detectado(s)!")
    for vela in acima_10:
        st.markdown(f"• ID {vela['id']} - Valor: **{vela['value']}x**")
else:
    st.success("Nenhum valor acima de 10x nas últimas velas.")

# ================================
# 3. Histórico e probabilidade média
# ================================
media = sum(valores) / len(valores)
st.metric("📈 Média das Últimas Velas", f"{media:.2f}x")

frequencia = Counter(valores)
mais_comuns = frequencia.most_common(3)

st.subheader("🔁 Valores Mais Frequentes")
for val, freq in mais_comuns:
    st.write(f"• {val}x apareceu **{freq}** vez(es)")
