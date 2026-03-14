import pygame
from random import randint

class Sprite:
    def __init__(self, center, image):
        self.image = image
        self.rect = self.image.get_frect()
        self.rect.center = center
    def render(self, surface):
        surface.blit(self.image, self.rect)

class MoveSprite(Sprite):
    def __init__(self, center, image, speed, direction):
        super().__init__(center, image)

        self.speed = speed
        self.direction = direction.normalize()

    def update(self):
        vector = self.direction * self.speed
        self.rect.move_ip(vector)

WIN_SIZE = (800, 600)
MAX_FPS = 60

window = pygame.Window("Tower Defence", WIN_SIZE)

surface = window.get_surface()

clock = pygame.Clock()

image = pygame.Surface((50,50))
image.fill('white')
center = WIN_SIZE[0]/2 , WIN_SIZE[1]/2
player = Sprite(center, image)
bullets = []
enemies = []
score = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.WINDOWCLOSE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            image = pygame.Surface((6,4))
            image.fill('yellow')
            center = pygame.Vector2(player.rect.center)
            pos = pygame.Vector2(pygame.mouse.get_pos())
            direction =pos - center
            bullet = MoveSprite(center, image, 7, direction)
            bullets.append(bullet)


    if randint(0, 100) <= 3:

        image = pygame.Surface((50, 50))
        image.fill("green")
        center = pygame.Vector2(player.rect.center)

        r = randint(1, 4)
        if r == 1:
            pos = pygame.Vector2(randint(0, WIN_SIZE[0]), -100)
        elif r == 2:
            pos = pygame.Vector2(WIN_SIZE[0] + 100, randint(0, WIN_SIZE[1]))
        elif r == 3:
            pos = pygame.Vector2(randint(0, WIN_SIZE[0]), WIN_SIZE[1] + 100)
        elif r == 4:
            pos = pygame.Vector2(-100, randint(0, WIN_SIZE[1]))

        direction = center - pos
        enemy = MoveSprite(pos, image, randint(100, 400)/100, direction)
        enemies.append(enemy)

    for bullet in bullets:
        bullet.update()
    for enemy in enemies:
        enemy.update()

    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect.coliderect(enemy.rect):
                score += 1
                bullets.remove(bullet)
                enemies.remove(enemy)
                break
    for enemy in enemies:
        if player.rect.coliderect(enemy.rect):
            score = 0
            enemies.clear()
            bullets.clear()
            break 
           

    surface.fill("black")
    player.render(surface)
    for bullet in bullets:
        bullet.render(surface)
    for enemy in enemies:
        enemy.render(surface)
    window.flip()

    clock.tick(MAX_FPS)

