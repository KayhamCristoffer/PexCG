import streamlit as st
import os

def show_galeria():
    if 'username' in st.session_state and st.session_state['username']:
        st.title("Galeria")
        st.write("Aqui estão as imagens da galeria, só para os VIPs ✨.")

        # Diretório da galeria
        galeria_path = "galeria"

        # Lista os arquivos de imagem na pasta "galeria"
        imagens = [img for img in os.listdir(galeria_path) if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if imagens:
            # Divida as imagens em grupos de três
            for i in range(0, len(imagens), 3):
                col1, col2, col3 = st.columns(3)  # Cria 3 colunas

                # Exibe cada imagem na coluna correspondente
                with col1:
                    if i < len(imagens):
                        img_path = os.path.join(galeria_path, imagens[i])
                        st.image(img_path, use_column_width=True)

                with col2:
                    if i + 1 < len(imagens):
                        img_path = os.path.join(galeria_path, imagens[i + 1])
                        st.image(img_path, use_column_width=True)

                with col3:
                    if i + 2 < len(imagens):
                        img_path = os.path.join(galeria_path, imagens[i + 2])
                        st.image(img_path, use_column_width=True)
        else:
            st.write("Nenhuma imagem encontrada na galeria.")
    else:
        st.warning("Você precisa estar logado para ver a galeria.")

