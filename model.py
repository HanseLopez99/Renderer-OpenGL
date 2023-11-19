from OpenGL.GL import *
import glm
from numpy import array, float32

class Model(object):
  def __init__(self, data):
    self.vertBuffer = array(data, dtype=float32)

    # Vertex buffer object
    self.VBO = glGenBuffers(1)

    # Vertex array object
    self.VAO = glGenVertexArrays(1)

    self.position = glm.vec3(0,0,0)
    self.rotation = glm.vec3(0,0,0)
    self.scale = glm.vec3(1,1,1)

  def getModelMatrix(self):
    identidad = glm.mat4(1)
    translateMat = glm.translate(identidad, self.position)

    pitch = glm.rotate(identidad, glm.radians(self.rotation.x), glm.vec3(1,0,0))
    yaw = glm.rotate(identidad, glm.radians(self.rotation.y), glm.vec3(0,1,0))
    roll = glm.rotate(identidad, glm.radians(self.rotation.z), glm.vec3(0,0,1))

    rotationMat = pitch * yaw * roll

    scaleMat = glm.scale(identidad, self.scale)

    return translateMat * rotationMat * scaleMat

  # Atamos los buffers del objeto a la GPU
  def render(self):
    glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
    glBindVertexArray(self.VAO)

    # Especificar la informacion de los vertices
    glBufferData(
      GL_ARRAY_BUFFER, # Buffer ID
      self.vertBuffer.nbytes, # Buffer size in bytes
      self.vertBuffer, # Buffer data 
      GL_STATIC_DRAW # Buffer usage
    )

    # Atributos, especificar que representa el contenido del vertice

    # Atributo de posiciones
    glVertexAttribPointer(
      0, # Atributo
      3, # Tamaño
      GL_FLOAT, # Tipo de dato
      GL_FALSE, # Normalizar
      4 * 6, # Stride 
      ctypes.c_void_p(0) # OffsetS
    )

    glEnableVertexAttribArray(0)

    # Atributo de colores
    glVertexAttribPointer(
      1, # Atributo
      3, # Tamaño
      GL_FLOAT, # Tipo de dato
      GL_FALSE, # Normalizar
      4 * 6, # Stride 
      ctypes.c_void_p(4 * 3) # OffsetS
    )

    glEnableVertexAttribArray(1)


    glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 6))