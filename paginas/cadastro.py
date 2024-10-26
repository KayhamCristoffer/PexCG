import streamlit as st
from paginas.controlador import load_users, save_users, create_user, delete_user, edit_user

def show_registration():
    # Verifica se o usuário está logado e se é um admin
    if st.session_state.get('logged_in') and st.session_state.get('username') == 'admin':
        show_cadastro()
    else:
        # Se não for admin ou não estiver logado, mostra mensagem apropriada
        st.warning("Você não tem permissão para acessar esta página, jovem padawan.")
        if not st.session_state.get('logged_in'):
            st.info("Por favor, faça login para acessar a página de administração.")

def show_cadastro():
    users = load_users()  # Carregar usuários no início
    #st.write(users)  # Debug: mostrar os usuários carregados

    # Colunas para título e botão
    col1, col2 = st.columns([5, 1])
    col1.title("Administração de Usuários")
    
    if col2.button("➕", key="add_user"):
        st.session_state.show_add_user = not st.session_state.get('show_add_user', False)
        #st.write("Mostrar seção de adicionar usuário:", st.session_state.show_add_user)  # Debug

    # Seção para adicionar novo usuário
    if st.session_state.get('show_add_user', False):
        st.subheader("Adicionar novo usuário")

        # Criando duas colunas para Nome de Usuário e Email
        col1, col2 = st.columns(2)
        new_username = col1.text_input("Nome do usuário", key="new_username")
        new_email = col2.text_input("Email", key="new_email")

        # Criando três colunas para Senha, Idade e Role
        col3, col4, col5 = st.columns(3)
        new_password = col3.text_input("Senha", type="password", key="new_password")  # Senha
        new_idade = col4.number_input("Idade", min_value=0, key="new_idade")  # Idade
        new_role = col5.selectbox("Role", ["common", "admin"], index=0)  # Role com "common" como primeira opção

        if st.button("Criar Usuário"):
            if create_user(users, new_username, new_email, new_password, new_idade, new_role):
                save_users(users)
                st.success(f"Usuário {new_username} criado com sucesso!")
            else:
                st.error("Usuário já existe!")

    # Cabeçalho da tabela
    st.write("### Usuários cadastrados:")
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
    col1.write("ID")
    col2.write("Nome")
    col3.write("Cargo")
    col4.write("Editar")
    col5.write("Deletar")
    st.write("---")

    # Lista para armazenar usuários a serem deletados
    users_to_delete = []

    # Tabela com Usuários
    for username, details in users.items():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
        col1.write(details["id"])
        col2.write(details["nome"])
        col3.write(details["role"])  # Mostra o nome do cargo
        
        editar_coluna = col4.button(f"✏️", key=f"edit_{username}")
        deletar_coluna = col5.button(f"🗑️", key=f"delete_{username}")

        if editar_coluna:
            st.session_state.editing_user = username

        # Lógica de deleção
        if deletar_coluna:
            users_to_delete.append(username)  # Adiciona o usuário à lista de deletar

    # Realiza a deleção após o loop
    for username in users_to_delete:
        if delete_user(users, username):  # Tenta deletar o usuário
            save_users(users)  # Salva as mudanças no arquivo JSON
            st.success(f"Usuário {username} deletado com sucesso!")
        else:
            st.error("Erro ao deletar o usuário.")

    # Formulário de edição
    if 'editing_user' in st.session_state:
        editing_user = st.session_state.editing_user
        user_details = users[editing_user]

        st.write(f"### Editando usuário: {editing_user}")

        # Primeira linha: Nome e Email
        col1, col2 = st.columns(2)
        new_name = col1.text_input("Nome do usuário", value=user_details["nome"], key="edit_name")
        new_email = col2.text_input("Email", value=user_details["email"], key="edit_email")

        # Segunda linha: Senha, Idade e Role
        col3, col4, col5 = st.columns(3)
        new_password = col3.text_input("Senha", type="password", key="edit_password")
        new_age = col4.number_input("Idade", min_value=0, value=user_details["idade"], key="edit_age")
        new_role = col5.selectbox("Role", ["admin", "common"], index=0 if user_details["role"] == "admin" else 1, key="edit_role")

        # Atualizar usuário
        if st.button("Salvar alterações"):
            if edit_user(users, editing_user, new_name, new_email, new_password, new_age, new_role):
                save_users(users)
                st.success(f"Usuário {editing_user} atualizado com sucesso!")
                del st.session_state.editing_user  # Limpar o estado de edição
            else:
                st.error("Erro ao atualizar o usuário.")
