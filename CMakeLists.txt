cmake_minimum_required(VERSION 3.10)
project(KNU_OpenGL_Yulia)

set(CMAKE_CXX_STANDARD 17)

# 1. Підключаємо GLFW
add_subdirectory(external/glfw)

# 2. Створюємо бібліотеку GLAD (переконайся, що файл glad.c є в external/glad/src)
add_library(glad external/glad/src/glad.c)
target_include_directories(glad PUBLIC external/glad/include)

# 3. Шукаємо OpenGL у системі
find_package(OpenGL REQUIRED)

# 4. Створюємо нашу програму
add_executable(MyApp main.cpp)

# 5. Лінкуємо (зшиваємо) все разом
target_link_libraries(MyApp glad glfw ${OPENGL_LIBRARIES})

# 6. Вказуємо, де шукати заголовочні файли
target_include_directories(MyApp PUBLIC 
    external/glfw/include 
    external/glad/include
    external/glm
)