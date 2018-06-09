import pygame
import numpy as np

pygame.init()
screenWidth = 384
screenHeight = 640

colScore = round(screenWidth/4)
colMark = round(screenWidth*.17)
colTarget = screenWidth - 2*colScore - 2*colMark

rowHeight = round(screenHeight/11)
rowTop = screenHeight - 10*rowHeight

screen = pygame.display.set_mode((screenWidth, screenHeight))

font = pygame.font.SysFont("comicsansms", 36)
fontBig = pygame.font.SysFont("comicsansms", 48)
fontDebug = pygame.font.SysFont("comicsansms", 12)



player1 = True
scoreMultiplier = 1
currentRound = 1
prevTot1 = 0
prevTot2 = 0

text20 = font.render("20", True, (0, 0, 0))
text19 = font.render("19", True, (0, 0, 0))
text18 = font.render("18", True, (0, 0, 0))
text17 = font.render("17", True, (0, 0, 0))
text16 = font.render("16", True, (0, 0, 0))
text15 = font.render("15", True, (0, 0, 0))
text14 = font.render("14", True, (0, 0, 0))
textDouble = font.render("D", True, (0, 0, 0))
textTriple = font.render("T", True, (0, 0, 0))
textBull = font.render("B", True, (0, 0, 0))
textPlayer1 = font.render("P1", True, (0, 0, 0))
textPlayer2 = font.render("P2", True, (0, 0, 0))

# 20-14, D, T, B, score
playerMatrix = np.matrix("3,3,3,3,3,3,3,3,3,3,0; 3,3,3,3,3,3,3,3,3,3,0")
#print(playerMatrix[1,0])

done = False

is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()
screen.fill((255, 255, 255))


def getTargetIndex(t):
    TargetOrder = ["20", "19", "18", "17", "16", "15", "14", "D", "T", "B"]
    return TargetOrder.index(t)

def getPlayerTargetSuccess(p1, t):
    if p1:
        return playerMatrix[0,getTargetIndex(t)]
    else:
        return playerMatrix[1,getTargetIndex(t)]

def TargetCenter(p1, t):
    y = rowTop - rowHeight + round((getTargetIndex(t)+1.5) * rowHeight)
    if p1:
        x = round(colScore + colMark /2)
    else:
        x = round(screenWidth - colScore - colMark /2)
    return x, y

def addMark(p1, t):
    xTarget, yTarget = TargetCenter(p1, t)
    tMark = getPlayerTargetSuccess(p1,t)
    #print(tMark)
    if tMark == 2:
        pygame.draw.line(screen, (0, 0, 0,), (xTarget-round(colMark/3), yTarget+round(rowHeight/3)), (xTarget+round(colMark/3), yTarget-round(rowHeight/3)), 3)
    elif tMark == 1:
        pygame.draw.line(screen, (0, 0, 0,), (xTarget-round(colMark/3), yTarget-round(rowHeight/3)), (xTarget+round(colMark/3), yTarget+round(rowHeight/3)), 3)
    else:
        pygame.draw.circle(screen, (0, 0, 0,), (xTarget, yTarget), round(min(colMark, rowHeight)/2), 3)

def updateRound(r):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore+colMark+1, 0, colTarget-1, rowTop-1))
    screen.blit(font.render(str(r), True, (0, 0, 0)), (colScore+colMark+round((colTarget-font.render(str(r), True, (0, 0, 0)).get_width())/2), 9))

def updatePlayerMatrix(p1, t):
    if p1:
        playerMatrix[0,getTargetIndex(t)] -= 1
    else:
        playerMatrix[1,getTargetIndex(t)] -= 1

def increasePlayerTotal(p1, t, sm):
    sIndex = getTargetIndex(t)
    if p1:
        playerMatrix[0, 10] += [20,19,18,17,16,15,14,0,0,25][sIndex]*sm
    else:
        playerMatrix[1, 10] += [20,19,18,17,16,15,14,0,0,25][sIndex]*sm

def scorePlayerThrow(p1, t, sm):
    xCenter, yDouble = TargetCenter(p1, "D")
    xCenter, yTriple = TargetCenter(p1, "T")
    xCenter = round(screenWidth / 2)
    radius = round(colMark * .4)

