import pygame
import random
from .player import Player
pygame.init()


class GameInformation:
    def __init__(self, score):
        self.score = score


class Game:
    
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (110, 110, 110)

    score = 0
    tries = 0
    WIDTH = 0
    HEIGHT = 0

    
    gridsize = 6
    gamegrid = [[]]
    cellspacing = 3
    cellh = 0
    cellw = 0

    def __init__(self, window, window_width, window_height):
        self.player = Player()
        self.window_width = window_width
        self.window_height = window_height
        self.window = window

        self.WIDTH = window_width
        self.HEIGHT = window_height

        self.top = window_height / 6

        self.cellh = (window_height - self.top) / self.gridsize - self.cellspacing
        self.cellw = (window_width) / self.gridsize - self.cellspacing

        self.gamegrid = [[0 for _ in range(self.gridsize)] for _ in range(self.gridsize)]

        self.score = 0
        self.tries = 0
        self.states = 0



    def draw(self):
        self.window.fill(self.RED)
        self.gamegrid, self.score = self.player.move(self.gamegrid)

        if self.gamegrid[0][0] == -10:
            self.reset()
            return

        pygame.draw.rect(self.window, self.GRAY, (0 , self.HEIGHT/6,    self.WIDTH, self.HEIGHT))
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if self.gamegrid[i][j] == 0:
                    pygame.draw.rect(self.window, self.BLACK, (
                        self.cellspacing * (i+1) + self.cellw * i ,
                        self.cellspacing * (j+1) + self.cellh * j + self.top,
                        self.cellw, self.cellh))
                elif self.gamegrid[i][j] == 1:
                    pygame.draw.rect(self.window, self.RED, (
                        self.cellspacing * (i+1) + self.cellw * i ,
                        self.cellspacing * (j+1) + self.cellh * j + self.top,
                        self.cellw, self.cellh))
                else :
                    pygame.draw.rect(self.window, self.WHITE, (
                        self.cellspacing * (i+1) + self.cellw * i ,
                        self.cellspacing * (j+1) + self.cellh * j + self.top,
                        self.cellw, self.cellh))


        self._draw_score()
        self.states += 1

    def loop(self):
        pass
        

    def _draw_score(self):
        score_text = self.SCORE_FONT.render(
            f"{self.score}", 1, self.BLACK)
        
        self.window.blit(score_text, (self.window_width / 2, 20))

        
        tries_text = self.SCORE_FONT.render(
            f"{self.tries}", 1, self.BLACK)
        
        self.window.blit(tries_text, (20, 20))

        states_text = self.SCORE_FONT.render(
            f"{self.states}", 1, self.BLACK)
        self.window.blit(states_text, (self.window_width / 1.32, 20))

    def reset(self):
        
        self.score = 0
        self.tries +=1
        self.states = 0
        self.player.reset()
        self.gamegrid = [[0 for _ in range(self.gridsize)] for _ in range(self.gridsize)]