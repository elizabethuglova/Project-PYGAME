import pygame
import os
import sys

if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 500
    screen = pygame.display.set_mode(size)
    screen.fill((135, 206, 250))
    pygame.display.set_caption('Поймай еду')
    running = True
    move_left = False
    move_right = False


    # загрузка скатерти
    fullname1 = os.path.join('data', 'skatert.jpg')
    if not os.path.isfile(fullname1):
        print(f"Файл с изображением '{fullname1}' не найден")
        sys.exit()
    image2 = pygame.image.load(fullname1)


    # загрузка корзины
    x = 100  # начальная позиция корзины
    y = 50  # начальная позиция корзины
    fullname = os.path.join('data', 'korzina.png')
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image1 = pygame.transform.scale(image, (x, y))


    # основной цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # завершение игры
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    running = False
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
        if move_left:
            x -= 0.05
            if x < 0:
                x = 0
        if move_right:
            x += 0.05
            if x > width - 100:
                x = width - 100

        #  обновление экрана

        screen.fill((135, 206, 250))
        screen.blit(image2, (0, 400))
        screen.blit(image1, (x, 355))
        pygame.display.flip()


    pygame.quit()