import pygame

from config import *
from os.path import join
from pygame.sprite import Sprite

def create_obstacles():
    """
    Cria os obstáculos e os adiciona ao grupo de sprites
    """
    
    for obstacle in range(4):   # Delimita a quantidade de obstaculos
        
        # Dimensionaliza o tamanho do obstaculo
        for x in range(0, 180, 5):
            for y in range(0, 60, 5):

                # Molda a estrutura do obstaculo
                if 463 + y >= 496 and 66 <= 33 + x <= 170:
                    continue
                
                # Desloca o posicionamento da estrutura
                coordenate_x = 342 * obstacle + 33 + x
                coordenate_y = 463 + y

                # Determina a opacidade dos pixels do obstaculo                
                OpacityControl = 5

                # Cria e adiciona o obstaculo
                obs = Obstacle(OpacityControl, coordenate_x, coordenate_y)
                obstacle_group.add(obs)

class Obstacle(Sprite):
    """
    Classe para representar cada obstáculo
    """

    def __init__(self, size, x, y):
        """
        Inicializa o sprite do obstáculo e define sua posição
        """
        
        # Confere quantidade e caracteristicas ao obstaculo
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.obstacles_amount = 4