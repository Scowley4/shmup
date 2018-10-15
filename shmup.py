# Shmup
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 # <http://creativecommons.org/licenses/by/3.0/>
# Art from Kenney.nl
import pygame
import random
import sys
import os

img_dir = os.path.join(os.path.dirname(__file__), 'img')
snd_dir = os.path.join(os.path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)


# Init pygame
pygame.init()

# Initializes for sound
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shmup!')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)

        # True is aliased or not
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    # 2 is the border
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Rect
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(GREEN)


        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

        # If have this, will do circular bounding box
        self.radius = 21
        # Use this to see the circle
        # pygame.draw.circle(self.image, RED,
        #                     (self.rect.width//2, self.rect.height//2),
        #                     self.radius)

        self.shoot_delay = 250 # miliseconds
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100

        self.lives = 3
        self.hidden = False
        self.hide_timer = None

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        # Always still unless key is down
        self.speedx = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        # Constrained to the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)
            shoot_snd.play()

    def get_killed(self):
        player.hide()
        player.lives -= 1
        player.shield = 100

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 500)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Rects
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(YELLOW)

        self.image = bullet_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])

        # Rects
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(YELLOW)

        self.image = bullet_img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 40))
        # self.image.fill(RED)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)

        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-2, 2)

        # If have this, will do circular bounding box
        self.radius = int(self.rect.width*.85/2)
        # Use this to see the circle
        # pygame.draw.circle(self.image, RED,
        #                     (self.rect.width//2, self.rect.height//2),
        #                     self.radius)

        # Rotation
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
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # If things go off the edge of the screen
        if (self.rect.top > HEIGHT + 10 or
                    self.rect.left < -150 or
                    self.rect.right > WIDTH + 150):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-100, -40)
            self.speedx = random.randrange(1, 8)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def spawn_expl(center, expl_type):
    expl = Explosion(center, expl_type)
    all_sprites.add(expl)
    return expl

def spawn_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Load game sounds
shoot_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'LaserShoot2.wav'))
expl_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'Explosion.wav'))
player_die_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(.4)

# Load game graphics
background = pygame.image.load(os.path.join(img_dir,
        'starfield.png')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(os.path.join(img_dir,
        'playerShip1_orange.png')).convert()

player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

meteor_dir = os.path.join(img_dir, 'meteor_imgs')
meteor_images = [pygame.image.load(os.path.join(meteor_dir, img_file)).convert()
                 for img_file in os.listdir(meteor_dir) if 'meteor' in img_file]

bullet_img = pygame.image.load(os.path.join(img_dir,
        'laserRed16.png')).convert()

# Make the explosion images
expl_dir = os.path.join(img_dir, 'expl_imgs')
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
size_names = ['lg', 'med', 'sm', 'tiny', 'player']
sizes = [(75, 75), (50, 50), (32, 32), (10, 10)]
for size_name in size_names:
    expl_anim[size_name] = []
for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(os.path.join(expl_dir, filename)).convert()
    img.set_colorkey(BLACK)
    for size, size_name in zip(sizes, size_names):
        expl_anim[size_name].append(pygame.transform.scale(img, size))

    filename = f'sonicExplosion0{i}.png'
    img = pygame.image.load(os.path.join(expl_dir, filename)).convert()
    img.set_colorkey(BLACK)
    #expl_anim['player'].append(pygame.transform.scale(img, (50,50)))
    expl_anim['player'].append(img)






all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    spawn_mob()

score = 0

# Loop forever
pygame.mixer.music.play(loops=-1)

# Game loop
running = True
while running:
    # Keep loop running at correct speed
    clock.tick(FPS) # Makes the loop run at 1/FPS seconds

    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()



    # Update
    all_sprites.update()

    # Check to see if bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - int(hit.radius)
        spawn_expl(hit.rect.center, 'lg')
        spawn_mob()
        expl_snd.play()

    # Check to see if mob hit player
        # Sprite, group, delete
    hits = pygame.sprite.spritecollide(player, mobs, True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        spawn_expl(hit.rect.center, 'sm')
        if player.shield <= 0:
            player_die_snd.play()
            death_expl = spawn_expl(hit.rect.center, 'player')
            player.get_killed()
            # Sound?
        spawn_mob()

    if player.lives == 0:
        player.kill()

    if not player.alive() and not death_expl.alive():
        running = False


    # Draw/render

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)

    # **After** drawing everything
    pygame.display.flip()

pygame.quit()




