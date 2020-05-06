import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from stopwatch import Stopwatch


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()  # sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def new(self):
        # start a new game
        self.timer = Stopwatch()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.last_update = 0
        pg.mixer.music.load(path.join(SOUND, GAME_TRACK))
        pg.mixer.music.play(LOOP)
        pg.mixer.music.set_volume(0.6)
        self.pausedtime = 0

        # Enemies
        for i in range(0):
            m = Enemy(self)
            self.all_sprites.add(m)
            self.enemies.add(m)

        # Platforms
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # Other platforms

        self.run()

    def run(self):  # The game loop
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def pause(self):
        paused = True
        tempTime = Stopwatch()

        # Fade out game music, start pause soundtrack
        pg.mixer.music.fadeout(750)
        pg.mixer.music.load(path.join(SOUND, PAUSE_TRACK))
        pg.mixer.music.play(LOOP)
        pg.mixer.music.set_volume(0.2)
        while paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        self.pausedtime += tempTime.get_seconds()
                        paused = False
                    elif event.key == pg.K_q:
                        pg.quit()
                        quit()

            self.screen.fill(BLACK)
            self.draw_text("Paused", 48, RED, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Press c to continue, q to quit", 22, WHITE, WIDTH / 2, HEIGHT / 2)

            pg.display.update()
            self.clock.tick(5)

        # Load and resume game music
        pg.mixer.music.load(path.join(SOUND, GAME_TRACK))
        pg.mixer.music.play(LOOP)
        pg.mixer.music.set_volume(0.6)
        self.update()

    def show_start_screen(self):
        # game splash/start screen
        img_dir = path.join(self.dir, 'img')
        self.background = Background(path.join(img_dir, BACKGROUNDTITLE), [-50, 0])
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.background.image, self.background.rect)

        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return

        pg.mixer.music.load(path.join(SOUND, GAME_OVER))
        pg.mixer.music.play()
        self.screen.fill([0, 0, 0])
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(round((self.timer.get_seconds() - self.pausedtime), 2)), 22, WHITE, WIDTH / 2,
                       HEIGHT / 2)
        self.draw_text("Press c to play again, q to quit", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.timer.get_seconds() - self.pausedtime > self.highscore:
            self.highscore = self.timer.get_seconds() - self.pausedtime
            self.draw_text("NEW HIGH SCORE!", 22, RED, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.timer.get_seconds() - self.pausedtime))
        else:
            self.draw_text("High Score: " + str(round(self.highscore, 2)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        # self.wait_for_key()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        waiting = False
                    elif event.key == pg.K_q:
                        pg.quit()
                        quit()

    ######## GAME LOOP FUNCTIONS ########

    def events(self):  # Import from game_loop.py
        sound_dir = path.join(self.dir, 'sound')
        jumpsound = path.join(sound_dir, "jump_01.wav")

        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    pg.mixer.Sound.play(pg.mixer.Sound(jumpsound))
                elif event.key == pg.K_p:
                    self.pause()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def update(self):  # Import from game_loop.py
        # Game Loop - Update
        self.all_sprites.update()

        # check for collision if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False

        # Tracking player collision with enemy sprites.
        if pg.sprite.spritecollide(self.player, self.enemies, True):
            self.player.isdead = True
            self.playing = False

        now = pg.time.get_ticks()
        if now - self.last_update > 1000:
            self.last_update = now
            m = Enemy(self)
            self.all_sprites.add(m)
            self.enemies.add(m)

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

    def draw(self):  # Import from game_loop.py
        # Game Loop - draw
        self.screen.fill([137, 207, 240])
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(round(self.timer.get_seconds() - self.pausedtime, 2)), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    ######### HELPER FUNCTIONS ##########

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = float(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False