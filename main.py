from snake import Game
import pygame
import neat
import os
import time
import pickle

class snakeGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.score = self.game.score

    def play(self):
        clock = pygame.time.Clock()
        run = True
        dir = 0
        while run:
            clock.tick(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("Detected")
            if keys[pygame.K_w]:
                dir = 12
            if keys[pygame.K_d]:
                dir = 3
            if keys[pygame.K_s]:
                dir = 6
            if keys[pygame.K_a]:
                dir = 9
            
            self.game.player.updatedir(dir)

            game_info = self.game.loop()
            self.game.draw()
            pygame.display.update()
            print(self.game.player.distleft)
            print(self.game.player.diststraight)
            print(self.game.player.distright)
            print("")

        
    def test_ai(self, genome, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome, config)

        
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            """
            output1 = net1.activate((self.game.player.distleft,
                                     self.game.player.diststraight,
                                     self.game.player.distright,
                                     self.game.player.curplace[0] - self.game.player.foodplace[0],
                                     self.game.player.curplace[1] - self.game.player.foodplace[1]
                                     ))
            """
            output1 = net1.activate((self.game.player.distleft,
                                     self.game.player.diststraight,
                                     self.game.player.distright,
                                     self.game.player.curplace[0] - self.game.player.foodplace[0],
                                     self.game.player.curplace[1] - self.game.player.foodplace[1]
                                     ))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                self.game.player.updatedir(12)
            elif decision1 == 1:
                self.game.player.updatedir(3)
            elif decision1 == 2:
                self.game.player.updatedir(6)
            elif decision1 == 3:
                self.game.player.updatedir(9)

            game_info = self.game.loop()
            self.game.draw()
            pygame.display.update()

        pygame.quit()

    def train_ai(self, genome1, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        old = 0
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.game.player.distleft,
                                     self.game.player.diststraight,
                                     self.game.player.distright,
                                     self.game.player.curplace[0] - self.game.player.foodplace[0],
                                     self.game.player.curplace[1] - self.game.player.foodplace[1]
                                     ))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                self.game.player.updatedir(12)
            elif decision1 == 1:
                self.game.player.updatedir(3)
            elif decision1 == 2:
                self.game.player.updatedir(6)
            elif decision1 == 3:
                self.game.player.updatedir(9)
            

            #game_info = self.game.loop()
            self.game.draw()
            pygame.display.update()
            if self.game.score != old:
                genome1.fitness += self.game.score
                old = self.game.score

            if self.game.score >= 100 or self.game.tries > 0 or self.game.player.static_states > 2000:
                self.calculate_fitness(genome1)
                break

    def calculate_fitness(self, genome1):
        genome1.fitness +=  self.game.score 


def eval_genomes(genomes, config):
    width, height = 600, 700
    window = pygame.display.set_mode((width,height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        if i == len(genomes) -1:
            break
        
        game = snakeGame(window, width, height)
        game.train_ai(genome1, config)

def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint(
       # r'C:/Users/lndnc/OneDrive/Desktop/AI test/dump/neat-checkpoint-4299')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    checkpoint_prefix = os.path.join("dump", "neat-checkpoint-")
    p.add_reporter(neat.Checkpointer(100, filename_prefix=checkpoint_prefix))

    winner = p.run(eval_genomes, 50000)

    with open("best.pickle", "wb" ) as f:
        pickle.dump(winner, f)

    best_genome = stats.best_genome()
    print("\nBest Genome:\n", best_genome)

def test_ai(config):
    width, height = 600, 700
    window = pygame.display.set_mode((width,height))
    with open("best.pickle", "rb" ) as f:
        winner = pickle.load(f)

    game = snakeGame(window,width,height)
    game.test_ai(winner, config)

if __name__ == '__main__':
    width, height = 600, 700
    window = pygame.display.set_mode((width,height))

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    

    game = snakeGame(window,width,height)
    #game.play()
    run_neat(config)
    #test_ai(config)
    
