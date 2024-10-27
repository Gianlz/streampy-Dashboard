import streamlit as st

def dashboard():
    st.set_page_config(
        page_title="Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.title("Dashboard")
    st.write("Bem-vindo ao dashboard!")
    # Adicione mais elementos do Streamlit conforme necessário

    # Exemplo de estatísticas
    st.header("Estatísticas Gerais")
    # Aqui você pode adicionar gráficos, tabelas e outras visualizações

if __name__ == "__main__":
    dashboard()
