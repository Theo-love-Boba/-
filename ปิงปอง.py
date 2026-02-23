from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 40)
player1win = font1.render("PLAYER ONE WIN !!!", True, (255, 255, 255))
player2win = font1.render("PLAYERTWO WIN !!!", True, (180,0,0))

font2 = font.SysFont('Arial',36)
score = 0
goal = 10
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, speed, up=K_UP, down=K_DOWN, left=K_LEFT, right=K_RIGHT):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.speed_y = speed
        self.speed_x = speed

    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class  Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[self.up] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[self.down] and self.rect.y < 400:
            self.rect.y += self.speed

class Ball(GameSprite):
    def update(self):
        self.rect.y -= self.speed_y
        self.rect.x -= self.speed_x
        global lost

        if self.rect.y > 420:
            self.speed_y*=-1

        if self.rect.y < 20:
            self.speed_y*=-1

        if self.rect.x < 20:
            self.speed_x*=-1

        if self.rect.x > 550:
            self.speed_x*=-1    

win_width = 600
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Pingpong")

game = True
clock= time.Clock()
FPS = 60

finish = False

player1 = Player("racket.png", 5, 225, 50, 100, 10,up= K_w ,down= K_s)
player2 = Player("racket.png", 545, 225, 50, 100, 10,up= K_UP ,down= K_DOWN)
ball = Ball("tenis_ball.png", 300, 250, 50, 50, 5)

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.fill((144,213,255))

        if ball.rect.x > 560:
            finish = True
            window.blit(player2win, (150,220))

        if ball.rect.x < 40:
            finish = True
            window.blit(player1win, (150,220))

        if sprite.collide_rect(player1,ball):
            ball.speed_x*= -1

        if sprite.collide_rect(player2,ball):
            ball.speed_x*= -1

        player1.update()
        player1.draw()

        player2.update()
        player2.draw()

        ball.update()
        ball.draw()
        
    display.update()
    clock.tick(FPS)
