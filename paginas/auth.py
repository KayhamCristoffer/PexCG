import streamlit as st
import json

# Função para carregar dados de usuários de um arquivo JSON
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def login():
    users = load_users()  # Carregar usuários do JSON

    # Verifica se o usuário está logado
    if 'username' in st.session_state and st.session_state['username']:
        # Mostrar botão de Logout
        if st.button("Logout"):
            # Limpar o estado da sessão
            st.session_state.clear()
            st.success("Você saiu! Tchau 👋")
    else:
        st.title("Login")
        user_input = st.text_input("Usuário ou Email")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            # Verificar se o usuário existe e a senha está correta
            user_found = False
            for username, user_info in users.items():
                if (username == user_input or user_info.get("email") == user_input) and user_info["senha"] == password:
                    st.session_state['username'] = username
                    st.session_state['logged_in'] = True  # Atualiza o estado de login
                    st.session_state['role'] = user_info.get("role", "user")  # Atribui um papel padrão
                    st.success(f"Bem-vindo(a), {username}!")
                    user_found = True
                    # Redirecionar para a Página Inicial
                    st.session_state.page = "Página Inicial"
                    break
            
            if not user_found:
                st.error("Usuário ou senha inválidos.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Criar Conta"):
                st.session_state.current_page = "novo_usuario"
        with col2:
            if st.button("Esqueci Senha"):
                st.session_state.current_page = "esqueci_senha"

        # Verifica qual página deve ser mostrada
        if st.session_state.get("current_page") == "novo_usuario":
            from paginas.novo_usuario import criar_conta
            criar_conta()  # Função para exibir a página de criação de conta
        elif st.session_state.get("current_page") == "esqueci_senha":
            from paginas.esqueci_senha import esqueci_senha
            esqueci_senha()  # Função para exibir a página de recuperação de senha

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logout realizado com sucesso!")
