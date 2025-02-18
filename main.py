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

menu = pygame.image.load('menu.png')
menu = pygame.transform.scale(menu, (window_width, window_height))

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
        fire_sfx.set_volume(0.1)
        fire_sfx.play()

class UFO(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        
    def move(self):
        self.hitbox.y += self.speed
        if self.hitbox.y > 800:
            global points_lost
            global points_lost_lb
            rx = random.randint(0, 330)
            ry = random.randint(-250, -50)
            rs = random.randint(2, 4)
            self.hitbox.x = rx
            self.hitbox.y = ry
            self.speed = rs
            points_lost += 1
            points_lost_lb = font.render(f'UFOs missed: {points_lost}', True, (255, 255, 255))

    def kill(self):
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
start_btn_img = pygame.image.load('start_btn.png')

game = True

pygame.mixer.music.load('menu.ogg')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

button = Sprite(100, 325, 200, 75, start_btn_img)

player = Player(170, 700, 60, 120, player_img, 3)

aliens = []
for i in range(7):
    rx = random.randint(0, 330)
    ry = random.randint(-600, -200)
    rs = random.randint(2, 4)
    aliens.append(UFO(rx, ry, 70, 53, ufo_img, rs))

bullets = []

asteroid = Asteroid(0, 801, 150, 150, asteroid_img, 1, 1)

font = pygame.font.SysFont('Midnight Letters', 25)
big_font = pygame.font.SysFont('Midnight Letters', 50)
massive_font = pygame.font.SysFont('Midnight Letters', 70) # and you know what else is massive?

points = 0
points_lost = 0

points_lb = font.render(f'UFOs shot down: {points}', True, (255, 255, 255))
points_lost_lb = font.render(f'UFOs missed: {points_lost}', True, (255, 255, 255))
pause_lb = massive_font.render('Pause', True, (255, 255, 255))
menu_btn_lb = font.render('press space to go to menu', True, (255, 255, 255))

lose = big_font.render('skill issue', True, (255, 0, 0))
win = big_font.render('let him cook', True, (0, 255, 0))

finish = False
win_state = False
start = False
pause = False

i = 0
i1 = 0
i2 = 0

def pause_game():
    global pause
    if not pause:
        pause = True
    else:
        pause = False

def return_to_menu():
    global start, finish, points, points_lost, points_lb, points_lost_lb, i, i1, i2, pause
    start = False
    finish = False
    pause = False
    points_lost = 0
    points_lb = font.render('UFOs shot down: 0', True, (255, 255, 255))
    points_lost_lb = font.render(f'UFOs missed: {points_lost}', True, (255, 255, 255))
    pygame.mixer.music.load('menu.ogg')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)
    i = 0
    i1 = 0
    i2 = 0

while game:
    if not start:
        window.blit(menu, (0, 0))
        if i1 == 0:
            with open('high_score.txt', 'r') as file:
                try:
                    old_score = int(file.read())
                except:
                    old_score = 0

                high_lb = font.render(f'High score: {old_score}', True, (255, 255, 255))
                new_rec_lb = font.render('', True, (255, 255, 255))
                if int(points) > old_score:
                    with open('high_score.txt', 'w') as file:
                        score = points
                        file.write(str(score))
                    high_lb = font.render(f'High score: {score}', True, (255, 255, 255))
                    new_rec_lb = font.render('New record!', True, (255, 255, 255))
            i1 = 1

        window.blit(high_lb, (0, 0))
        window.blit(new_rec_lb, (0, 30))
        button.draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = True
            if event.type == pygame.QUIT:
                game = False

    if start:
        i1 = 0
        if i != 1:
            pygame.mixer.music.load('space.wav')
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.2)

            player.hitbox.x, player.hitbox.y = 170, 700
            for alien in aliens:
                alien.hitbox.x, alien.hitbox.y = 0, 0
                alien.kill()
            asteroid.hitbox.x, asteroid.hitbox.y = 0, 801

            bullets = []

            points = 0

            i = 1
    
        window.blit(background, (0, 0))
        window.blit(points_lb, (1, 0))
        window.blit(points_lost_lb, (1, 26))

        if not finish:
            if not pause:
                player.move(pygame.K_a, pygame.K_d)
                asteroid.move()
            player.draw()
            asteroid.draw()
            for alien in aliens:
                if not pause:
                    alien.move()
                alien.draw()

                for bullet in bullets:
                    if alien.hitbox.colliderect(bullet.hitbox):
                        alien.kill()
                        bullet.stop()
                        hit_sfx = pygame.mixer.Sound('hit.ogg')
                        hit_sfx.set_volume(0.1)
                        hit_sfx.play()
                        points += 1
                        points_lb = font.render(f'UFOs shot down: {points}', True, (255, 255, 255))
                                    
                if alien.hitbox.colliderect(asteroid.hitbox) and alien.hitbox.y >= 0:
                    alien.kill()
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
  
                if player.hitbox.colliderect(asteroid.hitbox) or player.hitbox.colliderect(alien.hitbox) or points_lost >= 10:
                    finish = True
                    win_state = False

            for bullet in bullets:
                if not pause:
                    bullet.move()
                bullet.draw()

            if pause:
                window.blit(pause_lb, (85, 325))
                window.blit(menu_btn_lb, (20, 425))

        else:
            if win_state:
                window.blit(win, (35, 350))
            else:
                window.blit(lose, (50, 350))
            window.blit(menu_btn_lb, (20, 450))

            pygame.mixer.music.stop()
            
            if i2 == 0:
                hit_sfx = pygame.mixer.Sound('hit.ogg')
                hit_sfx.set_volume(0.6)
                hit_sfx.play()
                i2 = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and not pause and not finish:
                player.fire()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
                return_to_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game()
            if event.type == pygame.KEYDOWN and pause and event.key == pygame.K_SPACE:
                return_to_menu()

    pygame.display.update()
    clock.tick(FPS)