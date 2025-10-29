from pygame import *
from random import *

WIDTH = 900
HEIGHT = 600
CENTER_X = WIDTH//2
CENTER_Y = HEIGHT//2 



window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("space shoot")
FPS = 60
 
bg = image.load("pictures/infinite_starts.jpg")
bg = transform.scale(bg, (WIDTH, HEIGHT))
run = True

class BaseSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, speed, width, height):
        super().__init__()

        self.image = transform.scale(image.load(sprite_image), (width, height) )
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(BaseSprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__( sprite_image, x, y, speed, width=100 , height=100 )

        self.score = 0
        self.hp = 100
        self.invulnerability_timer = time.get_ticks()
        self.fire_timer = time.get_ticks()

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.speed 
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


    def fire(self):
        now = time.get_ticks()
        if now - self.fire_timer >= 250:
            fire = Shoot("pictures/fire.png", self.rect.centerx, self.rect.top - 40, 3)
            fires.add(fire)
            self.fire_timer = time.get_ticks()
        
    def take_damage(self):
        now = time.get_ticks()
        if now - self.invulnerability_timer >= 2000:
            self.hp -= 20
            print(self.hp)
            self.invulnerability_timer = time.get_ticks()


            

class Enemy(BaseSprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__(sprite_image, x, y, speed, width=80 , height=60)

        self.hp = randint(15, 25) 
        self.dir = choice(["L","R"])
        self.invulnerability_timer = time.get_ticks()

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.respawn()
        if self.rect.x >= WIDTH:
            self.dir = "L"
        if self.rect.x <= 0:
            self.dir = "R"
        if self.dir == "L":
            self.rect.x -= self.speed
        if self.dir == "R":
            self.rect.x += self.speed
        
    def respawn(self):
            self.rect.y = randint(-600, 0)
            self.rect.x = randint(0, WIDTH)
            self.dir = choice(["L","R"])
            self.speed = randint(1,2)
            self.hp = randint(15, 25)
        

    def take_damage(self):
        now = time.get_ticks()
        if now - self.invulnerability_timer >= 200:
            self.hp -= 5
            if self.hp <= 0:
                self.respawn()
            self.invulnerability_timer = time.get_ticks()


        
class Shoot(BaseSprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__(sprite_image, x, y, speed, width=30 , height=40)
    
    def update(self):
        self.rect.y -= self.speed
  
    




spaceship = Player("pictures/spaceship.png", CENTER_X, CENTER_Y + 150, 4)
aliens = sprite.Group()
fires = sprite.Group()
for i in range(5):
    numx = randint(0,WIDTH)
    numy = randint(-HEIGHT,-50)

    alien1 = Enemy("pictures/alien.png",numx, numy, randint(1,2))
    aliens.add(alien1)


while run:
    window.blit(bg, (0, 0))
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                spaceship.fire()
        if e.type == QUIT:
            run = False
        
    spaceship.draw(window)
    spaceship.update()
    aliens.draw(window)
    aliens.update()
    fires.draw(window)
    fires.update()
    sprite_list = sprite.spritecollide(spaceship, aliens, False)
    if len(sprite_list) > 0:
        spaceship.take_damage()
        if spaceship.hp <= 0:
            run = False

    alien_list = sprite.groupcollide(aliens, fires, False, True)
    for alien in alien_list:
        alien.take_damage()






    display.update()
    clock.tick(FPS)

