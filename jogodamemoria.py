import pygame
import random
import os
import time
import sys

# Inicializando o Pygame
pygame.init()

def get_resource_path(relative_path):
    """Retorna o caminho absoluto para arquivos de recursos."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Definindo as cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Configurações da tela
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_WIDTH = 150
CARD_HEIGHT = 200
MARGIN = 20
GRID_SIZE = 2  # Ajuste o tamanho conforme o número de pares predefinidos

# Pares de cartas predefinidos com nomes de arquivos de imagem
card_pairs = [
    ("1.png", "2.png"),
    ("3.png", "4.png"),
    ("5.png", "6.png"),
    ("7.png", "8.png"),
    ("9.png", "10.png"),
    ("11.png", "12.png"),
    ("13.png", "14.png"),
    ("15.png", "16.png"),
    ("17.png", "18.png"),
    ("19.png", "20.png"),
    ("21.png", "22.png"),
    ("23.png", "24.png"),
]

# Função para carregar as imagens das cartas
def load_images():
    images = {}
    for pair in card_pairs:
        for image_name in pair:
            image_path = get_resource_path(os.path.join("imagens", image_name)) 
            images[image_name] = pygame.transform.scale(
                pygame.image.load(image_path), (CARD_WIDTH, CARD_HEIGHT)
            )
    return images

# Função para carregar a imagem de fundo
def load_background():
    background = pygame.image.load(get_resource_path("imagens/agua.jpg"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Redimensiona para o tamanho da tela
    return background

# Função para carregar a imagem das estrelas
def load_star_images():
    star_image = pygame.image.load(get_resource_path("imagens/star.png"))  # Caminho para a imagem de estrela
    star_image = pygame.transform.scale(star_image, (125, 125))  # Redimensionar a estrela
    return star_image

# Função para carregar os sons
def load_sounds():
    correct_sound = pygame.mixer.Sound(get_resource_path("sons/right.ogg")) # Caminho para o som de acerto
    #wrong_sound = pygame.mixer.Sound(os.path.join(basepath, "sons", "lose.flac"))      # Caminho para o som de erro
    return correct_sound

# Função para criar o baralho sem duplicação
def create_deck(size):
    # Seleciona dois pares aleatórios de `card_pairs`
    selected_pairs = random.sample(card_pairs, size)
    # Cria uma lista com as cartas dos pares selecionados e embaralha
    deck = [item for pair in selected_pairs for item in pair]
    random.shuffle(deck)
    return deck

## Função para desenhar as cartas
def draw_cards(screen, deck, revealed_cards, images, size, show_all=False):
    # Calcula a largura e a altura total do grid de cartas
    GRID_SIZE = size
    # print("Size:", size)
    total_width = GRID_SIZE * CARD_WIDTH + (GRID_SIZE - 1) * MARGIN
    total_height = (len(deck) // GRID_SIZE) * CARD_HEIGHT + (len(deck) // GRID_SIZE - 1) * MARGIN

    # Calcula a posição inicial para centralizar o grid
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - total_height) // 2

    for i, card in enumerate(deck):
        x = start_x + (i % GRID_SIZE) * (CARD_WIDTH + MARGIN)
        y = start_y + (i // GRID_SIZE) * (CARD_HEIGHT + MARGIN)
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        # Se show_all for True, todas as cartas serão mostradas
        if show_all or i in revealed_cards:
            screen.blit(images[card], (x, y))  # Exibir a imagem da carta revelada
        else:
            pygame.draw.rect(screen, BLUE, rect)  # Fundo da carta
            pygame.draw.rect(screen, WHITE, rect, 5)  # Borda da carta


def draw_timer(screen, start_time):
    # Calcula o tempo de jogo passado desde o início
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Tempo em segundos
    
    # Define a fonte
    font = pygame.font.SysFont('Graduate', 30)

    # Função auxiliar para desenhar texto com borda
    def draw_text_with_border(text, font, text_color, border_color, x, y, screen):
        # Renderiza o texto para a borda
        text_surface = font.render(text, True, border_color)
        screen.blit(text_surface, (x - 2, y - 2))  # canto superior esquerdo
        screen.blit(text_surface, (x + 2, y - 2))  # canto superior direito
        screen.blit(text_surface, (x - 2, y + 2))  # canto inferior esquerdo
        screen.blit(text_surface, (x + 2, y + 2))  # canto inferior direito

        # Renderiza o texto principal
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, (x, y))

    # Cor do texto principal (amarelo queimado) e da borda (marrom escuro)
    text_color = (250, 210, 61)  # Amarelo queimado
    border_color = (84, 20, 16)  # Marrom escuro

    # Renderiza o texto com o tempo decorrido
    time_text = f'{elapsed_time} seg'

    # Define a posição no canto superior direito
    time_x = WIDTH - 150  # Ajuste horizontal
    time_y = 10           # Ajuste vertical

    # Desenha o texto com borda
    draw_text_with_border(time_text, font, text_color, border_color, time_x, time_y, screen)




# Função para desenhar o placar de estrelas com a mensagem de parabéns
def draw_score(screen, stars, star_image):
    # Calcular o espaço total necessário para as estrelas na horizontal
    total_width = stars * star_image.get_width() + (stars - 1) * 20  # 20 é o espaçamento entre as estrelas
    start_x = (WIDTH - total_width) // 2  # Calcular a posição inicial para centralizar as estrelas na horizontal
    
    # Calcular o espaço total necessário para as estrelas na vertical
    total_height = star_image.get_height()  # Altura de uma estrela
    start_y = (HEIGHT - total_height) // 2  # Calcular a posição inicial para centralizar as estrelas na vertical

    # Desenhar a mensagem de parabéns
    font = pygame.font.SysFont('Graduate', 70, bold=True)  # Fonte estilizada com 70 de tamanho

    # Função auxiliar para desenhar texto com borda
    def draw_text_with_border(text, font, text_color, border_color, x, y, screen):
        # Renderiza o texto para a borda preta
        text_surface = font.render(text, True, border_color)
        screen.blit(text_surface, (x - 2, y - 2))  # canto superior esquerdo
        screen.blit(text_surface, (x + 2, y - 2))  # canto superior direito
        screen.blit(text_surface, (x - 2, y + 2))  # canto inferior esquerdo
        screen.blit(text_surface, (x + 2, y + 2))  # canto inferior direito

        # Renderiza o texto principal
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, (x, y))

    # Texto "Parabéns!" com a cor amarelo queimado (#FAD23D) e borda preta
    message_text = "Parabéns!"
    text_color = (250, 210, 61)  # Amarelo queimado
    border_color = (84, 20, 16)  # marrom

    # Calcule a posição para centralizar o texto
    message_width = font.render(message_text, True, text_color).get_width()
    message_x = (WIDTH - message_width) // 2  # Centraliza horizontalmente
    message_y = 150  # Posição vertical (ajuste conforme necessário)

    # Exibe a mensagem com borda
    draw_text_with_border(message_text, font, text_color, border_color, message_x, message_y, screen)

    # Desenhar as estrelas na tela
    for i in range(stars):
        screen.blit(star_image, (start_x + i * (star_image.get_width() + 20), start_y))

# Função para calcular as estrelas com base no tempo
def calculate_stars(elapsed_time):
    if elapsed_time <= 20:
        return 3
    elif elapsed_time <= 40:
        return 2
    elif elapsed_time <= 60:
        return 1
    else:
        return 0
    
# Função para desenhar o botão
def draw_rounded_button(screen, text, x, y, width, height, color, border_radius=15):
    # Desenha um botão com bordas arredondadas
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=border_radius)
    
    # Define a fonte do texto
    font = pygame.font.SysFont('Graduate', 30)
    
    # Renderiza o texto com cor branca
    text_surface = font.render(text, True, (255, 255, 255))  # Branco
    
    # Centraliza o texto dentro do botão
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    
    # Desenha o texto no botão
    screen.blit(text_surface, (text_x, text_y))

def draw_turn(screen, turn):
    font = pygame.font.SysFont('Graduate', 30)
    text_color = (250, 210, 61)  # Amarelo queimado
    border_color = (84, 20, 16)  # Marrom

    # Renderizar o texto principal e o texto de borda
    turn_text = font.render(f'Turno: {turn}', True, text_color)
    border_text = font.render(f'Turno: {turn}', True, border_color)

    # Definir a posição para o canto superior esquerdo
    x, y = 10, 10

    # Desenhar a borda ao redor do texto
    screen.blit(border_text, (x - 1, y))      # Esquerda
    screen.blit(border_text, (x + 1, y))      # Direita
    screen.blit(border_text, (x, y - 1))      # Cima
    screen.blit(border_text, (x, y + 1))      # Baixo
    screen.blit(border_text, (x - 1, y - 1))  # Canto superior esquerdo
    screen.blit(border_text, (x + 1, y - 1))  # Canto superior direito
    screen.blit(border_text, (x - 1, y + 1))  # Canto inferior esquerdo
    screen.blit(border_text, (x + 1, y + 1))  # Canto inferior direito

    # Desenhar o texto principal no topo da borda
    screen.blit(turn_text, (x, y))


def draw_best_time(screen, best_time):
    font = pygame.font.SysFont('Graduate', 30)
    text_color = (250, 210, 61)  # Amarelo queimado
    border_color = (84, 20, 16)  # Marrom

    if best_time == float('inf'):
        best_time_text = font.render('Não há um melhor tempo!', True, text_color)
        border_text = font.render('Não há um melhor tempo!', True, border_color)
    else:
        best_time_text = font.render(f'Melhor Tempo: {best_time} seg', True, text_color)
        border_text = font.render(f'Melhor Tempo: {best_time} seg', True, border_color)

    # Definir posição para o texto
    x = (WIDTH - best_time_text.get_width()) // 1.15
    y = HEIGHT - best_time_text.get_height() - 10 

    # Desenhar a borda ao redor do texto
    screen.blit(border_text, (x - 1, y))      # Esquerda
    screen.blit(border_text, (x + 1, y))      # Direita
    screen.blit(border_text, (x, y - 1))      # Cima
    screen.blit(border_text, (x, y + 1))      # Baixo
    screen.blit(border_text, (x - 1, y - 1))  # Canto superior esquerdo
    screen.blit(border_text, (x + 1, y - 1))  # Canto superior direito
    screen.blit(border_text, (x - 1, y + 1))  # Canto inferior esquerdo
    screen.blit(border_text, (x + 1, y + 1))  # Canto inferior direito

    # Desenhar o texto principal no topo
    screen.blit(best_time_text, (x, y))

# Função principal do jogo
def memory_game(size, turn=1, best_time=float('inf')):
    GRID_SIZE = size
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memória Aquática")

    # Carregar as imagens
    images = load_images()
    background = load_background()  # Carregar a imagem de fundo
    star_image = load_star_images()  # Carregar a imagem de estrela
    
    # Criar o baralho e embaralhar
    deck = create_deck(size)

    # Listas de cartas viradas e combinadas
    revealed_cards = []
    matched_cards = []

    # No início da função principal do jogo
    correct_sound = load_sounds()

    start_time = pygame.time.get_ticks()  # Tempo de início do jogo
    # print("start_time" , start_time)

    # Loop principal do jogo
    running = True
    first_card = None
    second_card = None
    last_flip_time = None
    while running:
        screen.fill(LIGHT_BLUE)
        screen.blit(background, (0, 0))  # Desenha a imagem de fundo


        draw_rounded_button(screen, "Voltar", 50, HEIGHT - 80, 200, 50, (0, 0, 255))  # Botão azul

        draw_turn(screen, turn)  # Desenha o turno
        draw_best_time(screen, best_time)  # Desenha o melhor tempo

        # Detecta clique no botão
        if pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo do mouse foi pressionado
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtém posição do mouse
            if 50 < mouse_x < 250 and HEIGHT - 80 < mouse_y < HEIGHT - 30:
                # Importa e chama a função do menu principal
                from choose_difficulty import main_menu
                main_menu()

        # Chama a função para desenhar as cartas, agora com o parâmetro 'show_all' sendo False enquanto o jogo não acabar
        draw_cards(screen, deck, revealed_cards, images, size, show_all=False)
        draw_timer(screen, start_time)  # Exibe o tempo
        # print("screen:", screen)
        # print("start_time,", start_time)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                        # Detectando clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN and second_card is None:
                x, y = event.pos

                # Calcula a posição inicial do grid de cartas
                total_width = GRID_SIZE * CARD_WIDTH + (GRID_SIZE - 1) * MARGIN
                total_height = (len(deck) // GRID_SIZE) * CARD_HEIGHT + (len(deck) // GRID_SIZE - 1) * MARGIN
                start_x = (WIDTH - total_width) // 2
                start_y = (HEIGHT - total_height) // 2

                # Ajusta x e y com a posição inicial do grid
                adjusted_x = x - start_x
                adjusted_y = y - start_y

                # Verifica se o clique está dentro do grid
                if 0 <= adjusted_x < total_width and 0 <= adjusted_y < total_height:
                    col = adjusted_x // (CARD_WIDTH + MARGIN)
                    row = adjusted_y // (CARD_HEIGHT + MARGIN)
                    card_index = row * GRID_SIZE + col

                    # Verifica se o índice está dentro dos limites do baralho e se a carta ainda não foi revelada ou combinada
                    if card_index < len(deck) and card_index not in revealed_cards and card_index not in matched_cards:
                        revealed_cards.append(card_index)

                        if first_card is None:
                            first_card = card_index  # Primeira carta virada
                        else:
                            second_card = card_index  # Segunda carta virada
                            last_flip_time = time.time()  # Registra o tempo da segunda virada

                            # Verifica se as cartas formam um par
                            if is_match(deck[first_card], deck[second_card]):
                                correct_sound.play()  # Toca o som de acerto
                                matched_cards.append(first_card)
                                matched_cards.append(second_card)
                                first_card = None
                                second_card = None
                                last_flip_time = None  # Reseta o tempo, pois o par foi encontrado
                                


        # Lógica para virar cartas para baixo se não forem pares
        if first_card is not None and second_card is not None:
            current_time = time.time()
            if current_time - last_flip_time >= 2:  # 2 segundos de espera
                revealed_cards.remove(first_card)
                revealed_cards.remove(second_card)
                first_card = None
                second_card = None
                last_flip_time = None
                #wrong_sound.play()  # Toca o som de erro

        # Verifica se o jogo acabou
        if len(matched_cards) == len(deck):
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Tempo total do jogo em segundos
            stars = calculate_stars(elapsed_time)  # Calcula as estrelas
            print(f"Você venceu! Tempo: {elapsed_time} segundos, Estrelas: {stars}")
            pygame.time.wait(1000)  # Atraso de 1 segundo antes de fechar

            # Exibe todas as cartas viradas
            draw_cards(screen, deck, revealed_cards, images, size, show_all=True)

            # Exibe o placar final com as estrelas
            draw_score(screen, stars, star_image)  # Exibe as estrelas
            pygame.display.flip()
            pygame.time.wait(2000)  # Exibe o placar final por 2 segundos
            # Atualiza o melhor tempo
            if elapsed_time < best_time:
                best_time = elapsed_time

            turn += 1  # Incrementa o turno após cada rodada
            running = False
            memory_game(size, turn, best_time)

    pygame.quit()


# Função para verificar se dois itens formam um par
def is_match(card1, card2):
    for image1, image2 in card_pairs:
        if (card1 == image1 and card2 == image2) or (card1 == image2 and card2 == image1):
            return True
    return False
