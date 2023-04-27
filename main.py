from pygame import *
from random import randint
import pygame_menu

init()
font.init()

WIDTH, HEIGHT = 800, 800 #розміри вікна
FPS = 60 #кількість кадрів в секунду
lost = 0 #кількість пропущених нло
points = 0  #кількість збитих нло

min_e_speed = 3
max_e_speed = 5


# #музика
# mixer.init() #підключаємо модуль mixer для роботи з музикою
# mixer.music.load('space.ogg')  #завантажуємо музику
# mixer.music.set_volume(0.3) #гучність музики
# # mixer.music.play() #запускаємо фонову музику
# # mixer.music.stop() #зупинити фонову музику

window = display.set_mode((WIDTH, HEIGHT)) #створюємо вікно
display.set_caption("Зомбі-шутер") #назва вікна

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height):
        super().__init__()  #створюємо порожній спрайтІ
        #завантажуємо картинку і змінюємо її розмір на width х height
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()  #отримуємо прямокутну область розміру картинки
        self.rect.x = x  #задаємо початкові координати спрайту
        self.rect.y = y
        self.mask = mask.from_surface(self.image)

    def draw(self):
        #відрисовуємо у вікні картинку self.image в координатах self.rect
        window.blit(self.image, self.rect) 

class Player(GameSprite): #гравець
    def update(self):
        #рух гравця з клавіатури
        pressed = key.get_pressed() #список натиснутих кнопок
        if pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 3
        if pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += 3
    
    def fire(self):
        """постріл кулею"""
        new_bullet = Bullet(self.rect.centerx-5, self.rect.y)
        bullets.add(new_bullet)

class Enemy(GameSprite):
    def __init__(self, x, y, speed):
        super().__init__("alien.png", x, y, 80, 60)
        self.speed = speed

    def update(self):
        """рух ворога"""
        global lost, lost_text
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            lost += 1  # збільшуємо лічильник пропущених ворогів
            lost_text = font1.render("Пропущено: " + str(lost), True,(255,255,255))
            self.rect.x = randint(0, WIDTH - 80)
            self.rect.y = randint(-500, -150)
            self.speed = randint(3,6) # швидкість ворога

class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("lazer.png", x, y, 10, 20)
        self.speed = 4  

    def update(self):
        """рух кулі"""
        self.rect.y -= self.speed #рух кулі вгору
        if self.rect.y < -30: #якщо вийшла за верхню межу екрану
            self.kill() #знищуємо кулю

player = Player("spaceship.png", x=WIDTH/2-50, y=HEIGHT-200, width=100, height = 100)
bg = transform.scale(image.load("infinite_starts.jpg"), (WIDTH, HEIGHT))

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

font1 = font.SysFont("Arial", 25)  #завантажуємо шрифт
lost_text = font1.render("Пропущено: " + str(lost), True,(255,255,255))
points_text =font1.render("Рахунок: " + str(points),True,(255,255,255))

font2 = font.SysFont("Arial", 50)
result_text = font2.render("ПРОГРАШ!",True,(250, 167, 12))
restart_text = font2.render("МЕНЮ",True,(250, 167, 12))

run = True
finish = True
clock = time.Clock() #cтворили таймер


while run: #поки гра запущена
    for e in event.get(): #перевіряємо всі події
        if e.type == QUIT: #якщо натиснуто закрити вікно
            run = False  # зупиняємо гру

    if not finish:
        window.blit(bg, (0,0))
      
        player.draw()
        player.update()
        
    display.update() #оновлюємо екран 
    clock.tick(FPS) #задаємо FPS



