import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import os

def show_desenho():
    detector = HandDetector()
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
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Não foi possível acessar a câmera.")
        return

    # Configurações da câmera
    cap.set(3, 1280)
    cap.set(4, 780)

    pontos_atual = []
    pontos_desenhos_anteriores = []
    pontos_buffer = []
    desenhando = False

    while True:
        ret, img = cap.read()
        if not ret:
            st.error("Não foi possível capturar o frame da câmera.")
            break

        img = cv2.flip(img, 1)
        
        # Desenha a borda da câmera
        altura, largura, _ = img.shape
        img_borda = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        
        # Desenha botões
        for bx, by, cor in botoes:
            cv2.circle(img_borda, (bx + 20, by + 20), botao_raio, cor, cv2.FILLED)

        # Botões de ação
        cv2.circle(img_borda, (botao_salvar[0] + 20, botao_salvar[1] + 20), botao_raio, (200, 200, 200), cv2.FILLED)
        cv2.putText(img_borda, "S", (botao_salvar[0] + 20 - 10, botao_salvar[1] + 20 + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.circle(img_borda, (botao_apagar[0] + 20, botao_apagar[1] + 20), botao_raio, (200, 200, 200), cv2.FILLED)
        cv2.putText(img_borda, "A", (botao_apagar[0] + 20 - 10, botao_apagar[1] + 20 + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.circle(img_borda, (botao_borracha[0] + 20, botao_borracha[1] + 20), botao_raio, (200, 200, 200), cv2.FILLED)
        cv2.putText(img_borda, "B", (botao_borracha[0] + 20 - 10, botao_borracha[1] + 20 + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        resultado = detector.findHands(img, draw=True)
        hand = resultado[0] if resultado else None

        if hand:
            lmlist = hand[0]['lmList']
            dedos = detector.fingersUp(hand[0])
            dedosLev = dedos.count(1)

            if dedosLev == 1:
                x, y = lmlist[8][0], lmlist[8][1]
                cv2.circle(img_borda, (x + 20, y + 20), 15, cor_desenho_atual, cv2.FILLED)

                if not desenhando:
                    pontos_atual = []
                    pontos_buffer = []
                    desenhando = True

                pontos_buffer.append((x + 20, y + 20, cor_desenho_atual))

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

            x_mao, y_mao = lmlist[8][0], lmlist[8][1]

            for bx, by, cor in botoes:
                if (bx < x < bx + botao_raio * 2) and (by < y < by + botao_raio * 2):
                    cor_desenho_atual = cor
                    cv2.circle(img_borda, (bx + 20, by + 20), botao_raio + 10, (0, 255, 0), 4)

            # Salvando o desenho
            if (botao_salvar[0] < x_mao < botao_salvar[0] + botao_raio * 2) and (botao_salvar[1] < y_mao < botao_salvar[1] + botao_raio * 2):
                tempo_atual = time.time()
                if tempo_atual - ultimo_tempo > intervalo:
                    salvar_desenho(img_borda, pontos_desenhos_anteriores, pontos_atual)
                    ultimo_tempo = tempo_atual

            # Apagando
            if (botao_apagar[0] < x_mao < botao_apagar[0] + botao_raio * 2) and (botao_apagar[1] < y_mao < botao_apagar[1] + botao_raio * 2):
                tempo_atual = time.time()
                if tempo_atual - ultimo_tempo > intervalo:
                    pontos_desenhos_anteriores.clear()
                    pontos_atual.clear()
                    pontos_buffer.clear()
                    ultimo_tempo = tempo_atual
            if (botao_borracha[0] - botao_raio < x_mao < botao_borracha[0] + botao_raio) and \
                    (botao_borracha[1] - botao_raio < y_mao < botao_borracha[1] + botao_raio):
                modo_borracha = not modo_borracha  # Alterna a borracha (ativa/desativa)

        for pontos in pontos_desenhos_anteriores + pontos_atual:
            x, y, cor = pontos
            cv2.circle(img_borda, (x, y), 5, cor, cv2.FILLED)

        video_feed.image(cv2.cvtColor(img_borda, cv2.COLOR_BGR2RGB), channels="RGB")

    # Libere a câmera ao final
    cap.release()
    cv2.destroyAllWindows()

def salvar_desenho(img, pontos_desenhos_anteriores, pontos_atual):
    # Verifica se o diretório 'galeria' existe, se não, cria
    if not os.path.exists("galeria"):
        os.makedirs("galeria")
    
    # Desenha os pontos no img
    for pontos in pontos_desenhos_anteriores + pontos_atual:
        x, y, cor = pontos
        cv2.circle(img, (x, y), 5, cor, cv2.FILLED)    
    
    # Nome do arquivo com timestamp
    nome_arquivo = time.strftime("desenho_%Y%m%d_%H%M%S.png")
    
    # Caminho completo para salvar a imagem na pasta 'galeria'
    caminho_completo = os.path.join("galeria", nome_arquivo)
    
    # Salva a imagem
    cv2.imwrite(caminho_completo, img)
    
    # Inicializa a lista saved_images se não existir
    if "saved_images" not in st.session_state:  
        st.session_state.saved_images = []  # Inicializa a lista se não existir
    
    # Adiciona o caminho à lista de imagens salvas
    st.session_state.saved_images.append(caminho_completo)
    
    # Mensagem de sucesso
    st.success(f"Desenho salvo: {nome_arquivo}")

def desenhar_page():
    st.title("Desenhar com Mãos")

    if "camera_running" not in st.session_state:
        st.session_state.camera_running = False

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []
   
    show_desenho()  

    st.subheader("Desenhos Salvos:")
    for img_path in st.session_state.saved_images:
        st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
