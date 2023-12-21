import os
import sys
import pygame
import random
from pygame import *

pygame.font.init()
font = pygame.font.Font(None, 20)
pygame.init()

scr_size = (width, height) = (600, 150)
FPS = 60
gravity = 0.6
score = 0
black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()     
pygame.display.set_caption("T-Rex Rush")

def load_image(name, sizex=-1, sizey=-1, colorkey=None):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))
    return image, image.get_rect()

def load_sprite_sheet(sheetname, nx, ny, scalex=-1, scaley=-1, colorkey=None):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    sprites = []
    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny
    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))
            sprites.append(image)
    sprite_rect = sprites[0].get_rect()
    return sprites, sprite_rect

class Dino():
    def __init__(self, sizex=-1, sizey=-1):
        self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width / 15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width


    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98 * height):
            self.rect.bottom = int(0.98 * height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:
            self.index = 4


        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1

        self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1 * speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

def gameplay():
    gamespeed = 4
    gameOver = False
    playerDino = Dino(44, 47)
    cacti = pygame.sprite.Group()

    Cactus.containers = cacti

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if playerDino.rect.bottom == int(0.98 * height):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.jumpSpeed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    playerDino.isDucking = False

        for c in cacti:
            c.movement[0] = -1 * gamespeed
            if pygame.sprite.collide_mask(playerDino, c):
                playerDino.isDead = True

        if len(cacti) < 2:
            if len(cacti) == 0:
                Cactus(gamespeed, 40, 40)
            else:
                for l in cacti:
                    if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                        Cactus(gamespeed, 40, 40)
        playerDino.update()
        cacti.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            cacti.draw(screen)
            playerDino.draw()

            pygame.display.update()

        clock.tick(FPS)

        if playerDino.isDead:
            gameOver = True

    pygame.quit()
    quit()

def main():
    gameplay()

main()
   