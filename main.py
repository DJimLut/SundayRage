import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Sunday Rage")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self)
        self.map = Map(self)
        self.all_sprites.add(self.map)
        self.all_sprites.add(self.player)
        for i in range(5):
            m = Mob(self)
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

            # Update
            self.all_sprites.update()

            # check to see if a bullet hit a mob
            hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
            for hit in hits:
                m = Mob(self)
                self.all_sprites.add(m)
                self.mobs.add(m)

            # check to see if a mob hit the player
            hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
            if hits:
                self.running = False

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            # *after* drawing everything, flip the display
            pg.display.flip()
    
    def show_start_screen(self):
        pass

g = Game()
g.show_start_screen()
# Game loop
while g.running:
    g.new()
    g.show_start_screen()

pg.quit()