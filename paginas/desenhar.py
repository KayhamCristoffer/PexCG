import streamlit as st
import mediapipe as mp
import numpy as np
import time
import os

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def show_desenho():
    cores = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
    cor_desenho_atual = (255, 0, 0)

    # Botões de cores
    botao_raio = 40
    espaco_entre_botoes = 20
    botoes = [(100 + (botao_raio * 2 + espaco_entre_botoes) * i, 100, cor) for i, cor in enumerate(cores)]

    # Botões de ação
    botao_salvar = (100 + botao_raio * 2 * 8 + espaco_entre_botoes * 5, 100)
    botao_apagar = (100 + botao_raio * 2 * 10 + espaco_entre_botoes * 6, 100)
    botao_borracha = (100 + botao_raio * 2 * 12 + espaco_entre_botoes * 7, 100)
    intervalo = 5
    ultimo_tempo = time.time()

    video_feed = st.empty()

    # Configurações da câmera
    cap = st.camera_input("Camera", key="camera")

    if cap is None:
        st.error("Não foi possível acessar a câmera.")
        return

    pontos_atual = []
    pontos_desenhos_anteriores = []
    pontos_buffer = []
    desenhando = False

    while True:
        frame = cap.read()
        if frame is None:
            st.error("Não foi possível capturar o frame da câmera.")
            break

        img = np.array(frame)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Processa a imagem para detectar mãos
        results = hands.process(img)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lmlist = [(int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0])) for landmark in hand_landmarks.landmark]

                dedos = [1 if landmark.y < lmlist[tip][1] else 0 for tip in [8, 12, 16, 20]]

                dedosLev = sum(dedos)

                if dedosLev == 1:  # Um dedo levantado
                    x, y = lmlist[8]
                    # Desenho do círculo na posição da ponta do dedo
                    cv2.circle(img, (x, y), 15, cor_desenho_atual, cv2.FILLED)

                    if not desenhando:
                        pontos_atual = []
                        pontos_buffer = []
                        desenhando = True

                    pontos_buffer.append((x, y, cor_desenho_atual))

                    if len(pontos_buffer) > 1:
                        for i in range(len(pontos_buffer) - 1):
                            p1 = pontos_buffer[i]
                            p2 = pontos_buffer[i + 1]
                            for t in np.linspace(0, 1, num=30):
                                x_interp = int((1 - t) * p1[0] + t * p2[0])
                                y_interp = int((1 - t) * p1[1] + t * p2[1])
                                pontos_atual.append((x_interp, y_interp, p1[2]))

                else:
                    desenhando = False
                    if pontos_atual:
                        pontos_desenhos_anteriores.extend(pontos_atual)
                        pontos_atual = []

                x_mao, y_mao = lmlist[8]

                # Lógica para mudança de cor
                for bx, by, cor in botoes:
                    if (bx < x_mao < bx + botao_raio * 2) and (by < y_mao < by + botao_raio * 2):
                        cor_desenho_atual = cor

                # Salvando o desenho
                if (botao_salvar[0] < x_mao < botao_salvar[0] + botao_raio * 2) and (botao_salvar[1] < y_mao < botao_salvar[1] + botao_raio * 2):
                    tempo_atual = time.time()
                    if tempo_atual - ultimo_tempo > intervalo:
                        salvar_desenho(img, pontos_desenhos_anteriores, pontos_atual)
                        ultimo_tempo = tempo_atual

                # Apagando
                if (botao_apagar[0] < x_mao < botao_apagar[0] + botao_raio * 2) and (botao_apagar[1] < y_mao < botao_apagar[1] + botao_raio * 2):
                    tempo_atual = time.time()
                    if tempo_atual - ultimo_tempo > intervalo:
                        pontos_desenhos_anteriores.clear()
                        pontos_atual.clear()
                        pontos_buffer.clear()
                        ultimo_tempo = tempo_atual

        # Desenho dos pontos anteriores
        for pontos in pontos_desenhos_anteriores + pontos_atual:
            x, y, cor = pontos
            cv2.circle(img, (x, y), 5, cor, cv2.FILLED)

        video_feed.image(img, channels="RGB")

def salvar_desenho(img, pontos_desenhos_anteriores, pontos_atual):
    if not os.path.exists("galeria"):
        os.makedirs("galeria")

    # Desenha os pontos no img
    for pontos in pontos_desenhos_anteriores + pontos_atual:
        x, y, cor = pontos
        cv2.circle(img, (x, y), 5, cor, cv2.FILLED)    

    # Nome do arquivo com timestamp
    nome_arquivo = time.strftime("desenho_%Y%m%d_%H%M%S.png")
    caminho_completo = os.path.join("galeria", nome_arquivo)

    # Salva a imagem
    cv2.imwrite(caminho_completo, img)

    if "saved_images" not in st.session_state:  
        st.session_state.saved_images = []

    st.session_state.saved_images.append(caminho_completo)
    st.success(f"Desenho salvo: {nome_arquivo}")

def desenhar_page():
    st.title("Desenhar com Mãos")

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []

    show_desenho()  

    st.subheader("Desenhos Salvos:")
    for img_path in st.session_state.saved_images:
        st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)

