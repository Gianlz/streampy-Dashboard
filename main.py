import streamlit as st


def main():
    # Configuração da página
    st.set_page_config(page_title="Meu Aplicativo Streamlit", page_icon=":shark:", layout="wide", initial_sidebar_state="collapsed")


    # Divisão da página
    col1, col2, col3 = st.columns([1, 2, 1])  # Aumentando a proporção da coluna central
    with col2:
        st.title("Gerenciamento de Rotina", anchor="Title-Main", help="Gerenciador de rotinas (Gastos, TODO, etc.)")
        # Espaço estilo README
        st.markdown("""
        # Features
        - Dashboard (Com gráfico de gastos)
        - TODO List (Com a fazeres do dia)
        - Configurações (Com as configurações do usuário)
        """)

if __name__ == "__main__":
    main()
