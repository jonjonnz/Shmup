import pygame #import pygame module
import random # import random module
import os #to open folders and commands on files/images

#Frozen Jam by tgfcoder licensed under CC-BY-3
#Art from Kenny.nl


#Predefined Values
width = 480
height = 700
FPS = 60

#make it work on all systems
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
sound_folder = os.path.join(game_folder,"snd")
player_folder = os.path.join(img_folder,"Ships")
enemy_folder = os.path.join(img_folder,"Meteors")
bullet_folder = os.path.join(img_folder,"Missiles")
effect_folder = os.path.join(img_folder,"Effects")
background_folder = os.path.join(img_folder,"Building")


#Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x , y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True,white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)


#Create Player
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #won't work without this
        self.image = pygame.image.load(os.path.join(player_folder,"spaceShips_001.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(black)
        
        #initialize and position the rectangle
        self.rect = self.image.get_rect()
        self.radius = 24
        #pygame.draw.circle(self.image , red, self.rect.center, self.radius)
        self.rect.centerx = width/2
        self.rect.bottom = height - 50
        self.speedx = 0
        

    def update(self):
        self.speedx = 0
        
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        self.rect.x +=self.speedx
        
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        
    def shoot(self):
        bullet = Bullets(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullet_group.add(bullet)
        shoot_sound.play()
    
#creating enemy

class mob(pygame.sprite.Sprite):
        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(os.path.join(enemy_folder,"spaceMeteors_002.png")).convert()
        self.image_orig = pygame.transform.scale(self.image_orig, (55, 55))
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image , red, self.rect.center, self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speed_y = random.randrange(1,5)
        self.speed_x = random.randrange(-2,2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            
            
    def update(self):
        self.rotate()
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > height + 10 or self.rect.right > width+self.rect.width or self.rect.left < -self.rect.width:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speed_y = random.randrange(1,5)
            self.speed_x = random.randrange(-2,2)

            
#Create bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(bullet_folder,"spaceMissiles_038.png"))
        self.image = pygame.transform.scale(self.image, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -15
        
        
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()



#Initialize pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size=(width, height)) #make a window
pygame.display.set_caption("Shoot Em Up") #Set the window name
background_img = pygame.image.load(os.path.join(background_folder,"spaceBackground_001.jpg")) #Load an image
background_img = pygame.transform.scale(background_img, (width, height)) # make it fullscreen
clock = pygame.time.Clock()


#Load sounds
shoot_sound = pygame.mixer.Sound(os.path.join(sound_folder,"Laser_Shoot.wav"))
exp_sounds = []
for snd in ["Explosion1.wav","Explosion2.wav"]:
    exp_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder,snd)))
pygame.mixer.music.load(os.path.join(sound_folder,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)





#make a group for all sprites to make it easier to update and draw everytime
mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group() 
bullet_group = pygame.sprite.Group()
player = Player()
for i in range(8):
    m = mob()
    all_sprites.add(m)
    mobs.add(m)
all_sprites.add(player)

score = 0

pygame.mixer.music.play(loops=-1, start=0_0)
#Main game loop
running = True
while running:
    clock.tick(FPS)
    #inputs/events
    for event in pygame.event.get():
        #checking for closing the game
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #Update
    all_sprites.update()
    
    #check to see if bullet hit the enemy
    hits = pygame.sprite.groupcollide(bullet_group, mobs,True, True)
    for hit in hits:
        score += 1
        random.choice(exp_sounds).play()
        m = mob()
        all_sprites.add(m)
        mobs.add(m)
    
    #check if player hit the sprite
    hits = pygame.sprite.spritecollide(player, mobs, False , pygame.sprite.collide_circle)
    if hits:
        running = False
    #draw/render
    screen.blit(background_img, [0, 0])
    all_sprites.draw(screen)
    draw_text(screen, str(score),18,width/2,10)
    # after drawing everyting flip the display
    pygame.display.flip()
    
pygame.quit()
