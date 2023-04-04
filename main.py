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
        self.font_name = pg.font.match_font(FONT_NAME)
        self.score = 0
        self.loaded = False
        self.noMobCheatCheck = False
        self.running = True
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        self.map = Map(self)
        self.all_sprites.add(self.map)
        for i in range(5):
            m = Mob(self)
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.all_sprites.add(self.player)
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    match event.key:
                        case pg.K_SPACE:
                            self.player.shoot()
                        case pg.K_n:
                            self.noMobCheatCheck = True
                        case pg.K_m:
                            if self.noMobCheatCheck:
                                for mob in self.mobs:
                                    mob.kill()
                                self.noMobCheatCheck = False
                            else:
                                for i in range(5):
                                    m = Mob(self)
                                    self.all_sprites.add(m)
                                    self.mobs.add(m)
                        case pg.K_q:
                            self.playing = False
                            self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    match event.button:
                        case 1:
                            self.player.shoot()

            # Update
            self.all_sprites.update()

            # check to see if new map is needed
            if self.map.rect.top > -10 and not self.loaded:
                self.newMap = Map(self)
                self.newMap.rect.bottom = self.map.rect.top
                self.all_sprites = pg.sprite.Group()
                self.all_sprites.add(self.map)
                self.all_sprites.add(self.newMap)
                for mob in self.mobs:
                    self.all_sprites.add(mob)
                self.all_sprites.add(self.player)
                self.loaded = True

            if self.map.rect.top == HEIGHT and self.loaded:
                self.map.kill()
                self.map = self.newMap
                self.loaded = False

            # check to see if a bullet hit a mob
            hits = pg.sprite.groupcollide(self.mobs, self.bullets, True, True)
            for hit in hits:
                self.score += 10
                m = Mob(self)
                self.all_sprites.add(m)
                self.mobs.add(m)

            # check to see if a mob hit the player
            hits = pg.sprite.spritecollide(self.player, self.mobs, False)
            if hits:
                self.playing = False
                self.running = False

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
            pg.display.flip()
    
    def show_start_screen(self):
        pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
# Game loop
while g.running:
    g.new()
    g.show_start_screen()

pg.quit()