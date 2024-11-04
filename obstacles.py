import pygame

from config import *
from os.path import join
from pygame.sprite import Sprite

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