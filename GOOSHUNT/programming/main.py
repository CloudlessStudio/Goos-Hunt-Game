import pygame, sys, random
from pygame.locals import*

pygame.init()

#-------------------------------------custom crosshair--------------------------
crosshair = (       #16x16 cursor
"                ",
"                ",
"                ",
"        XX      ",
"        XX      ",
"        XX      ",
"                ",
"    XXX    XXX  ",
"    XXX    XXX  ",
"                ",
"        XX      ",
"        XX      ",
"        XX      ",
"                ",
"                ",
"                "
)

newCursor = pygame.cursors.compile(crosshair, black = "X", white = ".", xor="o")
pygame.mouse.set_cursor((16,16),(8,8), *newCursor)

#------------------------display and fps setup global vars----------------------

WIDTH = 800
HEIGHT =  600
speed = 2
RANDOM_X = random.randint(0,800)
Y = 500
direction = random.randint(1,3)
pos_check = 1
numDucks = 10
numFrames = 0
bullets = 13
score = 0
escaped =  0
hit = False
list_of_num = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13"]
window = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
pygame.display.set_caption("GOOS HUNT")
FPS = pygame.time.Clock()

#-------------------loading Sounds----------------------------------------------

hit_sound = pygame.mixer.Sound("Sounds\\Boom.wav")
duck_death = pygame.mixer.Sound("Sounds\\Death.wav")
new_round = pygame.mixer.Sound("Sounds\\newRound.wav")
miss_sound = pygame.mixer.Sound("Sounds\\Miss.wav")
select_sound = pygame.mixer.Sound("Sounds\\Select.wav")
gun_sound = pygame.mixer.Sound("Sounds\\Gun.wav")
music = pygame.mixer.music.load("Sounds\\menusong.wav")
lost = pygame.mixer.Sound("Sounds\\loseSound.wav")

#--------------------------------------fonts and text---------------------------

myfont = pygame.font.Font("bButtercreamChocolate.ttf", 40)
myscore = myfont.render("SCORE:", True, (235,210,52))
myducks = myfont.render("GOOS LEFT:", True, (235,210,52))
mybullets = myfont.render("BULLETS:", True,(235,210,52))
start_game = myfont.render("PRESS ENTER TO PLAY", True, (235,210,52))
restart_game = myfont.render("PRESS ENTER TO PLAY AGAIN", True, (235,210,52))
credits_konrad = myfont.render("Konrad Pawlikowski", True, (235,210,52))
credits_cliff = myfont.render("Cliff Moore", True, (235,210,52))
credits = myfont.render("MADE BY:", True,(235,210,52))

#---------------------------------------------Loading Image from path-----------

def image_load(name):

    image = pygame.image.load("Images\\"+name)
    return image

#--------------------------------ducks------------------------------------------

d1 = image_load("Duck1.png")          #--------up left--------------------------
d2 = image_load("Duck2.png")          #--------up left--------------------------

d3 = image_load("Duck3.png")          #--------up top---------------------------
d4 = image_load("Duck4.png")          #--------up top---------------------------

d5 = image_load("Duck7.png")          #--------up right-------------------------
d6 = image_load("Duck8.png")          #--------up right-------------------------

#-------------------------------title image-------------------------------------

gH = image_load("GoosHunt.png")

#--------------------------------explosion--------------------------------------

e0 = image_load("splatter0.png")
e0 = pygame.transform.scale(e0, (96,96))
e1 = image_load("splatter1.png")
e1 = pygame.transform.scale(e1, (96,96))
e2 = image_load("splatter2.png")
e2 = pygame.transform.scale(e2, (96,96))
e3 = image_load("splatter3.png")
e3 = pygame.transform.scale(e3, (96,96))
e4 = image_load("splatter4.png")
e4 = pygame.transform.scale(e4, (96,96))
e5 = image_load("splatter5.png")
e5 = pygame.transform.scale(e5, (96,96))
e6 = image_load("splatter6.png")
e6 = pygame.transform.scale(e6, (96,96))

#----------------------------boom class-----------------------------------------

