import streamlit as st

def show_guia():
    st.title("Como usar o Aplicativo/Site")

    st.write("Bem-vindo ao guia tutorial do nosso aplicativo! Este guia vai explicar como utilizar todas as páginas disponíveis e as funcionalidades do nosso site.")

    # Introdução
    st.subheader("1. Página Inicial (Home)")
    st.write("Na página inicial, você encontra uma introdução ao nosso projeto, que tem como objetivo proporcionar uma experiência de desenho acessível usando gestos dos dedos. Essa página é o ponto de partida, onde você pode explorar as opções do menu para começar a desenhar ou aprender mais sobre o site.")

    # Guia
    st.subheader("2. Guia")
    st.write("No Guia, você encontrará instruções detalhadas sobre como utilizar cada página e funcionalidade do aplicativo. É o local ideal para entender melhor o funcionamento do nosso site e suas funcionalidades, ajudando você a tirar o máximo proveito da experiência.")

    # Desenhar
    st.subheader("3. Desenhar")
    st.write("A página 'Desenhar' permite que você crie desenhos utilizando gestos dos dedos. Aqui está como você pode usá-la:")
    st.write("- **Como Desenhar**: Para desenhar, levante 1 dedo e mova-o pela tela. O aplicativo detectará o movimento e criará o traço.")
    st.write("- **Interromper o Desenho**: Levante 2 dedos para parar de desenhar.")
    st.write("- **Mudança de Cores**: Na parte superior, você verá 5 botões de cores (preto, branco, vermelho, verde e azul). Para mudar a cor do traço, mantenha 2 dedos sobre a cor desejada por 3 segundos.")
    st.write("- **Salvar e Apagar**: Os botões de salvar e apagar estão localizados no canto superior direito da tela. Para salvar ou apagar um desenho, mantenha 2 dedos sobre o respectivo botão por 3 segundos.")

    # Galeria
    st.subheader("4. Galeria")
    st.write("Na Galeria, você pode visualizar todos os desenhos que foram salvos. É necessário estar logado para acessar a galeria, garantindo que cada usuário veja apenas os seus desenhos.")

    # FAQ
    st.subheader("5. FAQ")
    st.write("A página de FAQ traz respostas para as perguntas mais comuns sobre o uso do site e suas funcionalidades. Para visualizar esta página, você também precisa estar logado.")

    # Logar
    st.subheader("6. Logar")
    st.write("Para acessar funcionalidades como a Galeria, FAQ e Configuração, é necessário fazer login. Caso não tenha uma conta, você pode criar uma nova usando a opção 'Criar Conta'. Também há uma opção para recuperar a senha em caso de esquecimento.")

    # Configuração
    st.subheader("7. Configuração")
    st.write("Na página de Configuração, você pode alterar a sua senha de forma segura. Este recurso é acessível apenas para usuários que já fizeram login no sistema.")

    # Logout
    st.subheader("8. Logout")
    st.write("Quando desejar sair da sua conta, basta clicar em 'Logout'. Isso garantirá que suas informações fiquem seguras até que você deseje acessar o site novamente.")

    # Pronto para Criar!
    st.subheader("9. Pronto para Criar!")
    st.write("Agora você está pronto para usar a página de desenho! Divirta-se criando suas obras de arte e explore as possibilidades com gestos e cores.")
    st.write("Se precisar de ajuda, retorne a este tutorial ou entre em contato com o suporte.")
