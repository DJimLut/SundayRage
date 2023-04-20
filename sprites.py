import random
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(LAWN_MOWER, (60, 120)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.infShooting = False
        self.hurt = False
        self.health = 1
        self.turning = False
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            if not self.turning:
                self.turning = True
                self.image = pygame.transform.rotate(self.image, 15)
            self.speedx = -8
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            if not self.turning:
                self.turning = True
                self.image = pygame.transform.rotate(self.image, -15)
            self.speedx = 8
        elif self.hurt:
            self.image = pygame.transform.scale(LAWN_MOWER_HURT, (60, 120)).convert_alpha()
            self.turning = False
        else:
            self.image = pygame.transform.scale(LAWN_MOWER, (60, 120)).convert_alpha()
            self.turning = False

        if self.game.speedUp:
            self.rect.x += self.speedx * 2
        else:
            self.rect.x += self.speedx

        if self.health == 0:
            self.hurt = True

        if self.hurt:
            self.image = pygame.transform.scale(LAWN_MOWER_HURT, (60, 120)).convert_alpha()

        if self.rect.right > WIDTH - 64:
            self.rect.right = WIDTH - 64
        if self.rect.left < 64:
            self.rect.left = 64

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(CHOMPY_IMG, (50, 50)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mouthOpen = False
        self.rect.x = random.randrange(64, WIDTH - 64 - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 2

    def update(self):        
        if self.game.framesPassed % 10 == 0:
            self.image = self.nextFrame(self.mouthOpen)

        if self.game.speedUp:
            self.rect.y += self.speedy * 2
        else:
            self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(64, WIDTH - 64 - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 2

    def nextFrame(self, mouthOpen):
        self.mouthOpen = not mouthOpen

        if mouthOpen:
            return pygame.transform.scale( CHOMPY_MOUTH_OPEN_IMG, ( 50, 50 ) ).convert_alpha()
        else:
            return pygame.transform.scale( CHOMPY_IMG, ( 50, 50 ) ).convert_alpha()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(SAW_BLADE, (60, 60)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        self.image = pygame.transform.rotate(self.image, 90)
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load(path.join(MAP_DIR, random.choice(MAPS))).convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.rect.left = 0

    def update(self):
        if self.game.speedUp:
            self.rect.y += 5
        else:
            self.rect.y += 1

class Item(pygame.sprite.Sprite):
    def __init__(self, game, image, sound, xCoord, yCoord):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.sound = sound
        self.flashing = False
        self.rect = image.get_rect()
        self.rect.centerx = xCoord
        self.rect.centery = xCoord

    def update(self):
        if self.game.speedUp:
            self.rect.y += 5
        else:
            self.rect.y += 1

        if self.rect.top > HEIGHT:
            self.rect.centerx = random.randint(64, WIDTH - 64)
            self.rect.centery = random.randint(-10, HEIGHT - 40)

    def execute(self):
        self.game.sounds[self.sound].play()


class Gas(Item):
    def __init__(self, game, xCoord, yCoord):
        self.image = pygame.transform.scale(GAS_CAN, (32,44)).convert_alpha()
        Item.__init__(self, game, self.image, 'gas.wav', xCoord, yCoord)

    def execute(self):
        Item.execute(self)
        self.game.speedUp = True
        
class Oil(Item):
    def __init__(self, game, xCoord, yCoord):
        self.image = pygame.transform.scale(OIL_CAN, (32, 44)).convert_alpha()
        Item.__init__(self, game, self.image, 'oil.wav', xCoord, yCoord)

    def execute(self):
        Item.execute(self)
        self.game.player.health = 1
        if self.game.player.hurt:
            self.game.player.hurt = False
        
class InfAmmo(Item):
    def __init__(self, game, xCoord, yCoord):
        self.image = pygame.transform.scale( SAW_BLADE, (60, 60))
        Item.__init__(self, game, self.image, 'saw.wav', xCoord, yCoord)

    def execute(self):
        Item.execute(self)
        self.game.player.infShooting = True