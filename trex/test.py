import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước cửa sổ
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("T-Rex Game")

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)

# T-Rex
trex_size = 50
trex_x = 50
trex_y = height - trex_size - 10
trex_speed = 5

# Cactus
cactus_size = 20
cactus_speed = 5
cactus_frequency = 25
cacti = []

# Clock
clock = pygame.time.Clock()

# Điểm số
score = 0
font = pygame.font.SysFont(None, 30)

def draw_trex(x, y):
    pygame.draw.rect(screen, white, [x, y, trex_size, trex_size])

def draw_cactus(x, y):
    pygame.draw.rect(screen, white, [x, y, cactus_size, cactus_size])

def display_score(score):
    score_display = font.render("Score: " + str(score), True, white)
    screen.blit(score_display, (10, 10))

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and trex_y == height - trex_size - 10:
        trex_y -= 100

    trex_y += 5  # Gravitational pull

    screen.fill(black)

    # Generate cactus
    if random.randint(1, cactus_frequency) == 1:
        cacti.append([width, height - cactus_size - 10])

    # Move and draw cacti
    for cactus in cacti:
        cactus[0] -= cactus_speed
        draw_cactus(cactus[0], cactus[1])

    # Move and draw T-Rex
    draw_trex(trex_x, trex_y)

    # Check for collisions
    for cactus in cacti:
        if trex_x < cactus[0] < trex_x + trex_size and trex_y + trex_size > cactus[1]:
            pygame.quit()
            sys.exit()

    # Remove cacti that are off-screen
    cacti = [cactus for cactus in cacti if cactus[0] > 0]

    # Update score
    score += 1

    # Display score
    display_score(score)

    pygame.display.flip()
    clock.tick(30)
