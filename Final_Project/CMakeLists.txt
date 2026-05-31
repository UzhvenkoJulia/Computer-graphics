cmake_minimum_required(VERSION 3.10)
project(Final_Project_3D)

set(CMAKE_CXX_STANDARD 17)

# 1. Підключаю GLFW (збираю його прямо з коду)
add_subdirectory(${CMAKE_SOURCE_DIR}/../external/glfw glfw_build)

# 2. Створюю бібліотеку GLAD
add_library(glad ${CMAKE_SOURCE_DIR}/../external/glad/src/glad.c)
target_include_directories(glad PUBLIC ${CMAKE_SOURCE_DIR}/../external/glad/include)

# 3. Шукаю OpenGL у системі
find_package(OpenGL REQUIRED)

# 4. Вказую шляхи до математики GLM та tinyobjloader
include_directories(
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/../external
    ${CMAKE_SOURCE_DIR}/../external/glm
    ${CMAKE_SOURCE_DIR}/../external/glm/glm
)

# 5. Створюю нашу програму
add_executable(${PROJECT_NAME} src/main.cpp)

# 6. Лінкую (зшиваю) все разом 
target_link_libraries(${PROJECT_NAME} glad glfw ${OPENGL_LIBRARIES})