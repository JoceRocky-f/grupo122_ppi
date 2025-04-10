import pygame
import sys
import os
import random

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hurban Heist")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fuente
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 36)

# Fondo
background = pygame.image.load("fondo.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Pantalla inicial con botones
def show_start_screen():
    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        draw_text("HURBAN HEIST", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)

        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(screen, BLUE, start_button)
        draw_text("START", button_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 25)

        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, RED, exit_button)
        draw_text("EXIT", button_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 75)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Pantalla de selección de roles
def show_role_selection_screen():
    while True:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        draw_text("Selecciona tu Rol", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)

        police_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 150, 50)
        pygame.draw.rect(screen, BLUE, police_button)
        draw_text("Policía", button_font, WHITE, screen, WIDTH // 2 - 75, HEIGHT // 2 - 25)

        thief_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 - 50, 150, 50)
        pygame.draw.rect(screen, RED, thief_button)
        draw_text("Ladrón", button_font, WHITE, screen, WIDTH // 2 + 125, HEIGHT // 2 - 25)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if police_button.collidepoint(event.pos):
                    return "Policía"
                if thief_button.collidepoint(event.pos):
                    return "Ladrón"

# Clase Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, role):
        super().__init__()
        if role == "Policía":
            self.image = pygame.image.load("policia.png")
        else:
            self.image = pygame.image.load("ladron.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.role = role
        self.vel_y = 0
        self.score = 0

    def update(self, keys):
        if self.role == "Policía":
            if keys[pygame.K_a]:
                self.rect.x -= 5
            if keys[pygame.K_d]:
                self.rect.x += 5
            if keys[pygame.K_w] and self.rect.bottom >= HEIGHT:
                self.vel_y = -15
        elif self.role == "Ladrón":
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if keys[pygame.K_UP] and self.rect.bottom >= HEIGHT:
                self.vel_y = -15

        self.vel_y += 1
        self.rect.y += self.vel_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

        self.rect.clamp_ip(screen.get_rect())

# Clase NPC
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, role):
        super().__init__()
        if role == "Policía":
            self.image = pygame.image.load("ladron.png")
        else:
            self.image = pygame.image.load("policia.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player_rect, role):
        if role == "Policía":
            self.rect.x += 3 if player_rect.x < self.rect.x else -3
        else:
            self.rect.x += -3 if player_rect.x < self.rect.x else 3
        self.rect.clamp_ip(screen.get_rect())

# Clase Moneda
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))

# --- Juego ---
start_action = show_start_screen()
if start_action != "start":
    pygame.quit()
    sys.exit()

role = show_role_selection_screen()
player = Player(50, HEIGHT - 60, role)
npc = NPC(600, HEIGHT - 60, role)

all_sprites = pygame.sprite.Group(player, npc)
coins = pygame.sprite.Group()

for _ in range(10):
    coin = Coin(random.randint(50, WIDTH - 50), HEIGHT - 30)
    all_sprites.add(coin)
    coins.add(coin)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)
    npc.update(player.rect, role)

    if player.rect.colliderect(npc.rect):
        print("¡El policía atrapó al ladrón! Fin del juego.")
        running = False

    for coin in pygame.sprite.spritecollide(player, coins, dokill=True):
        player.score += 5

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(f"Puntos: {player.score}", button_font, BLACK, screen, 100, 30)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()


