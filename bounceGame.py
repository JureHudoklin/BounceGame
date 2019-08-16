import pygame
import numpy as np 
import random
import sys

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
Blue = (0,0,255)

GAME_SCREEN_WIDTH = 800
GAME_SCREEN_HEIGHT = 600

def limitNumber(number, limit):
    if number > limit:
        return limit
    elif number < -limit:
        return -limit
    else:
        return number

class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the board controls """
 
    def __init__(self, x, y, width, height, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class boardArea(object):
    """ Base class for all rooms. """
 
    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    cubes_list = None
    enemy_sprites = None
 
    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.cubes_list = pygame.sprite.Group()

class boardArea1(boardArea):
    """This creates all the walls in room 1"""
    def __init__(self):
        super().__init__()
        # Make the walls. (x_pos, y_pos, width, height)
 
        # This is a list of walls. Each is in the form [x, y, width, height]
        thickness = 5

        walls = [[0, 0, GAME_SCREEN_WIDTH, thickness, WHITE],
                [GAME_SCREEN_WIDTH-thickness, 0, thickness, GAME_SCREEN_HEIGHT, WHITE],
                [0, 0, thickness, GAME_SCREEN_HEIGHT, WHITE]]
 
        # Loop through the list. Create the wall, add it to the list
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        # Create cubes
        space_between = 2
        size = 20
        area_width = GAME_SCREEN_WIDTH - 2 * thickness
        for j in range(10):
            
            for i in range(int(area_width / size)):
                x = i*size + space_between + thickness
                y = j*size + space_between + thickness
                self.cubes_list.add(Cube(x, y, size - 2*space_between, size - 2*space_between, random.randint(1,3)))


        

class Ball(pygame.sprite.Sprite):

    # Speed Vector
    change_x = 0.
    change_y = 0.

    def __init__(self, size, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([size, size])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = int(GAME_SCREEN_WIDTH/2)
        self.rect.y = int(GAME_SCREEN_HEIGHT/2)

    def startBall(self):
        self.rect.x = int(GAME_SCREEN_WIDTH/2)
        self.rect.y = int(GAME_SCREEN_HEIGHT/2)
        self.change_x = random.randint(-10,10)
        self.change_y = -10

    def moveBall(self, walls, board, cubes):

        """ Detect colisions in x direction """    
        # Update ball position
        self.rect.x += self.change_x

        # Detect collisions with walls
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for item in collisions:
            if self.change_x > 0:
                self.rect.right = item.rect.left
            else:
                self.rect.left = item.rect.right
            self.change_x *= -1
            return

        # Detect collision with cubes
        collisions = pygame.sprite.spritecollide(self, cubes, False)
        if len(collisions)>0:
            for item in collisions:
                if self.change_x > 0:
                    self.rect.right = item.rect.left
                else:
                    self.rect.left = item.rect.right
                item.cubeHit()       
            self.change_x *= -1
            return


        """ Detect colisions in y direction """ 
        # Update ball position
        self.rect.y += self.change_y

        # Detect collisionswith walls
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for item in collisions:
            if self.change_y < 0:
                self.rect.top = item.rect.bottom
            self.change_y *= -1
            return     

        # Detect colisions with board 
        collisions = pygame.sprite.collide_rect(self, board)
        if collisions == 1:
            if self.change_y > 0:
                self.rect.bottom = board.rect.top 
            self.change_y *= -1
            pos_difference = (self.rect.x + self.rect.width/2) - (board.rect.x + board.rect.width/2)
            speed_difference = self.change_x + board.change_x
            self.change_x = limitNumber(int(pos_difference/4 + speed_difference), 10)
            return

         # Detect collision with cubes
        collisions = pygame.sprite.spritecollide(self, cubes, False)
        if len(collisions)>0:
            for item in collisions:
                if self.change_y < 0:
                    self.rect.top = item.rect.bottom
                else:
                    self.rect.bottom = item.rect.top

                item.cubeHit() 

            self.change_y *= -1
            return

        # Detect game lost



class Cube(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, life):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([width, height])
        self.image.fill((255,255-60*life,255-60*life))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set HP
        self.life = life

    def cubeHit(self):
        if self.life > 1:
            self.life -= 1
            self.image.fill((255,255-60*self.life,255-60*self.life))
        else:
            pygame.sprite.Sprite.kill(self)

class Board(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, width, height, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = GAME_SCREEN_HEIGHT - height
        self.rect.x = int((GAME_SCREEN_WIDTH-width)/2.)

    def changespeed(self, x):
        """ Change the speed of the board. Called with a keypress. """
        self.change_x += x

    def moveBoard(self, walls):
        """ Find a new position for the board """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for item in collisions:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = item.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = item.rect.right


def main():
    """ Main Program """
    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT])

    # Set the title of the window
    pygame.display.set_caption('Ball Game')

    # Create the bounce board
    board = Board(100,20,RED)
    board_list = pygame.sprite.Group()
    board_list.add(board)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(board)

    # Create the ball
    ball = Ball(10, RED)
    movingsprites.add(ball)


    area = boardArea1()

    clock = pygame.time.Clock()
 
    done = False

    while not done:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

            SPEED = 20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.changespeed(-SPEED)
                if event.key == pygame.K_RIGHT:
                    board.changespeed(SPEED)
                if event.key == pygame.K_SPACE:
                    ball.startBall()

 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    board.changespeed(SPEED)
                if event.key == pygame.K_RIGHT:
                    board.changespeed(-SPEED)

        # --- Move Objects --- #
        board.moveBoard(area.wall_list)
        ball.moveBall(area.wall_list, board, area.cubes_list)


        # --- Drawing ---
        screen.fill(BLACK)
 
        movingsprites.draw(screen)
        area.wall_list.draw(screen)
        area.cubes_list.draw(screen)
 
        pygame.display.flip()
 
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()