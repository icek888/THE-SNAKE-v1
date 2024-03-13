pip inimport pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=WHITE):
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Отрисовка объекта."""
        pass


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self):
        super().__init__(body_color=RED)
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции для яблока."""
        x = random.randint(0, 31) * 20
        y = random.randint(0, 23) * 20
        self.position = (x, y)

    def draw(self, screen):
        """Отрисовка яблока."""
        pygame.draw.rect(
            screen, self.body_color, (self.position[0], self.position[1], 20, 20)
        )


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self):
        super().__init__(body_color=GREEN)
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = "RIGHT"
        self.next_direction = None

    def update_direction(self, direction):
        """Обновление направления движения змейки."""
        if direction == "UP" and self.direction != "DOWN":
            self.next_direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.next_direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.next_direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.next_direction = "RIGHT"

    def move(self):
        """Обновление позиции змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        x, y = self.position
        if self.direction == "UP":
            y -= 20
            if y < 0:
                y = 480 - 20
        elif self.direction == "DOWN":
            y += 20
            if y >= 480:
                y = 0
        elif self.direction == "LEFT":
            x -= 20
            if x < 0:
                x = 640 - 20
        elif self.direction == "RIGHT":
            x += 20
            if x >= 640:
                x = 0

        self.position = (x, y)
        self.positions.insert(0, self.position)

        if self.position in self.positions[1:]:
            return False

        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def draw(self, screen):
        """Отрисовка змейки."""
        for position in self.positions:
            pygame.draw.rect(
                screen, self.body_color, (position[0], position[1], 20, 20)
            )


def handle_game_over(screen):
    """Обработка проигрыша."""
    font = pygame.font.Font(None, 36)
    text = font.render("Для выхода - X", True, WHITE)
    text_rect = text.get_rect(center=(320, 240))
    screen.blit(text, text_rect)
    text = font.render("Для начала заново - C", True, WHITE)
    text_rect = text.get_rect(center=(320, 280))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    return True


def main():
    """Основной игровой цикл."""
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Змейка")

    snake = Snake()
    apple = Apple()

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.update_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.update_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction("RIGHT")

        screen.fill(BLACK)

        if not snake.move():
            game_over = True

        snake.draw(screen)

        if snake.position == apple.position:
            snake.length += 1
            apple.randomize_position()

        apple.draw(screen)

        pygame.display.update()
        clock.tick(10)

        if game_over:
            if handle_game_over(screen):
                main()


if __name__ == "__main__":
    main()
