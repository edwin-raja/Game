import pygame

pygame.init()

WIDTH = 700
HEIGHT = 700
FPS = 60

# Colors RGB(0-255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (80, 175, 90)
BLUE = (60, 160, 200)

COLS = 10
ROWS = 6

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BreakOut Game")
clock = pygame.time.Clock()

# Brick class
class Brick():
    def __init__(self):
        self.width = int(WIDTH / COLS)
        self.height = 30
        self.bricks = []

    def create_brick(self):
        for row in range(ROWS):
            bricks_row = []
            for col in range(COLS):
                bricks_x = col * self.width
                bricks_y = row * self.height
                br = pygame.Rect(bricks_x, bricks_y, self.width, self.height)
                bricks_row.append(br)
            self.bricks.append(bricks_row)

    def draw_bricks(self):
        for row in self.bricks:
            for br in row:
                pygame.draw.rect(win, GREEN, br)
                pygame.draw.rect(win, BLACK, br, 2)

# Paddle class
class Paddle():
    def __init__(self):
        self.width = int(WIDTH / COLS)
        self.height = 20
        self.x = int(WIDTH / 2) - int(self.width / 2)
        self.y = HEIGHT - 40
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_paddle(self):
        pygame.draw.rect(win, WHITE, self.rect)

    def move_paddle(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Ball class
class Ball():
    def __init__(self, x, y):
        self.radius = 10
        self.x = x - self.radius
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.dx = 3
        self.dy = -3
        self.game_status = 0

    def draw_ball(self):
        pygame.draw.circle(win, BLUE, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def move_ball(self):
        # Wall collision
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.dx *= -1
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > HEIGHT:
            self.game_status = -1  # Game over

        # Paddle collision
        if self.rect.colliderect(paddle.rect) and self.dy > 0:
            self.dy *= -1
            sound = pygame.mixer.Sound("Game/Breakout/Breakout_bounce.wav")
            sound.play()

        # Brick collision
        all_done = True
        row_num = 0
        for row in brick_wall.bricks:
            col_num = 0
            for br in row:
                if self.rect.colliderect(br):
                    hit_sound = pygame.mixer.Sound("Game/Breakout/Breakout_hit.wav")
                    hit_sound.play()
                    if abs(self.rect.bottom - br.top) < 5 and self.dy > 0:
                        self.dy *= -1
                    if abs(self.rect.top - br.bottom) < 5 and self.dy < 0:
                        self.dy *= -1
                    if abs(self.rect.left - br.right) < 5 and self.dx < 0:
                        self.dx *= -1
                    if abs(self.rect.right - br.left) < 5 and self.dx > 0:
                        self.dx *= -1
                    brick_wall.bricks[row_num][col_num] = pygame.Rect(0, 0, 0, 0)  # Mark the brick as hit
                if brick_wall.bricks[row_num][col_num] != pygame.Rect(0, 0, 0, 0):
                    all_done = False
                col_num += 1
            row_num += 1
        if all_done:
            self.game_status = 1

        self.rect.x += self.dx
        self.rect.y += self.dy
        return self.game_status

paddle = Paddle()
ball = Ball(paddle.x + int(paddle.width / 2), paddle.y - paddle.height)
brick_wall = Brick()
brick_wall.create_brick()

run = True
while run:
    clock.tick(FPS)
    win.fill(BLACK)
    paddle.draw_paddle()
    paddle.move_paddle()
    ball.draw_ball()
    brick_wall.draw_bricks()
    game_status = ball.move_ball()

    if game_status == -1:
        win.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render('GAME OVER', True, BLUE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        win.blit(text, text_rect)
    elif game_status == 1:
        win.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render('YOU WON', True, BLUE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        win.blit(text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
