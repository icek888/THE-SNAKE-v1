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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Инициализация объекта.

        Args:
            position (tuple): Позиция объекта на экране.
            body_color (tuple): Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Отрисовка объекта.

        Args:
            surface: Поверхность для отрисовки.
        """
        pass


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции для яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """
        Отрисовка яблока.

        Args:
            surface: Поверхность для отрисовки.
        """
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None  # Добавим переменную для хранения последней позиции

    def draw(self, surface):
        """
        Отрисовка змейки.

        Args:
            surface: Поверхность для отрисовки.
        """
        for position in self.positions:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE)
                               )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect((self.last[0], self.last[1]),
                                    (GRID_SIZE, GRID_SIZE)
                                    )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Обновление позиции змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        self.last = self.positions[-1]  # Сохраняем позицию последнего сегмента

        x, y = self.position
        x += self.direction[0] * GRID_SIZE
        y += self.direction[1] * GRID_SIZE

        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT

        self.position = (x, y)
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.positions.pop()

        # Проверка столкновения с собой
        if self.position in self.positions[1:]:
            return False  # Завершение игры

        return True

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс настроек змейки."""
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def update_direction(self, direction):
        """Обновление направления движения змейки."""
        self.next_direction = direction


def handle_keys(game_object):
    """
    Обработка действий пользователя.

    Args:
        game_object: Игровой объект, для которого обрабатываются действия.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        if not snake.move():
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Проверка столкновения змейки с яблоком
        if snake.position == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
