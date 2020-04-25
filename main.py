import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create a window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")  # .convert() can be used without increasing enemy & ship speed

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load('spaceship.png')
PlayerX = 360
PlayerY = 480
PlayerX_change = 0
PlayerY_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 10

# Score
score_value = 0
font = pygame.font.Font('Game_font.ttf', 32)
textX = 10
textY = 10

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('enemy1.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(0, 150))
    EnemyX_change.append(6)
    EnemyY_change.append(40)

# Bullet
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 0
BulletX_change = 0
BulletY_change = 13
Bullet_state = 'ready'

# Game Over Text
over_font = pygame.font.Font('Game_font.ttf', 64)
overX = 216
overY = 236

def game_over(x,y):
    over = over_font.render('Game Over', True, (255, 255, 255))
    screen.blit(over, (x, y))


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # blit is used to draw on screen
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    # blit is used to draw on screen
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = 'fire'
    screen.blit(BulletImg, (x + 30, y + 10))


def isCollision(EnemyX, EnemyY, PlayerX, PlayerY):
    distance = math.hypot(EnemyX - BulletX, EnemyY - BulletY)
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB (Red,Green,Blue) fill is used to fill the screen
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # key movement of spaceship
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -7
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 7
            if event.key == pygame.K_UP:
                PlayerY_change = -7
            if event.key == pygame.K_DOWN:
                PlayerY_change = 7
            if event.key == pygame.K_SPACE:
                if Bullet_state is 'ready':

                    BulletX = PlayerX
                    BulletY = PlayerY
                    fire_bullet(BulletX, BulletY)
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                PlayerY_change = 0
            if event.key == pygame.K_SPACE:
                pass

    PlayerX += PlayerX_change
    PlayerY += PlayerY_change

    EnemyX += EnemyX_change

    # Boundary Condition
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    if PlayerY <= 0:
        PlayerY = 0
    elif PlayerY >= 536:
        PlayerY = 536
    for i in range(num_of_enemies):

        if EnemyY[i] > 440 or math.hypot(EnemyX[i] - PlayerX, EnemyY[i] - PlayerY)<27:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over(overX, overY)
            break
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 5
            EnemyY[i] += EnemyY_change[i]
        if EnemyX[i] >= 736:
            EnemyX_change[i] = -5
            EnemyY[i] += EnemyY_change[i]

        # collision
        collision = isCollision(EnemyX[i], EnemyY[i], PlayerX, PlayerY)

        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            score_value += 1
            BulletY = PlayerY
            Bullet_state = 'ready'
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(0, 150)
        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if BulletY < 0:
        Bullet_state = 'ready'
    if Bullet_state is 'fire':
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()  # update is to update everything on display as it is needed in every  pygame program
