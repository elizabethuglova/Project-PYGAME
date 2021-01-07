import pygame
from random import randint
import os
import sys

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1500)

size = w, h = 300, 500
screen = pygame.display.set_mode(size)
screen.fill((135, 206, 250))
pygame.display.set_caption('Поймай еду')
pygame.display.set_icon(pygame.image.load('data/korzina.png'))

running = True
move_left = False
move_right = False

clock = pygame.time.Clock()
FPS = 60

#  загрузка скатерти
fullname1 = os.path.join('data', 'skatert.jpg')
if not os.path.isfile(fullname1):
    print(f"Файл с изображением '{fullname1}' не найден")
    sys.exit()
image1 = pygame.image.load(fullname1)

#  загрузка корзины
x1 = 100
y1 = 50
fullname = os.path.join('data', 'korzina.png')
if not os.path.isfile(fullname):
    print(f"Файл с изображением '{fullname}' не найден")
    sys.exit()
image = pygame.image.load(fullname).convert_alpha()
image2 = pygame.transform.scale(image, (x1, y1))

#  спрайты еда
class Food(pygame.sprite.Sprite):
    def __init__(self, x, speed, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()


food_images = ['apple.png', 'burger.png', 'cookies.png', 'orange.png',
               'pizza.png', 'sushi.png',
               'boot.png', 'disk.png', 'toy.png']

food_surf1 = [pygame.image.load('data/' + i).convert_alpha() for i in food_images]

food_surf = [pygame.transform.scale(image, (40, 40)) for image in food_surf1]

food = pygame.sprite.Group()


def createFood(group):
    index = randint(0, len(food_surf) - 1)
    x = randint(20, w - 20)
    speed = randint(1, 3)
    return Food(x, speed, food_surf[index], group)


createFood(food)

#  основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createFood(food)

    #  отрисовка кадра
    screen.fill((135, 206, 250))
    screen.blit(image1, (0, 400))
    screen.blit(image2, (x1, 355))
    food.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

    food.update(h)
