import pygame
import os

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
font = pygame.font.SysFont("Arial", 40)

# Configurações de dificuldade
difficulties = {
    "Fácil": 2,     # Grade 2x2
    "Médio": 4,      # Grade 4x4
}
def draw_button(text, x, y, width, height, color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 3)
    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    return button_rect

# Função para escolher a dificuldade
def choose_difficulty():
    print("Escolhendo a dificuldade...")
    running = True
    background_image = pygame.image.load('imagens/backgroundDificuldade.png')

    while running:
        #screen.fill(LIGHT_BLUE)
        screen.blit(background_image, (0, 0))

        draw_button("Voltar ao Menu", 50, HEIGHT - 80, 200, 50, BLUE)

        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 50 < mouse_x < 250 and HEIGHT - 80 < mouse_y < HEIGHT - 30:
                # running = False
                from telaInicial import main_menu
                main_menu()
        # Título
        title_text = font.render("Escolha a Dificuldade", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Desenhar botões para cada nível de dificuldade
        button_rects = []
        y_offset = 200
        for difficulty in difficulties.keys():
            button_text = font.render(difficulty, True, WHITE)
            button_rect = pygame.Rect(WIDTH // 2 - 100, y_offset, 200, 60)
            button_rects.append((button_rect, difficulty))

            pygame.draw.rect(screen, BLUE, button_rect)
            pygame.draw.rect(screen, WHITE, button_rect, 3)
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
