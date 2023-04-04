from os import path
import pygame

WIDTH = 480
HEIGHT = 600
FPS = 60
ASSET_DIR = path.join( path.dirname(__file__), 'assets' )

# define colors
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )
YELLOW = ( 255, 255, 0 )

# sprites
MAP = pygame.image.load( path.join( ASSET_DIR, 'map.png' ) )
ENEMY_IMG = pygame.image.load( path.join( ASSET_DIR, 'enemy1-frame1.png' ) )
ENEMY_IMG_FRAME2 = pygame.image.load( path.join( ASSET_DIR, 'enemy1-frame2.png' ) )