import pygame
import sys

# 1. Inicializar Pygame y el módulo de Joysticks
pygame.init()
pygame.joystick.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Control de Xbox con Pygame")
clock = pygame.time.Clock()

# 2. Conectar e inicializar el control de Xbox
joysticks = []
if pygame.joystick.get_count() > 0:
    # Obtener el primer control conectado
    xbox_controller = pygame.joystick.Joystick(0)
    xbox_controller.init()
    joysticks.append(xbox_controller)
    print(f"Control detectado: {xbox_controller.get_name()}")
else:
    print("No se detectó ningún control de Xbox. Conéctalo antes de iniciar.")

# Variables de la entidad (un cuadrado móvil)
x, y = WIDTH // 2, HEIGHT // 2
speed = 2
color = (0, 128, 255) # Azul por defecto

# Umbral de zona muerta (evita el movimiento por el desgaste del stick)
DEADZONE = 0.2

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos basados en el control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Detectar cuando se presiona un botón
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # Botón A
                color = (0, 255, 128) # Cambia a Verde
                print("Presionaste el botón A")
                
        # Detectar cuando se suelta un botón
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:  # Botón A
                color = (0, 128, 255) # Vuelve a Azul

    # 3. Leer movimiento continuo desde las palancas analógicas (fuera del bucle de eventos)
    if joysticks:
        # Leer el eje horizontal (0) y vertical (1) del stick izquierdo
        axis_x = xbox_controller.get_axis(0)
        axis_y = xbox_controller.get_axis(1)
        
        # Aplicar la zona muerta para evitar derivas no deseadas
        if abs(axis_x) > DEADZONE:
            x += axis_x * speed
        if abs(axis_y) > DEADZONE:
            y += axis_y * speed

    # Mantener el cuadrado dentro de los límites de la ventana
    x = max(0, min(WIDTH - 50, x))
    y = max(0, min(HEIGHT - 50, y))

    # Renderizado de gráficos
    screen.fill((30, 30, 30)) # Fondo gris oscuro
    pygame.draw.rect(screen, color, (int(x), int(y), 50, 50)) # Dibujar cuadrado
    
    pygame.display.flip()
    clock.tick(60) # Limitar a 60 FPS

pygame.quit()
sys.exit()