# if sm > 1:
#     increasePlayerTotal(p1, t, sm)
#     global scoreMultiplier # TODO Try to remove this global variable : Return the scoreMultiplier instead!!
#     scoreMultiplier = 1
#     pygame.draw.circle(screen, (255, 255, 255), (xCenter, yDouble), radius, 1)
#     pygame.draw.circle(screen, (255, 255, 255), (xCenter, yTriple), radius, 1)
#
# else:
    if getPlayerTargetSuccess(p1,t) > 0:
        updatePlayerMatrix(p1, t)
        addMark(p1,t)
    elif getPlayerTargetSuccess(not p1,t) > 0:
        if t == "D":
            print("Double Scoring")
            pygame.draw.circle(screen, (0, 0, 0), (xCenter, yDouble), radius, 2)
            #scoreMultiplier = 2
            scoreMultiplierTarget(p1, 2)
            pygame.draw.circle(screen, (255, 255, 255), (xCenter, yDouble), radius, 2)
        elif t == "T":
            print("Triple Scoring")
            pygame.draw.circle(screen, (0, 0, 0), (xCenter, yTriple), radius, 2)
            scoreMultiplierTarget(p1, 3)
            pygame.draw.circle(screen, (255, 255, 255), (xCenter, yTriple), radius, 2)
            #scoreMultiplier = 3
        else:
            increasePlayerTotal(p1,t, sm)

def updateScoreScreen(p1):
    if p1:
        p1Score = font.render(str(playerMatrix[0, 10]), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, colScore, rowTop))
        screen.blit(p1Score, (round(colScore-p1Score.get_width())/2, 9))
    else:
        p2Score = font.render(str(playerMatrix[1, 10]), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screenWidth-colScore+1, 0, colScore, rowTop))
        screen.blit(p2Score, (screenWidth-colScore+round((colScore-p2Score.get_width())/2), 9))

def changePlayer(p1):
    if p1:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screenWidth-colScore-colMark+1, 0, colMark-1, rowTop))
        screen.blit(textPlayer1,
                    ((colScore + colMark / 2 - textPlayer1.get_width() / 2), 9))  # Remove y+9 (for testing)
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore+1, 0, colMark-1, rowTop))
        screen.blit(textPlayer2, ((screenWidth - colScore - colMark / 2 - textPlayer2.get_width() / 2), 9))

def checkWinner():
    if playerMatrix[0, 0:10].sum() == 0 and playerMatrix[0,10] > playerMatrix[1,10]:
        textP1Wins = fontBig.render("Player 1 WINS!", True, (0, 0, 0))
        screen.blit(textP1Wins, (round(screenWidth - textP1Wins.get_width()) / 2, screenHeight / 2))
    elif playerMatrix[1, 0:10].sum() == 0 and playerMatrix[0, 10] < playerMatrix[1, 10]:
        textP2Wins = fontBig.render("Player 2 WINS!", True, (0, 0, 0))
        screen.blit(textP2Wins, (round(screenWidth - textP2Wins.get_width()) / 2, screenHeight / 2))
    elif playerMatrix[:, 0:10].sum() == 0 and playerMatrix[0,10] == playerMatrix[1,10]:
        textDraw = fontBig.render("DRAW!", True, (0, 0, 0))
        screen.blit(textDraw, (round(screenWidth-textDraw.get_width())/2, screenHeight / 2))

def scoreMultiplierTarget(p1, sm):
    otherTarget = 1
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                updateRound(currentRound)
                if p1:
                    playerMatrix[0, 10] += otherTarget * sm
                else:
                    playerMatrix[1, 10] += otherTarget * sm
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                otherTarget += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                otherTarget += 4
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                otherTarget *= 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                increasePlayerTotal(p1, "20", sm)
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                increasePlayerTotal(p1, "19", sm)
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                increasePlayerTotal(p1, "18", sm)
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                increasePlayerTotal(p1, "17", sm)
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                increasePlayerTotal(p1, "16", sm)
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                increasePlayerTotal(p1, "15", sm)
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                increasePlayerTotal(p1, "14", sm)
                done = True
        print("other Target loop:", otherTarget)
        if otherTarget > 13: otherTarget = 1
        otherTargetText = font.render(str(otherTarget), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore + colMark + 1, 0, colTarget - 1, rowTop - 1))
        screen.blit(otherTargetText, (round((screenWidth - otherTargetText.get_width()) / 2), 9))
        pygame.display.flip()
        updateRound(currentRound) # todo global variable...
        clock.tick(2)

    # column Grid
