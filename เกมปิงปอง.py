from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE", True, (180,0,0))

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

    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class  Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[self.left] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[self.right] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Shoter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

ship = Player("rocket.png", 5, 400, 80, 100, 5)
for i in range (1,6):
    monster = Enemy("asteroid.png", randint(80, win_width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster)


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

game = True
clock= time.Clock()
FPS = 60

finish = False

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
    
    if finish != True:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()

        ship.draw()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("asteroid.png", randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,[200,200])

        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        text = font2.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text2 = font2.render("Missed: " + str(lost), 1, (255,255,255))
        window.blit(text2, (10,50))
        display.update()  
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
    
    display.update()
    clock.tick(FPS)
