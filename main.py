import pygame
import random

pygame.init()

FPS = 60
clock = pygame.time.Clock()
window_width, window_height = 400, 800

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space Shooter')

background = pygame.image.load('galaxy.png')
background = pygame.transform.scale(background, (window_width, window_height))

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.hitbox = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.hitbox.x, self.hitbox.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        
    def move(self, a, d):
        keys = pygame.key.get_pressed()
        if keys[a]:
            self.hitbox.x -= self.speed
        if keys[d]:
            self.hitbox.x += self.speed

        self.hitbox.x = max(0, min(self.hitbox.x, window_width - self.hitbox.width))
        self.hitbox.y = max(0, min(self.hitbox.y, window_height - self.hitbox.height))

    def fire(self):
        bullets.append(Bullet((self.hitbox.centerx - 10), self.hitbox.y, 20, 20, bullet_img, 15))
        fire_sfx = pygame.mixer.Sound('fire.ogg')
        fire_sfx.set_volume(0.3)
        fire_sfx.play()

class UFO(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        
    def move(self):
        self.hitbox.y += self.speed
        if self.hitbox.y > 800:
            rx = random.randint(0, 330)
            ry = random.randint(-250, -50)
            rs = random.randint(2, 4)
            self.hitbox.x = rx
            self.hitbox.y = ry
            self.speed = rs

class Asteroid(Sprite):
    def __init__(self, x, y, w, h, image, speed, skew):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.skew = skew
        
    def move(self):
        self.hitbox.y += self.speed
        if self.hitbox.y >= -50:
            self.hitbox.x += self.skew

        if self.hitbox.y > 800:
            rx = random.randint(-100, 350)
            ry = random.randint(-12000, -3000)
            rs = random.randint(10, 15)
            rwh = random.randint(50, 200)
            rsw = random.randint(-3, 3)
            self.hitbox.x = rx
            self.hitbox.y = ry
            self.speed = rs
            self.skew = rsw
            self.hitbox.w = rwh
            self.hitbox.h = rwh

            self.image = pygame.transform.scale(asteroid_img, (rwh, rwh))

class Bullet(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        
    def move(self):
        self.hitbox.y -= self.speed
        if self.hitbox.y <= 0:
            self.stop()

    def stop(self):
        if self in bullets:
            bullets.remove(self)

player_img = pygame.image.load('rocket.png')
ufo_img = pygame.image.load('ufo.png')
asteroid_img = pygame.image.load('asteroid.png')
bullet_img = pygame.image.load('bullet.png')

font = pygame.font.SysFont('Arial', 90, True)
small_font = pygame.font.SysFont('Arial', 50, True)
lose = font.render('skill issue', True, (255, 0, 0))
win = font.render('let him cook', True, (0, 255, 0))
replay = small_font.render('press space to play again', True, (0, 0, 0))

game = True

pygame.mixer.music.load('space.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

player = Player(170, 700, 60, 120, player_img, 3)

aliens = []
for i in range(7):
    rx = random.randint(0, 330)
    ry = random.randint(-600, -200)
    rs = random.randint(2, 4)
    aliens.append(UFO(rx, ry, 70, 53, ufo_img, rs))

bullets = []

asteroid = Asteroid(0, 801, 150, 150, asteroid_img, 1, 1)

finish = False
win_state = False

while game:
    window.blit(background, (0, 0))

    if not finish:
        player.move(pygame.K_a, pygame.K_d)
        player.draw()
        asteroid.move()
        asteroid.draw()
        for alien in aliens:
            alien.move()
            alien.draw()

            for bullet in bullets:
                if alien.hitbox.colliderect(bullet.hitbox):
                    alien.hitbox.x = 801
                    bullet.stop()
                    hit_sfx = pygame.mixer.Sound('hit.ogg')
                    hit_sfx.set_volume(0.3)
                    hit_sfx.play()
            
            if alien.hitbox.colliderect(asteroid.hitbox) and alien.hitbox.y >= 0:
                alien.hitbox.x = 801
                if asteroid.speed - 1 > 1:
                    asteroid.speed -= 1
                if asteroid.speed == 5:
                    if asteroid.skew > 0:
                        asteroid.skew -= 1
                    elif asteroid.skew < 0:
                        asteroid.skew += 1

                hit_sfx = pygame.mixer.Sound('hit.ogg')
                hit_sfx.set_volume(0.6)
                hit_sfx.play()

        for bullet in bullets:
            bullet.move()
            bullet.draw()

    else:
        if win_state:
            window.blit(win, (100, 140))
        else:
            window.blit(lose, (140, 140))
        window.blit(replay, (40, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            player.fire()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
            player = Player(170, 700, 60, 120, player_img, 3)
            finish = False

    pygame.display.update()
    clock.tick(FPS)