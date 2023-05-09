import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        pg.mixer.music.load(path.join(SOUND_DIR, "loop3.mp3"))
        pg.mixer.music.set_volume(0.4)
        pg.mixer.music.play(loops=-1)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.scalex = 1
        self.scaley = 1
        pg.display.set_caption("Sunday Rage")
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.score = 0
        self.framesPassed = 0
        self.loaded = False
        self.noMobCheatCheck = False
        self.running = True
        self.speedUp = False
        self.currentTime = 0
        self.previousTime = 0

        # sounds
        self.sounds = {}
        for sound in ["gas.wav", "oil.wav", "saw.wav"]:
            self.sounds[sound] = pg.mixer.Sound(path.join(SOUND_DIR, sound))

        # highscore
        try:
            with open("highscore.txt", "r") as f:
                self.highscore = int(f.readline())
        except Exception as e:
            self.highscore = 0

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.sawBlades = pg.sprite.Group()
        self.peas = pg.sprite.Group()
        self.items = pg.sprite.Group()

        # player
        self.player = Player(self)

        # map
        self.map = Map(self)
        self.all_sprites.add(self.map)

        # mobs
        for i in range(3):
            m = random.choice([Chompy(self), Shooter(self)])
            self.mobs.add(m)
            self.all_sprites.add(m)

        # items
        items = [
            Gas(self, random.randint(64, WIDTH - 64), random.randint(-10, HEIGHT - 40)),
            Oil(self, random.randint(64, WIDTH - 64), random.randint(-10, HEIGHT - 40)),
            InfAmmo(
                self, random.randint(64, WIDTH - 64), random.randint(-10, HEIGHT - 40)
            ),
        ]
        item = random.choice(items)
        self.items.add(item)
        self.all_sprites.add(item)

        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            # keep loop running at the right speed
            self.clock.tick(FPS)

            for sprite in self.all_sprites:
                sprite.rect.centerx *= self.scalex
                sprite.rect.centery *= self.scaley

            # Process input (events)
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    match event.key:
                        case pg.K_SPACE:
                            self.currentTime = pg.time.get_ticks()
                            if self.currentTime - self.previousTime > 250:
                                self.player.shoot()
                                self.previousTime = self.currentTime
                        case pg.K_KP1:
                            self.noMobCheatCheck = True
                            for mob in self.mobs:
                                    mob.kill()
                        case pg.K_KP2:
                                for i in range(3):
                                    m = random.choice([Chompy(self), Shooter(self)])
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

            # check if 10 seconds have passed from when powerup was picked up
            if self.framesPassed % 600 == 0:
                self.speedUp = False
                self.player.infShooting = False

            self.framesPassed += 1

            # check if more items needed
            if not self.items:
                items = [
                    Gas(
                        self,
                        random.randint(64, self.screen.get_width() - 64),
                        random.randint(-10, self.screen.get_height() - 40),
                    ),
                    Oil(
                        self,
                        random.randint(64, self.screen.get_width() - 64),
                        random.randint(-10, self.screen.get_height() - 40),
                    ),
                    InfAmmo(
                        self,
                        random.randint(64, self.screen.get_width() - 64),
                        random.randint(-10, self.screen.get_height() - 40),
                    ),
                ]
                item = random.choice(items)
                self.items.add(item)
                self.all_sprites.add(item)

            # check to see if more mobs are needed
            if not self.mobs and not self.noMobCheatCheck:
                for i in range(3):
                    m = random.choice([Chompy(self), Shooter(self)])
                    self.mobs.add(m)
                    self.all_sprites.add(m)

            # check to see if new map is needed
            if self.map.rect.top > -10 and not self.loaded:
                self.newMap = Map(self)
                self.newMap.rect.bottom = self.map.rect.top
                self.all_sprites = pg.sprite.Group()
                self.all_sprites.add(self.map)
                self.all_sprites.add(self.newMap)
                for mob in self.mobs:
                    self.all_sprites.add(mob)
                for item in self.items:
                    self.all_sprites.add(item)
                self.all_sprites.add(self.player)
                self.loaded = True

            if self.map.rect.top >= HEIGHT and self.loaded:
                self.map.kill()
                self.map = self.newMap
                self.loaded = False

            # check to see if a sawblade hit a mob
            hits = pg.sprite.groupcollide(self.mobs, self.sawBlades, True, True)
            for hit in hits:
                self.score += 10
                m = random.choice([Chompy(self), Shooter(self)])
                self.mobs.add(m)
                self.all_sprites.add(m)

            # check to see if a sawblade hit a pea
            hits = pg.sprite.groupcollide(self.peas, self.sawBlades, True, True)

            # check to see if a pea hit the player
            hits = pg.sprite.spritecollide(self.player, self.peas, False)
            if hits:
                if self.player.health == 0:
                    self.playing = False
                else:
                    self.player.health -= 1
                    hits[0].kill()

            # check to see if a mob hit the player
            hits = pg.sprite.spritecollide(self.player, self.mobs, False)
            if hits:
                if self.player.health == 0:
                    self.playing = False
                else:
                    self.player.health -= 1
                    hits[0].kill()

            # infinite shooting powerup
            if self.player.infShooting:
                self.currentTime = pg.time.get_ticks()
                if self.currentTime - self.previousTime > 250:
                    self.player.shoot()
                    self.previousTime = self.currentTime

            for sprite in self.all_sprites:
                if (
                    sprite != self.player
                    and sprite != self.map
                    and abs(sprite.rect.y - self.player.rect.y) < 2
                    and abs(sprite.rect.x - self.player.rect.x) < 2
                ):
                    pg.sprite.collide_mask(self.player, sprite)

            # check to see if an item hit the player
            hits = pg.sprite.spritecollide(self.player, self.items, False)
            for hit in hits:
                hit.execute()
                hit.kill()

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
            pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(GREEN)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(
            "Arrows / WASD to move, Space to shoot", 22, WHITE, WIDTH / 2, HEIGHT / 2
        )
        self.draw_text("Press ENTER to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        # game over/continue
        if not self.running:
            return

        self.screen.fill(RED)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(
            "Press ENTER to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4
        )
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open("highscore.txt", "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text(
                "High Score: " + str(self.highscore),
                22,
                WHITE,
                WIDTH / 2,
                HEIGHT / 2 + 40,
            )
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.loaded = False
                    self.running = False
                    waiting = False
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.speedUp = False
                    waiting = False

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
    g.show_game_over_screen()

pg.quit()
