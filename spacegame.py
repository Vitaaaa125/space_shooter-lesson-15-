from pygame import *
from random import *

WIDTH = 900
HEIGHT = 600
CENTER_X = WIDTH//2
CENTER_Y = HEIGHT//2 

font.init()
font1 = font.Font('RubikGlitch-Regular.ttf', 30)
font2 = font.Font('RubikGlitch-Regular.ttf', 500)


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
        self.hp_text = font1.render(f"Player HP: {self.hp}", True, (90, 3, 252))
        self.score_text = font1.render(f"Player score: {self.score}", True, (90, 3, 252))

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
            self.hp_text = font1.render(f"Player HP: {self.hp}", True, (90, 3, 252))
            self.invulnerability_timer = time.get_ticks()


            

class Enemy(BaseSprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__(sprite_image, x, y, speed, width=80 , height=60)

        self.hp = randint(15, 25) 
        self.dir = choice(["L","R"])
        self.invulnerability_timer = time.get_ticks()
        self.damage_time = 200 
        self.damage_lvl = 0


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
            if self.speed <= 2.5:
                self.speed = self.speed + 0.05
            self.hp = randint(15, 25)
        

    def take_damage(self):
        now = time.get_ticks()
        is_kill = False
        if now - self.invulnerability_timer >= self.damage_time:
            self.hp -= 5
            if self.hp <= 0:
                is_kill = True
                if self.damage_time < 20:
                    self.damage_lvl += 20
                    self.damage_time = self.damage_time - self.damage_lvl
                self.respawn()

            self.invulnerability_timer = time.get_ticks()
            return True, is_kill 
        else:
            return False, is_kill 

       
class Shoot(BaseSprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__(sprite_image, x, y, speed, width=30 , height=40)
    
    def update(self):
        self.rect.y -= self.speed
  
    
spaceship = Player("pictures/spaceship.png", CENTER_X, CENTER_Y + 150, 4)
finish_text = font1.render("GAME OVER!", True, (90, 3, 252))
restart_text = font1.render(f"press R to restart game:", True, (90, 3, 252))
restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 200))
finish_rect = finish_text.get_rect(center=(WIDTH/2, HEIGHT/2))
aliens = sprite.Group()
fires = sprite.Group()
for i in range(5):
    numx = randint(0,WIDTH)
    numy = randint(-HEIGHT,-50)

    alien1 = Enemy("pictures/alien.png",numx, numy, randint(1,2))
    aliens.add(alien1)

is_finished = False 

while run:
    window.blit(bg, (0, 0))
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                spaceship.fire()
            if e.key == K_r and is_finished == True:
                spaceship = Player("pictures/spaceship.png", CENTER_X, CENTER_Y + 150, 4)
                for alien in aliens:
                    alien.respawn()
                is_finished = False
        if e.type == QUIT:
            is_finished = True 
            run = False
    
    if not is_finished:
    
        spaceship.update()
        aliens.update()
        fires.update()

        sprite_list = sprite.spritecollide(spaceship, aliens, False)
        if len(sprite_list) > 0:
            spaceship.take_damage()
            if spaceship.hp <= 0:
                is_finished = True


        alien_list = sprite.groupcollide(aliens, fires, False, True)
        for alien in alien_list:
            is_shoot, is_kill = alien.take_damage()
            if is_shoot == True:
                if is_kill == False:
                    spaceship.score += 5
                else:
                    spaceship.score += 30

                spaceship.score_text = font1.render(f"Player score: {spaceship.score}", True, (90, 3, 252))

 
    window.blit(spaceship.hp_text,(15, HEIGHT - 40))
    window.blit(spaceship.score_text,(15, 20))
    spaceship.draw(window)
    aliens.draw(window)
    fires.draw(window)
    if is_finished == True:
        window.blit(finish_text,finish_rect)
        window.blit(restart_text,restart_rect)

    display.update()
    clock.tick(FPS)

