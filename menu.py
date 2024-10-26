import streamlit as st

# Função para exibir o menu de navegação
def show_menu():
    if "page" not in st.session_state:
        st.session_state.page = "Página Inicial"  # Página padrão

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Define o estado de login padrão

    if "role" not in st.session_state:
        st.session_state.role = "user"  # Define o papel padrão

    st.sidebar.title("Menu")

    # Condição para exibir os menus baseados no estado de login
    if st.session_state.logged_in:
        # Exibir opções para usuários logados
        if st.sidebar.button("🏠 Página Inicial"):
            st.session_state.page = "Página Inicial"

        if st.sidebar.button("⚙️ Configurações"):
            st.session_state.page = "Configurações"

        if st.sidebar.button("📄 FAQ"):
            st.session_state.page = "FAQ"

        if st.sidebar.button("🎨 Galeria"):
            st.session_state.page = "Galeria"

        if st.session_state.role == "admin":  # Exibe "Cadastro" apenas para o admin
            if st.sidebar.button("👥 Cadastro"):
                st.session_state.page = "Cadastro"  # Página de cadastro

        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False  # Desloga o usuário
            st.session_state.page = "Página Inicial"  # Redireciona para a página inicial
    else:
        # Exibir opções para usuários não logados
        if st.sidebar.button("🏠 Página Inicial"):
            st.session_state.page = "Página Inicial"

        if st.sidebar.button("📚 Guia"):
            st.session_state.page = "Guia"

        if st.sidebar.button("🖌️ Desenhar"):
            st.session_state.page = "Desenhar"

        if st.sidebar.button("🔑 Logar"):
            st.session_state.page = "Login"  # Redireciona para a página de login
