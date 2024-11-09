import pygame
import os
import sys

def get_resource_path(relative_path):
    """Retorna o caminho absoluto para arquivos de recursos."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Memória - Escolher Dificuldade")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Fontes
font = pygame.font.SysFont("Graduate", 40)

# Configurações de dificuldade
difficulties = {
    "Fácil": 2,     
    "Médio": 3,      
    "Difícil": 4
}

def draw_rounded_button(screen, text, x, y, width, height, color, font, border_radius=15):
    # Desenha um botão com bordas arredondadas
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=border_radius)
    
    # Renderiza o texto com a cor branca
    button_text = font.render(text, True, (255, 255, 255))  # Branco
    
    # Centraliza o texto dentro do botão
    text_x = x + (width - button_text.get_width()) // 2
    text_y = y + (height - button_text.get_height()) // 2
    
    # Desenha o texto no botão
    screen.blit(button_text, (text_x, text_y))
    
    # Retorna o retângulo do botão para verificações de clique
    return pygame.Rect(x, y, width, height)
font = pygame.font.SysFont('Graduate', 30)

# Função para escolher a dificuldade
def choose_difficulty():
    print("Escolhendo a dificuldade...")
    running = True
    background_image = pygame.image.load(get_resource_path("imagens/backgroundDificuldade.png"))

    while running:
        #screen.fill(LIGHT_BLUE)
        screen.blit(background_image, (0, 0))

        button_rect = draw_rounded_button(screen, "Voltar ao Menu", 50, HEIGHT - 80, 200, 50, (0, 0, 255), font)

        # Detecta clique no botão
        if pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo do mouse foi pressionado
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtém posição do mouse
            if button_rect.collidepoint(mouse_x, mouse_y):  # Verifica se o clique foi dentro do botão
                # Importa e chama a função do menu principal
                from telaInicial import main_menu
                main_menu()
        # Título
        # title_text = font.render("Escolha a Dificuldade", True, BLACK)
        # screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Desenhar botões para cada nível de dificuldade
        button_rects = []
        y_offset = 250
        border_radius = 20  # Definindo um valor para o raio da borda

        for difficulty in difficulties.keys():
            button_text = font.render(difficulty, True, WHITE)
            button_rect = pygame.Rect(WIDTH // 2 - 100, y_offset, 200, 60)
            button_rects.append((button_rect, difficulty))

            # Desenha o botão com bordas arredondadas
            pygame.draw.rect(screen, BLUE, button_rect, border_radius=border_radius)
            pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=border_radius)  # Borda branca

            # Centraliza o texto dentro do botão
            screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                                    button_rect.y + (button_rect.height - button_text.get_height()) // 2))
            y_offset += 100

        pygame.display.flip()


        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Verifica se algum botão foi clicado
                for button_rect, difficulty in button_rects:
                    if button_rect.collidepoint(mouse_pos):
                        print(f"Dificuldade escolhida: {difficulty}")
                        return difficulties[difficulty]  # Retorna o tamanho da grade (linhas, colunas)

# Função para iniciar o jogo com a dificuldade escolhida
def start_game(grid_size):
    print(f"Iniciando o jogo com dificuldade ({grid_size})")
    print("Iniciando o jogo...")
    from jogodamemoria import memory_game
    memory_game(grid_size)

def main_menu():
    running = True
    while running:
        screen.fill(LIGHT_BLUE)

        print("Iniciar Jogo selecionado!")
        grid_size = choose_difficulty()
        if grid_size:
            start_game(grid_size)
        else:
            print("Seleção de dificuldade cancelada.")

main_menu()
pygame.quit()
