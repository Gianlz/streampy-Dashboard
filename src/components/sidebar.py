# import streamlit as st

# def exibir_sidebar():
#     st.sidebar.title("Menu")
    
#     paginas = {
#         "Dashboard": "pages/dashboard.py",
#         "Configurações": "pages/config.py",
#         "Lista de Tarefas": "pages/todo.py"
#     }
    
#     if st.session_state.get('admin', False):
#         paginas["Painel de Administração"] = "pages/admin_panel.py"
    
#     escolha = st.sidebar.selectbox("Navegue para:", list(paginas.keys()))
    
#     # Definir a página atual no estado da sessão
#     st.session_state['pagina_atual'] = paginas[escolha]
    
#     if st.sidebar.button("Sair"):
#         st.session_state.clear()
#         st.experimental_rerun()
