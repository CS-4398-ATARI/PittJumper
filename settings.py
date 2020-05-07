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
GAME_BG = "sky.png"

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
# PLATFORM_LIST = [(0, HEIGHT - 60),
#                  (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
#                  (125, HEIGHT - 350),
#                  (350, 200),
#                  (400, 300),
#                  (500, 40),
#                  (900, 600),
#                  (500, 100),
#                  (800, 100),
#                  (600, 40),
#                  (450, 600),
#                  (150, HEIGHT-60),
#                  (800, HEIGHT - 60),
#                  ]
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (300, HEIGHT - 60),
                 (600, HEIGHT - 60),
                 (900, HEIGHT - 60),
                 (150, HEIGHT -280),
                 (450, HEIGHT - 180),
                 (750, HEIGHT - 200),
                 (1050, HEIGHT - 240),
                 ]

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