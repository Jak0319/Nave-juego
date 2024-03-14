import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir constantes de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Clase para la nave espacial
class NaveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("spaceship64.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10
        self.velocidad_x = 0

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA
        if self.rect.left < 0:
            self.rect.left = 0

# Clase para los meteoritos
class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor128.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randrange(-150, -100)  # Ajuste en la posición inicial
        self.velocidad_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO_PANTALLA + 10:
            self.rect.x = random.randrange(ANCHO_PANTALLA - self.rect.width)
            self.rect.y = random.randrange(-150, -100)  # Ajuste en la posición inicial
            self.velocidad_y = random.randrange(1, 8)

# Clase para los proyectiles
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego de Nave Espacial")

# Crear lista de sprites y grupos de sprites
todos_los_sprites = pygame.sprite.Group()
meteoritos = pygame.sprite.Group()
proyectiles = pygame.sprite.Group()

# Crear nave espacial
nave = NaveEspacial()
todos_los_sprites.add(nave)

# Crear meteoritos
for i in range(8):
    meteorito = Meteorito()
    todos_los_sprites.add(meteorito)
    meteoritos.add(meteorito)

# Crear reloj
reloj = pygame.time.Clock()

# Variable para el juego activo
jugando = True

# Bucle principal del juego
while jugando:
    # Procesar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                nave.velocidad_x = -5
            elif evento.key == pygame.K_RIGHT:
                nave.velocidad_x = 5
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                nave.velocidad_x = 0
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Disparar con clic izquierdo
            proyectil = Proyectil(nave.rect.centerx, nave.rect.top)
            todos_los_sprites.add(proyectil)
            proyectiles.add(proyectil)

    # Detectar colisiones entre proyectiles y meteoritos
    colisiones = pygame.sprite.groupcollide(proyectiles, meteoritos, True, True)

    # Actualizar sprites
    todos_los_sprites.update()

    # Dibujar pantalla
    pantalla.fill(BLANCO)
    todos_los_sprites.draw(pantalla)

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar FPS
    reloj.tick(60)

# Cerrar Pygame
pygame.quit()
