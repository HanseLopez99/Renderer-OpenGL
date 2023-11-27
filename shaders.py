# En OpenGL, los shaders se escriben en un nuevo lenguaje de programacion llamada GLSL
# Graphics Library Shader Language

vertex_shader = '''
# version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 outNormals;
out vec3 outPosition;

void main()
{
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(position,1.0);
    UVs = texCoords;
    outNormals = (modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    outPosition = position;
}
'''

fragment_shader = '''
  #version 450 core

  layout (binding=0) uniform sampler2D tex;

  in vec2 UVs;
  in vec3 outNormals;

  out vec4 fragColor;

  void main()
  {
    fragColor = texture(tex, UVs);
  }

'''

fat_vertex_shader = '''
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float fatness;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    outNormals  =(modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position+(fatness/4)*outNormals;
    
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(pos,1.0);
    UVs = texCoords;
}
'''

toon_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    if (intensity<0.33)
        intensity=0.2;
    else if (intensity<0.66)
        intensity=0.6;
    else
        intensity=1.0;
    fragColor = texture(tex,UVs)*intensity;
}

'''

gourad_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    fragColor = texture(tex,UVs)*intensity;
}

'''

unlit_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex,UVs);
}

'''

skybox_vertex_shader = '''
#version 450 core
layout (location=0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix*viewMatrix*vec4(inPosition,1.0);
}
'''

skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox,texCoords);
}

'''