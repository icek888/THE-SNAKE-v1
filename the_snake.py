from random import choice, randint

import pygame
import sys

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Базовый класс для игровых объектов
class GameObject:
    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    # Отрисовка объекта
    def draw(self, surface):
        pass


# Класс для представления яблока
class Apple(GameObject):
    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    # Установка случайной позиции для яблока
    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    # Отрисовка яблока
    def draw(self, surface):
        pygame.draw.rect(
            surface, self.body_color, (*self.position, GRID_SIZE, GRID_SIZE)
        )


# Класс для представления змейки
class Snake(GameObject):
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    # Обновление направления движения змейки
    def update_direction(self, direction):
        if direction != tuple(map(lambda x: -x, self.direction)):
            self.next_direction = direction

    # Обновление позиции змейки
    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        x, y = self.position
        x += self.direction[0] * GRID_SIZE
        y += self.direction[1] * GRID_SIZE

        # Обработка выхода за границы поля
        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT

        self.position = (x, y)
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    # Отрисовка змейки
    def draw(self, surface):
        for position in self.positions:
            pygame.draw.rect(
                surface, self.body_color, (*position, GRID_SIZE, GRID_SIZE)
            )


def main():
    snake = Snake()
    apple = Apple()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)

        screen.fill(BOARD_BACKGROUND_COLOR)

        if not snake.move():
            game_over = True

        snake.draw(screen)

        if snake.position == apple.position:
            snake.length += 1
            apple.randomize_position()

        apple.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)

        if game_over:
            if handle_game_over(screen):
                main()


if __name__ == "__main__":
    main()
