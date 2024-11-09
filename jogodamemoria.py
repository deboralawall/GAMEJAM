import pygame
import random
import os

# Inicializando o Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)

# Configurações da tela
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_WIDTH = 150
CARD_HEIGHT = 200
MARGIN = 10
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

# Função para criar o baralho sem duplicação
def create_deck():
    deck = [item for pair in card_pairs for item in pair]  # Flatten dos pares predefinidos
    random.shuffle(deck)  # Embaralha o baralho mantendo os pares predefinidos
    return deck

# Função para desenhar as cartas
def draw_cards(screen, deck, revealed_cards, images):
    for i, card in enumerate(deck):
        x = (i % GRID_SIZE) * (CARD_WIDTH + MARGIN) + MARGIN
        y = (i // GRID_SIZE) * (CARD_HEIGHT + MARGIN) + MARGIN
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if i in revealed_cards:
            screen.blit(images[card], (x, y))  # Exibir a imagem da carta revelada
        else:
            pygame.draw.rect(screen, BLUE, rect)  # Fundo da carta
            pygame.draw.rect(screen, WHITE, rect, 5)  # Borda da carta

# Função principal do jogo
def memory_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memoria Aquática")

    # Carregar as imagens
    images = load_images()

    # Criar o baralho e embaralhar
    deck = create_deck()

    # Listas de cartas viradas e combinadas
    revealed_cards = []
    matched_cards = []

    # Loop principal do jogo
    running = True
    first_card = None
    while running:
        screen.fill(LIGHT_BLUE)
        draw_cards(screen, deck, revealed_cards, images)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detectando clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // (CARD_HEIGHT + MARGIN)
                col = x // (CARD_WIDTH + MARGIN)
                card_index = row * GRID_SIZE + col

                if card_index not in revealed_cards and card_index not in matched_cards:
                    revealed_cards.append(card_index)

                    if first_card is None:
                        first_card = card_index
                    else:
                        # Verifica se o par é válido (imagem e imagem correspondente)
                        if is_match(deck[first_card], deck[card_index]):
                            matched_cards.append(first_card)
                            matched_cards.append(card_index)
                            first_card = None
                        else:
                            pygame.time.wait(500)  # Espera antes de esconder as cartas
                            revealed_cards.remove(card_index)
                            revealed_cards.remove(first_card)
                            first_card = None

        # Verifica se o jogo acabou
        if len(matched_cards) == len(deck):
            print("Você venceu!")
            pygame.time.wait(1000)  # Atraso de 1 segundo antes de fechar
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
