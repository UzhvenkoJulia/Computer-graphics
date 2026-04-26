import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image # Бібліотека Pillow для читання файлів зображень (.jpg, .png)

# 1. Шейдери
vertex_src = """
#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTexCoord;

out vec2 TexCoord;
uniform vec2 offset; // Зсув для кожного прямокутника, uniform змінна — це параметр, який однаковий для всіх вершин при одному малюванні 

void main() {
    gl_Position = vec4(aPos + offset, 0.0, 1.0);
    TexCoord = aTexCoord;
}
"""

fragment_src = """
#version 330 core
out vec4 FragColor;
in vec2 TexCoord;
uniform sampler2D texture1;

void main() {
    FragColor = texture(texture1, TexCoord);
}
"""

# Функція завантаження текстури (картинки)
def load_texture(path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "1. Три текстуровані прямокутники", None, None)
    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

    # Вершини одного прямокутника (X, Y, TexX, TexY)
    # Зроблю його невеликим, щоб три помістилися на екрані
    vertices = np.array([
        # Трикутник 1
        -0.2, -0.3,   0.0, 0.0,
         0.2, -0.3,   1.0, 0.0,
         0.2,  0.3,   1.0, 1.0,
        # Трикутник 2
        -0.2, -0.3,   0.0, 0.0,
         0.2,  0.3,   1.0, 1.0,
        -0.2,  0.3,   0.0, 1.0
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Координати
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # Текстурні координати
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)

    tex1 = load_texture("tex1.jpg")
    tex2 = load_texture("tex2.jpg")
    tex3 = load_texture("tex3.jpg")

    glUseProgram(shader)
    offset_loc = glGetUniformLocation(shader, "offset")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(VAO)

        # Малюю 1-й прямокутник (зліва)
        glBindTexture(GL_TEXTURE_2D, tex1)
        glUniform2f(offset_loc, -0.6, 0.0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # Малюю 2-й прямокутник (по центру)
        glBindTexture(GL_TEXTURE_2D, tex2)
        glUniform2f(offset_loc, 0.0, 0.0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # Малюю 3-й прямокутник (справа)
        glBindTexture(GL_TEXTURE_2D, tex3)
        glUniform2f(offset_loc, 0.6, 0.0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()