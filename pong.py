from classes import *
import sys
from time import sleep

def createBorder():
    for coords in borderDashes:
        screen.blit(border,coords)

def collision():
   collideList = pygame.sprite.groupcollide(playersGroup, ballGroup, False, False)
   for key in collideList:
       collideList[key][0].vector.x *= -1
       paddleHit.play()


def updateTimer():
    global ms
    ms = int(ms / 2)
    ballTimer = pygame.USEREVENT + 1
    pygame.time.set_timer(ballTimer, ms)

def speedScaling():
    names = [player]
    ballLength = len(ballGroup)/2
    for name in names:
        if ballLength <= 50:
            x = ballLength - 50
            name.speed = int((-1 * (x ** 2) / 93) + 30)
        else:
            name.speed = 30

def gameEnd():
    screen.fill((0, 0, 0))
    if player.score > bot.score:
        winner = "You Win!"
        playerWin.play()
    elif player.score < bot.score:
        winner = "The Bot Wins"
        playerLose.play()
    else:
        winner = "Tie"

    # Text
    playerFinal = gameFont.render(f'{player.score} - {bot.score}', False, (255, 255, 255))
    playerFinalRect = playerFinal.get_rect(center=(400, 240))
    winner = gameFont.render(f"{winner}", False, (255, 255, 255))
    winnerRect = winner.get_rect(center=(400, 300))
    screen.blit(playerFinal, playerFinalRect)
    screen.blit(winner, winnerRect)
    pygame.display.update()

    sleep(5)
    pygame.quit()
    sys.exit()


# Initial Variables
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong')
gameFont = pygame.font.Font('Pixeltype.ttf', 60)
clock = pygame.time.Clock()
ball.spawn()

# Ball Spawning Timer
ms = 5000
ballTimer = pygame.USEREVENT + 1
exponentialTimer = pygame.USEREVENT + 2
pygame.time.set_timer(exponentialTimer, 5000)
pygame.time.set_timer(ballTimer, ms)

run = True
while run:
    screen.fill((0,0,0))
    if len(ballGroup) == 0 and pygame.time.get_ticks() > 20000:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ballTimer:
            newBall = Ball()
            ballGroup.add(newBall)
            newBall.spawn()
        if event.type == exponentialTimer:
            updateTimer()

    # Updating Sprites
    player.move()
    player.draw(screen)
    bot.move()
    bot.draw(screen)
    for sprite in ballGroup:
        sprite.move()
        sprite.draw(screen)

    # Creating Border and Scores
    createBorder()
    playerScore = gameFont.render(f'{player.score}', False, (255, 255, 255))
    playerScoreRect = playerScore.get_rect(topright=(380, 20))
    botScore = gameFont.render(f'{bot.score}', False, (255, 255, 255))
    botScoreRect = playerScore.get_rect(topleft=(430, 20))
    screen.blit(playerScore, playerScoreRect)
    screen.blit(botScore, botScoreRect)

    # Collision + Speed Scaling
    collision()
    speedScaling()

    pygame.display.update()
    clock.tick(60)
while not run:
    gameEnd()
