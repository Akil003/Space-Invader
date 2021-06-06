import pygame
import random
import tkinter as tk
from pygame.constants import KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_ESCAPE, K_d, K_g, K_l, K_o, K_p, K_r, K_u, QUIT
from pygame import mixer
from pygame import time
from math import log

# initialize the pygame
pygame.init()

# Title, Icon and font
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
font1 = pygame.font.Font("Caramel Sweets.ttf", 64)
font2 = pygame.font.Font("Caramel Sweets.ttf", 48)

#create the screen
root = tk.Tk()
width, height= int(root.winfo_screenwidth()),int(root.winfo_screenheight())
screen = pygame.display.set_mode((width, height))
background = random.choice(["Background"+str(i)+".jpg" for i in range(2,8) ])
backgroundImage = pygame.transform.scale(pygame.image.load(background), (width, height))

# Music
music1 = "Su Turno.wav"
music2 = "Dreaming.wav"

music_intro = "Interplanetary Odyssey.wav"
levelUpSound = mixer.Sound("levelup.wav")
exp_sound = mixer.Sound("explosion_enemy.wav")
laser_sound = mixer.Sound("laserEnemy.wav")
gun_sound = mixer.Sound("Laser.wav")
shieldsound = mixer.Sound("shield.wav")

def initials():
    screen.fill((0, 0, 0))
    screen.blit(backgroundImage, (0, 0))
    screen.blit(initialText, (iTextX, iTextY))
    screen.blit(initialTexta, (iTextaX, iTextaY))

def finals():
    screen.fill((0, 0, 0))
    screen.blit(backgroundImage, (0, 0))
    screen.blit(final_score, (fScoreX, fScoreY))
    screen.blit(final_level, (flevelX, flevelY))
    screen.blit(finalText, (fTextX, fTextY))
    screen.blit(finalTexta, (fTextaX, fTextaY))
    screen.blit(finalTextb, (fTextbX, fTextbY))

def initial_values():
    global previous_kill_score, previous_kill_shield, kill
    global clock, previousTime, currentTime, tc
    global health, numOfEnemy 
    global level_player, level_prev, noOfBullets 
    global playerX, playerY, changeX, changeY
    global enemyX, enemyY, eChangeX, eChangeY
    global bulletImg, bulletWidth, bulletHeight, bulletX, bulletY, bChangeX, bChangeY, bState, pBullet, reload_value
    global eBulletImg, eBulletX, eBulletY, eBChangeX,eBChangeY
    global score_player, i, j
    global count_movement, count_fire 
    global ultra_started
    global shield

    ultra_started = 0

    # To display text in level 0
    count_movement = 0
    count_fire = 0
    
    # kill
    previous_kill_score = 0
    previous_kill_shield = 0
    kill = 0
    
    #Score 
    score_player = 0

    # Shield
    shield = True

    # Clock
    clock = pygame.time.Clock()
    previousTime = 0
    currentTime = 0
    tc = 2000

    # level
    level_prev = 0
    level_player = 0

    #Player location
    playerX = width/2 -playerWidth/2
    playerY = height - 120
    changeX = 0
    changeY = 0

    #enemy
    numOfEnemy = 1

    enemyX = []
    enemyY = []
    eChangeX = []
    eChangeY = []
    for i in range(numOfEnemy):

        enemyX.append(random.randint(0, width-64))
        enemyY.append(random.randint(50, 200))
        eChangeX.append(random.random()*random.choice([-1, 1])*width/4000*log(level_player+1)**(1/2))
        eChangeY.append(height*log(level_player+1)**(1/2)/1000)

    # Health
    health = 5
    
    # Bullet
    bChangeY = -height
    bulletX = playerX + playerWidth/2 - bulletWidth
    bulletY = -height
    bState = "Ready"

    # reload_value 
    reload_value = height*200/(1+level_player)**(5/4)

    # Enemy Bullets
    eBulletImg = []
    eBulletX = []
    eBulletY = []
    eBChangeX = 0
    speed_factor = 1/400 * ((level_player+1)**(1/3))
    eBChangeY = height*speed_factor
    for i in range(numOfEnemy):
        eBulletImg.append(pygame.transform.scale(pygame.image.load(eBullet), (eBulletWidth, eBulletHeight)))
        eBulletX.append(enemyX[i]+enemyWidth/2)
        eBulletY.append(enemyY[i])

