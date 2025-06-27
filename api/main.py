import streamlit as st
import requests

st.title("🔍 Teste de Conexão com a API")

def obter_velas():
    try:
        url = "https://aviator-api-bz4x.onrender.com/velas"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"erro": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"erro": str(e)}

dados = obter_velas()

st.write("📦 Resposta da API:")
st.json(dados)
