import pygame
from random import choice, randrange

pygame.init()

borderDashes = []
for i in range(5,600,20):
    borderDashes.append((400,i))

border = pygame.surface.Surface((10,10))
border.fill((255,255,255))
border1 = border.get_rect(midtop=(400,0))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midleft=(30,300))
        self.speed = 3
        self.score = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top >= 0:
            self.rect.move_ip(0,-self.speed)
        elif keys[pygame.K_s] and self.rect.bottom <= 600:
            self.rect.move_ip(0, self.speed)
        elif keys[pygame.K_SPACE]:
            self.score = 10
            ballGroup.empty()

    def draw(self,screen):
        screen.blit(self.image, self.rect)

class Bot(Player):
    def __init__(self):
        super().__init__()
        self.rect = self.image.get_rect(midright=(770, 300))
        #self.speed = 40

    def move(self):
        global ballY
        ballY = 400

        # Movement Algorithm
        balls = ballGroup.sprites()
        endX = 760
        incoming = []
        for ball in balls: # Select only balls moving right
            if ball.vector[0] > 0:
                incoming.append(ball)
        if incoming: # Target the closest ball
            incoming.sort(reverse=True, key=lambda x: x.rect.midright[0])
            ball = incoming[0]
            vectorX = ball.vector.x
            vectorY = ball.vector.y
            ballX = ball.rect.midright[0]
            ballY = ball.rect.midright[1]
            while ballX <= 760:
                # Find ticks until end position and when ball hits wall
                endTicks = abs(int((endX - ballX)/vectorX))
                if vectorY > 0:
                    resetTicks = abs(int((600 - ballY)/vectorY))
                else:
                    resetTicks = abs(int(ballY/vectorY))

                if resetTicks < endTicks:
                    ballX += vectorX * resetTicks
                    ballY += vectorY * resetTicks
                    vectorY *= -1
                else:
                    ballX += vectorX * endTicks + 1
                    ballY += vectorY * endTicks

            if self.rect.centery > ballY and self.rect.top >= 0:
                self.rect.move_ip(0, -self.speed)
            elif self.rect.centery < ballY and self.rect.bottom <= 600:
                self.rect.move_ip(0, self.speed)
        else:
            # Move back to center when no balls incoming
            if self.rect.centery < 300:
                self.rect.move_ip(0, self.speed)
            elif self.rect.centery > 300:
                self.rect.move_ip(0, -self.speed)
            elif self.rect.centery == 300:
                self.rect.move_ip(0, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(400,randrange(0,600,20)))
        self.vector = pygame.Vector2(0, 0)
        self.age = 0

    def spawn(self):
        list = [-5,-4,-3,-2,-1,1,2,3,4,5]
        self.vector = pygame.Vector2((choice((-2,2)), choice(list)))

    def move(self):
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            wallHit.play()
            self.vector.y *= -1
        self.rect.move_ip(self.vector)

        if self.rect.left <= 0:
            bot.score += 1
            scoreSound.play()
            self.kill()
        elif self.rect.right >= 800:
            player.score += 1
            scoreSound.play()
            self.kill()
        self.age += 0.1
        if self.age >= 30:
            if self.vector.x < 0: self.vector.x += -1
            else: self.vector.x += 0.5
            self.age = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Initializing Player and Bot
playersGroup = pygame.sprite.Group()
player = Player()
bot = Bot()
playersGroup.add(player,bot)

# Initializing Ball
ballGroup = pygame.sprite.Group()
ball = Ball()
ballGroup.add(ball)

# Sounds
paddleHit = pygame.mixer.Sound('sounds/Pong_Paddle.wav')
wallHit = pygame.mixer.Sound('sounds/Pong_Wall.wav')
scoreSound = pygame.mixer.Sound('sounds/Pong_Score.wav')
scoreSound.set_volume(0.5)
playerWin = pygame.mixer.Sound('sounds/Pong_Win.wav')
playerWin.set_volume(0.5)
playerLose = pygame.mixer.Sound('sounds/Pong_Lose.wav')
playerLose.set_volume(0.8)
