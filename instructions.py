import pygame
import sys
import os

def get_resource_path(relative_path):
    """Retorna o caminho absoluto para arquivos de recursos."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Inicializando o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Instruções")

# Definindo as cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)

# Fontes
title_font = pygame.font.SysFont('Graduate', 60)
button_font = pygame.font.SysFont('Graduate', 40)

# Função para desenhar o botão
def draw_button(text, x, y, width, height, active_color, inactive_color, text_color, action=None, border_radius=15):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Detecta se o mouse está sobre o botão
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height), border_radius=border_radius)  # Botão com bordas arredondadas
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height), border_radius=border_radius)  # Botão com bordas arredondadas
    
    # Renderiza o texto do botão
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Função para voltar ao menu
def back_to_menu():
    from telaInicial import main_menu
    main_menu()

# Função para exibir a tela de instruções
def show_instructions():
    running = True

    # Carregar a imagem de fundo das instruções
    background_image = pygame.image.load(get_resource_path("imagens/backgroundInstrucoes.png"))
    
    while running:
        screen.fill(LIGHT_GRAY)
        
        # Exibe a imagem de instruções
        screen.blit(background_image, (0, 0))

        # Botão para voltar ao menu
        button_width, button_height = 200, 40
        back_button_x = (WIDTH - button_width) // 8.6
        back_button_y = HEIGHT - 60
        draw_button("Menu", back_button_x, back_button_y, button_width, button_height, DARK_BLUE, BLUE, WHITE, back_to_menu)
        
        pygame.display.flip()
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Se pressionar 'ESC', voltar ao menu
                    running = False
    
    pygame.quit()
    sys.exit()
