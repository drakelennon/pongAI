'''Média de tempo de treinamento: 1m:30s'''

import pygame
import neat
import sys, os, time
from pygame.locals import *

pygame.init()

# tela
WIDTH, HEIGHT = 1024, 768
TELA = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong AI')

FONT = pygame.font.SysFont('comicsansms', 20, True, False)


# classes
class RaqueteUm:
    def __init__(self):
        self.posX = 20
        self.posY = HEIGHT / 2
        self.tamX = 18
        self.tamY = 150
        self.cor = (255, 255, 255)
        self.rect = pygame.Rect(self.posX, self.posY, self.tamX, self.tamY)
        self.velY = 0
        self.pontos = 0
        self.inicio = time.time()
        self.fim = 0
        self.tempo_vida = 0

    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.posY += self.velY

        self.fim = time.time()
        self.tempo_vida = self.fim - self.inicio

        if (self.posY + self.tamY) >= HEIGHT:
            self.posY = HEIGHT - self.tamY
        elif self.posY <= 0:
            self.posY = 0

    def move_cima(self):
        self.velY = -RAQ_VEL

    def move_baixo(self):
        self.velY = RAQ_VEL
    
    def draw(self):
        pygame.draw.rect(TELA, self.cor, self.rect, 0)

class RaqueteDois(RaqueteUm):
    def __init__(self):
        super().__init__()
        self.posX = WIDTH - 20 - self.tamX

class Bola:
    def __init__(self):
        self.posX = WIDTH / 2
        self.posY = HEIGHT / 2
        self.tamX = 20
        self.tamY = 20
        self.cor = (255, 255, 255)
        self.rect = pygame.Rect(self.posX, self.posY, self.tamX, self.tamY)
        self.velX = BOLA_VEL
        self.velY = BOLA_VEL

    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.posX += self.velX
        self.posY += self.velY

        if (self.posY + self.tamY) <= 0:
            self.velY = -self.velY
        elif self.posY >= HEIGHT:
            self.velY = -self.velY
    
    def reset(self):
        self.posX = WIDTH / 2
        self.posY = HEIGHT / 2
        self.velX = -self.velX
        self.velY = -self.velY

    def draw(self):
        pygame.draw.rect(TELA, self.cor, self.rect, 0)

# contants
BOLA_VEL = 12
RAQ_VEL= 18
INICIO = time.time()

# variaveis
ticks = 1
fim = time.time()
gols = 0
        
# funcoes
def remove_raquete_esq(i):
    ge[i].fitness -= .1
    raquetes_esq.pop(i)
    ge.pop(i)
    redes.pop(i)

def remove_raquete_dir(i):
    ge2[i].fitness -= .1
    raquetes_dir.pop(i)
    ge2.pop(i)
    redes2.pop(i)

