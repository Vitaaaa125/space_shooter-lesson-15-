from pygame import *

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

class Player(sprite.Sprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__()

        self.image = transform.scale(image.load(sprite_image), (100, 100) )
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed
        self.score = 0
        self.hp = 100

    
    def draw(self, window):
        window.blit(self.image, self.rect)
    
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
    
spaceship = Player("pictures/spaceship.png", CENTER_X, CENTER_Y + 150, 4)

while run:
    window.blit(bg, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        
    spaceship.draw(window)
    spaceship.update()




    display.update()
    clock.tick(FPS)

