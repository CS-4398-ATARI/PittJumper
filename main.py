# Using KidsCanCode - Game Development with Pygame video series as a framework
# Improved Jumping
# Art from Kenney.nl

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from settings import *


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

        # Loading the sound directory and all music will go under here? Probably will have to reference
        # the music somewhere in the game loop if we want to switch,
        sound_dir = path.join(self.dir, 'sound')
        pg.mixer.music.load(path.join(sound_dir, 'Venus.wav'))
        pg.mixer.music.play(-1)

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        # start a new game
        self.score = pg.time.get_ticks()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.score = (pg.time.get_ticks() - self.score) / 1000

        # Enemies
        for i in range(8):
            m = Enemy()
            self.all_sprites.add(m)
            self.enemies.add(m)

        # Platforms
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
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
            #pg.time.delay(10000)
            self.playing = False

        # if player reaches top 1/4 of screen
        #if self.player.rect.top <= HEIGHT / 4:
            #self.player.pos.y += max(abs(self.player.vel.y), 2)
            #for plat in self.platforms:
                #plat.rect.y += max(abs(self.player.vel.y), 2)
                #if plat.rect.top >= HEIGHT:
                    #plat.kill()

        # Timer
        self.score = pg.time.get_ticks()

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
#        while len(self.platforms) < 6:
#            width = random.randrange(50, 100)
#            p = Platform(self, random.randrange(0, WIDTH - width),
#                         random.randrange(-75, -30))
#            self.platforms.add(p)
            #self.all_sprites.add(p)

    def events(self):

        # Going to throw all sounds above here. There's probably a better place to put them.
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
#        BackGround = Background(r"C:\Users\Lumir\PycharmProjects\testgame\img\Background\bg_layer1.png", [0, 0])
        self.screen.fill([137, 207, 240])
#        self.screen.blit(BackGround.image, BackGround.rect)
        #        self.screen.blit(BackGround.image, BackGround.rect)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(round(self.score/10000, 2)), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        img_dir = path.join(self.dir, 'img')
        self.background = Background(path.join(img_dir, BACKGROUNDTITLE), [0, 0])
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.background.image, self.background.rect)
        #self.screen.fill(BGCOLOR)
#        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
#        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
#        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
#        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(round(self.score/10000, 2)), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(round(self.highscore/10000, 2)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

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

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()