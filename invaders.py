import pygame
import random
from config import *
from os.path import join
from fire import Fire


def check_invader_position() -> None:
    '''
        Checa a posição do invader
        
        Se qualquer um dos invaders encostarem nas bordas, altera sentido horizontal e desce 10
        pixels em y se não for o boss
    '''

    # inicialmente False, mantendo a movimentação horizontal
    change_direction = False
    all_invaders = invader_group.sprites()
    # checa se qualquer um dos invaders interagiu com a borda delimitada como "LARGURA_TELA" e
    # invader.rect.left
    for invader in all_invaders:
        if invader.rect.right >= LARGURA_TELA or invader.rect.left <= 0:
            change_direction = True
            break
    
    # change_direction sendo True, altera o sentido de movimento e desce 10 pixels em y, caso o
    # nivel atual não seja divisivel por 10 (boss)
    if change_direction:
        for invader in all_invaders:
            invader.direction *= -1
            if invader.nivel % 10 != 0:
                invader.rect.y += 10


def invaders_fire(attack_speed):
    '''
    Definindo o sprite do tiro dos invaders:\n
    Caso o evento de tiro seja triggered, um invader
    aleatório será selecionado para originar o ataque,
    criando uma classe Fire e adicionando a grupo invader_fire
    '''
    if invader_group.sprites(): 
        random_invader = random.choice(invader_group.sprites()) 
        fire = Fire(random_invader.rect.center, attack_speed, invader_fire) 
        invader_fire.add(fire)

class Invaders(pygame.sprite.Sprite):
    def __init__(self, x, y, nivel):
        super().__init__()

        self.nivel = nivel
        self.boss = nivel % 10 == 0
        if not self.boss:
            invader_type = random.randint(0,1)
            if invader_type == 0:
                frame1 = pygame.image.load(join('images', 'frame1_invader0.png')).convert_alpha()
                frame2 = pygame.image.load(join('images', 'frame2_invader0.png')).convert_alpha()

            else:
                frame1 = pygame.image.load(join('images', 'frame1_invader1.png')).convert_alpha()
                frame2 = pygame.image.load(join('images', 'frame2_invader1.png')).convert_alpha()
        else:
            self.health_start = nivel
            self.health_left = nivel
            invader_type = 2
            frame1 = pygame.image.load(join('images', 'frame1_boss_1.png')).convert_alpha()
            frame2 = pygame.image.load(join('images', 'frame2_boss_1.png')).convert_alpha()

        self.frames = [frame1, frame2]
        self.x = x
        self.y = y

        self.reward = 10 if invader_type == 0 else 20 if invader_type == 1 else 500
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = 2 + nivel // 10

    def animation_state(self):
        self.animation_index += 0.02
        if self.animation_index >= len(self.frames): 
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)] 

    def update(self):
        self.animation_state()
        if not self.boss:
            self.rect.x += self.direction
        else:
            pygame.draw.rect(display, RED, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 5))

            if self.health_left > 0:
                pygame.draw.rect(display, GREEN, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_left / self.health_start)), 5))

            self.rect.x += self.direction


class SpecialInvader(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(join('images', 'frame1_invader1.png')).convert_alpha()
        
        self.reward = random.choice([150, 200, 250])
        screen_side = random.choice([LARGURA_TELA + 30, -30])
        if screen_side > 0:
            self.speed = -4
        else:
            self.speed = 4
        
        self.rect = self.image.get_rect(topleft=(screen_side, 30))

    def update(self):
        self.rect.x += self.speed
        if not (-40 < self.rect.x < LARGURA_TELA + 40):
            self.kill()