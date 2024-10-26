import streamlit as st
import numpy as np
import time
import os
from cvzone.HandTrackingModule import HandDetector
import cv2

def show_desenho():
    detector = HandDetector(maxHands=1)  # Detectar apenas uma mão
    cores = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
    cor_desenho_atual = (255, 0, 0)

    # Botões de cores
    botao_raio = 40
    espaco_entre_botoes = 20
    botoes = [(100 + (botao_raio * 2 + espaco_entre_botoes) * i, 100, cor) for i, cor in enumerate(cores)]

    # Intervalo de tempo para salvar/apagar
    intervalo = 5
    ultimo_tempo = time.time()

    # Usar a câmera do Streamlit
    image = st.camera_input("Capture a photo")  # Captura a imagem usando a câmera

    if image is not None:
        img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        img = cv2.flip(img, 1)  # Inverter a imagem

        # Desenho inicial
        drawing = np.zeros_like(img)

        # Botões de cores
        for bx, by, cor in botoes:
            cv2.circle(img, (bx + 20, by + 20), botao_raio, cor, cv2.FILLED)

        # Exibir a imagem com os botões
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), channels="RGB")

        # Processar a imagem para detecção de mão
        hands, img = detector.findHands(img)

        if hands:
            lmList = hands[0]['lmList']  # Lista de pontos de referência da mão
            x1, y1, x2, y2 = lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1]  # Dedo indicador e dedo médio
            dedo_indicador = lmList[8]  # Ponto do dedo indicador
            dedo_medio = lmList[12]  # Ponto do dedo médio
            
            # Desenhar quando o dedo indicador estiver levantado
            if dedo_indicador[1] < dedo_medio[1]:  # Se o indicador estiver acima do médio
                cv2.line(drawing, (x1, y1), (x1, y1), cor_desenho_atual, 5)

        # Misturar a imagem de desenho e a imagem original
        img = cv2.add(img, drawing)
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), channels="RGB")

        # Armazenar a imagem desenhada
        if st.button("Salvar Desenho"):
            st.session_state.saved_images.append(img)

    else:
        st.warning("Por favor, habilite sua câmera para capturar uma imagem.")

def desenhar_page():
    st.title("Desenhar com Mãos")

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []

    show_desenho()

    st.subheader("Desenhos Salvos:")
    for img in st.session_state.saved_images:
        st.image(img, caption="Desenho Salvo", use_column_width=True)

if __name__ == "__main__":
    desenhar_page()
