import streamlit as st
import json

# Função para carregar dados de usuários de um arquivo JSON
def load_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

# Função para salvar usuários de volta no arquivo JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Função para recuperar a senha
def esqueci_senha():
    st.title("Esqueci Minha Senha")
    
    username = st.text_input("Nome de Usuário")
    email = st.text_input("Email")
    col1, col2 = st.columns(2)
    with col1:
        new_password = st.text_input("Nova Senha", type="password")
    with col2:
        confirm_password = st.text_input("Confirme a Nova Senha", type="password")

    if st.button("Alterar Senha"):
        if not username or not email or not new_password or not confirm_password:
            st.error("Todos os campos devem ser preenchidos.")
        else:
            users = load_users()
            if username in users and users[username]["email"] == email:
                if new_password == confirm_password:
                    users[username]["senha"] = new_password
                    save_users(users)
                    st.success("Senha alterada com sucesso!")
                    st.session_state.page = "Login"  # Voltar para a página de login
                else:
                    st.error("As senhas não coincidem.")
            else:
                st.error("Nome de usuário ou email incorretos.")

    if st.button("Voltar para Login"):
        st.session_state.page = "Login"  # Volta para a página de login