def level(kill, score_player):
    global level_player, level
    if level_player < int(kill/((level_player+2)**(5/4))) + int(score_player/(10000*(1+level_player**1/2))):
        level_player = int(kill/((level_player+2)**(5/4))) + int(score_player/(10000*(1+level_player**1/2)))
    level_disp = font2.render(f"Level: {level_player}", True, (255, 255, 255))
    screen.blit(level_disp, (levelX, levelY))
    return level_player


# Final Screen
def finishing():
    global running, kill, health
    # Background sound
    mixer.music.load(music1)
    mixer.music.play(-1)
    finish = False
    while not finish:
        finals()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    mixer.music.stop()
                    initial_values()
                    mixer.music.load(music2)
                    mixer.music.play(-1)
                    finish = True
                if event.key == K_ESCAPE:
                    mixer.music.stop()
                    initial_values()
                    return 1
            pygame.display.update() 

def level_values():
    global enemyX, enemyY, eChangeX, eChangeY, eBChangeY, score
    global pBullet, bulletImg, bulletX, bulletY, bState, reload_value
    global eBullet, bulletWidth, bulletHeight, ebState, eBullet, eBulletImg, eBulletX, eBulletY, i
    global uEnemyImg, uEnemyX, uEnemyY, uEChangeX, uEChangeY, uEBChangeY, numOfUEnemy, uEHealth
    global level_player
    global uEBulletImg, uEBulletX, uEBulletY, shield

    # Enemy Update
    enemyX = []
    enemyY = []
    eChangeX = []
    eChangeY = []
    
    for i in range(numOfEnemy):
        enemyX.append(random.randint(0, width-64))
        enemyY.append(random.randint(50, 200))
        eChangeX.append(random.random()*random.choice([-1, 1])*width/400*log(level_player+1)**(1/3))
        eChangeY.append(random.random()*random.choice([-1, 1])*height*log(level_player+1)**(1/4)/1000)

    # Ultra Enemy Update
    if level_player > level_ultra:
        numOfUEnemy = int((level_player-1)/2)
        uEnemyImg = []
        uEnemyX = []
        uEnemyY = []
        uEChangeX = []
        uEChangeY = []
        uEHealth = [1 for l in range(numOfUEnemy)]
        for l in range(numOfUEnemy):
            uEnemyImg.append(u_enemy_scaled)
            uEnemyX.append(random.randint(0, width-64))
            uEnemyY.append(random.randint(50, 200))
            uEChangeX.append(random.random()*random.choice([-1, 1])*width/1000*log(level_player+1)**(1/2))
            uEChangeY.append(random.random()*random.choice([-1, 1])*height*log(level_player+1)**(1/4)/2000)

    # Bullet Update

    bulletX = playerX + playerWidth/2 - bulletWidth/2
    bulletY = -height
    bState = "Ready"
    reload_value = height*200/(1+level_player)**(5/4)

    # Enemy Bullet Update
    eBulletImg = []
    eBulletX = []
    eBulletY = [height for k in range(numOfEnemy)]
    speed_factor = 1/400 * ((level_player+1)**(1/3))
    eBChangeY = height* speed_factor
    for i in range(numOfEnemy):
        eBulletImg.append(pygame.transform.scale(pygame.image.load(eBullet), (eBulletWidth, eBulletHeight)))
        eBulletX.append(enemyX[i]+enemyWidth/2)
        luck_list = [0 for _ in range(25)]
        luck_list.append(1)
        luck = random.choice(luck_list)
    if luck:
        for i in range(numOfEnemy):
            if eBulletY[i] >= height:
                laser_sound.play()
                eBulletX[i], eBulletY[i] = enemyX[i]+enemyWidth/2, enemyY[i] + enemyHeight

    # Ultra Enemy Bullet Update
    if level_player > level_ultra:
        uEBulletImg = []
        uEBulletX = []
        uEBulletY = [height for k in range(numOfUEnemy)]
        speed_factor = 1/400 * ((level_player+1)**(1/3))
        uEBChangeY = 0*speed_factor
        for l in range(numOfUEnemy):
            uEBulletImg.append(pygame.transform.scale(pygame.image.load(uEBullet), (uEBulletWidth, uEBulletHeight)))
            uEBulletX.append(enemyX[i]+enemyWidth/2-uEBulletWidth)
            
            luck_list = [0 for _ in range(25)]
            luck_list.append(1)
            luck = random.choice(luck_list)
            if luck:
                laser_sound.play()
                uEBulletY[l] = uEnemyY[l] - enemyHeight*4/5
            else:
                uEBulletY[l] = height


