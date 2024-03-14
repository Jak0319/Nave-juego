import pygame
import random
#-----------------------------------------------------------------------------#
# Inicializar Pygame
pygame.init()
#-----------------------------------------------------------------------------#
# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
#-----------------------------------------------------------------------------#
# Definir constantes de la pantalla
#-----------------------------------------------------------------------------#
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
#-----------------------------------------------------------------------------#
# Clase para la nave espacial
#-----------------------------------------------------------------------------#
class NaveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("spaceship64.png").convert()            # Cargar imagen de la nave
        self.image.set_colorkey(NEGRO)                                         # Establecer color transparente
        self.rect = self.image.get_rect()                                      # Obtener el rectángulo de la imagen para el posicionamiento
        self.rect.centerx = ANCHO_PANTALLA // 2                                # Posicionar la nave en el centro inferior de la pantalla
        self.rect.bottom = ALTO_PANTALLA - 10                                  # Posicionar la nave en el centro inferior de la pantalla
        self.velocidad_x = 0                                                   # Inicializar la velocidad en el eje x
        self.vida = 200                                                        # Inicializar la vida de la nave
#-----------------------------------------------------------------------------#
    def update(self):
        self.rect.x += self.velocidad_x                                        # Actualizar la posición de la nave según su velocidad
        if self.rect.right > ANCHO_PANTALLA:                                   # Limitar la posición de la nave dentro de la pantalla
            self.rect.right = ANCHO_PANTALLA                                   # Limitar la posición de la nave dentro de la pantalla
        if self.rect.left < 0:                                                 # Limitar la posición de la nave dentro de la pantalla
            self.rect.left = 0                                                 # Limitar la posición de la nave dentro de la pantalla
#-----------------------------------------------------------------------------#
# Clase para los meteoritos
#-----------------------------------------------------------------------------#
class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor128.png").convert()             # Cargar imagen del meteorito
        self.image.set_colorkey(NEGRO)                                        # Establecer color transparente
        self.rect = self.image.get_rect()                                     # Obtener el rectángulo de la imagen para el posicionamiento
        self.reset()                                                          # Llamar al método reset para posicionar el meteorito inicialmente
#-----------------------------------------------------------------------------#
    def reset(self):
        self.rect.x = random.randrange(ANCHO_PANTALLA - self.rect.width)      # Posicionar el meteorito en una ubicación aleatoria arriba de la pantalla
        self.rect.y = random.randrange(-150, -100)                            # Ajuste en la posición inicial
        self.velocidad_y = random.randrange(1, 8)                             # Establecer una velocidad vertical aleatoria
#-----------------------------------------------------------------------------#
    def update(self):
        self.rect.y += self.velocidad_y                                       # Mover el meteorito hacia abajo
        if self.rect.top > ALTO_PANTALLA + 10:                                # Si el meteorito sale de la pantalla, reiniciar su posición
            self.reset()
#-----------------------------------------------------------------------------#
# Clase para los proyectiles
#-----------------------------------------------------------------------------#
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()   
        self.image = pygame.Surface((10, 20))   # Crear una superficie (proyectil) con un color rojo
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()       # Obtener el rectángulo de la imagen para el posicionamiento
        self.rect.bottom = y                    # Posicionar el proyectil en la ubicación inicial
        self.rect.centerx = x
        self.velocidad_y = -10                  # Establecer la velocidad del proyectil hacia arriba
#-----------------------------------------------------------------------------#
    def update(self):
        self.rect.y += self.velocidad_y         # Mover el proyectil hacia arriba
        if self.rect.bottom < 0:                # Si el proyectil sale de la pantalla, eliminarlo
            self.kill()
#-----------------------------------------------------------------------------#
# Función para mostrar el mensaje de Game Over
def mostrar_game_over(pantalla):
    fuente = pygame.font.Font(None, 36)                       # Crear una fuente para el texto
    texto_game_over = fuente.render("GAME OVER", True, ROJO)  # Renderizar el texto "GAME OVER" en rojo
    rect_game_over = texto_game_over.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))  # Obtener el rectángulo del texto para el posicionamiento
    rect_barra = pygame.Rect(0, ALTO_PANTALLA // 2 - 50, ANCHO_PANTALLA, 100)  
    pygame.draw.rect(pantalla, NEGRO, rect_barra)             # Dibujar la barra negra en la pantalla
    pantalla.blit(texto_game_over, rect_game_over)            # Dibujar el texto "GAME OVER" en la pantalla
#-----------------------------------------------------------------------------#
# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("DARK SPACE :)")
#-----------------------------------------------------------------------------#
# Cargar imagen de fondo
fondo = pygame.image.load("background.jpg").convert()
#-----------------------------------------------------------------------------#
# Crear lista de sprites y grupos de sprites
todos_los_sprites = pygame.sprite.Group()
meteoritos = pygame.sprite.Group()
proyectiles = pygame.sprite.Group()
#-----------------------------------------------------------------------------#
# Crear nave espacial
nave = NaveEspacial()
todos_los_sprites.add(nave)
#-----------------------------------------------------------------------------#
# Crear reloj
reloj = pygame.time.Clock()
#-----------------------------------------------------------------------------#
jugando = True     # Variable para el juego activo
game_over = False  # Variable para controlar el estado de Game Over
puntaje = 0        # Inicializar puntaje.
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
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

    # Actualizar sprites
    todos_los_sprites.update()
#-----------------------------------------------------------------------------#
    # Crear nuevos meteoritos si la cantidad actual es menor a 8
    if puntaje < 500:
        while len(meteoritos) < 8:
            meteorito = Meteorito()
            todos_los_sprites.add(meteorito)
            meteoritos.add(meteorito)
    elif puntaje < 1000:
        while len(meteoritos) < 16:
            meteorito = Meteorito()
            todos_los_sprites.add(meteorito)
            meteoritos.add(meteorito)
    else:
        while len(meteoritos) < 24:  # Aumentar aún más la cantidad de meteoritos
            meteorito = Meteorito()
            todos_los_sprites.add(meteorito)
            meteoritos.add(meteorito)
            
    # Detectar colisiones entre proyectiles y meteoritos
    colisiones = pygame.sprite.groupcollide(proyectiles, meteoritos, True, True)

    # Actualizar puntaje si hay colisiones
    for colision in colisiones:
        puntaje += 5

    # Verificar colisiones entre la nave y los meteoritos
    for meteorito in pygame.sprite.spritecollide(nave, meteoritos, True):
        nave.vida -= 10

    # Verificar si la vida de la nave ha llegado a 0
    if nave.vida <= 0:
        game_over = True

    # Dibujar fondo
    pantalla.blit(fondo, (0, 0))

    # Dibujar pantalla
    todos_los_sprites.draw(pantalla)

    # Dibujar barra de vida
    pygame.draw.rect(pantalla, ROJO, (10, 10, 200, 20), 2)
    pygame.draw.rect(pantalla, VERDE, (10, 10, nave.vida, 20))

    # Dibujar puntaje
    texto_puntaje = pygame.font.Font(None, 24).render("Puntaje: " + str(puntaje), True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 40))

    # Si el juego está en modo game over, mostrar el mensaje de game over
    if game_over:
        mostrar_game_over(pantalla)

    pygame.display.flip()    # Actualizar pantalla

    # Limitar FPS
    reloj.tick(60)

# Cerrar Pygame
pygame.quit()
