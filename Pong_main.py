import pygame
import os
pygame.init()
pygame.mixer.init()

ABSOLUTE_PATH = os.path.dirname(__file__)
BOUNCE_OFF_SOUND_FILE = os.path.join(ABSOLUTE_PATH, "254__noisecollector__pong-softsynth", "4374__noisecollector__pongblipf5.wav")
BOUNCE_OFF_SOUND = pygame.mixer.Sound(BOUNCE_OFF_SOUND_FILE)
WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('consolas', 40)
pygame.display.set_caption('Pong Game, two player version')
FPS = 60    # dictates speed of the game, lower value makes it easier and uglier (change ball velocity)
WHITE, GRAY, BLACK = (255, 255, 255), (100, 100, 100), (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VELOCITY = WIDTH//50, HEIGHT//6, 4
BALL_RADIUS, BALL_VELOCITY = ((WIDTH+HEIGHT)//170), (PADDLE_VELOCITY + 1)
WINNING_SCORE = 10

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
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # adding outlines
        
    def move(self, move_down = True):
        if move_down:
            self.y_position += PADDLE_VELOCITY
            # self.rect.move_ip(0, +PADDLE_VELOCITY)
        else:
            self.y_position -= PADDLE_VELOCITY
            # self.rect.move_ip(0, -PADDLE_VELOCITY)

class Ball:
    def __init__(self, color, x_position, y_position, radius):
        self.x_position = self.original_x_position = x_position
        self.y_position = self.original_y_position = y_position
        self.radius = radius
        self.color = color
        self.x_velocity = BALL_VELOCITY
        self.y_velocity = 0
        # self.rect = pygame.Rect(self.x_position, self.y_position, self.radius, self.radius)   # needed for 'colliderect' collision detection method

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x_position, self.y_position), self.radius)
        # self.rect = pygame.Rect(self.x_position, self.y_position, self.radius, self.radius)   # needed for 'colliderect' collision detection method
        # pygame.draw.ellipse(surface, self.color, self.rect)                                   # needed for 'colliderect' collision detection method

    def move(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity

    def reset(self):
        self.x_position = self.original_x_position
        self.y_position = self.original_y_position
        self.x_velocity *= -1   # after reset the other player starts the game
        self.y_velocity = 0

def keys_input(left_paddle, right_paddle):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and right_paddle.y_position - PADDLE_VELOCITY > 0:                                 # screen top boundary
        right_paddle.move(move_down = False)
    if keys[pygame.K_DOWN] and right_paddle.y_position + PADDLE_VELOCITY + right_paddle.height <= HEIGHT:   # screen bottom boundary
        right_paddle.move(move_down = True)
'''
    if keys[pygame.K_w] and left_paddle.y_position - PADDLE_VELOCITY > 0:                                   # screen top boundary
        left_paddle.move(move_down = False)
    if keys[pygame.K_s] and left_paddle.y_position + PADDLE_VELOCITY + left_paddle.height <= HEIGHT:        # screen bottom boundary
        left_paddle.move(move_down = True)
'''
def bot_opponent(ball, paddle):                                                 # simple, mildly effective computer opponent (scale with paddle move speed)
    if ball.y_position <= paddle.y_position and ball.x_position <= WIDTH//2:    # tries to keep paddle on the level with the ball when it's on left half
        paddle.move(move_down = False)
    if ball.y_position > (paddle.y_position + paddle.height) and (ball.x_position <= WIDTH//2):
        paddle.move(move_down = True)
                    
def bounce_off(ball, paddle):                                          # this function pretends there is some physics in the game
    paddle_middle_y_position = paddle.y_position + (paddle.height / 2) # in short - the ball bounces differently depending where it collided with a paddle
    difference_in_Y_position = paddle_middle_y_position - ball.y_position
    reduction_factor = (paddle.height / 2) / BALL_VELOCITY
    y_velocity = difference_in_Y_position / reduction_factor
    ball.y_velocity = -1 * y_velocity
    ball.x_velocity *= -1
    BOUNCE_OFF_SOUND.play()
                
def handle_collision(ball, left_paddle, right_paddle):
    # collision check with floor and ceiling, if true reverse direction on Y axis
    if ball.y_position + ball.radius >= HEIGHT:  # floor check
        ball.y_velocity *= -1
    elif ball.y_position - ball.radius <= 0:   # ceiling check
        ball.y_velocity *= -1

    if (ball.y_position >= left_paddle.y_position) and (ball.y_position <= left_paddle.y_position + PADDLE_HEIGHT) and (ball.x_velocity < 0): 
        # ball lower then the top of the paddle         ball higher then the bottom of the paddle                       ball going left
        if ball.x_position - ball.radius <= left_paddle.x_position + left_paddle.width:
        # leftmost part of the ball         right side of the left paddle    
            bounce_off(ball, left_paddle)

    if ball.y_position >= right_paddle.y_position and ball.y_position <= right_paddle.y_position + PADDLE_HEIGHT and (ball.x_velocity > 0):
        # ball lower then the top of the paddle       ball higher then the bottom of the paddle                       ball going right
        if ball.x_position + ball.radius >= right_paddle.x_position:
        # rightmost part of the ball        left side of the right paddle
            bounce_off(ball, right_paddle)

def handle_collision_2(ball, left_paddle, right_paddle):               #TODO trying to find better collision detection method, probably not worth it
    # collision check with floor and ceiling, if true reverse direction on Y axis
    if ball.y_position + ball.radius >= HEIGHT:  # floor check
        ball.y_velocity *= -1
    elif ball.y_position - ball.radius <= 0:   # ceiling check
        ball.y_velocity *= -1
    
    if ball.rect.colliderect(left_paddle) or ball.rect.colliderect(right_paddle):   # this gives weird results as ball is not really a rect object
        bounce_off(ball, right_paddle)                                              # even if drawn as one
        print('kolizja wykryta metodą 2')
    
def draw_game_loop(surface, left_paddle, right_paddle, ball, left_score, right_score):
    surface.fill(BLACK)
    
    # draw center line 
    centerline_X_position = (WIDTH//2 - WIDTH//140)
    centerline_element_width = HEIGHT//100
    centerline_element_height = HEIGHT//30
    for i in range(HEIGHT//30, HEIGHT, HEIGHT//10): # first element Y position, total screen Y, length breaks between elements
            if i % 2 == 0:                          # every other element
                obj = pygame.Rect(centerline_X_position, i, centerline_element_width, centerline_element_height)
                pygame.draw.rect(surface, GRAY, obj)
    

    left_score_text = FONT.render(str(left_score), 1, GRAY)
    right_score_text = FONT.render(str(right_score), 1, GRAY)
    surface.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))      # center of the left half of the screen
    surface.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20)) # center of the right half of the screen

    left_paddle.draw(surface)
    right_paddle.draw(surface)
    ball.draw(surface)
    pygame.display.update()            

def main():
    clock = pygame.time.Clock()
    left_paddle_X_position = WIDTH//70
    left_paddle_Y_position = (HEIGHT//2 - PADDLE_HEIGHT//2)
    left_paddle = Paddle(GRAY, left_paddle_X_position, left_paddle_Y_position, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    right_paddle_X_position = (WIDTH - WIDTH//70 - PADDLE_WIDTH)
    right_paddle_Y_position = (HEIGHT//2 - PADDLE_HEIGHT//2)   
    right_paddle = Paddle(GRAY, right_paddle_X_position, right_paddle_Y_position, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WHITE, WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while True:
        clock.tick(FPS)
        draw_game_loop(SCREEN, left_paddle, right_paddle, ball, left_score, right_score)
        keys_input(left_paddle, right_paddle)
        bot_opponent(ball, left_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        # handle_collision_2(ball, left_paddle, right_paddle)
        
        if ball.x_position < 0:
            right_score += 1
            ball.reset()
        elif ball.x_position > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_txt = 'Left'
        elif right_score >= WINNING_SCORE:
            won = True
            win_txt = 'Right'

        if won:
            text = FONT.render(win_txt + ' Player Won!', 1, WHITE)
            SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        pygame.display.update()

main()