# Constants throughout the game

def constants():
    global like, pBullet, eBullet, bullet, playerPic, enemyPic, uEnemyPic, uEBullet, shieldImg
    global rLives, lLives, iTextX, iTextY, iTextaX, iTextaY, initialText, initialTexta
    global uECollisionRange, collisionRange, eCollisionRange, peCollisionRange, unitKill, unitMovement, lUCollisionRange, sUCollisionRange, pueCollisionRange
    global fTextX, fTextY, fTextaX, fTextaY, fTextbX, fTextbY, fScoreX, fScoreY, flevelX, flevelY
    global kTextX, kTextY, unitKill
    global sTextX, sTextY
    global levelX, levelY
    global player_scaled, playerWidth, playerHeight
    global enemyWidth, enemyHeight, enemy_scaled
    global bulletWidth, bulletHeight, bulletImg
    global eBulletWidth, eBulletHeight
    global uEnemyWidth, uEnemyHeight, u_enemy_scaled
    global uEBulletWidth, uEBulletHeight
    global level_ultra
    global shield_scaled

    # Icons
    uEBullet = "Ultra Bullet.png"
    eBullet = "ebullet.png"
    bullet = "bullet.png"
    rlike = "rlike.png"
    llike = "llike.png"
    enemyPic = "Enemy_a.png"
    playerPic = "Spaceship.png"
    uEnemyPic = "Enemy.png"
    pBullet = "bullet.png"
    shieldImg = "shield.png"
    rLives = pygame.image.load(rlike)
    lLives = pygame.image.load(llike)

    

    # Initial Text
    iTextX = int(width/6)
    iTextY = int(height/2)
    iTextaX = int(width/20)
    iTextaY = int(height*4/5)
    initialText = font2.render("Welcome! Press spacebar to enter the game", True, (255, 255, 255))
    initialTexta = font2.render("Press Esc to exit", True, (255, 255, 255))

    # Final Text location
    fTextX = int(width*2/5)
    fTextY = int(height/3)
    fTextaX = int(width/20)
    fTextaY = int(height*4/5)
    fTextbX = int(width/20)
    fTextbY = int(height*3/5)
    fScoreX = int(width*4/10)
    fScoreY = int(height/2)
    flevelX = int(width*4/10)
    flevelY = int(height*3/5)

    # Kill text location
    unitKill = 1
    kTextX = int(width/20)
    kTextY = int(height/20)

    # Score text location
    sTextX = int(width*8/10)
    sTextY = int(height/20)

    # Level text location
    levelX = width/20
    levelY = height*2/10
    
    # Player
    playerWidth, playerHeight = int(width/10), int(height/8)
    player_scaled = pygame.transform.scale(pygame.image.load(playerPic),(playerWidth, playerHeight))

    # Shield
    shield_scaled = pygame.transform.scale(pygame.image.load(shieldImg),(int(playerWidth*3/2), int(playerHeight*5/4)))

    # Enemy
    enemyWidth, enemyHeight = int(width/14), int(height/10)
    enemy_scaled = pygame.transform.scale(pygame.image.load(enemyPic), (enemyWidth, enemyHeight))

    # Ultra Enemy
    uEnemyWidth, uEnemyHeight = int(width/12), int(height/8)
    u_enemy_scaled = pygame.transform.scale(pygame.image.load(uEnemyPic), (uEnemyWidth, uEnemyHeight))

    # Collision
    eCollisionRange = (enemyWidth/2)
    uECollisionRange = (uEnemyWidth/2)
    pueCollisionRange = ((((uEnemyWidth/2)**2 + (uEnemyHeight/2)**2)**(1/2)) + (((playerWidth/2)**2 + (playerHeight/2)**2)**(1/2)))/2**(1/2)
    collisionRange = (((playerWidth/2)**2 + (playerHeight/2)**2)**(1/2))/(2)**(1/2)
    peCollisionRange = (((enemyWidth/2)**2 + (enemyHeight/2)**2)**(1/2))/(2)**(1/2) + (((playerWidth/2)**2 + (playerHeight/2)**2)**(1/2))/(2)**(1/2)
    sUCollisionRange = playerWidth/2*9/10
    lUCollisionRange = uEnemyWidth*4/10
    unitMovement = width/400

    # Bullet
    bulletWidth, bulletHeight = int(width/340), int(height)
    bulletImg = (pygame.transform.scale(pygame.image.load(pBullet), (bulletWidth, bulletHeight)))

    # Enemy Bullet
    eBulletWidth, eBulletHeight = int(width/100), int(height/40)

    # Ultra Enemy Bullet
    uEBulletWidth, uEBulletHeight = int(uEnemyWidth*3/4), int(height)

    # Ultra level
    level_ultra = 5

