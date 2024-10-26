import streamlit as st
from paginas.home import show_home
from paginas.guia import show_guia
from paginas.cadastro import show_registration
from paginas.desenhar import show_desenho
from paginas.galeria import show_galeria
from paginas.auth import login, logout
from paginas.configuracoes import show_configuracoes  # Importa a página de configurações
from paginas.faq import show_faq  # Importa a página de FAQ

def main():
    # Inicialização do estado da sessão
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

    st.sidebar.title("Menu")

    # Exibe as opções no menu baseado no estado de login
    if st.session_state.logged_in:
        st.sidebar.button("Logout", on_click=logout)
        page = st.sidebar.selectbox("Selecione uma opção", 
            ["Home", "Guia", "Desenhar", "Galeria", "Configurações", "Cadastro","FAQ"])
    else:
        page = st.sidebar.selectbox("Selecione uma opção", ["Home", "Guia", "Desenhar","Login"])

    # Chama a função correspondente à página selecionada
    if page == "Home":
        show_home()
    elif page == "Guia":
        show_guia()
    elif page == "Desenhar":
        show_desenho()
    elif page == "Galeria":
        if st.session_state.logged_in:
            show_galeria()
        else:
            st.warning("Faça login para acessar a galeria.")
    elif page == "Login":
        login()
    elif page == "Cadastro":
        show_registration()  # Chama a página de cadastro
    elif page == "Configurações":
        if st.session_state.logged_in:
            show_configuracoes()  # Chama a página de configurações
        else:
            st.warning("Faça login para acessar as configurações.")
    elif page == "FAQ":
        if st.session_state.logged_in:
            show_faq()  # Chama a página de FAQ
        else:
            st.warning("Faça login para acessar a FAQ.")

if __name__ == "__main__":
    main()
