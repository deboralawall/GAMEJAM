import pygame
import random
import os
import time

# Inicializando o Pygame
pygame.init()

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
    # Adicione mais pares conforme necessário
]

# Função para carregar as imagens das cartas
def load_images():
    images = {}
    for pair in card_pairs:
        for image_name in pair:
            image_path = os.path.join("imagens", image_name)
            images[image_name] = pygame.transform.scale(
                pygame.image.load(image_path), (CARD_WIDTH, CARD_HEIGHT)
            )
    return images

# Função para carregar a imagem de fundo
def load_background():
    background = pygame.image.load(os.path.join("imagens", "agua.jpg"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Redimensiona para o tamanho da tela
    return background

# Função para carregar a imagem das estrelas
def load_star_images():
    star_image = pygame.image.load(os.path.join("imagens", "star.png"))  # Caminho para a imagem de estrela
    star_image = pygame.transform.scale(star_image, (125, 125))  # Redimensionar a estrela
    return star_image

# Função para carregar os sons
def load_sounds():
    correct_sound = pygame.mixer.Sound(os.path.join("sons", "win.ogg"))  # Caminho para o som de acerto
    wrong_sound = pygame.mixer.Sound(os.path.join("sons", "lose.flac"))      # Caminho para o som de erro
    return correct_sound, wrong_sound

# Função para criar o baralho sem duplicação
def create_deck():
    deck = [item for pair in card_pairs for item in pair]  # Flatten dos pares predefinidos
    random.shuffle(deck)  # Embaralha o baralho mantendo os pares predefinidos
    return deck

## Função para desenhar as cartas
def draw_cards(screen, deck, revealed_cards, images, show_all=False):
    # Calcula a largura e a altura total do grid de cartas
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
    elapsed_time = pygame.time.get_ticks() // 1000  # Tempo em segundos
    font = pygame.font.SysFont('Arial', 30)
    time_text = font.render(f'{elapsed_time} seg', True, WHITE)
    screen.blit(time_text, (WIDTH - 150, 10))  # Posiciona no canto superior direito

# Função para desenhar o placar de estrelas com a mensagem de parabéns
def draw_score(screen, stars, star_image):
    # Calcular o espaço total necessário para as estrelas na horizontal
    total_width = stars * star_image.get_width() + (stars - 1) * 20  # 20 é o espaçamento entre as estrelas
    start_x = (WIDTH - total_width) // 2  # Calcular a posição inicial para centralizar as estrelas na horizontal
    
    # Calcular o espaço total necessário para as estrelas na vertical
    total_height = star_image.get_height()  # Altura de uma estrela
    start_y = (HEIGHT - total_height) // 2  # Calcular a posição inicial para centralizar as estrelas na vertical

    # Desenhar a mensagem de parabéns
    font = pygame.font.SysFont('Arial', 50)
    message_text = font.render("Parabéns!", True, (255, 255, 255))  # Texto branco
    message_width = message_text.get_width()
    message_x = (WIDTH - message_width) // 2  # Centraliza a mensagem horizontalmente
    message_y = start_y - 60  # Posiciona a mensagem um pouco acima das estrelas

    screen.blit(message_text, (message_x, message_y))  # Exibe a mensagem de Parabéns!

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

# Função principal do jogo
def memory_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memória Aquática")

    # Carregar as imagens
    images = load_images()
    background = load_background()  # Carregar a imagem de fundo
    star_image = load_star_images()  # Carregar a imagem de estrela
    
    # Criar o baralho e embaralhar
    deck = create_deck()

    # Listas de cartas viradas e combinadas
    revealed_cards = []
    matched_cards = []

    # No início da função principal do jogo
    correct_sound, wrong_sound = load_sounds()

    start_time = pygame.time.get_ticks()  # Tempo de início do jogo

    # Loop principal do jogo
    running = True
    first_card = None
    second_card = None
    last_flip_time = None
    while running:
        screen.fill(LIGHT_BLUE)
        screen.blit(background, (0, 0))  # Desenha a imagem de fundo

        # Chama a função para desenhar as cartas, agora com o parâmetro 'show_all' sendo False enquanto o jogo não acabar
        draw_cards(screen, deck, revealed_cards, images, show_all=False)
        draw_timer(screen, start_time)  # Exibe o tempo
        
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
                                matched_cards.append(first_card)
                                matched_cards.append(second_card)
                                first_card = None
                                second_card = None
                                last_flip_time = None  # Reseta o tempo, pois o par foi encontrado
                                correct_sound.play()  # Toca o som de acerto


        # Lógica para virar cartas para baixo se não forem pares
        if first_card is not None and second_card is not None:
            current_time = time.time()
            if current_time - last_flip_time >= 2:  # 2 segundos de espera
                revealed_cards.remove(first_card)
                revealed_cards.remove(second_card)
                first_card = None
                second_card = None
                last_flip_time = None
                wrong_sound.play()  # Toca o som de erro

        # Verifica se o jogo acabou
        if len(matched_cards) == len(deck):
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Tempo total do jogo em segundos
            stars = calculate_stars(elapsed_time)  # Calcula as estrelas
            print(f"Você venceu! Tempo: {elapsed_time} segundos, Estrelas: {stars}")
            pygame.time.wait(1000)  # Atraso de 1 segundo antes de fechar

            # Exibe todas as cartas viradas
            draw_cards(screen, deck, revealed_cards, images, show_all=True)

            # Exibe o placar final com as estrelas
            draw_score(screen, stars, star_image)  # Exibe as estrelas
            pygame.display.flip()
            pygame.time.wait(2000)  # Exibe o placar final por 2 segundos
            running = False

    pygame.quit()


# Função para verificar se dois itens formam um par
def is_match(card1, card2):
    for image1, image2 in card_pairs:
        if (card1 == image1 and card2 == image2) or (card1 == image2 and card2 == image1):
            return True
    return False

# Iniciar o jogo
memory_game()
