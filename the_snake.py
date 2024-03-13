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

# Цвета:
WHITE = (255, 255, 255)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=WHITE):
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
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        """
        Отрисовка яблока.

        Args:
            surface: Поверхность для отрисовки.
        """
        pygame.draw.rect(
            surface, self.body_color, (*self.position, GRID_SIZE, GRID_SIZE)
        )


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def update_direction(self, direction):
        """
        Обновление направления движения змейки.

        Args:
            direction (tuple): Новое направление движения.
        """
        if direction != tuple(map(lambda x: -x, self.direction)):
            self.next_direction = direction

    def move(self):
        """Обновление позиции змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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

    def draw(self, surface):
        """
        Отрисовка змейки.

        Args:
            surface: Поверхность для отрисовки.
        """
        for position in self.positions:
            pygame.draw.rect(
                surface, self.body_color, (*position, GRID_SIZE, GRID_SIZE)
            )


def handle_game_over(screen):
    """
    Обработка конца игры.

    Args:
        screen: Поверхность игрового окна.
    """
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Press Space to Play Again", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    # Ожидание нажатия клавиши "Space" для перезапуска игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def handle_events(snake):
    """
    Обработка событий клавиатуры.

    Args:
        snake (Snake): Экземпляр класса Snake.
    """
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


def handle_game_logic(snake, apple):
    """
    Обработка игровой логики.

    Args:
        snake (Snake): Экземпляр класса Snake.
        apple (Apple): Экземпляр класса Apple.

    Returns:
        bool: Флаг завершения игры.
    """
    if not snake.move():
        return True

    if snake.position == apple.position:
        snake.length += 1
        apple.randomize_position()

    return False


def update_display(screen, snake, apple):
    """
    Обновление отображения.

    Args:
        screen: Поверхность для отрисовки.
        snake (Snake): Экземпляр класса Snake.
        apple (Apple): Экземпляр класса Apple.
    """
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw(screen)
    apple.draw(screen)
    pygame.display.update()


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    game_over = False

    while not game_over:
        handle_events(snake)
        game_over = handle_game_logic(snake, apple)
        update_display(screen, snake, apple)

        clock.tick(SPEED)
        if clock.get_fps() < SPEED:
            delay = 1000 // SPEED
            pygame.time.delay(delay)  # Делаем паузу для соблюдения скорости

        if game_over:
            if handle_game_over(screen):
                # При перезапуске игры сбрасываем состояние змейки и яблока
                snake = Snake()
                apple = Apple()


if __name__ == "__main__":
    main()
