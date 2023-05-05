import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('consolas', 50)
pygame.display.set_caption('Pong Game')
FPS = 60
WHITE, GRAY, BLACK = (255, 255, 255), (100, 100, 100), (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VELOCITY = 20, 100, 4
BALL_RADIUS, BALL_VELOCITY = 7, 5
WINNING_SCORE = 10


class Paddle:
    def __init__(self, color, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
    def draw(self, surface):
        rect = pygame.Rect((self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color, rect)
        
    def move(self, up=True):
        if up:
            self.y -= self.PADDLE_VELOCITY
        else:
            self.y += self.PADDLE_VELOCITY    
    
    def keys_input(self, left_paddle, right_paddle):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and right_paddle.y - right_paddle.PADDLE_VELOCITY > 0:
                    right_paddle.move(up=True)
                elif event.key == pygame.K_DOWN and right_paddle.y + right_paddle.PADDLE_VELOCITY + right_paddle.height <= HEIGHT:
                    right_paddle.move(up=False)
                elif event.key == pygame.K_w and left_paddle.y - left_paddle.PADDLE_VELOCITY > 0:
                    left_paddle.move(up=True)
                elif event.key == pygame.K_s and left_paddle.y + left_paddle.PADDLE_VELOCITY + left_paddle.height < HEIGHT:
                    left_paddle.move(up=False)


class Ball:
    def __init__(self, color, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.color = color
        self.x_velocity = BALL_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x * -1
        self.y = self.original_y


def draw_separation_line(surface):
    for i in range(HEIGHT//30, HEIGHT, HEIGHT//10):
            if i % 2 != 0:
                rect = pygame.Rect((WIDTH//2 - WIDTH//140, i, HEIGHT//50, HEIGHT//30))
                pygame.draw.rect(surface, GRAY, rect)
                
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:  # sprawdzamy kolizję z sufitem okna
        ball.y_velocity *= -1    # zmiana kierunku poruszania się
    elif ball.y - ball.radius <= 0:   # sprawdzamy kolizję z podłogą okna ?
        ball.y_velocity *= -1

    if ball.x_velocity < 0:  # kolizja dla left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + PADDLE_HEIGHT:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1

                # cały poniższy blok kodu służy zróżnicowaniu odbicia piłki przez paletkę, im bliżej krawędzi(góra/dół) paletki uderzy piłka tym mocniej ma być odbita
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_Y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / BALL_VELOCITY
                y_velocity = difference_in_Y / reduction_factor
                ball.y_velocity = -1 * y_velocity

    else:   # right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + PADDLE_HEIGHT:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1

                # to samo co powyżej tylko prawej paletki, bez tego gra byłaby mało zróżnicowana i nudna
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_Y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / BALL_VELOCITY
                y_velocity = difference_in_Y / reduction_factor
                ball.y_velocity = -1 * y_velocity                

def draw_game_loop(surface, paddles, ball, left_score, right_score):
    surface.fill(BLACK)
    draw_separation_line(surface) 

    left_score_text = FONT.render(f'{left_score}', 1, WHITE)
    right_score_text = FONT.render(f'{right_score}', 1, WHITE)
    surface.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    surface.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))


    for paddle in paddles:  # todo przekombinowane -> do usunięcia
        paddle.draw(surface)

    ball.draw(surface)
    pygame.display.update()            

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    # draw_separation_line(surface)   # just for a game boot up
    
    
    left_paddle = Paddle(WHITE, WIDTH//70, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) 
    right_paddle = Paddle(WHITE, WIDTH - WIDTH//70 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WHITE, WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while True:
        clock.tick(FPS)
        draw_game_loop(surface, [left_paddle, right_paddle], ball, left_score, right_score)
        # snake.handle_keys()
        # snake.move()
        # if snake.get_head_position() == food.position:
        #     snake.length += 1
        #     score += 1
        #     food.randomize_position()
        # snake.draw(surface)
        # food.draw(surface)
        # screen.blit(surface, (0, 0))    # surface separate from screen (37 min), blit the surface otherwise it won't be displayed anywhere
        # text = FONT.render("score {0}".format(score), True, BLACK)
        # screen.blit(text, (5, 10))
        
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         break
        
        keys = pygame.key.get_pressed()
        left_paddle.keys_input(left_paddle, right_paddle)
        right_paddle.keys_input(left_paddle, right_paddle)
        # handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        
        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_txt = 'Left Player Won!'
        elif right_score >= WINNING_SCORE:
            won = True
            win_txt = 'Right Player Won!'

        if won:
            text = FONT.render(win_txt, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        
        
        pygame.display.update()
        
        
        
main()