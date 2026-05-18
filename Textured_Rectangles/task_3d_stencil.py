import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
import math

# ШЕЙДЕРИ

vertex_src = """
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 aTexCoord;
out vec2 TexCoord;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
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

# Шейдер для рамки (суцільним кольором)
outline_fragment_src = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 1.0, 0.0, 1.0); 
}
"""

camera_pos = np.array([0.0, 0.0, 5.0], dtype=np.float32)
camera_front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

yaw, pitch = -90.0, 0.0
last_x, last_y = 400, 300
first_mouse = True
delta_time, last_frame = 0.0, 0.0

def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2.0)
    mat = np.zeros((4, 4), dtype=np.float32)
    mat[0, 0] = f / aspect
    mat[1, 1] = f
    mat[2, 2] = (far + near) / (near - far)
    mat[2, 3] = -1.0
    mat[3, 2] = (2.0 * far * near) / (near - far)
    return mat

def look_at(eye, target, up):
    F = target - eye
    f = F / np.linalg.norm(F)
    s = np.cross(f, up)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)
    
    mat = np.eye(4, dtype=np.float32)
    mat[0, 0:3] = s
    mat[1, 0:3] = u
    mat[2, 0:3] = -f
    
    trans = np.eye(4, dtype=np.float32)
    trans[0:3, 3] = -eye
    
    return (mat @ trans).T # для OpenGL

def scale_matrix(s):
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32).T

def translate_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32).T

def rotate_y_matrix(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([
        [c,  0, s, 0],
        [0,  1, 0, 0],
        [-s, 0, c, 0],
        [0,  0, 0, 1]
    ], dtype=np.float32).T

active_cube_idx = 0 # Індекс активного куба (0, 1 або 2)

def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    global camera_pos, active_cube_idx
    speed = 2.5 * delta_time
    
    # Рух камери 
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera_pos += speed * camera_front
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera_pos -= speed * camera_front
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera_pos -= np.cross(camera_front, camera_up) * speed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera_pos += np.cross(camera_front, camera_up) * speed

    if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS: active_cube_idx = 0
    if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS: active_cube_idx = 1
    if glfw.get_key(window, glfw.KEY_3) == glfw.PRESS: active_cube_idx = 2

def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse, camera_front
    
    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False
        
    xoffset = xpos - last_x
    yoffset = last_y - ypos # Інвертую Y
    last_x, last_y = xpos, ypos
    
    sensitivity = 0.1
    yaw += xoffset * sensitivity
    pitch += yoffset * sensitivity
    
    # Обмежую кут огляду по вертикалі
    if pitch > 89.0: pitch = 89.0
    if pitch < -89.0: pitch = -89.0
        
    front = np.zeros(3, dtype=np.float32)
    front[0] = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
    front[1] = math.sin(math.radians(pitch))
    front[2] = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    camera_front = front / np.linalg.norm(front)

def main():
    global delta_time, last_frame
    
    if not glfw.init(): return
    
    # Обов'язково прошу вікно з підтримкою буфера трафарету (8 біт)
    glfw.window_hint(glfw.STENCIL_BITS, 8)
    window = glfw.create_window(800, 600, "2.5: ЗD, Камера та Буфер трафарету", None, None)
    glfw.make_context_current(window)
    
    # Захоплюю курсор миші для камери 
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    # Компілюю шейдери
    shader_normal = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )
    shader_outline = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(outline_fragment_src, GL_FRAGMENT_SHADER)
    )

    # Позиція + Текстурні координати
    cube_vertices = np.array([
        # Задня грань
        -0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 0.0,
        # Передня грань
        -0.5, -0.5,  0.5,  0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        # Ліва грань
        -0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 0.0,
        # Права грань
         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5,  0.5,  0.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
        # Нижня грань
        -0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  1.0, 1.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        # Верхня грань
        -0.5,  0.5, -0.5,  0.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5, -0.5,  0.0, 1.0
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube_vertices.nbytes, cube_vertices, GL_STATIC_DRAW)

    # Вказівники на атрибути
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    img = Image.open("tex1.jpg").transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    # Вмикаю буфер глибини та буфер трафарету
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE) # Якщо тест пройдено, замінюю значення в буфері

    cube_positions = [
        (-2.0, 0.0, 0.0), # Куб 0 (Зліва)
        ( 0.0, 0.0, 0.0), # Куб 1 (По центру)
        ( 2.0, 0.0, 0.0)  # Куб 2 (Справа)
    ]

    while not glfw.window_should_close(window):
        glfw.poll_events()
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        
        process_input(window)

        # Очистка - Колір, Глибина, Трафарет
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

        # Створюю матриці камери та проекції
        projection = perspective(45.0, 800/600, 0.1, 100.0)
        view = look_at(camera_pos, camera_pos + camera_front, camera_up)

        # НОРМАЛЬНІ КУБИ
        glUseProgram(shader_normal)
        glUniformMatrix4fv(glGetUniformLocation(shader_normal, "projection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(shader_normal, "view"), 1, GL_FALSE, view)

        glBindVertexArray(VAO)
        glBindTexture(GL_TEXTURE_2D, texture)

        for i in range(3):
            model = translate_matrix(*cube_positions[i])
            
            # Якщо куб активний
            if i == active_cube_idx:
                # + обертання навколо Y (анімація)
                model = model @ rotate_y_matrix(current_frame * 1.5)
                # 1 у буфер трафарету в тих пікселях, де малюється активний куб
                glStencilFunc(GL_ALWAYS, 1, 0xFF)
                glStencilMask(0xFF)
            else:
                # Для неактивних кубів нічого не пишу в трафарет
                glStencilMask(0x00)

            glUniformMatrix4fv(glGetUniformLocation(shader_normal, "model"), 1, GL_FALSE, model)
            glDrawArrays(GL_TRIANGLES, 0, 36)

        # РАМКа
        # НЕ ДОРІВНЮЄ 1 (навколо)
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
        glStencilMask(0x00) # Більше не записую в трафарет
        glDisable(GL_DEPTH_TEST) # Вимикаю глибину, щоб рамка малювалася поверх усього

        glUseProgram(shader_outline)
        glUniformMatrix4fv(glGetUniformLocation(shader_outline, "projection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(shader_outline, "view"), 1, GL_FALSE, view)

        # Беру позицію активного куба, масштабую його трохи (на 10% більше) і обертаю так само
        outline_model = translate_matrix(*cube_positions[active_cube_idx])
        outline_model = outline_model @ rotate_y_matrix(current_frame * 1.5)
        outline_model = outline_model @ scale_matrix(1.1) # Збільш розмір

        glUniformMatrix4fv(glGetUniformLocation(shader_outline, "model"), 1, GL_FALSE, outline_model)
        
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glStencilMask(0xFF)
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glEnable(GL_DEPTH_TEST)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()