#define TINYOBJLOADER_IMPLEMENTATION
#include "tiny_obj_loader.h"

#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

// Налаштування вікна
const unsigned int SCR_WIDTH = 800;
const unsigned int SCR_HEIGHT = 600;

// Змінні камери (Fly Camera)
glm::vec3 cameraPos = glm::vec3(0.0f, 0.0f, 5.0f);
glm::vec3 cameraFront = glm::vec3(0.0f, 0.0f, -1.0f);
glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);

float yaw = -90.0f; // Огляд вліво/вправо
float pitch = 0.0f; // вгору/вниз
float lastX = SCR_WIDTH / 2.0f;
float lastY = SCR_HEIGHT / 2.0f;
bool firstMouse = true;

// Час між кадрами
float deltaTime = 0.0f;
float lastFrame = 0.0f;

// Позиція точкового джерела світла у просторі
glm::vec3 lightPos(1.2f, 1.0f, 2.0f);

// Функція для зчитування шейдерів з файлів
std::string readShaderCode(const char *filePath)
{
    std::string code;
    std::ifstream file;
    file.exceptions(std::ifstream::failbit | std::ifstream::badbit);
    try
    {
        file.open(filePath);
        std::stringstream stream;
        stream << file.rdbuf();
        // беру весь буфер файлу (rdbuf) і одним махом "переливаю" його у тимчасове сховище (stream)
        file.close();
        code = stream.str();
    }
    catch (std::ifstream::failure &e)
    {
        std::cout << "ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ: " << filePath << std::endl;
    }
    return code;
}

// Обробка клавіатури (WASD + ESC)
void processInput(GLFWwindow *window)
{
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    float cameraSpeed = 2.5f * deltaTime;
    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        cameraPos += cameraSpeed * cameraFront;
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        cameraPos -= cameraSpeed * cameraFront;

    // векторний добуток (glm::cross) - перпендикулярний до них обох. Front × Up = Right
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        cameraPos -= glm::normalize(glm::cross(cameraFront, cameraUp)) * cameraSpeed;
    // я викликаю normalize, щоб примусово повернути довжину цього вектора до 1
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        cameraPos += glm::normalize(glm::cross(cameraFront, cameraUp)) * cameraSpeed;
}

// Обробка руху миші (зміна кутів огляду)
void mouse_callback(GLFWwindow *window, double xposIn, double yposIn)
{
    float xpos = static_cast<float>(xposIn);
    float ypos = static_cast<float>(yposIn);

    if (firstMouse)
    {
        lastX = xpos;
        lastY = ypos;
        firstMouse = false;
    }

    float xoffset = xpos - lastX;
    float yoffset = lastY - ypos; // інвертую, бо координати екрану йдуть зверху вниз
    lastX = xpos;
    lastY = ypos;

    // чутливість
    float sensitivity = 0.1f;
    xoffset *= sensitivity;
    yoffset *= sensitivity;

    yaw += xoffset;
    pitch += yoffset;

    // Обмеження, щоб камера не переверталася
    // вектор мого погляду став би паралельним вектору "неба" (cameraUp) - так не повинно бути
    if (pitch > 89.0f)
        pitch = 89.0f;
    if (pitch < -89.0f)
        pitch = -89.0f;

    glm::vec3 front;
    front.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
    front.y = sin(glm::radians(pitch));
    front.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
    cameraFront = glm::normalize(front);
}

