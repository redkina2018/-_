#Создай собственный Шутер!

from pygame import *
from random import* 
from time import time as timer
font.init()
num_fire = 0
rel_time = False
life = 3
font1 = font.Font(None, 36)
font2 = font.Font(None, 60)
win = display.set_mode((700,500))
lost = 0
score = 0
display.set_caption = ("СУПЕР КРУТОЙ ШУТЕР")
x_bg = 0
y_bg = 0
x_bg2 = 0
y_bg2 = -500
bg = transform.scale(image.load("galaxy.jpg"),(700,500))
sbg_2 = transform.scale(image.load("galaxy.jpg"),(700,500))
flag = True
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
text_noooob =  font2.render("ТЫ ПРАИГРАЛ",1,(255,0,0))
text_gooood =  font2.render("ТЫ ВЫЙГРАЛ",1,(255,0,0))
reset_bun =  font1.render("ПЕРЕЗАРЯДКА",1,(255,51,51))
finish = False
finish_good = False
class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,pl_y,pl_x,pl_speed,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(pl_image),(size_x,size_y))
        self.speed = pl_speed
        self.rect =self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
    def show_pl(self):
        win.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 1:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= 634:
            self.rect.x += self.speed

        if keys[K_LEFT] and self.rect.x >= 1:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= 634:
            self.rect.x += self.speed
    def fire(self):
        center_x = self.rect.centerx
        y_top = self.rect.top
        bul = Bullet("bullet.png",y_top,center_x,randint(5,15),15,15)
        bullets.add(bul)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(90,620)

class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(90,620)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


monsters = sprite.Group() 
bullets = sprite.Group()
metiors = sprite.Group()
for i in range(3):
    metior = Enemy1("asteroid.png",-70,randint(90,620),randint(int(0.2),3),65,50)
    metiors.add(metior)

for i in range(10):
    monster = Enemy("ufo.png",-70,randint(90,620),randint(int(0.2),3),65,50)
    monsters.add(monster)
pl = Player("rocket.png",420,350,5,65,65)
# en = Enemy("ufo.png",,420,0,,65,65 )  
while flag:
    for e in event.get():
        if e.type == QUIT:
            flag = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time == False:
                    num_fire+=1
                    fire.play()
                    pl.fire()
                    pl.fire()
                    pl.fire()
                if num_fire>=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



            if e.key == K_SPACE and finish == True or finish_good == True:
                finish = False
                finish_good == False
                score = 0
                lost = 0
                monsters.remove()

    if finish == False and finish_good ==  False:
        sprites_list = sprite.groupcollide(monsters,bullets, True, True)
        for sp in sprites_list:
            score+=1
            monster = Enemy("ufo.png",-70,randint(90,620),randint(int(0.2),10),65,50)
            monsters.add(monster)
        text_lose =  font1.render("Пропущено "+ str(lost),1,(50,32,165))
        text_score =  font1.render("Cчет: "+ str(score),1,(50,32,165))
        '''if y_bg <= 500:
            y_bg+=2
            win.blit(bg,(0,y_bg))
            win.blit(sbg_2,(0,y_bg2))
            y_bg2+=2
        else:
            y_bg = 0
            y_bg2 = -500'''
        
        win.blit(bg,(0,y_bg))

        pl.show_pl()
        pl.move()
        # monsters.update()
        # monsters.draw(win)
        metiors.update()
        metiors.draw(win)
        bullets.update()
        bullets.draw(win)
        win.blit(text_lose,(5,5))
        win.blit(text_score,(5,30))
        print(sprites_list)
        if rel_time:
            new_time = timer()
            if new_time-last_time < 3:
                win.blit(reset_bun,(250,400))
            if new_time-last_time >= 3:
                rel_time = False
                num_fire = 0
        if sprite.spritecollide(pl,monsters,False) or sprite.spritecollide(pl,metiors,False):
            life-=1
            sprite.spritecollide(pl,monsters,True)
            sprite.spritecollide(pl,metiors,True)
        if lost >= 5 or life == 0:
            finish = True
            win.blit(text_noooob,(200,250))
        if score >=15:
            finish_good = True
            win.blit(text_gooood,(200,250))






                    
    clock.tick(FPS)
    display.update()
