import pygame
import random as r
import sys
import time


class Player:
    SCORE = 0
    def __init__(self, name):
        self.name = name;

class Ball:
    RADIUS = 15

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.running = False
        self.draw(pygame.Color('red'))

    def draw(self, colour):
        pygame.draw.circle(screen, colour, (self.x, self.y), self.RADIUS)

    def move(self):
        self.draw(pygame.Color('white'))
        self.x += self.vx
        self.y += self.vy
        self.draw(pygame.Color('red'))

    def bouncing_velocity_change(self, pad):
        pad_center_y = pad.y + Paddle.HEIGHT // 2
        distance_from_center = abs(self.y - pad_center_y)
        if (distance_from_center > Paddle.HEIGHT // 4):
            self.vx = int(self.vx * -(r.randrange(12, 9, -1) * 0.1))
            self.vy += r.randint(-1,2) if r.randint(0,2) == 0 else 0
        elif (distance_from_center > Paddle.HEIGHT // 3):
            self.vx = int(self.vx * -(r.randrange(15, 12, -1) * 0.1))
            self.vy += r.choice([r.randint(1,3)]) if r.randint(0,1) == 0 else 0
        else:
            self.vx = -self.vx if r.randint(0,1) == 0 else int(self.vx * -1.1)
            # self.vy += r.choice([r.randint(-2,-1), r.randint(1,2)]) if r.randint(0,1) == 0 else 0

    def update(self):
        if not self.running:
            return
        newx = self.x + self.vx
        newy = self.y + self.vy

        # if collisions with the paddles:
        if newx + Ball.RADIUS > WIDTH - right_pad.WIDTH or newx - Ball.RADIUS < left_pad.WIDTH:
            # left paddle
            if (left_pad.y < self.y < left_pad.y + left_pad.HEIGHT and newx - Ball.RADIUS < left_pad.WIDTH):
                self.bouncing_velocity_change(left_pad)
                pong.play()
            # right paddle
            elif right_pad.y < self.y < right_pad.y + right_pad.HEIGHT and newx + Ball.RADIUS > WIDTH - right_pad.WIDTH:
                self.bouncing_velocity_change(right_pad)
                pong.play()
            else:
                # while ball is within frame
                while 0 < self.x + Ball.RADIUS and self.x - Ball.RADIUS < WIDTH:
                    # check the 2 cases for each paddle
                    if (left_pad.y < self.y < left_pad.y + left_pad.HEIGHT and newx - Ball.RADIUS < left_pad.WIDTH) or \
                        (right_pad.y < self.y < right_pad.y + right_pad.HEIGHT and newx + Ball.RADIUS > WIDTH - right_pad.WIDTH):
                        self.vx = int(self.vx * -(r.randrange(13, 8, -1) * 0.1))
                        pong.play()
                        while not (self.x + Ball.RADIUS < WIDTH - Paddle.WIDTH and self.x - Ball.RADIUS > Paddle.WIDTH):
                            self.move()
                            make_frame(right_pad=right_pad, left_pad=left_pad)
                        return

                    self.move()
                    make_frame(right_pad=right_pad, left_pad=left_pad)

                if self.x - Ball.RADIUS < 0:
                    p2.SCORE += 1
                elif self.x + Ball.RADIUS > WIDTH:
                    p1.SCORE += 1

                whoosh.play()

                if p1.SCORE >= WINNING_SCORE or p2.SCORE >= WINNING_SCORE:
                    return
                else:
                    pause()
                    self.reinit(BALL_MAX_X, BALL_MAX_Y, BALL_X_SPEED_MIN, BALL_Y_SPEED_MIN)
                    return

        elif newy + Ball.RADIUS > HEIGHT or newy - Ball.RADIUS < 0:
            hit_wall.play()
            self.vy = int(self.vy * -(r.randrange(11, 9, -1) * 0.1))

        self.move()


    def reinit(self, speed_max_x, speed_max_y, speed_min_x, speed_min_y):
            self.__init__(WIDTH // 2 , HEIGHT // 2, vx=Ball.find_random_speed(speed_min_x, speed_max_x),
                      vy=Ball.find_random_speed(speed_min_y, speed_max_y))

    @classmethod
    def init(cls, speed_max_x, speed_max_y, speed_min_x, speed_min_y):
        return Ball(WIDTH // 2, HEIGHT // 2, vx=Ball.find_random_speed(speed_min_x, speed_max_x),
                      vy=Ball.find_random_speed(speed_min_y, speed_max_y))

    @classmethod
    def find_random_speed(cls,min, max):
        r_speed = r.randrange(min, max + 1)
        return r_speed if r.randrange(2) == 0 else -r_speed

class Paddle:
    WIDTH = 12
    HEIGHT = 250
    SPEED = 35

    move_up = False
    move_down = False

    def __init__(self, x, y, colour=pygame.Color('black')):
        self.x = x
        self.y = y
        self.colour = colour

    def draw(self, colour):
        r = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(screen, colour, r)

    def update(self):
        self.draw(pygame.Color('white'))

        if self.move_up:
            if self.y > 0:
                self.y -= self.SPEED
            self.move_up = False
        elif self.move_down:
            if self.y < HEIGHT - Paddle.HEIGHT:
                self.y += self.SPEED
            self.move_down = False

        self.draw(self.colour)


WIDTH = 1700
HEIGHT = 750
BALL_X_SPEED_MIN=12
BALL_Y_SPEED_MIN=5
BALL_MAX_X = 20
BALL_MAX_Y = 18
FRAME_RATE = 50
WINNING_SCORE = 5
TITLE = 'sam\'s pong'
pygame.mixer.init(frequency=44100, size=-16, buffer=1024, channels=1)
pygame.init()
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
screen.fill(pygame.Color(255, 255, 255))
pygame.display.flip()
clock = pygame.time.Clock()
font = "ubuntumono"
my_font = pygame.font.SysFont(font, 20, bold=True)

count_down = False
COUNTDOWN = 3
t1 = 0

left_pad = Paddle(0, HEIGHT // 2 - Paddle.HEIGHT // 2)
right_pad = Paddle(WIDTH - Paddle.WIDTH, HEIGHT // 2 - Paddle.HEIGHT // 2)

p1 = Player("Player 1")
p2 = Player("Player 2")

ball = Ball.init(BALL_MAX_X, BALL_MAX_Y, BALL_X_SPEED_MIN, BALL_Y_SPEED_MIN)
# sounds
pong = pygame.mixer.Sound('Sounds/pong.wav')
whoosh = pygame.mixer.Sound('Sounds/whoosh.wav')
hit_wall = pygame.mixer.Sound("Sounds/wall.wav")


def make_frame(ball=None, right_pad=None, left_pad=None):
    show("Score: {}".format(p1.SCORE), 100, 50)
    p2_score_text = "Score: {}".format(p2.SCORE)
    p2_s_width, p2_s_height = my_font.size(p2_score_text)
    show("Score: {}".format(p2.SCORE), WIDTH-(100+p2_s_width), 50)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    # show count down:
    global count_down, t1, COUNTDOWN
    if count_down:
        t2 = time.time()
        count_down_time = int(t2 - t1)
        for i in range(0,COUNTDOWN+1):
            if count_down_time == i:
                show_num(COUNTDOWN-count_down_time)
        if count_down_time >= 3:
            count_down = False
            ball.running = True


    if p1.SCORE >= WINNING_SCORE or p2.SCORE >= WINNING_SCORE:
        if p1.SCORE >= WINNING_SCORE:
            prompt = "{} wins!".format(p1.name)
        elif p2.SCORE >= WINNING_SCORE:
            prompt = "{} wins!".format(p2.name)
        f_width, f_height = my_font.size(prompt)
        show(prompt, WIDTH//2-f_width//2, HEIGHT//2 - f_height//2)
        pygame.display.flip()
        p1.SCORE = 0
        p2.SCORE = 0
        pause()
        erase = "                          "
        show(erase, WIDTH//2-f_width//2, HEIGHT//2 - f_height//2)
        ball.reinit(BALL_MAX_X, BALL_X_SPEED_MIN, BALL_MAX_Y, BALL_Y_SPEED_MIN)
        ball.draw(pygame.Color("red"))
        pygame.display.flip()
        return

    if not (keys[pygame.K_w] and keys[pygame.K_s]):
        if keys[pygame.K_w]:
            left_pad.move_up = True
        elif keys[pygame.K_s]:
            left_pad.move_down = True

    if not (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
        if keys[pygame.K_UP]:
            right_pad.move_up = True
        elif keys[pygame.K_DOWN]:
            right_pad.move_down = True

    for e in events:
        if e.type == pygame.QUIT:
            quit_game()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if not ball.running:
                count_down = True
                t1 = time.time()
    if ball is not None:
        ball.update()
    if right_pad is not None:
        right_pad.update()
    if left_pad is not None:
        left_pad.update()
    clock.tick(FRAME_RATE)
    pygame.display.flip()


def quit_game():
    if pygame.get_init():
        pygame.quit()

    sys.exit()


def pause():
    while True:
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            quit_game()
        if e.type == pygame.MOUSEBUTTONDOWN:
            break

def show_num(num):
    f = pygame.font.SysFont(font, size=100, bold=True)
    if num == 0:
        num_text = " "
    else:
        num_text = str(num)
    num_text_w, num_text_h = f.size(num_text)
    show(num_text, WIDTH//2 - num_text_w//2, HEIGHT//3 - num_text_h//2,f=f)

def show(text, x, y,f=my_font):
    pygame.font.init()
    bg = f.render("               ", False, pygame.Color('white'), pygame.Color('white'))
    screen.blit(bg,(x,y))
    sur = f.render(text, False, pygame.Color('black'), pygame.Color('white'))
    screen.blit(sur, (x, y))

def main():
    pygame.display.set_caption(TITLE)
    running = True

    # gameloop:
    while running:
        make_frame(ball=ball, right_pad=right_pad, left_pad=left_pad)


if __name__ == "__main__":
    main()
