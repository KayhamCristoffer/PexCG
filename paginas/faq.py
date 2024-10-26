import streamlit as st

def show_faq():
    st.title("Perguntas Frequentes (FAQ)")

    faqs = [
        {
            "pergunta": "Como posso acessar a plataforma?",
            "resposta": "Você pode acessar a plataforma através do site oficial. Certifique-se de que sua câmera está ativada para usar as funcionalidades de gestos."
        },
        {
            "pergunta": "Quem pode usar a plataforma?",
            "resposta": "A plataforma é projetada para crianças, adultos e pessoas com deficiências motoras que desejam expressar sua criatividade através da arte digital."
        },
        {
            "pergunta": "Quais gestos são utilizados para desenhar?",
            "resposta": "Você pode desenhar levantando um dedo. Para parar de desenhar, levante dois dedos. Para mudar de cor, mantenha dois dedos sobre a cor desejada por 3 segundos."
        },
        {
            "pergunta": "Como faço para salvar meu desenho?",
            "resposta": "Para salvar seu desenho, clique no botão 'Salvar' e mantenha pressionado por 3 segundos."
        },
        {
            "pergunta": "Posso limpar meu desenho?",
            "resposta": "Sim, você pode limpar o desenho clicando no botão 'Limpar' e mantendo pressionado por 3 segundos."
        },
        {
            "pergunta": "O que é necessário para usar a plataforma?",
            "resposta": "Para usar a plataforma, você precisa de um dispositivo com câmera e conexão à internet. Certifique-se de que sua câmera está funcionando corretamente."
        },
        {
            "pergunta": "Como posso criar uma conta?",
            "resposta": "Você pode criar uma conta acessando a página de cadastro e preenchendo os campos necessários."
        },
        {
            "pergunta": "Como posso recuperar minha senha?",
            "resposta": "Para recuperar sua senha, vá até a página de login e clique em 'Esqueci a Senha' para seguir as instruções."
        },
        {
            "pergunta": "Posso usar a plataforma em dispositivos móveis?",
            "resposta": "Sim, a plataforma é acessível em dispositivos móveis, desde que a câmera e a conexão à internet estejam disponíveis."
        },
        {
            "pergunta": "Qual é o objetivo do projeto?",
            "resposta": "O projeto visa criar uma ferramenta digital acessível e inclusiva que permita a criação de arte por meio de gestos, ajudando no desenvolvimento motor e cognitivo de crianças e pessoas com deficiências."
        },
        {
            "pergunta": "Como posso entrar em contato para mais informações?",
            "resposta": "Você pode entrar em contato conosco pelo e-mail: projeto.acessebilidade.digital@drummond.com."
        }
    ]

    for faq in faqs:
        st.subheader(f"Pergunta: {faq['pergunta']}")
        st.write(f"Resposta: {faq['resposta']}")

