import streamlit as st
import json
import os

# Função para carregar dados de usuários de um arquivo JSON
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)
    else:
        users = {}
    return users

# Função para salvar usuários de volta no arquivo JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Função para criar uma nova conta
def criar_conta():
    st.title("Criar Conta")
    
    username = st.text_input("Nome de Usuário", key="new_username")
    email = st.text_input("Email", key="new_email")
    
    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input("Senha", type="password", key="new_password")
    with col2:
        confirm_password = st.text_input("Confirme a Senha", type="password", key="new_confirm_password")

    # Botão para criar conta
    if st.button("Criar Conta", key="create_account"):
        if not username or not email or not password or not confirm_password:
            st.error("Todos os campos devem ser preenchidos.")
        elif password != confirm_password:
            st.error("As senhas não coincidem.")
        else:
            users = load_users()
            if username in users:
                st.error("Usuário já existe!")
            else:
                # Definir um novo ID baseado nos IDs existentes
                new_id = max([details['id'] for details in users.values()], default=0) + 1
                users[username] = {
                    "id": new_id,
                    "nome": username,
                    "email": email,
                    "senha": password,
                    "idade": 0,
                    "role": "common"
                }
                save_users(users)
                st.success(f"Usuário {username} criado com sucesso!")
                st.session_state.page = "Login"  # Voltar para a página de login