# Initial Screen
def initializing():
    initial_values()
    global backgroundImage, initialText, initialTexta, music1, music2
    game = True

    # Background sound
    mixer.music.load(music_intro)
    mixer.music.play(-1)
    while game:
        initials()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mixer.music.stop()
                    mixer.music.load(music2)
                    mixer.music.play(-1)
                    game = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        pygame.display.update()

constants()
initializing()
level(kill, score_player)

# Boss
bossWidth = int(width*3/5)
bossHeight = int(height*7/10)
boss = pygame.transform.scale(pygame.image.load("Boss.png"), (bossWidth, bossHeight))
bossX = width/2- bossWidth/2 + random.random()*random.choice([-1, 1])*width*3/5
bossY = height
bossChangeX = width*1/4000
bossAppearanceError = width/500
if bossX > width/2 - bossWidth/2:
    bossChangeX = -bossChangeX
bossChangeY = height*1/800
bosstext = font2.render("This level will be available soon! Thankyou for playing.", True, (255, 255, 255))
def boss_level():
    
    global bossX, bossY
    if not width/2- bossWidth/2 - bossAppearanceError <= bossX <= width/2 + bossAppearanceError -bossWidth/2:
        bossX += bossChangeX
    if bossY > bossAppearanceError/5:
        bossY -= bossChangeY
    screen.blit(boss, (bossX, bossY))
    screen.blit(bosstext, (width/100, height/2))
    

def player(x, y):
    screen.blit(player_scaled, (playerX, playerY))

def lives_remaining(health):
    for i in range(int(2*health)):
        if i%2 == 0:
            screen.blit(lLives, (width/20 + int(i/2)*width/20, height/8))
        else:
            screen.blit(rLives, (width/20 + int(i/2)*width/20, height/8))

def enemy(x, y):
    screen.blit(enemy_scaled, (x, y))

def bullet(x, y):
    global bState
    bState = "Fire"
    screen.blit(bulletImg, (x, y))

def e_bullet(x, y):
    screen.blit(eBulletImg[i], (x, y))

def u_enemy(x, y):
    screen.blit(uEnemyImg[l], (x, y))

def u_e_bullet(x, y):
    screen.blit(uEBulletImg[l],(x, y))

def contact(x1, y1, x2, y2):
    if ((x2 - x1)**2 + (y2 - y1)**2)**(1/2) <= collisionRange**(19/20):
        exp_sound.play()
        return 1
    return 0

def e_contact(x1, x2):
    if (abs(x2 - x1)) <= eCollisionRange:
        return 1
    return 0

def u_e_contact(x1, x2):
    if (abs(x2 - x1)) <= uECollisionRange:
        return 1
    return 0

def u_contact(x1, x2):
    if abs(x1 - x2) <= sUCollisionRange:
        return  2
    if abs(x1 - x2) <= lUCollisionRange:
        return 1
    return 0
def player_enemy_contact(x1, y1, x2, y2):
    if ((x2 - x1)**2 + (y2 - y1)**2)**(1/2) <= peCollisionRange:
        exp_sound.play()
        return 1
    return 0

def player_u_enemy_contact(x1, y1, x2, y2):
    if ((x2 - x1)**2 + (y2 - y1)**2)**(1/2) <= pueCollisionRange and abs(y2-y1)<= playerHeight*3/5:
        exp_sound.play()
        return 1
    return 0

def kill_enemy(kills):
    kills = font2.render(f"kills: {kills}", True, (255, 255, 255))
    screen.blit(kills, (kTextX, kTextY))

