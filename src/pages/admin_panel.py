import streamlit as st
import json
import os
import bcrypt
from utils.database import carregar_json, salvar_json

def carregar_usuarios():
    return carregar_json('usuarios.json')

def salvar_usuarios(usuarios):
    salvar_json('usuarios.json', usuarios)

def admin_panel():
    if not st.session_state.get('autenticado', False) or not st.session_state.get('admin', False):
        st.error("Acesso negado. Você precisa ser um administrador para acessar esta página.")
        st.stop()

    st.set_page_config(
        page_title="Painel de Administração",
        page_icon=":gear:",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Painel de Administração")

    usuarios = carregar_usuarios()

    st.subheader("Gerenciar Usuários")
    
    col_headers = st.columns([2, 2, 1, 1, 1, 1, 1])
    col_headers[0].write("**Usuário**")
    col_headers[1].write("**Senha (Hash)**") 
    col_headers[2].write("**Admin**")
    col_headers[3].write("**Editar**")
    col_headers[4].write("**Excluir**")
    col_headers[5].write("**Alterar Senha**")
    col_headers[6].write("**Entrar como Usuário**")

    for usuario, dados in usuarios.items():
        cols = st.columns([2, 2, 1, 1, 1, 1, 1])
        
        cols[0].write(usuario)
        cols[1].write(dados['senha'][:15] + "...")
        cols[2].write("Sim" if dados.get('admin', False) else "Não")
        
        if cols[3].button("✏️", key=f"edit_{usuario}"):
            st.session_state.usuario_editando = usuario
            st.session_state.novo_nome = usuario
            st.session_state.novo_admin = dados.get('admin', False)
            
        if usuario != "StrongerFX":
            if cols[4].button("🗑️", key=f"del_{usuario}"):
                del usuarios[usuario]
                salvar_usuarios(usuarios)
                st.success(f"Usuário {usuario} excluído com sucesso!")
                st.rerun()
                
        if cols[5].button("🔑", key=f"pass_{usuario}"):
            st.session_state.alterando_senha = usuario

        if cols[6].button("👤", key=f"login_{usuario}"):
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.admin = dados.get('admin', False)
            st.success(f"Você entrou na conta de {usuario}")
            st.rerun()

    if hasattr(st.session_state, 'usuario_editando'):
        with st.form(key="edit_form"):
            st.subheader(f"Editando usuário: {st.session_state.usuario_editando}")
            novo_nome = st.text_input("Novo nome de usuário", value=st.session_state.novo_nome)
            novo_admin = st.checkbox("É administrador?", value=st.session_state.novo_admin)
            
            if st.form_submit_button("Salvar alterações"):
                if st.session_state.usuario_editando != novo_nome:
                    usuarios[novo_nome] = usuarios.pop(st.session_state.usuario_editando)
                usuarios[novo_nome]['admin'] = novo_admin
                salvar_usuarios(usuarios)
                del st.session_state.usuario_editando
                st.success("Usuário atualizado com sucesso!")
                st.rerun()

    if hasattr(st.session_state, 'alterando_senha'):
        with st.form(key="password_form"):
            st.subheader(f"Alterando senha: {st.session_state.alterando_senha}")
            nova_senha = st.text_input("Nova senha", type="password")
            confirmar_senha = st.text_input("Confirmar nova senha", type="password")
            
            if st.form_submit_button("Alterar senha"):
                if nova_senha == confirmar_senha:
                    salt = bcrypt.gensalt()
                    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), salt)
                    usuarios[st.session_state.alterando_senha]['senha'] = senha_hash.decode('utf-8')
                    salvar_usuarios(usuarios)
                    del st.session_state.alterando_senha
                    st.success("Senha alterada com sucesso!")
                    st.rerun()
                else:
                    st.error("As senhas não coincidem!")

    st.divider()
    st.subheader("Adicionar Novo Usuário")
    with st.form(key="new_user_form"):
        novo_usuario = st.text_input("Nome do usuário")
        nova_senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirmar senha", type="password")
        is_admin = st.checkbox("É administrador?")
        
        if st.form_submit_button("Adicionar Usuário"):
            if nova_senha != confirmar_senha:
                st.error("As senhas não coincidem!")
            elif novo_usuario in usuarios:
                st.error("Este usuário já existe!")
            else:
                salt = bcrypt.gensalt()
                senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), salt)
                usuarios[novo_usuario] = {'senha': senha_hash.decode('utf-8'), 'admin': is_admin}
                salvar_usuarios(usuarios)
                st.success(f"Usuário '{novo_usuario}' adicionado com sucesso!")
                st.rerun()

if __name__ == "__main__":
    if st.session_state.get('autenticado', False) and st.session_state.get('admin', False):
        admin_panel()
    else:
        st.error("Acesso negado. Você precisa ser um administrador para acessar esta página.")
        st.stop()
