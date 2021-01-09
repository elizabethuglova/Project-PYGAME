import pygame
from random import randint
import os
import sys
import pygame_menu

pygame.init()

size = w, h = 300, 500
screen = pygame.display.set_mode(size)

speed_food = 1
speed_korzina = 7
life = 3
score = 0


def start_the_game():
    screen.fill((135, 206, 250))  # основного игрового окна

    pygame.display.set_caption('Поймай еду')
    pygame.display.set_icon(pygame.image.load('data/korzina.png'))

    pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3 секунды - время, через которое начинает падать новый объект
    running = True

    clock = pygame.time.Clock()
    FPS = 60

    #  загрузка скатерти
    fullname1 = os.path.join('data', 'skatert.jpg')
    if not os.path.isfile(fullname1):
        print(f"Файл с изображением '{fullname1}' не найден")
        sys.exit()
    skatert = pygame.image.load(fullname1)

    #  загрузка фона для подсчета жизней
    fullname2 = os.path.join('data', 'life_fon.png')
    if not os.path.isfile(fullname2):
        print(f"Файл с изображением '{fullname2}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname2)
    life_fon = pygame.transform.scale(image2, (50, 50))
    life_font = pygame.font.SysFont('arial', 25)

    #  загрузка фона для подсчета очков
    fullname3 = os.path.join('data', 'score_fon.png')
    if not os.path.isfile(fullname3):
        print(f"Файл с изображением '{fullname3}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname3)
    score_fon = pygame.transform.scale(image2, (90, 40))
    score_font = pygame.font.SysFont('arial', 25)

    #  загрузка корзины
    fullname4 = os.path.join('data', 'korzina.png')
    if not os.path.isfile(fullname4):
        print(f"Файл с изображением '{fullname4}' не найден")
        sys.exit()
    image = pygame.image.load(fullname4)
    korzina = pygame.transform.scale(image, (100, 50))
    korzina_rect = korzina.get_rect(centerx=w // 2, bottom=h - 95)

    #  спрайты еда
    class Food(pygame.sprite.Sprite):
        def __init__(self, x, speed, surf, life, score, group):
            pygame.sprite.Sprite.__init__(self)
            self.image = surf
            self.rect = self.image.get_rect(center=(x, 0))
            self.life = life
            self.score = score
            self.speed = speed
            self.add(group)

        def update(self, *args):
            if self.rect.y < args[0] - 20:
                self.rect.y += self.speed
            else:
                self.kill()

    food_images = ['data/apple.png', 'data/avocado.png', 'data/burger.png', 'data/cookies.png', 'data/orange.png',
                   'data/pizza.png', 'data/sushi.png',
                   'data/boot.png', 'data/disk.png', 'data/phone.png', 'data/toy.png']  # изображения еды

    food_life = {'data/apple.png': 0, 'data/avocado.png': 0, 'data/burger.png': 0,
                 'data/cookies.png': 0, 'data/orange.png': 0,
                 'data/pizza.png': 0, 'data/sushi.png': 0,
                 'data/boot.png': 1, 'data/disk.png': 1,
                 'data/phone.png': 1, 'data/toy.png': 1}  # словарь со згачением количества жизни

    food_score = {'data/apple.png': 50, 'data/avocado.png': 50, 'data/burger.png': 50,
                  'data/cookies.png': 100, 'data/orange.png': 100,
                  'data/pizza.png': 200, 'data/sushi.png': 200,
                  'data/boot.png': 0, 'data/disk.png': 0,
                  'data/phone.png': 0, 'data/toy.png': 0}  # словрь со значением очков

    food_surf1 = [pygame.image.load(i).convert_alpha() for i in food_images]  # загрузка изображений еды

    food_surf = [pygame.transform.scale(image, (40, 40)) for image in food_surf1]  # преобразование изображений

    food = pygame.sprite.Group()

    def createFood(group):
        global speed_food
        index = randint(0, len(food_surf) - 1)
        x = randint(20, w - 20)
        speed_food += 0.08
        return Food(x, speed_food, food_surf[index], food_life[food_images[index]],
                    food_score[food_images[index]], group)

    createFood(food)

    def catchFood():  # проверка столкновения падающей еды и корзины; проверка съедобную ли еду поймала корзина
        global life
        global score
        for i in food:
            if korzina_rect.collidepoint(i.rect.center):
                life -= i.life
                score += i.score
                if life == 0:
                    sys.exit()
                i.kill()

    #  основной цикл игры
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.USEREVENT:
                createFood(food)

        # движение корзины с помощью клавиш стрелок
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            korzina_rect.x -= speed_korzina
            if korzina_rect.x < 0:
                korzina_rect.x = 0
        elif keys[pygame.K_RIGHT]:
            korzina_rect.x += speed_korzina
            if korzina_rect.x > w - korzina_rect.width:
                korzina_rect.x = w - korzina_rect.width

        # отрисовка нового кадра
        catchFood()
        screen.fill((135, 206, 250))

        screen.blit(life_fon, (0, 0))
        text1 = life_font.render(str(life), 1, (0, 0, 0))
        screen.blit(text1, (19, 11))

        screen.blit(score_fon, (210, 5))
        text2 = score_font.render(str(score), 1, (0, 0, 0))
        screen.blit(text2, (235, 11))

        screen.blit(skatert, (0, 400))
        food.draw(screen)
        screen.blit(korzina, korzina_rect)

        pygame.display.flip()

        clock.tick(FPS)

        food.update(h)


# меню заставки игры
menu = pygame_menu.Menu(500, 300, 'Welcom', theme=pygame_menu.themes.THEME_GREEN)

menu.add_button('Играть', start_the_game)
menu.add_button('Выход', pygame_menu.events.EXIT)

menu.mainloop(screen)