def score_of_player(current_kill, time_elapsed, y_position):
    global score_player, previousTime, previous_kill_score
    score_player += ((current_kill - previous_kill_score)*1000) + (time_elapsed-previousTime)/10
    if (y_position < height - height/5):
        score_player += (height - y_position)*level_player**2/pow(10,3)
    previousTime = time_elapsed
    previous_kill_score = current_kill
    score_disp = font2.render(f"Score: {int(score_player)}", True, (255, 255, 255))
    screen.blit(score_disp, (sTextX, sTextY))

def shield_protection(x, y):
    screen.blit(shield_scaled, (x - playerWidth*1/4, y-playerHeight/20))

# Game loop
running = True
# Background Sound
mixer.music.load(music2)
mixer.music.play(-1)

pause = False
space_pressed = 0
prevFrame = 0

currentFrame = 0
killPerFrame = 0
kill_per_frame = 0

# Power up
frameLog = []
shield = False

# Cheat
g, o, d = 0, 0, 0
godMode = 0

l, u = 0, 0

l, b = 0, 0

while running:
    if godMode:
        health = 5
    currentFrame += 1

    killPerFrame = 0

    space_clicked = 0
    if space_pressed:
        space_pressed -= 1

    # Background Color
    screen.fill((0, 0, 0))
    # Background Image

    screen.blit(backgroundImage, (0, 0))

    # intro
    text1 = "Press arrow keys for movement and space to fire at the enemies. "
    texta = font2.render(text1, True, (255, 255, 255))
    text2 = "Beware though because enemies can shoot too."
    textb = font2.render(text2, True, (255, 255, 255))
    # Event Handling
    for event in pygame.event.get():
        if level_player == 0 and event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE: # For exiting the game
                running = False
            if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                count_movement += 1
            if event.key == K_SPACE:
                space_pressed = 10
                space_clicked = 1
                count_fire +=1
        
        if event.type == pygame.QUIT: # For exiting the game
            running = False
        # keyboard Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE: # For exiting the game
                running = False
            if event.key == K_LEFT:
                    changeX = -unitMovement
            if event.key == K_RIGHT:
                    changeX = unitMovement
            if event.key == K_UP:
                    changeY -= unitMovement
            if event.key == K_DOWN:
                    changeY += unitMovement
            if event.key == K_SPACE:
                space_pressed = 10
                space_clicked = 1
            if event.key == K_g:
                g = 1
            if event.key == K_o:
                o = 1
            if event.key == K_d:
                d = 1
            if event.key == K_r:
                g, o, d = 0, 0, 0
            
            if event.key == K_l:
                l = 1
            if event.key == K_u:
                u = 1
            if event.key == K_d:
                b = 1

            if event.key == K_p:
                pause = True
                if pause:
                    pygame.time.delay(5*pow(10, 3))
            
                
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                changeX = 0
                changeY = 0 
    if level_player == 0:
        if count_fire>0 and count_movement>0:
            screen.blit(textb, (width/8, height/2))
        else:
            screen.blit(texta, (10, height/2))
    if level_player == 10:
            boss_level()

    # Border Conditions

    # a. For player
    if playerX <= -playerWidth/2:
        playerX = -playerWidth/2
    if playerX >= width - playerWidth/2:
        playerX = width - playerWidth/2
    if playerY <=0:
        playerY = 0
    if playerY >= height - playerHeight:
        playerY = height - playerHeight
    
    # c. For player bullet
    bulletCloneX = -10
    bulletCloneY = -height
    if bState == "Ready" and space_clicked:
        gun_sound.play()
        bulletX = playerX + playerWidth/2 - bulletWidth/2
        bulletY = playerY - height
        bulletCloneX = playerX + playerWidth/2 - bulletWidth/2
        bulletCloneY = playerY - height
        bState = "fire"
        if space_pressed:
            bullet(bulletCloneX, bulletCloneY)
    
    bulletY += bChangeY
    if bulletY <= -reload_value:
        bState = "Ready"

                
    # Implementing the changes for the player
    playerX += changeX
    playerY += changeY

    # Updating the frame for Score and the bullet
    
    for i in range(numOfEnemy):
        # b. For enemy
        if enemyX[i] <= 0 or enemyX[i] >= width - enemyWidth:
            eChangeX[i] = -eChangeX[i]
        if enemyY[i] <= 0 or enemyY[i] >= height - enemyHeight*4:
            eChangeY[i] = -eChangeY[i]

        # Implementing the changes for enemies
        
        enemyX[i] += eChangeX[i]
        enemyY[i] += eChangeY[i]
        
        # Kill check
        if e_contact(bulletX + bulletWidth/2, enemyX[i] + enemyWidth/2) and bulletY - height < enemyY[i] and playerY > enemyY[i] + enemyHeight and space_clicked and bState == "Fire":
            exp_sound.play()
            enemyX[i] = random.randint(0, width-enemyWidth)
            enemyY[i] = random.randint(enemyHeight, int(height/5))
            eChangeX[i] = random.random()*random.choice([-1, 1])*width/1000
            eChangeY[i] = random.random()*random.choice([-1, 1])*height*log(level_player+1)**(1/3)/1000
            kill += unitKill
            prevFrame = currentFrame
            bulletX = playerX + playerWidth/2
            bulletY = playerY - height
            for i in range(numOfEnemy):
                if e_contact(bulletX + bulletWidth/2, enemyX[i] + enemyWidth/2):
                    enemyX[i] = random.randint(0, width-enemyWidth)
                    enemyY[i] = random.randint(enemyHeight, int(height/5))
                    eChangeX[i] = random.random()*random.choice([-1, 1])*width/1000
                    eChangeY[i] = random.random()*random.choice([-1, 1])*height*log(level_player+1)**(1/3)/1000
                    kill += unitKill
            bState = "Ready"




        # Player kills
        kill_enemy(kill)

        # Updating the frame for enemy
        enemy(enemyX[i], enemyY[i])
   

    # Implementing the changes for the player
    playerX += changeX
    playerY += changeY

    # Updating the frame for player
    player(playerX, playerY)

    # Implementing the changes for bullet
    luck_list = [0 for i in range(25)]
    luck_list.append(1)
    luck = random.choice(luck_list)
    if luck:
        for i in range(numOfEnemy):
            if eBulletY[i] >= height:
                laser_sound.play()
                eBulletX[i], eBulletY[i] = enemyX[i]+enemyWidth/2-eBulletWidth/2, enemyY[i] + enemyHeight*2/5

    # Implementing the changes for Ultra Buller
    if level_player > level_ultra:
        luck_list = [0 for i in range(50)]
        luck_list.append(1)
        for l in range(numOfUEnemy):
            luck = random.choice(luck_list)
            if luck:
                if uEnemyY[l] < height:
                    laser_sound.play()
                uEBulletX[l], uEBulletY[l] = uEnemyX[l]+uEBulletWidth*1/5, uEnemyY[l] + uEnemyHeight*4/5
            else:
                uEBulletY[l] = height
    
    for i in range(numOfEnemy):
        eBulletX[i] += eBChangeX
        eBulletY[i] += eBChangeY
        e_bullet(eBulletX[i], eBulletY[i])
        if contact(eBulletX[i] + eBulletWidth/2, eBulletY[i] + eBulletHeight/2, playerX + playerWidth/2, playerY + playerHeight/2):
            if not shield:
                health -= 1/2
            eBulletX[i], eBulletY[i] = enemyX[i]+enemyWidth/2-eBulletWidth/2, enemyY[i] + enemyHeight*2/5

        if player_enemy_contact(playerX + playerWidth/2, playerY + playerHeight/2, enemyX[i] + enemyWidth/2, enemyY[i] + enemyHeight/2):
            kill += 1
            if not shield:
                health -= 1
            enemyX[i], enemyY[i]  = random.randint(0, width-64), random.randint(50, 200)

    if level_player> level_ultra:
        for l in range(numOfUEnemy):
            # Constratnst for ultra enemy enemy
            if uEnemyX[l] <= 0 or uEnemyX[l] >= width - uEnemyWidth:
                uEChangeX[l] = -uEChangeX[l]
            if uEnemyY[l] <= 0 or uEnemyY[l] >= height - uEnemyHeight*4:
                uEChangeY[l] = -uEChangeY[l]

            # Implementing the changes for enemies
            
            uEnemyX[l] += uEChangeX[l]
            uEnemyY[l] += uEChangeY[l]
            uEBulletY[l] += uEBChangeY


            for j in range(noOfBullets):
                if u_e_contact(bulletX + bulletWidth/2, uEnemyX[l] + uEnemyWidth/2) and bulletY + height < uEnemyY[l] and playerY > uEnemyY[l] + uEnemyHeight and space_clicked:
                    space_clicked = 0
                    uEHealth[l] -= 1/2
                    bulletY = -height
                    if uEHealth[l] == 0:  
                        uEnemyX[l], uEnemyY[l]  = random.randint(0, width-64), height + uEnemyHeight
                        exp_sound.play()
            # For Ultra bullets
            

            if uEBulletY[l]< height and playerY >uEnemyY[l] + uEnemyHeight:
                if u_contact(uEBulletX[l] + uEnemyWidth/2, playerX + playerWidth/2) == 1:
                    if not shield:
                        health -= 1/2
                    exp_sound.play()
                if u_contact(uEBulletX[l] + uEnemyWidth/2, playerX + playerWidth/2) == 2:
                    if not shield:
                        health -= 1
                    exp_sound.play()
            if player_u_enemy_contact(playerX + playerWidth/2, playerY + playerHeight, uEnemyX[l]+ uEnemyWidth/2, uEnemyY[l] + uEnemyHeight/2):
                exp_sound.play()
                if not shield:
                    health -= 1
                kill += 1
                uEnemyY[l] = height + uEnemyHeight



            # Updating position of Ultra Enemy and it's bullet
            
            u_e_bullet(uEBulletX[l], uEBulletY[l])
            u_enemy(uEnemyX[l], uEnemyY[l])

    if kill - previous_kill_score:
        if len(frameLog) == (2+level_player):
            if level_player>=4:
                if len(frameLog)>(2+level_player) and frameLog[len(frameLog)-1] - frameLog[0] < 400:
                        shieldsound.play()
                        shield = True
                        health = 5       
                        print("Shield and health")   
                if len(frameLog)>3 and frameLog[level_player+1] - frameLog[level_player-2] < 120:
                        shield = True
                        shieldsound.play()
                        print("Shield")
            frameLog.remove(frameLog[0])
        frameLog.append(currentFrame)
            
        prevFrame = currentFrame
        previous_kill_score = kill
        if len(frameLog)==(2+level_player):
            print(frameLog[level_player+1])
            print( frameLog[level_player-1])
        print(frameLog)

    if shield and currentFrame - prevFrame < 200:
        shield_protection(playerX, playerY)
    else:
        shield = False

    lives_remaining(health)

    # Final screen
    if health <= 0:
        # Final texts
        finalText = font1.render("Game over!", True, (255, 255, 255))
        finalTexta = font2.render("Press 'Space' to restart and 'Esc' to reuturn to main menu", True, (255, 255, 255))
        finalTextb = font2.render(f"kills: {kill}", True, (255, 255, 255))
        final_score = font2.render(f"Your score: {int(score_player)}", True, (255, 255, 255))
        final_level = font2.render(f"Level: {level_player}", True, (255, 255, 255))
        finishing()
        if finishing():
            initials()
            mixer.music.stop()
            initializing()
            # Background sound
            mixer.music.load(music2)
            mixer.music.play(-1)
    score_of_player(kill, time.get_ticks(), playerY)
    level(kill, score_player)
    
    levelDifference = level_player - level_prev 
    if levelDifference:
        levelUpSound.play()
        noOfBullets = 1 + int(log(level_player+1)**2)
        numOfEnemy = 1 + int(log(level_player+1)**(3))
        level_prev = level_player
        if not level == 10:
            level_values() 
    if g and o and d:
        godMode = 1
    else:
        godMode = 0
    if l and u:
        level_player += 1
        levelUpSound.play()
        noOfBullets = 1 + int(log(level_player+1)**2)
        numOfEnemy = 1 + int(log(level_player+1)**(3))
        level_prev = level_player
        l, u = 0, 0
        if not level == 10:
            level_values() 
    if l and b:
        level_player -= 1
        noOfBullets = 1 + int(log(level_player+1)**2)
        numOfEnemy = 1 + int(log(level_player+1)**(3))
        level_prev = level_player
        l, b = 0, 0
        if not level == 10:
            level_values()


    pygame.display.update()
pygame.quit()