class Splat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(e0)
        self.sprites.append(e1)
        self.sprites.append(e2)
        self.sprites.append(e3)
        self.sprites.append(e4)
        self.sprites.append(e5)
        self.sprites.append(e6)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.moving = False
        self.rect = self.image.get_rect()
        self.rect = [pos_x,pos_y]
    def animate(self):
        self.moving = True

    def spawn_anim(self):

        if self.moving == True:
            self.current_sprite += .5
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.moving = False
            self.image = self.sprites[int(self.current_sprite)]
explosion = pygame.sprite.Group()
splat = Splat(0,700)
explosion.add(splat)

#--------------------------- Goose class----------------------------------------

class Goose(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []   #--------------sprite sheet
        self.is_moving = False  #------- anim check------
        self.sprites.append(d1)
        self.sprites.append(d2)
        self.sprites.append(d3)
        self.sprites.append(d4)
        self.sprites.append(d5)
        self.sprites.append(d6)
        self.animstate = 0
        self.current_sprite = 0 #---------set animation start------
        self.image = self.sprites[self.current_sprite] #---- sets first sprite--
        self.rect = self.image.get_rect()       #----------creates rectangle
        self.rect = [pos_x,pos_y]              #creates position


    def animate(self):
        self.is_moving =True

    def update(self):
        if self.is_moving == True:

            if self.animstate == 1:
  #--------fly left-------------------------------------------------------------
                if numFrames < 30:
                    self.current_sprite = 0
                else:
                    self.current_sprite = 1


            if self.animstate == 2:
  #---------fly up--------------------------------------------------------------
                if numFrames < 30:
                    self.current_sprite = 2
                else:
                    self.current_sprite = 3


            if self.animstate == 3:
  #---------fly right-----------------------------------------------------------
                if numFrames < 30:
                    self.current_sprite = 4
                else:
                    self.current_sprite = 5



            self.image = self.sprites[int(self.current_sprite)]

#---------------------------UP--------------------------------------------------

    def moveUP(self):
        self.animstate = 2
        #print(int(self.current_sprite))
        goose.animate()
        if self.rect[1] >= -32:
            self.rect[1] -= speed*2

#-------------------------RIGHT-------------------------------------------------

    def moveRIGHT(self):
        self.animstate = 3
        #print(int(self.current_sprite))
        goose.animate()
        if self.rect[0] <= 832:
            self.rect[0] += speed
            self.rect[1] -= speed

#-----------------------LEFT----------------------------------------------------

    def moveLEFT(self):
        self.animstate = 1
        #print(int(self.current_sprite))
        goose.animate()
        if self.rect[0] >= -32:
            self.rect[0] -= speed
            self.rect[1] -= speed

#---------------------GOOSCLASSANIMSSETUP---------------------------------------

moving_ducks = pygame.sprite.Group()
goose = Goose(RANDOM_X, Y)
moving_ducks.add(goose)

#--------------------------------GROUND-----------------------------------------

grass = image_load("Grass.png")
grasspos = [0,600-96]
border = image_load("Border.png")
borderpos = [0, 600-64]
ground = image_load("Ground.png")
groundpos = [0,600-32]

def ground_sprites():
    for pixel in range(int(WIDTH/32)):

        window.blit(grass, grasspos)
        grasspos[0]+= 32
        if grasspos[0] >= 800:
            grasspos[0] = 0

        window.blit(border, borderpos)
        borderpos[0] +=32
        if borderpos[0] >= 800:
            borderpos[0] = 0

        window.blit(ground, groundpos)
        groundpos[0] += 32
        if groundpos[0] >= 800:
            groundpos[0] = 0

#--------------------------CLOUDS-----------------------------------------------

cloud = image_load("Clouds.png")
cld1 = [500,90]
cld2 = [650,120]
cld3 = [200,100]
clouds = [cld1, cld2, cld3]

def rolling_clouds():

    for item in range(len(clouds)):
        window.blit(cloud, clouds[item])
        for eachval in clouds:
            eachval[0] +=.05
            eachval[0] +=.08
            eachval[0] +=.1
            if eachval[0] >= 800:
                eachval[0] = -128

#------------------menu---------------------------------------------------------

musicon = False
menu = True
play = False
end = False
while True:
    while menu:
        if musicon == False:
            pygame.mixer.music.play(-1)
            musicon = True
        window.fill((163,220,255))
        rolling_clouds()
        ground_sprites()
        window.blit(credits, (300,470))
        window.blit(credits_konrad, (80, 550))
        window.blit(credits_cliff, (500, 550))
        window.blit(gH, (180,150))
        window.blit(start_game, (200,350))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    select_sound.play()
                    menu = False
                    play = True
        pygame.display.update()
        FPS.tick(60)

#---------------------------------------main loop-------------------------------

    while play:
        pygame.mixer.music.stop()
        if hit == True:
            splat.rect[0] = cursor_pos[0]-48
            splat.rect[1] = cursor_pos[1]-48
            splat.animate()
            hit_sound.play()

            hit = False

#-----------various text--------------------------------------------------------

        score_text = str(score)
        ducksleft = myfont.render(list_of_num[numDucks], True,(0,0,0))
        bulletsleft = myfont.render(list_of_num[bullets], True, (0,0,0))
        Score = myfont.render(score_text, True, (0,0,0))
        clicked = False
        window.fill((163,220,255))
        window.blit(myscore, (580, 10))
        window.blit(myducks, (20, 10))
        window.blit(ducksleft, (250,10))
        window.blit(mybullets, (300,10))
        window.blit(bulletsleft, (500,10))
        window.blit(Score, (720,10))

#------------------- calling clouds---------------------------------------------

        rolling_clouds()

#-------------------- spawning ducks randomly-----------------------------------

        if numDucks != 0:
            if direction == 1:
                goose.moveLEFT()
                if goose.rect[0] <= -32:
                    numDucks -= 1
                    escaped += 1
                    miss_sound.play()
                    direction = random.randint(1,3)
                    goose.rect[0] = random.randint(200,600)
                    goose.rect[1] = 600


            if direction == 2:
                goose.moveRIGHT()
                if goose.rect[0] >= 832:
                    numDucks -= 1
                    escaped += 1
                    miss_sound.play()
                    direction = random.randint(1,3)
                    goose.rect[0] = random.randint(200,600)
                    goose.rect[1] = 600


            if direction == 3:
                goose.moveUP()
                if goose.rect[1] <= -32:
                    numDucks -= 1
                    escaped += 1
                    miss_sound.play()
                    direction = random.randint(1,3)
                    goose.rect[0] = random.randint(200,600)
                    goose.rect[1] = 600


        moving_ducks.draw(window)
        moving_ducks.update()
        explosion.draw(window)
        splat.spawn_anim()

#--------------------------drawing gorund---------------------------------------

        ground_sprites()

#--------------------------------events-----------------------------------------

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():
                    if bullets != 0:
                        clicked = True
                        gun_sound.play()
                    cursor_pos = pygame.mouse.get_pos()

#----------------------checking if duck hit-------------------------------------

        if clicked == True:
            if bullets != 0:
                bullets -= 1
            if abs(goose.rect[0] - cursor_pos[0]) <= 32 and abs(goose.rect[1] - cursor_pos[1]) <= 32: #error checking up to 32 pixels
                hit = True
                splat.animate()
                numDucks -= 1
                score += 10
                direction = random.randint(1,3)
                goose.rect[0] = random.randint(200,600)
                goose.rect[1] = 600
            else:
                hit = False

#---------------------- checking if missed 3------------------------------------

        if escaped == 3:
            lost.play()
            play = False
            end = True

#---------------------- reset and increase speed--------------------------------

        if numDucks == 0:
            new_round.play()
            numDucks = 10
            speed *= 1.1
            bullets = 13
            escaped = 0

#---------------------checking frames for animation ----------------------------

        numFrames += 1
        if numFrames >= 60:
            numFrames = 0
        pygame.display.update()
        FPS.tick(60)

#-------------------------- end screen------------------------------------------

    while end:
        window.fill((163,220,255))
        rolling_clouds()
        ground_sprites()
        window.blit(myscore, (300, 200))
        window.blit(Score, (450,200))
        window.blit(restart_game, (150, 400))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    select_sound.play()
                    numDucks = 10
                    speed = 2
                    bullets = 13
                    escaped = 0
                    score = 0
                    direction = random.randint(1,3)
                    goose.rect[0] = random.randint(200,600)
                    goose.rect[1] = 600
                    end = False
                    play = True

        pygame.display.update()
        FPS.tick(60)
