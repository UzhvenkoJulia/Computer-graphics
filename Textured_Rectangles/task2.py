import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
import time

is_paused = False

def key_callback(window, key, scancode, action, mods):
    global is_paused
    
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        is_paused = not is_paused

# Вертексний шейдер, який САМ обертає об'єкт
vertex_src = """
#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aTexCoord;

out vec2 TexCoord;
uniform float u_time; 

void main() {
    // Рахую матрицю повороту навколо центру (Z-вісь)
    float c = cos(u_time);
    float s = sin(u_time);
    mat4 rotation = mat4(  // щоб повернути точку, її координати множe на таку матрицю
        c, -s, 0.0, 0.0,
        s,  c, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
    
    gl_Position = rotation * vec4(aPos, 0.0, 1.0);
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
    """.convert("RGBA"): Перетворює зображення у формат Red, Green, Blue, Alpha. 
    Це важливо, бо вихідний файл може бути в RGB (без прозорості) або мати палітру. 
    OpenGL найлегше працює саме з RGBA, де кожен піксель має 4 канали"""
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture

def main():
    global is_paused
    
    if not glfw.init():
        return
    
    window = glfw.create_window(600, 600, "2. Анімований квадрат (Пробіл - Пауза)", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

    # Квадрат по центру (-0.5 до 0.5)
    vertices = np.array([
        -0.5, -0.5,   0.0, 0.0,
         0.5, -0.5,   1.0, 0.0,
         0.5,  0.5,   1.0, 1.0,
        -0.5, -0.5,   0.0, 0.0,
         0.5,  0.5,   1.0, 1.0,
        -0.5,  0.5,   0.0, 1.0
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)

    tex = load_texture("tex_square.jpg") 

    glUseProgram(shader)
    time_loc = glGetUniformLocation(shader, "u_time")

    accumulated_time = 0.0
    last_frame_time = glfw.get_time()
    
    # Цільовий час на один кадр 
    target_frame_time = 1.0 / 60.0 

    while not glfw.window_should_close(window):
        # Логіка часу для паузи
        current_time = glfw.get_time()
        delta_time = current_time - last_frame_time
        last_frame_time = current_time
        
        if not is_paused:
            accumulated_time += delta_time

        glfw.poll_events()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Передаю час у шейдер
        glUniform1f(time_loc, accumulated_time)

        glBindVertexArray(VAO)
        glBindTexture(GL_TEXTURE_2D, tex)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        glfw.swap_buffers(window)

        # Ліміт 60 FPS
        time_spent = glfw.get_time() - current_time
        if time_spent < target_frame_time:
            time.sleep(target_frame_time - time_spent)

    glfw.terminate()

if __name__ == "__main__":
    main()