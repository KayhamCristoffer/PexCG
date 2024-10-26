import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import os
from PIL import Image, ImageDraw

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
    intervalo = 5
    ultimo_tempo = time.time()
    
    video_feed = st.empty()
    
    # Inicializando a captura de vídeo
    cap = st.camera_input("Captura de vídeo", key="camera")
    
    if cap is None:
        st.error("Não foi possível acessar a câmera.")
        return

    pontos_atual = []
    pontos_desenhos_anteriores = []
    pontos_buffer = []
    desenhando = False

    while True:
        img = cap.read()
        if img is None:
            st.error("Não foi possível capturar o frame da câmera.")
            break
        
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)

        # Desenha botões
        for bx, by, cor in botoes:
            draw.ellipse([bx, by, bx + botao_raio * 2, by + botao_raio * 2], fill=cor)

        # Botões de ação
        draw.ellipse([botao_salvar[0], botao_salvar[1], botao_salvar[0] + botao_raio * 2, botao_salvar[1] + botao_raio * 2], fill=(200, 200, 200))
        draw.text((botao_salvar[0] + 15, botao_salvar[1] + 5), "S", fill=(0, 0, 0))
        draw.ellipse([botao_apagar[0], botao_apagar[1], botao_apagar[0] + botao_raio * 2, botao_apagar[1] + botao_raio * 2], fill=(200, 200, 200))
        draw.text((botao_apagar[0] + 15, botao_apagar[1] + 5), "A", fill=(0, 0, 0))

        resultado = detector.findHands(np.array(img), draw=True)
        hand = resultado[0] if resultado else None

        if hand:
            lmlist = hand[0]['lmList']
            dedos = detector.fingersUp(hand[0])
            dedosLev = dedos.count(1)

            if dedosLev == 1:
                x, y = lmlist[8][0], lmlist[8][1]
                draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=cor_desenho_atual)

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

            x_mao, y_mao = lmlist[8][0], lmlist[8][1]

            for bx, by, cor in botoes:
                if (bx < x < bx + botao_raio * 2) and (by < y < by + botao_raio * 2):
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

        for pontos in pontos_desenhos_anteriores + pontos_atual:
            x, y, cor = pontos
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=cor)

        video_feed.image(np.array(img), channels="RGB")

    # Libere a câmera ao final
    cap.release()

def salvar_desenho(img, pontos_desenhos_anteriores, pontos_atual):
    # Verifica se o diretório 'galeria' existe, se não, cria
    if not os.path.exists("galeria"):
        os.makedirs("galeria")
    
    # Desenha os pontos no img
    draw = ImageDraw.Draw(img)
    for pontos in pontos_desenhos_anteriores + pontos_atual:
        x, y, cor = pontos
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=cor)    
    
    # Nome do arquivo com timestamp
    nome_arquivo = time.strftime("desenho_%Y%m%d_%H%M%S.png")
    
    # Caminho completo para salvar a imagem na pasta 'galeria'
    caminho_completo = os.path.join("galeria", nome_arquivo)
    
    # Salva a imagem
    img.save(caminho_completo)
    
    # Inicializa a lista saved_images se não existir
    if "saved_images" not in st.session_state:  
        st.session_state.saved_images = []  # Inicializa a lista se não existir
    
    # Adiciona o caminho à lista de imagens salvas
    st.session_state.saved_images.append(caminho_completo)
    
    # Mensagem de sucesso
    st.success(f"Desenho salvo: {nome_arquivo}")

def desenhar_page():
    st.title("Desenhar com Mãos")

    if "saved_images" not in st.session_state:
        st.session_state.saved_images = []
   
    show_desenho()  

    st.subheader("Desenhos Salvos:")
    for img_path in st.session_state.saved_images:
        st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)

