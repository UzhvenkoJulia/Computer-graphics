import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
import math

# Шейдери
# матриця трансформації (u_transform), щоб рухати та обертати об'єкт

vertex_src = """
#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTexCoord;

out vec2 TexCoord;
uniform mat4 u_transform; 

void main() {
    gl_Position = u_transform * vec4(aPos, 0.0, 1.0);
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
    
    # вікно 800x800, щоб було зручно рахувати координати
    window = glfw.create_window(800, 800, "2.4 Keyboard and Mouse", None, None)
    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

    # Вершини прямокутника (позиція x, y та координати текстури)
    vertices = np.array([
        -0.2, -0.2,  0.0, 0.0,
         0.2, -0.2,  1.0, 0.0,
         0.2,  0.2,  1.0, 1.0,
        -0.2,  0.2,  0.0, 1.0
    ], dtype=np.float32)

    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)

    texture = load_texture("tex1.jpg") 
    glUseProgram(shader)
    transform_loc = glGetUniformLocation(shader, "u_transform")

    pos_x, pos_y = 0.0, 0.0  
    angle = 0.0              
    speed = 0.02             # швидкість руху

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # рух - клавіатура
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            pos_x -= speed
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            pos_x += speed
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            pos_y += speed
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            pos_y -= speed

        # мишка - обертання при наведенні
        # позиція курсора в пікселях
        mouse_x, mouse_y = glfw.get_cursor_pos(window)
        width, height = glfw.get_window_size(window)

        # пікселі в координати OpenGL (від -1.0 до 1.0)
        # (піксель / ширина * 2) - 1
        gl_mouse_x = (mouse_x / width) * 2 - 1
        gl_mouse_y = -((mouse_y / height) * 2 - 1) # Y в OpenGL інвертований

        # Перевірка, чи миша "всередині" прямокутника (з урахуванням його позиції)
        # розмір 0.4 на 0.4 (від -0.2 до 0.2)
        if (pos_x - 0.2 < gl_mouse_x < pos_x + 0.2 and 
            pos_y - 0.2 < gl_mouse_y < pos_y + 0.2):
            angle += 0.05 # якщо навели — обертаємо

        translation = np.array([
            [1, 0, 0, pos_x],
            [0, 1, 0, pos_y],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32).T

        # поворот навколо осі Z
        c = math.cos(angle)
        s = math.sin(angle)
        rotation = np.array([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ], dtype=np.float32).T

        # спочатку повертаємо, потім переносимо
        transform = rotation @ translation

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, transform)
        
        glBindVertexArray(VAO)
        glBindTexture(GL_TEXTURE_2D, texture)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()