# main
def treinar(genomas, config):
    global raquetes_dir, raquetes_esq, ge, ge2, redes, redes2, count_dir, count_esq, ticks, tempo_vivo, fim, gols
    bola = Bola()
    raquetes_esq = []
    raquetes_dir = []
    ge = []
    ge2 = []
    redes = []
    redes2 = []

    def stats():
        text_ger = FONT.render(f'Geração: {p.generation + 1}', True, (255, 255, 255))
        text_tmp = FONT.render(f'Treinando IA: {int(tempo_vivo)}s', True, (255, 255, 255))
        text_gls = FONT.render(f'Gols: {int(gols)}', True, (255, 255, 255))

        TELA.blit(text_ger, (450, 35))
        TELA.blit(text_tmp, (420, 10))
        TELA.blit(text_gls, (480, 60))

    def sucesso():
        text_ger = FONT.render(f'Geração: {p.generation + 1}', True, (255, 255, 255))
        text_tmp = FONT.render(f'Concluído em: {int(tempo_vivo)}s', True, (255, 255, 255))
        text_gls = FONT.render(f'Foram necessários {int(gols)} gols para treinar', True, (255, 255, 255))

        TELA.blit(text_ger, (450, 35))
        TELA.blit(text_tmp, (420, 10))
        TELA.blit(text_gls, (310, 60))

    for id_genoma, genoma in genomas:
        raquetes_esq.append(RaqueteUm())
        ge.append(genoma)
        rede = neat.nn.FeedForwardNetwork.create(genoma, config)
        redes.append(rede)
        genoma.fitness = 0

    for id_genoma2, genoma2 in genomas:
        raquetes_dir.append(RaqueteDois())
        ge2.append(genoma2)
        rede2 = neat.nn.FeedForwardNetwork.create(genoma2, config)
        redes2.append(rede2)
        genoma2.fitness = 0

    clock = pygame.time.Clock()
    RUN = True
    count_esq = 24
    count_dir = 24
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                RUN = False

            key = pygame.key.get_pressed()

            if event.type == KEYDOWN:
                if key[K_1]:
                    ticks = 1
                if key[K_2]:
                    ticks = 2
                if key[K_3]:
                    ticks = 3
                if key[K_4]:
                    ticks = 4
                if key[K_5]:
                    ticks = 5

            '''if key[K_DOWN]:
                    raquete_um.velY = RAQ_VEL
                elif key[K_UP]:
                    raquete_um.velY = -RAQ_VEL
            if event.type == KEYUP:
                raquete_um.velY = 0

            if event.type == KEYDOWN:
                if key[K_DOWN]:
                    raquete_dois.velY = RAQ_VEL
                elif key[K_UP]:
                    raquete_dois.velY = -RAQ_VEL
            if event.type == KEYUP:
                raquete_dois.velY = 0'''
        
        TELA.fill((0, 0, 0))

        if len(raquetes_esq) > 0 and len(raquetes_dir) > 0:

            tempo_vivo = fim - INICIO
            
            dist_ball_x_esq = raquetes_esq[count_esq].rect.center[0] - bola.rect.center[0]
            dist_ball_y_esq = raquetes_esq[count_esq].rect.center[1] - bola.rect.center[0]

            dist_ball_x_dir = raquetes_dir[count_dir].rect.center[0] - bola.rect.center[0]
            dist_ball_y_dir = raquetes_dir[count_dir].rect.center[1] - bola.rect.center[0]

            if bola.rect.colliderect(raquetes_esq[count_esq].rect):
                ge[count_esq].fitness += .3
                bola.velX = BOLA_VEL
                raquetes_esq[count_esq].pontos += 1
            elif bola.rect.colliderect(raquetes_dir[count_dir].rect):
                ge2[count_dir].fitness += .3
                bola.velX = -BOLA_VEL
                raquetes_dir[count_dir].pontos += 1
                

            if bola.posX >= WIDTH + 25:
                remove_raquete_dir(count_dir)
                count_dir -= 1
                bola.reset()
                gols += 1
                if len(raquetes_dir) != 0:
                    raquetes_dir[count_dir].inicio = time.time()
                    raquetes_dir[count_dir].tempo_vida = 0
                
            elif bola.posX <= -25:
                remove_raquete_esq(count_esq)
                count_esq -= 1
                bola.reset()
                gols += 1
                if len(raquetes_esq) != 0:
                    raquetes_esq[count_esq].inicio = time.time()
                    raquetes_esq[count_esq].tempo_vida = 0

            if len(raquetes_esq) != 0 and len(raquetes_dir) != 0:
                
                if len(redes) != 0:
                    output_esq = redes[count_esq].activate((dist_ball_x_esq, dist_ball_y_esq, bola.velY, bola.posY, raquetes_esq[count_esq].rect.center[1]))

                    if output_esq[0] > output_esq[1]:
                        raquetes_esq[count_esq].move_cima()
                    else:
                        raquetes_esq[count_esq].move_baixo()

                if len(redes2) != 0:
                    output_dir = redes2[count_dir].activate((dist_ball_x_dir, dist_ball_y_dir, bola.velY, bola.posY, raquetes_dir[count_dir].rect.center[1]))

                    if output_dir[0] > output_dir[1]:
                        raquetes_dir[count_dir].move_cima()
                    else:
                        raquetes_dir[count_dir].move_baixo()

                if int(raquetes_esq[count_esq].tempo_vida) >= 10 and int(raquetes_dir[count_dir].tempo_vida) >= 10:
                    ticks = 1
                    sucesso()
                else:
                    fim = time.time()
                    ticks = 10
                    stats()
                
                raquetes_esq[count_esq].update()
                raquetes_esq[count_esq].draw()
                raquetes_dir[count_dir].update()
                raquetes_dir[count_dir].draw()

                bola.update()
                bola.draw()

        if len(raquetes_esq) == 0 or len(raquetes_dir) == 0:
            break
        
        
        clock.tick(60 * ticks)
        pygame.display.flip()

def run(config_path):
    global p, winner
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    p.add_reporter(statistics)

    winner = p.run(treinar, 1000)

def main():
    if __name__ == '__main__':
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'C:/Users/drake/vsCode/PythonProjects/pongAI/config.txt')
        run(config_path)


main()