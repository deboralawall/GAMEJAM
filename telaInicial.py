import pygame
import sys
import os

basepath = os.path.dirname(os.path.abspath(__file__))

# Inicializando o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Inicial")

# Definindo as cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)

# Fontes
title_font = pygame.font.SysFont('Comic Sans MS', 60)
button_font = pygame.font.SysFont('Comic Sans MS', 40)

# Definindo as opções do menu
options = ["Iniciar Jogo", "Instruções", "Sair"]

# Função para desenhar o botão
def draw_button(text, x, y, width, height, active_color, inactive_color, text_color, action=None, border_radius=15):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Detecta se o mouse está sobre o botão
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height), border_radius=border_radius)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height), border_radius=border_radius)
    
    # Renderiza o texto do botão
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)



def choose_difficulty():
    print("Escolhendo a dificuldade...")
    from choose_difficulty import main_menu
    main_menu()
    
def show_instructions():
    print("Exibindo as instruções...")
    from instructions import show_instructions
    show_instructions()
    
def quit_game():
    pygame.quit()
    sys.exit()

# Função principal para exibir o menu
def main_menu():
    running = True
    image_path = os.path.join(basepath, "imagens", "backgroundInicial.png")
    background_image = pygame.image.load(image_path)
    while running:

        # screen.fill(LIGHT_GRAY)
        screen.blit(background_image, (0, 0))
        # Título
        title_surface = title_font.render(" ", True, DARK_BLUE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        screen.blit(title_surface, title_rect)
        
        # Desenha os botões do menu
        button_width, button_height = 300, 60
        gap = 20  # Espaço entre os botões
        start_y = HEIGHT // 2.5
        # Lista de botões com texto, posição e função associada
        buttons = [
            ("Iniciar Jogo", choose_difficulty),
            ("Instruções", show_instructions),
            ("Sair", quit_game),
        ]
        for i, (text, action) in enumerate(buttons):
            x = (WIDTH - button_width) // 2
            y = start_y + i * (button_height + gap)
            draw_button(text, x, y, button_width, button_height, DARK_BLUE, BLUE, WHITE, action)
        
        # Atualiza a tela
        pygame.display.flip()
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()

# Executa o menu principal
main_menu()
