import pygame

# initializing window
pygame.init()
width, height = 1000, 750
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG")

# setting parameters
FPS = 100
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
paddle_width, paddle_height = 20, 100
ball_radius = 10
winning_score = 10
score = pygame.font.SysFont("arial", 70)


# creating paddle class
class Paddle:
    COLOR = white
    VEL = 6

    def __init__(self, x, y, width, height):
        self.x = self.starting_x = x
        self.y = self.starting_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))

    # moving the paddle up and down depending on button clicked (w, s, arrowUP, arrowDown)
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    # reset to starting position
    def reset(self):
        self.x = self.starting_x
        self.y = self.starting_y


class Ball:
    MAX_VEL = 6
    COLOR = red

    # setting initial starting ball position and velocity
    def __init__(self, x, y, radius):
        self.x = self.starting_x = x
        self.y = self.starting_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(black)

    left_score_text = score.render(f"{left_score}", 1, white)
    right_score_text = score.render(f"{right_score}", 1, white)

    # setting top left corner of the scores
    win.blit(left_score_text, (width // 4 - left_score_text.get_width() // 2, 30))
    win.blit(right_score_text, (width * (3 / 4) -
                                right_score_text.get_width() // 2, 30))
    # drawing both paddles
    for paddle in paddles:
        paddle.draw(win)

    # drawing dashed line to split screen
    for i in range(10, height, height // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, white, (width // 2 - 10, i, 20, height // 20))

    ball.draw(win)
    pygame.display.update()


def collision(ball, left_paddle, right_paddle):
    # check if it collides with top or bottom
    if ball.y + ball.radius >= height:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    # check if it collides with left or right paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # check where the ball hits the paddle(closer to center -> less velocity) and return it
                # in opposite direction
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    # moving paddle up or down and check if they go out of the window
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= height:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= height:
        right_paddle.move(up=False)


# main loop for updating the window
def main():
    clock = pygame.time.Clock()
    running = True

    # creating paddles in the middle of the left and right side and ball in the middle
    left_paddle = Paddle(20, height // 2 - paddle_height //
                         2, paddle_width, paddle_height)
    right_paddle = Paddle(width - 20 - paddle_width, height //
                          2 - paddle_height // 2, paddle_width, paddle_height)
    ball = Ball(width // 2, height // 2, ball_radius)

    left_score = 0
    right_score = 0

    while running:
        clock.tick(FPS)
        draw(window, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        # handling pressed keys
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        collision(ball, left_paddle, right_paddle)
        # check if a player made point
        if ball.x < 0:
            right_score += 1
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
        elif ball.x > width:
            left_score += 1
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
        # check if a player made 10 points
        won = False
        if left_score >= winning_score:
            won = True
            winning_message = "Left Player Won!"
        elif right_score >= winning_score:
            won = True
            winning_message = "Right Player Won!"
        # finish the game if there is winner
        if won:
            # display winning message in the center
            text = score.render(winning_message, 1, white)
            window.blit(text, (width // 2 - text.get_width() //
                               2, height // 2 - text.get_height() // 2))
            pygame.display.update()
            # 5 seconds pause after finishing the game and then starts new game
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
