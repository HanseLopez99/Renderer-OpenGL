import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from shaders import *


width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader, fragment_shader)

modelos = [
    Model("models/human.obj", glm.vec3(0, -1.5, -5), glm.vec3(0, 0, 0), glm.vec3(0.03, 0.03, 0.03)),
    Model("models/monkey.obj", glm.vec3(0, -1.5, -5), glm.vec3(-90, 0, 0), glm.vec3(0.06, 0.06, 0.06)),
    Model("models/stone.obj", glm.vec3(0, -0.5, -5), glm.vec3(-90, 0, 0), glm.vec3(0.5, 0.5, 0.5)),
    Model("models/table.obj", glm.vec3(0, -1, -5), glm.vec3(0, 90, 0), glm.vec3(2, 2, 2)),
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

isRunning = True
while isRunning:
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_1:
                rend.scene.clear()
                rend.scene.append(modelos[0])
            elif event.key == pygame.K_2:
                rend.scene.clear()
                rend.scene.append(modelos[1])
            elif event.key == pygame.K_3:
                rend.scene.clear()
                rend.scene.append(modelos[2])
            elif event.key == pygame.K_4:
                rend.scene.clear()
                rend.scene.append(modelos[3])
            elif event.key == pygame.K_5:
                rend.scene.clear()
                rend.scene.append(modelos[4])
            elif event.key == pygame.K_6:
                rend.scene.clear()
                rend.scene.append(modelos[5])

    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime
    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime

    if keys[K_w]:
        rend.camPosition.y += 5 * deltaTime
    elif keys[K_s]:
        rend.camPosition.y -= 5 * deltaTime

    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime

    if keys[K_UP]:
        rend.camRotation.x += 45 * deltaTime
    elif keys[K_DOWN]:
        rend.camRotation.x -= 45 * deltaTime

    if keys[K_LEFT]:
        rend.camRotation.y += 45 * deltaTime
    elif keys[K_RIGHT]:
        rend.camRotation.y -= 45 * deltaTime

    rend.elapsedTime += deltaTime

    rend.render()
    pygame.display.flip()

pygame.quit()

    