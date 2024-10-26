import streamlit as st
import datetime
import pandas as pd

def todo():
    st.set_page_config(page_title="Lista de Tarefas", page_icon=":clipboard:", layout="wide", initial_sidebar_state="collapsed")
    st.title("Gerenciador de Tarefas")

    # Inicializar a lista de tarefas no estado da sessão
    if 'tarefas' not in st.session_state:
        st.session_state.tarefas = pd.DataFrame(columns=['Data', 'Hora', 'Tarefa', 'Concluída'])

    # Adicionar nova tarefa
    with st.expander("Adicionar Nova Tarefa", expanded=False):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            nova_tarefa = st.text_input("Descrição da tarefa")
        with col2:
            data_tarefa = st.date_input("Data", min_value=datetime.date.today())
        with col3:
            hora_tarefa = st.time_input("Hora")
        
        if st.button("Adicionar"):
            if nova_tarefa:
                nova_linha = pd.DataFrame({'Data': [data_tarefa], 'Hora': [hora_tarefa], 'Tarefa': [nova_tarefa], 'Concluída': [False]})
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_linha], ignore_index=True)
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()

    # Exibir e gerenciar tarefas
    st.subheader("Suas Tarefas")
    data_filtro = st.date_input("Filtrar tarefas por data", value=datetime.date.today())
    tarefas_filtradas = st.session_state.tarefas[st.session_state.tarefas['Data'] == data_filtro].sort_values('Hora')

    for idx, tarefa in tarefas_filtradas.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 3, 0.5, 0.5])
            
            with col1:
                concluida = st.checkbox("", value=tarefa['Concluída'], key=f"check_{idx}", on_change=lambda: st.session_state.tarefas.at.__setitem__((idx, 'Concluída'), st.session_state[f"check_{idx}"]))
            with col2:
                st.write(tarefa['Hora'].strftime("%H:%M"))
            with col3:
                st.write(tarefa['Tarefa'])
            with col4:
                if st.button("✏️", key=f"edit_{idx}"):
                    st.session_state[f"editing_{idx}"] = True
            with col5:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.tarefas = st.session_state.tarefas.drop(idx)
                    st.rerun()
           
            
            if st.session_state.get(f"editing_{idx}", False):
                nova_tarefa = st.text_input("Editar tarefa", value=tarefa['Tarefa'], key=f"edit_input_{idx}")
                nova_hora = st.time_input("Editar hora", value=tarefa['Hora'], key=f"edit_time_{idx}")
                if st.button("Salvar", key=f"save_edit_{idx}"):
                    st.session_state.tarefas.at[idx, 'Tarefa'] = nova_tarefa
                    st.session_state.tarefas.at[idx, 'Hora'] = nova_hora
                    st.session_state[f"editing_{idx}"] = False
                    st.success("Tarefa atualizada com sucesso!")
                    st.rerun()

    # Estatísticas
    st.subheader("Estatísticas")
    total_tarefas = len(st.session_state.tarefas)
    tarefas_concluidas = len(st.session_state.tarefas[st.session_state.tarefas['Concluída'] == True])
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de tarefas", total_tarefas)
    with col2:
        st.metric("Tarefas concluídas", tarefas_concluidas)
    if total_tarefas > 0:
        st.progress(tarefas_concluidas / total_tarefas, text=f"{tarefas_concluidas}/{total_tarefas} concluídas")

if __name__ == "__main__":
    todo()