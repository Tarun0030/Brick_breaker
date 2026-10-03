import pygame
import random
import sys

pygame.init()

# ----------------------------
# Screen settings
# ----------------------------
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Brick Breaker")

clock = pygame.time.Clock()

# ----------------------------
# Colors
# ----------------------------
BLACK = (5, 10, 20)
WHITE = (255, 255, 255)
BLUE = (30, 120, 255)
RED = (255, 60, 70)
YELLOW = (255, 190, 30)
GREEN = (30, 210, 170)
CYAN = (30, 220, 220)
PURPLE = (180, 80, 255)

# ----------------------------
# Game variables
# ----------------------------
score = 0
combo = 0
lives = 3
game_over = False
game_won = False

# ----------------------------
# Paddle
# ----------------------------
paddle = pygame.Rect(
    WIDTH // 2 - 60,
    HEIGHT - 45,
    120,
    15
)

PADDLE_SPEED = 8

# ----------------------------
# Ball class
# ----------------------------
class Ball:
    def __init__(self, x, y):
        self.radius = 8
        self.x = x
        self.y = y

        self.dx = random.choice([-4, 4])
        self.dy = -4

    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius
        )

    def update(self):
        self.x += self.dx
        self.y += self.dy


# ----------------------------
# Create balls
# ----------------------------
ball = Ball(WIDTH // 2, HEIGHT - 70)
balls = [ball]


# ----------------------------
# Bricks
# ----------------------------
bricks = []

rows = 5
cols = 8

brick_width = 85
brick_height = 25

gap = 8

start_x = 30
start_y = 70

brick_colors = [
    BLUE,
    RED,
    YELLOW,
    GREEN,
    CYAN
]

for row in range(rows):
    for col in range(cols):

        x = start_x + col * (brick_width + gap)
        y = start_y + row * (brick_height + gap)

        brick = pygame.Rect(
            x,
            y,
            brick_width,
            brick_height
        )

        bricks.append({
            "rect": brick,
            "color": brick_colors[row % len(brick_colors)]
        })


# ----------------------------
# Powerup
# ----------------------------
powerup = None


def spawn_powerup(x, y):
    return pygame.Rect(
        x,
        y,
        20,
        20
    )


# ----------------------------
# Fonts
# ----------------------------
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 50)


# ----------------------------
# Reset ball
# ----------------------------
def reset_ball():

    ball = Ball(
        WIDTH // 2,
        HEIGHT - 70
    )

    return ball


