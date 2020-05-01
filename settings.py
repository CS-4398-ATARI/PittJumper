from os import path

# game options/settings
TITLE = "Pit Jumper"
WIDTH = 1200
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
BACKGROUNDTITLE = "pitjumpertitle.png"

# Sound properties
SOUND = path.join('./sound')
GAME_TRACK = 'Venus.wav'
PAUSE_TRACK = 'Mars.wav'
GAME_OVER = 'Win Jingle.wav'
LOOP = -1

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60)]

# Starting Enemies
ENEMY_LIST = [(0, HEIGHT - 60, 5)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE