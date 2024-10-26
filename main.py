import streamlit as st
import json
import os
from hashlib import sha256

def verificar_credenciais(usuario, senha):
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
            if usuario in usuarios:
                senha_hash = sha256(senha.encode()).hexdigest()
                return senha_hash == usuarios[usuario]
    return False

def salvar_usuario(usuario, senha):
    usuarios = {}
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
    
    senha_hash = sha256(senha.encode()).hexdigest()
    usuarios[usuario] = senha_hash
    
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f)

def main():
    # Configuração da página
    st.set_page_config(page_title="Meu Aplicativo Streamlit", page_icon=":shark:", layout="wide", initial_sidebar_state="collapsed")

    # Inicializar estado de autenticação
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if 'usuario' not in st.session_state:
        st.session_state.usuario = None

    # Esconder sidebar se não estiver autenticado
    if not st.session_state.autenticado:
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
            </style>
            """, unsafe_allow_html=True)
            
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("Login", anchor="Title-Main")
            
            tab_login, tab_cadastro = st.tabs(["Login", "Cadastro"])
            
            with tab_login:
                usuario_login = st.text_input("Usuário", key="login_user")
                senha = st.text_input("Senha", type="password")
                
                if st.button("Entrar"):
                    if verificar_credenciais(usuario_login, senha):
                        st.session_state.autenticado = True
                        st.session_state.usuario = usuario_login
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos")
            
            with tab_cadastro:
                novo_usuario = st.text_input("Novo Usuário")
                nova_senha = st.text_input("Nova Senha", type="password")
                confirmar_senha = st.text_input("Confirmar Senha", type="password")
                
                if st.button("Cadastrar"):
                    if nova_senha != confirmar_senha:
                        st.error("As senhas não coincidem")
                    else:
                        salvar_usuario(novo_usuario, nova_senha)
                        st.success("Usuário cadastrado com sucesso!")
    
    else:
        # Mostrar sidebar quando autenticado
        st.sidebar.empty()
        
        # Criar colunas para o botão de sair no topo direito
        col_space, col_btn = st.columns([6, 1])
        with col_btn:
            if st.button("Sair"):
                st.session_state.autenticado = False
                st.session_state.usuario = None
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title(f"Bem-vindo, {st.session_state.usuario}!", anchor="Title-Main")
            st.title("Gerenciamento de Rotina", anchor="Title-Sub", help="Gerenciador de rotinas (Gastos, TODO, etc.)")
                
            st.markdown("""
            # Features
            - Dashboard (Com gráfico de gastos)
            - TODO List (Com a fazeres do dia)
            - Configurações (Com as configurações do usuário)
            """)

if __name__ == "__main__":
    main()
