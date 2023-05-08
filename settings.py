from os import path
import pygame

TITLE = 'Sunday Rage'
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = "arial"

# directories
ASSET_DIR = path.join(path.dirname(__file__), "assets")
MAP_DIR = path.join(ASSET_DIR, "maps")
MOWER_DIR = path.join(ASSET_DIR, "mower")
ENEMY_DIR = path.join(ASSET_DIR, "enemies")
CHOMPY_DIR = path.join(ENEMY_DIR, "chompy")
SHOOTER_DIR = path.join(ENEMY_DIR, "shooter")
ITEM_DIR = path.join(ASSET_DIR, "items")
JERRYCAN_DIR = path.join(ITEM_DIR, "jerrycan")
OIL_CAN_DIR = path.join(ITEM_DIR, "oilcan")
SAW_BLADE_DIR = path.join(ITEM_DIR, "sawblade")
PEA_DIR = path.join(ITEM_DIR, "pea")
IDLE_ANIMATION_DIR = path.join(MOWER_DIR, "idle")
HURT_ANIMATION_DIR = path.join(MOWER_DIR, "hurt")
SOUND_DIR = path.join(ASSET_DIR, "sounds")

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# sprites
MAPS = ["map.png", "map2.png", "map3.png", "map4.png"]
CHOMPY_IMG = pygame.image.load(path.join(CHOMPY_DIR, "chompy01.png"))
CHOMPY_MOUTH_OPEN_IMG = pygame.image.load(path.join(CHOMPY_DIR, "chompy02.png"))
SHOOTER_IMG = pygame.transform.rotate(
    pygame.image.load(path.join(SHOOTER_DIR, "shooter.png")), 180
)
SHOOTER_LOADED_IMG = pygame.image.load(path.join(SHOOTER_DIR, "shooter01.png"))
LAWN_MOWER = pygame.image.load(path.join(IDLE_ANIMATION_DIR, "idle01.png"))
LAWN_MOWER_HURT = pygame.image.load(path.join(HURT_ANIMATION_DIR, "hurt05.png"))
PEA_IMG = pygame.image.load(path.join(PEA_DIR, "pea.png"))
SAW_BLADE = pygame.image.load(path.join(SAW_BLADE_DIR, "saw-blade.png"))
GAS_CAN = pygame.image.load(path.join(JERRYCAN_DIR, "jerrycan.png"))
OIL_CAN = pygame.image.load(path.join(OIL_CAN_DIR, "oilcan.png"))