# ----------------------------
# Main game loop
# ----------------------------
while True:

    # ------------------------
    # Events
    # ------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart game
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if game_over or game_won:

                    score = 0
                    combo = 0
                    lives = 3
                    game_over = False
                    game_won = False

                    paddle.x = WIDTH // 2 - 60

                    bricks.clear()

                    for row in range(rows):
                        for col in range(cols):

                            x = start_x + col * (brick_width + gap)
                            y = start_y + row * (brick_height + gap)

                            bricks.append({
                                "rect": pygame.Rect(
                                    x,
                                    y,
                                    brick_width,
                                    brick_height
                                ),
                                "color": brick_colors[
                                    row % len(brick_colors)
                                ]
                            })

                    balls.clear()
                    balls.append(
                        Ball(
                            WIDTH // 2,
                            HEIGHT - 70
                        )
                    )


    # ------------------------
    # Game logic
    # ------------------------
    if not game_over and not game_won:

        keys = pygame.key.get_pressed()

        # Paddle movement
        if keys[pygame.K_LEFT]:
            paddle.x -= PADDLE_SPEED

        if keys[pygame.K_RIGHT]:
            paddle.x += PADDLE_SPEED

        # Keep paddle inside screen
        if paddle.left < 0:
            paddle.left = 0

        if paddle.right > WIDTH:
            paddle.right = WIDTH


        # --------------------
        # Ball movement
        # --------------------
        for ball in balls:

            ball.update()

            ball_rect = ball.rect()

            # Left wall
            if ball.x - ball.radius <= 0:

                ball.x = ball.radius
                ball.dx *= -1

            # Right wall
            if ball.x + ball.radius >= WIDTH:

                ball.x = WIDTH - ball.radius
                ball.dx *= -1

            # Top wall
            if ball.y - ball.radius <= 0:

                ball.y = ball.radius
                ball.dy *= -1


            # ----------------
            # Paddle collision
            # ----------------
            if ball_rect.colliderect(paddle):

                if ball.dy > 0:

                    ball.y = paddle.top - ball.radius

                    ball.dy *= -1

                    # Change angle based on paddle position
                    hit_position = (
                        ball.x - paddle.centerx
                    ) / (paddle.width / 2)

                    ball.dx = hit_position * 5

                    combo += 1


            # ----------------
            # Brick collision
            # ----------------
            for brick_data in bricks[:]:

                brick = brick_data["rect"]

                if ball_rect.colliderect(brick):

                    # Remove brick
                    bricks.remove(brick_data)

                    # Reverse ball direction
                    ball.dy *= -1

                    # Score
                    score += 100

                    combo += 1

                    # Random powerup
                    if random.random() < 0.10:

                        powerup = spawn_powerup(
                            brick.centerx,
                            brick.centery
                        )

                    break


            # ----------------
            # Ball falls down
            # ----------------
            if ball.y > HEIGHT:

                balls.remove(ball)

                lives -= 1

                combo = 0

                if lives > 0:

                    balls.append(
                        reset_ball()
                    )

                else:

                    game_over = True

                    break


        # --------------------
        # Powerup movement
        # --------------------
        if powerup:

            powerup.y += 5

            if powerup.colliderect(paddle):

                # Extra ball
                balls.append(
                    Ball(
                        paddle.centerx,
                        paddle.top - 20
                    )
                )

                powerup = None

            elif powerup.top > HEIGHT:

                powerup = None


        # --------------------
        # Win condition
        # --------------------
        if len(bricks) == 0:

            game_won = True


    # ------------------------
    # Drawing
    # ------------------------
    screen.fill(BLACK)

    # ------------------------
    # Draw bricks
    # ------------------------
    for brick_data in bricks:

        brick = brick_data["rect"]
        color = brick_data["color"]

        pygame.draw.rect(
            screen,
            color,
            brick,
            border_radius=5
        )

        # Highlight
        pygame.draw.rect(
            screen,
            WHITE,
            brick,
            2,
            border_radius=5
        )


    # ------------------------
    # Draw paddle
    # ------------------------
    pygame.draw.rect(
        screen,
        BLUE,
        paddle,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        WHITE,
        paddle,
        2,
        border_radius=8
    )


    # ------------------------
    # Draw balls
    # ------------------------
    for ball in balls:
        ball.draw()


    # ------------------------
    # Draw powerup
    # ------------------------
    if powerup:

        pygame.draw.rect(
            screen,
            PURPLE,
            powerup,
            border_radius=5
        )


    # ------------------------
    # Score
    # ------------------------
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 15)
    )


    # Combo
    combo_text = font.render(
        f"Combo: {combo}",
        True,
        WHITE
    )

    screen.blit(
        combo_text,
        (WIDTH - 150, 15)
    )


    # Lives
    lives_text = font.render(
        f"Lives: {lives}",
        True,
        WHITE
    )

    screen.blit(
        lives_text,
        (WIDTH // 2 - 50, 15)
    )


    # ------------------------
    # Game Over
    # ------------------------
    if game_over:

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )

        restart = font.render(
            "Press SPACE to restart",
            True,
            WHITE
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )


    # ------------------------
    # You Win
    # ------------------------
    if game_won:

        text = big_font.render(
            "YOU WIN!",
            True,
            GREEN
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )

        restart = font.render(
            "Press SPACE to play again",
            True,
            WHITE
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )


    pygame.display.flip()

    clock.tick(60)