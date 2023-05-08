import random
import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(LAWN_MOWER, (60, 120)).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.infShooting = False
        self.hurt = False
        self.health = 5
        self.turning = False
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8

        if self.game.speedUp:
            self.rect.x += self.speedx * 2
        else:
            self.rect.x += self.speedx

        if self.health < 5:
            self.hurt = True

        if self.hurt:
            self.image = pygame.transform.scale(
                LAWN_MOWER_HURT, (60, 120)
            ).convert_alpha()
        else:
            self.image = pygame.transform.scale(LAWN_MOWER, (60, 120)).convert_alpha()
            self.health = 5

        if self.rect.right > WIDTH - 64:
            self.rect.right = WIDTH - 64
        if self.rect.left < 64:
            self.rect.left = 64

    def shoot(self):
        sawBlade = SawBlade(self.game, self.rect.centerx, self.rect.top)
        self.game.all_sprites.add(sawBlade)
        self.game.sawBlades.add(sawBlade)


class Chompy(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(
            CHOMPY_IMG,
            (50, 50),
        ).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.mouthOpen = False
        self.rect.x = random.randrange(
            64, self.game.screen.get_width() - 64 - self.rect.width
        )
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 2

    def update(self):
        if self.game.framesPassed % 10 == 0:
            self.image = self.nextFrame(self.mouthOpen)

        if self.game.speedUp:
            self.rect.y += self.speedy * 2
        else:
            self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(
                64, self.game.screen.get_width() - 64 - self.rect.width
            )
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 2

    def nextFrame(self, mouthOpen):
        self.mouthOpen = not mouthOpen

        if mouthOpen:
            return pygame.transform.scale(
                CHOMPY_MOUTH_OPEN_IMG, (50, 50)
            ).convert_alpha()
        else:
            return pygame.transform.scale(
                CHOMPY_IMG,
                (50, 50),
            ).convert_alpha()


class Shooter(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(
            SHOOTER_IMG,
            (150, 150),
        ).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.loaded = False
        self.rect.x = random.randrange(
            64, self.game.screen.get_width() - 64 - self.rect.width
        )
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 1

    def update(self):
        if self.game.framesPassed % 60 == 0:
            self.loaded = True
            self.shoot()

        if self.game.speedUp:
            self.rect.y += self.speedy * 2
        else:
            self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(
                64, self.game.screen.get_width() - 64 - self.rect.width
            )
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 2

    def shoot(self):
        pea = Pea(self.game, self.rect.centerx, self.rect.bottom)
        self.game.all_sprites.add(pea)
        self.game.peas.add(pea)
        self.loaded = False


class SawBlade(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(
            SAW_BLADE,
            (60, 60),
        ).convert_alpha()
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


class Pea(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(PEA_IMG, (30, 30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > self.game.screen.get_height():
            self.kill()


class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load(
            path.join(MAP_DIR, random.choice(MAPS))
        ).convert()
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
        self.rect = image.get_rect()
        self.rect.centerx = xCoord
        self.rect.centery = yCoord

    def update(self):
        if self.game.speedUp:
            self.rect.y += 5
        else:
            self.rect.y += 1

        if self.rect.top > HEIGHT:
            self.rect.centerx = random.randint(64, self.game.screen.get_width() - 64)
            self.rect.centery = random.randint(-10, self.game.screen.get_height() - 40)

    def execute(self):
        self.game.sounds[self.sound].play()


class Gas(Item):
    def __init__(self, game, xCoord, yCoord):
        self.image = pygame.transform.scale(GAS_CAN, (32, 44)).convert_alpha()
        Item.__init__(self, game, self.image, "gas.wav", xCoord, yCoord)

    def execute(self):
        Item.execute(self)
        self.game.speedUp = True


class Oil(Item):
    def __init__(self, game, xCoord, yCoord):
        self.image = pygame.transform.scale(OIL_CAN, (32, 44)).convert_alpha()
        Item.__init__(self, game, self.image, "oil.wav", xCoord, yCoord)

    def execute(self):
        Item.execute(self)
        self.game.player.health = 5
        if self.game.player.hurt:
            self.game.player.hurt = False


class InfAmmo(Item):
    def __init__(self, game, xCoord, yCoord):
        self.image = pygame.transform.scale(SAW_BLADE, (60, 60))
        Item.__init__(self, game, self.image, "saw.wav", xCoord, yCoord)

    def execute(self):
        Item.execute(self)
        self.game.player.infShooting = True
