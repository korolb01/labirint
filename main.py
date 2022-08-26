from pygame import*

window = display.set_mode((1600,900),FULLSCREEN)
object_fon=transform.scale(image.load('img.png'),(1600,900))
object_win=transform.scale(image.load('victory.png'),(1280,720))
object_lose=transform.scale(image.load('lose.jpg'),(1280,720))
mixer.init()
sound_win=mixer.Sound('sound win.mp3')
sound_win.set_volume(0.2)
sound_lose=mixer.Sound('sound lose.mp3')
sound_lose.set_volume(0.2)

class Sprite(sprite.Sprite):
    def __init__(self,pictures_name,width,height,x,y):
        super().__init__()
        self.image=transform.scale(image.load(pictures_name),(width,height))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.direction='right'
    def me_pers(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class bullet(Sprite):
    def update(self):
        self.rect.x += 15
        if self.rect.x >= 1593:
            self.kill()

class Player(Sprite):
    def hod(self):
        all_knopks=key.get_pressed()
        if all_knopks[K_w] and self.rect.y>=0:
            self.rect.y-=10
            if sprite.spritecollide(self,stens,False):
                self.rect.y+=10
        if all_knopks[K_a] and self.rect.x>=0:
            self.rect.x -= 10
            if sprite.spritecollide(self,stens,False):
                self.rect.x+=10
        if all_knopks[K_s] and self.rect.y<=750:
            self.rect.y+=10
            if sprite.spritecollide(self,stens,False):
                self.rect.y-=10
        if all_knopks[K_d] and self.rect.x<=1450:
            self.rect.x+=10
            if sprite.spritecollide(self,stens,False):
                self.rect.x-=10
    def gun(self):
        global bullets
        new_bullet=bullet('patron.png',60,13,self.rect.right,self.rect.centery)
        bullets.add(new_bullet)

class bot(Sprite):
    def automove(self):
        if self.rect.x>=1450 and self.direction=='right':
            self.image=transform.flip(self.image, True, False)
            self.direction='left'
        if self.rect.x<=850 and self.direction=='left':
            self.image=transform.flip(self.image, True, False)
            self.direction='right'
        if self.direction=='right':
            self.rect.x+=8
        else:
            self.rect.x-=8

health_bot=3
stens=sprite.Group()
enemy_is_life=True
bullets=sprite.Group()
object_sten2=Sprite('stena_gor.png',550,100,230,450)
object_sten1=Sprite('stena_vert.png',100,800,760,200)
object_chest=Sprite('chest.png',130,130,1350,700)
object_bot=bot('bot.png',150,150,850,400)
object_me=Player('me.png',150,150,40,400)
stens.add(object_sten2,object_sten1)
game = True
finish=False
clock = time.Clock()
win=True

while game:
    for ivent in event.get():
        if ivent.type == QUIT:
            game = False
        if ivent.type == KEYDOWN:
            if ivent.key == K_ESCAPE:
                    game = False
        if ivent.type == MOUSEBUTTONDOWN and ivent.button == 1:
            object_me.gun()
    window.blit(object_fon,(0,0))
    if finish == False:
        object_me.me_pers()
        object_me.hod()
        if sprite.collide_rect(object_me,object_chest):
            finish=True
            win=True
            sound_win.play()
        if enemy_is_life==True:
            object_bot.me_pers()
            object_bot.automove()
            if sprite.collide_rect(object_me,object_bot):
                finish=True
                win=False
                sound_lose.play()
            if sprite.spritecollide(object_bot,bullets,dokill=True):
                if health_bot<=1:
                    enemy_is_life=False
                else:
                    health_bot-=1
        object_chest.me_pers()
        stens.draw(window)
        sprite.groupcollide(bullets,stens,True,False)
        bullets.draw(window)
        bullets.update()
    else:
        if win==True:
            window.blit(object_win,(160,90))
        if win==False:
            window.blit(object_lose,(160,90))

    display.update()
    clock.tick(60)