import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from shaders import *


width = 1080
height = 720

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader, fragment_shader)

modelos = [
    Model("models/human.obj", glm.vec3(0, -1.5, -5), glm.vec3(0, 90, 0), glm.vec3(0.03, 0.03, 0.03)),
    Model("models/monkey.obj", glm.vec3(0, -1.5, -5), glm.vec3(-90, 0, 0), glm.vec3(0.06, 0.06, 0.06)),
    Model("models/stone.obj", glm.vec3(0, -0.5, -5), glm.vec3(-90, 0, 0), glm.vec3(0.5, 0.5, 0.5)),
    Model("models/table.obj", glm.vec3(0, -1, -5), glm.vec3(0, 0, 0), glm.vec3(2, 2, 2)),
    Model("models/thunderphone.obj", glm.vec3(0, 0, -5), glm.vec3(0, 0, 0), glm.vec3(0.05, 0.05, 0.05)),
    Model("models/model.obj", glm.vec3(0, 0, -5), glm.vec3(0, 0, 0), glm.vec3(1.5, 1.5, 1.5)),
]

modelos[0].loadTexture("textures/human.bmp")
modelos[1].loadTexture("textures/monkey.bmp")
modelos[2].loadTexture("textures/stone.bmp")
modelos[3].loadTexture("textures/table.bmp")
modelos[4].loadTexture("textures/thunderphone.bmp")
modelos[5].loadTexture("textures/model.bmp")

rend.scene.append(modelos[0])

# Variables para controlar la cámara y el modelo
angulo_horizontal = 0 # Ángulo horizontal de la cámara
angulo_vertical = 0 # Ángulo vertical de la cámara
radio = 10 # Distancia de la cámara al origen
zoom_min = 0.1 # Distancia mínima de la cámara al origen
zoom_max = 10 # Distancia máxima de la cámara al origen
modelo_actual = 0 # Índice del modelo actual
shader_actual = 0 # Índice del shader actual

# Calcular el punto medio para el zoom inicial
zoom_inicial = (zoom_min + zoom_max) / 2

# Usar zoom_inicial como valor inicial para el zoom
zoom = zoom_inicial

# Variables para rastrear si una tecla está presionada
tecla_q_presionada = False
tecla_e_presionada = False

# Bucle principal
isRunning = True
while isRunning:
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[2]:  # Botón derecho del mouse presionado
                xoffset = event.rel[0] * 0.1
                yoffset = -event.rel[1] * 0.1
                angulo_horizontal += xoffset
                angulo_vertical = max(-89, min(89, angulo_vertical + yoffset))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll hacia arriba
                radio = max(zoom_min, radio - 1)
            elif event.button == 5:  # Scroll hacia abajo
                radio = min(zoom_max, radio + 1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key==pygame.K_SPACE:
                rend.toggleFilledMode()
            elif event.key==pygame.K_7:
                rend.setShaders(fat_vertex_shader, fragment_shader)
            elif event.key==pygame.K_8:
                rend.setShaders(vertex_shader, toon_shader)
            elif event.key==pygame.K_9:
                rend.setShaders(vertex_shader, gourad_shader)
            elif event.key==pygame.K_0:
                rend.setShaders(vertex_shader, unlit_shader)
            elif event.key >= pygame.K_1 and event.key <= pygame.K_6:
                # Cambiar modelo
                num_modelo = event.key - pygame.K_1
                if num_modelo < len(modelos):
                    rend.scene.clear()
                    rend.scene.append(modelos[num_modelo])
                    modelo_actual = num_modelo
                    print(f"Cambiado al modelo {modelo_actual}")

    # Actualizar posición de la cámara
    rend.camPosition.x = radio * glm.sin(glm.radians(angulo_horizontal)) * glm.cos(glm.radians(angulo_vertical))
    rend.camPosition.y = radio * glm.sin(glm.radians(angulo_vertical))
    rend.camPosition.z = radio * glm.cos(glm.radians(angulo_horizontal)) * glm.cos(glm.radians(angulo_vertical))
    rend.update()

    # Rotar modelo con WASD
    if keys[K_w]:
        modelos[modelo_actual].rotate(glm.vec3(1, 0, 0))
    if keys[K_s]:
        modelos[modelo_actual].rotate(glm.vec3(-1, 0, 0))
    if keys[K_a]:
        modelos[modelo_actual].rotate(glm.vec3(0, 1, 0))
    if keys[K_d]:
        modelos[modelo_actual].rotate(glm.vec3(0, -1, 0))

    rend.elapsedTime += deltaTime
    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()

    