int main()
{
    // Ініціалізація GLFW
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow *window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Exam Project: 3D Blinn-Phong", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    // Захоплення курсора миші для камери
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
    glfwSetCursorPosCallback(window, mouse_callback);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE); // Відсікання задніх граней - вимога

    // Завантаження коду шейдерів - збірка
    std::string vertexCodeStr = readShaderCode("shaders/vertex.glsl");
    std::string fragmentCodeStr = readShaderCode("shaders/fragment.glsl");
    const char *vertexShaderSource = vertexCodeStr.c_str();
    const char *fragmentShaderSource = fragmentCodeStr.c_str();

    // Компіляція шейдерів
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    // & о- взяття адреси у пам'яті
    glCompileShader(vertexShader);

    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    // ЗАВАНТАЖЕННЯ 3D МОДЕЛІ ЧЕРЕЗ TINYOBJLOADER (Вимога 1)
    tinyobj::attrib_t attrib;
    std::vector<tinyobj::shape_t> shapes;
    std::vector<tinyobj::material_t> materials;
    std::string warn, err;

    // Читаю наш cube.obj
    if (!tinyobj::LoadObj(&attrib, &shapes, &materials, &warn, &err, "models/cube.obj"))
    {
        std::cout << "Failed to load OBJ file: " << err << std::endl;
        return -1;
    }

    std::vector<float> vertices;
    std::vector<unsigned int> indices;

    // Розпаковую дані у формат, який розуміє OpenGL (Позиція + Текстура + Нормаль)
    for (const auto &shape : shapes)
    {
        for (const auto &index : shape.mesh.indices)
        // mesh: Безпосередньо набір вершин (точок у просторі) та граней, які утворюють поверхню цього об'єкта
        {
            // Позиція (X, Y, Z)
            vertices.push_back(attrib.vertices[3 * index.vertex_index + 0]);
            vertices.push_back(attrib.vertices[3 * index.vertex_index + 1]);
            vertices.push_back(attrib.vertices[3 * index.vertex_index + 2]);

            // Текстурні координати (U, V) - якщо немає - 0
            if (index.texcoord_index >= 0)
            // відеокарта прочитала б нормалі замість текстур
            {
                vertices.push_back(attrib.texcoords[2 * index.texcoord_index + 0]);
                vertices.push_back(attrib.texcoords[2 * index.texcoord_index + 1]);
            }
            else
            {
                vertices.push_back(0.0f);
                vertices.push_back(0.0f);
            }

            // Нормалі (X, Y, Z)
            if (index.normal_index >= 0)
            {
                vertices.push_back(attrib.normals[3 * index.normal_index + 0]);
                vertices.push_back(attrib.normals[3 * index.normal_index + 1]);
                vertices.push_back(attrib.normals[3 * index.normal_index + 2]);
            }
            else
            {
                vertices.push_back(0.0f);
                vertices.push_back(0.0f);
                vertices.push_back(1.0f);
            }

            indices.push_back(indices.size());
        }
    }

    // Налаштування буферів VAO, VBO, EBO
    unsigned int VAO, VBO, EBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    // VBO (Vertex Buffer Object) - коробка, куди я скидаю весь свій масив vertices (координати, текстури, нормалі)
    glGenBuffers(1, &EBO);
    // EBO (Element Buffer Object) - це коробка для масиву indices, яка каже, в якому порядку з'єднувати точки
    // VAO (Vertex Array Object) - менеджер. Він запам'ятовує всі налаштування VBO та EBO. Під час малювання мені не треба буде налаштовувати все заново, достатньо просто викликати VAO

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float), vertices.data(), GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size() * sizeof(unsigned int), indices.data(), GL_STATIC_DRAW);

    // Крок у байтах між вершинами = 8 чисел (3 позиція + 2 текстура + 3 нормаль) * sizeof(float) = 32 байти
    GLsizei stride = 8 * sizeof(float);
    // 3 позиція + 2 текстура + 3 нормаль
    // Я множу 8 на розмір типу float (4 байти), тобто відеокарта має робити крок у 32 байти, щоб перейти до наступної точки
    // Текстура починається після трьох чисел позиції (3*4 = 12 байт). А нормалі починаються після п'яти чисел (зміщення 5*4 = 20)

    // Атрибут 0: Позиція
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, (void *)0);
    glEnableVertexAttribArray(0);
    // Атрибут 1: Текстура
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, (void *)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);
    // Атрибут 2: Нормаль
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, (void *)(5 * sizeof(float)));
    glEnableVertexAttribArray(2);

    // Головний цикл програми
    while (!glfwWindowShouldClose(window))
    {
        float currentFrame = static_cast<float>(glfwGetTime());
        deltaTime = currentFrame - lastFrame;
        lastFrame = currentFrame;

        processInput(window);

        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glUseProgram(shaderProgram);

        // Налаштування матриць камери (Вимога 2)
        glm::mat4 projection = glm::perspective(glm::radians(45.0f), (float)SCR_WIDTH / (float)SCR_HEIGHT, 0.1f, 100.0f);
        glm::mat4 view = glm::lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
        glm::mat4 model = glm::mat4(1.0f);

        // Повільне обертання куба для красивої демонстрації відблисків світла
        model = glm::rotate(model, currentFrame * glm::radians(25.0f), glm::vec3(0.5f, 1.0f, 0.0f));

        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "projection"), 1, GL_FALSE, glm::value_ptr(projection));
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "view"), 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "model"), 1, GL_FALSE, glm::value_ptr(model));

        // R (червоний), G (зелений), B (синій)
        // f у кінці просто каже компілятору, що це дробове число типу float

        // Передача позиції камери у фрагментний шейдер
        glUniform3fv(glGetUniformLocation(shaderProgram, "viewPos"), 1, glm::value_ptr(cameraPos));

        // НАЛАШТУВАННЯ МАТЕРІАЛУ (Вимога 3: у мене, ЗОЛОТО)
        glUniform3f(glGetUniformLocation(shaderProgram, "material.ambient"), 0.24725f, 0.1995f, 0.0745f);
        glUniform3f(glGetUniformLocation(shaderProgram, "material.diffuse"), 0.75164f, 0.60648f, 0.22648f);
        glUniform3f(glGetUniformLocation(shaderProgram, "material.specular"), 0.628281f, 0.555802f, 0.366065f);
        glUniform1f(glGetUniformLocation(shaderProgram, "material.shininess"), 51.2f);

        // Налаштування точкового джерела світла
        glUniform3fv(glGetUniformLocation(shaderProgram, "light.position"), 1, glm::value_ptr(lightPos));
        glUniform3f(glGetUniformLocation(shaderProgram, "light.ambient"), 0.2f, 0.2f, 0.2f);
        glUniform3f(glGetUniformLocation(shaderProgram, "light.diffuse"), 1.0f, 1.0f, 1.0f); // Яскраве біле світло
        glUniform3f(glGetUniformLocation(shaderProgram, "light.specular"), 1.0f, 1.0f, 1.0f);

        // Параметри затухання світла з відстанню (Point Light attenuation)
        glUniform1f(glGetUniformLocation(shaderProgram, "light.constant"), 1.0f);
        glUniform1f(glGetUniformLocation(shaderProgram, "light.linear"), 0.09f);
        glUniform1f(glGetUniformLocation(shaderProgram, "light.quadratic"), 0.032f);

        // Малювання об'єкта
        glBindVertexArray(VAO);
        glDrawElements(GL_TRIANGLES, static_cast<GLsizei>(indices.size()), GL_UNSIGNED_INT, 0);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);

    glfwTerminate();
    return 0;
}