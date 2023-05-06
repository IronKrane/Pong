import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
# WIN =    pygame.display.set_mode((WIDTH, HEIGHT))
# SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# surface = pygame.Surface(SCREEN.get_size())
# surface = surface.convert()
FONT = pygame.font.SysFont('consolas', 40)
pygame.display.set_caption('Pong Game')
FPS = 60
WHITE, GRAY, BLACK = (255, 255, 255), (100, 100, 100), (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VELOCITY = WIDTH//50, HEIGHT//6, 4
BALL_RADIUS, BALL_VELOCITY = ((WIDTH+HEIGHT)//170), (PADDLE_VELOCITY + 1) # 
WINNING_SCORE = 10


# * important information
# ! alert / warning
# ? not sure... question maybe? 
# todo something to be done
# // strikethrough / commented out
# common comment


class Paddle:
    def __init__(self, color, x_position, y_position, width, height):
        self.x_position = self.original_x_position = x_position
        self.y_position = self.original_y_position = y_position
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect((self.x_position, self.y_position, self.width, self.height))
        
    def reset(self):
        self.x_position = self.original_x_position
        self.y_position = self.original_y_position
        
    def draw(self, surface):
        self.rect = pygame.Rect((self.x_position, self.y_position, self.width, self.height))
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
    def move(self, up=True):    #todo zmienić z up na direction
        if up:
            self.y_position -= PADDLE_VELOCITY
        else:
            self.y_position += PADDLE_VELOCITY    

class Ball:
    def __init__(self, color, x_position, y_position, radius):
        self.x_position = self.original_x_position = x_position
        self.y_position = self.original_y_position = y_position
        self.radius = radius
        self.color = color
        self.x_velocity = BALL_VELOCITY
        self.y_velocity = 0
        self.rect = pygame.Rect((self.x_position, self.y_position, self.radius, self.radius))

    def draw(self, surface):
        
        # ball_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # pygame.draw.circle(ball_surface, self.color, (self.x_position, self.y_position), self.radius)
        pygame.draw.circle(surface, self.color, (self.x_position, self.y_position), self.radius)
        # surface.blit(ball_surface, (self.x_position - self.radius, self.y_position - self.radius))
        

    def move(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity

    def reset(self):
        self.x_position = self.original_x_position
        self.y_position = self.original_y_position
        self.x_velocity *= -1
        self.y_velocity = 0

def keys_input(left_paddle, right_paddle):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and right_paddle.y_position - PADDLE_VELOCITY > 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y_position + PADDLE_VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
    if keys[pygame.K_w] and left_paddle.y_position - PADDLE_VELOCITY > 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y_position + PADDLE_VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
                    
def bounce_off(ball, paddle):
    middle_y_position = (paddle.y_position + paddle.height) / 2
    difference_in_Y = middle_y_position - ball.y_position
    reduction_factor = (paddle.height / 2) / BALL_VELOCITY
    y_velocity = difference_in_Y / reduction_factor
    ball.y_velocity = -1 * y_velocity
    
                
def handle_collision(ball, left_paddle, right_paddle):  #todo może kod kolizji zrobić jako osobną funkcję by blok kodu się nie powielał?
    # collision check with floor and ceiling, if true reverse direction on Y axis
    if ball.y_position + ball.radius >= HEIGHT:  # floor check
        ball.y_velocity *= -1
    elif ball.y_position - ball.radius <= 0:   # ceiling check
        ball.y_velocity *= -1

    if ball.y_position >= left_paddle.y_position and ball.y_position <= left_paddle.y_position + PADDLE_HEIGHT:
        if ball.x_position - ball.radius < left_paddle.x_position + left_paddle.width:
            ball.x_velocity *= -1
            bounce_off(ball, left_paddle)

    elif ball.y_position >= right_paddle.y_position and ball.y_position <= right_paddle.y_position + PADDLE_HEIGHT:
        if ball.x_position + ball.radius > right_paddle.x_position:
            ball.x_velocity *= -1
            bounce_off(ball, right_paddle)

# def handle_collision2(ball, left_paddle, right_paddle):                             #todo
#     # collision check with floor and ceiling, if true reverse direction on Y axis
#     if ball.y_position + ball.radius >= HEIGHT:  # floor check
#         ball.y_velocity *= -1
#     elif ball.y_position - ball.radius <= 0:   # ceiling check
#         ball.y_velocity *= -1
    
    
    # ball_rect = pygame.Rect(ball.x_position - ball.radius, ball.y_position - ball.radius, ball.radius * 2, ball.radius * 2)
    # if ball_rect.colliderect(right_paddle):
    #     ball.x_velocity *= -1
    #     print('kolizja z prawą paletką wykryta metodą 2')
    
    
def draw_game_loop(surface, paddles, ball, left_score, right_score):
    surface.fill(BLACK)
    
    # draw separation line 
    for i in range(HEIGHT//30, HEIGHT, HEIGHT//10):
            if i % 2 == 0:
                obj = pygame.Rect(WIDTH//2 - WIDTH//140, i, HEIGHT//100, HEIGHT//30)
                pygame.draw.rect(surface, GRAY, obj)
    
    

    left_score_text = FONT.render(f'{left_score}', 1, GRAY)                             #todo 
    right_score_text = FONT.render(f'{right_score}', 1, GRAY)
    surface.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    surface.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))


    for paddle in paddles:  # todo przekombinowane
        paddle.draw(surface)

    ball.draw(surface)
    # surface.blit(ball, (ball.x_position, ball.y_position))
    pygame.display.update()            

def main():
    clock = pygame.time.Clock()
    # SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    # surface = pygame.Surface(SCREEN.get_size())
    # surface = surface.convert()
    # właściwości paletek = color, x, y, width, height
    left_paddle = Paddle(GRAY, WIDTH//70, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) 
    right_paddle = Paddle(GRAY, WIDTH - WIDTH//70 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WHITE, WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while True:
        clock.tick(FPS)
        draw_game_loop(SCREEN, [left_paddle, right_paddle], ball, left_score, right_score)
        # SCREEN.blit(surface, (0, 0))
        # text = FONT.render("score {0}".format(score), True, BLACK)
        # SCREEN.blit(text, (5, 10))
        
        keys_input(left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        
        
        if ball.x_position < 0:
            right_score += 1
            ball.reset()
        elif ball.x_position > WIDTH:
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
            SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        
        
        # pygame.display.update()
        # pygame.display.flip()
        
        
        
main()