pygame.draw.line(screen, (0,0,0,), (colScore, 0), (colScore, screenHeight), 1)
pygame.draw.line(screen, (0,0,0,), (colScore+colMark, 0), (colScore+colMark, screenHeight), 1)
pygame.draw.line(screen, (0,0,0,), (colScore+colMark+colTarget, 0), (colScore+colMark+colTarget, screenHeight), 1)
pygame.draw.line(screen, (0,0,0,), (colScore+2*colMark+colTarget, 0), (colScore+2*colMark+colTarget, screenHeight), 1)
    # Row Grid
for r in range(1,10):
    pygame.draw.line(screen, (0,0,0,), (colScore, rowTop + r*rowHeight), (screenWidth-colScore, rowTop + r*rowHeight), 1)
    # Draw double first line
pygame.draw.line(screen, (0,0,0,), (0, rowTop + 2), (screenWidth, rowTop + 2), 1)
pygame.draw.line(screen, (0,0,0,), (0, rowTop), (screenWidth, rowTop), 1)


    # Target TODO Better center the text with textVar.get_width(), get_heigth() & round()
screen.blit(textPlayer1,((colScore+colMark/2-textPlayer1.get_width()/2), 9)) # Remove y+9 (for testing)
#screen.blit(textPlayer2,((screenWidth-colScore-colMark/2 - textPlayer2.get_width()/2), 9))
screen.blit(text20,(round((screenWidth-text20.get_width())/2), rowTop))
screen.blit(text19,(round((screenWidth-text19.get_width())/2), rowTop+1*rowHeight))
screen.blit(text18,(round((screenWidth-text18.get_width())/2), rowTop+2*rowHeight))
screen.blit(text17,(round((screenWidth-text17.get_width())/2), rowTop+3*rowHeight))
screen.blit(text16,(round((screenWidth-text16.get_width())/2), rowTop+4*rowHeight))
screen.blit(text15,(round((screenWidth-text15.get_width())/2), rowTop+5*rowHeight))
screen.blit(text14,(round((screenWidth-text14.get_width())/2), rowTop+6*rowHeight))
screen.blit(textDouble,(round((screenWidth-textDouble.get_width())/2), rowTop+7*rowHeight))
screen.blit(textTriple,(round((screenWidth-textTriple.get_width())/2), rowTop+8*rowHeight))
screen.blit(textBull,(round((screenWidth-textBull.get_width())/2), rowTop+9*rowHeight))
screen.blit(font.render(str(currentRound), True, (0, 0, 0)), (round((screenWidth-font.render(str(currentRound), True, (0, 0, 0)).get_width())/2), 9))

# Main game loop

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player1 = not player1
            changePlayer(player1)
            scoreMultiplier = 1
            if player1:
                #print("increase round")
                currentRound = currentRound + 1
                updateRound(currentRound)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            scorePlayerThrow(player1,"20",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
            scorePlayerThrow(player1,"19",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
            scorePlayerThrow(player1,"18",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
            scorePlayerThrow(player1,"17",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
            scorePlayerThrow(player1,"16",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            scorePlayerThrow(player1,"15",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            scorePlayerThrow(player1,"14",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            scorePlayerThrow(player1,"T",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            scorePlayerThrow(player1,"D",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            scorePlayerThrow(player1,"B",scoreMultiplier)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            startGame()
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
        #    selectOtherTarget(player1, scoreMultiplier)

# live action section

    updateScoreScreen(player1)
    print("Success Left:", playerMatrix[:, 0:10].sum())
    checkWinner()


    # pressed = pygame.key.get_pressed()
    # if pressed[pygame.K_UP]: y -= 3
    # if pressed[pygame.K_DOWN]: y += 3
    # if pressed[pygame.K_LEFT]: x -= 3
    # if pressed[pygame.K_RIGHT]: x += 3


    if is_blue:
        color = (0, 128, 255)
    else:
        color = (255, 100, 0)



    #updateScoreScreen(not player1, playerMatrix[1, 10])
    #screen.blit(font.render(str(playerMatrix[0, 10]), True, (0, 0, 0) ),(9,9))
    #screen.blit(font.render(str(playerMatrix[1, 10]), True, (0, 0, 0)), (300, 9))

# DEBUG message
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 484, 20))
    playerdata = fontDebug.render(str(playerMatrix), True, (0, 255, 255))
    screen.blit(playerdata, (2, 0))


    pygame.display.flip()
    clock.tick(2)