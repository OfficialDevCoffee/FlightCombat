#flightcombat.py
__author__ = 'stdio.chem@gmail.com'

import pygame, random
from time import sleep
import color

pad_width = 480
pad_height = 720
caption = "Flight Combat"

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj,(x,y))
    pass

def textObject(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def drawText(text, size, color, x, y):
    global gamepad
    textFont = pygame.font.Font('font/pixel.ttf', size)
    TextSurf, TextRect = textObject(text, textFont, color)
    TextRect.center = (x, y)
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    pass

def gameOver():
    global gamepad
    drawText("Game Over", 100, color.red, pad_width / 2, pad_height / 2)
    sleep(2)
    runGame()
    pass

def initGame():
    global gamepad, clock, background1, background2
    global player, enemy, meteor, bullet, bullet_enemy

    enemy = []
    meteor = []
    
    pygame.init()

    gamepad = pygame.display.set_mode((pad_width,pad_height))
    pygame.display.set_caption(caption)

    background1 = pygame.image.load('image/background.png')
    background2 = background1.copy()
    player = pygame.image.load('image/player.png')
    enemy.append(pygame.image.load("image/enemy_a.png"))
    enemy.append(pygame.image.load("image/enemy_b.png"))
    enemy.append(pygame.image.load("image/boom.png"))
    meteor.append(pygame.image.load("image/meteor_a.png"))
    meteor.append(pygame.image.load("image/meteor_b.png"))
    bullet = pygame.image.load("image/bullet.png")
    bullet_enemy = pygame.image.load("image/bullet_enemy.png")
    
    clock = pygame.time.Clock()
    runGame()
    pass

def runGame():
    global gamepad, clock, background1, background2
    global player, enemy, meteor, bullet, bullet_enemy

    enemy_txy = []
    meteor_txy = []
    bullet_xy = []
    bullet_enemy_xy = []
    
    speed = 5
    enemy_max = 5
    
    background1_y = 0
    background2_y = -pad_height
    
    player_x = 200
    player_y = 620
    player_x_change = 0
    player_y_change = 0

    player_health = 100

    crashed = False
    while not crashed:
        if player_health <= 0:
            gameOver()
            pass
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_w]:
                player_y_change = -5
                pass
            elif pygame.key.get_pressed()[pygame.K_s]:
                player_y_change = 5
                pass
            else:
                player_y_change = 0
                pass
            if pygame.key.get_pressed()[pygame.K_a]:
                player_x_change = -5
                pass
            elif pygame.key.get_pressed()[pygame.K_d]:
                player_x_change = 5
                pass
            else:
                player_x_change = 0
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_xy.append([player_x+11,player_y])
                    pass
                pass
            if event.type == pygame.QUIT:
                crashed = True
                pass
            pass
        
        meteor_type = random.randrange(1,200)
        if meteor_type == 1:
            meteor_txy.append([meteor[0],random.randrange(30, pad_width - 30),-100])
            pass
        elif meteor_type == 2:
            meteor_txy.append([meteor[1],random.randrange(30, pad_width - 30),-100])
            pass

        enemy_type = random.randrange(1,500)
        if enemy_type == 1 and len(enemy_txy) < enemy_max:
            enemy_txy.append([enemy[0],random.randrange(100, pad_width - 100),-100,False,0,speed / 2, random.randrange(10,100), 0])
            pass
        elif enemy_type == 2 and len(enemy_txy) < enemy_max:
            enemy_txy.append([enemy[1],random.randrange(100, pad_width - 100),-100,False,0,speed / 2, random.randrange(10,100), 0])
            pass
        
        background1_y += speed
        background2_y += speed

        if background1_y > pad_height:
            background1_y = -pad_height
            pass
        if background2_y > pad_height:
            background2_y = -pad_height
            pass
            
        player_x += player_x_change
        player_y += player_y_change

        if player_x > pad_width - 80:
            player_x = pad_width - 80
            pass
        elif player_x < 0:
            player_x = 0
            pass
        if player_y > pad_height - 80:
            player_y = pad_height - 80
            pass
        elif player_y < 0:
            player_y = 0
            pass

        if not len(bullet_xy) == 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 15
                bullet_xy[i][1] = bxy[1]
                for i, emy in enumerate(enemy_txy):
                    if bxy[1] > emy[2] and bxy[1] < emy[2] + 40 and bxy[0] > emy[1] - 60 and bxy[0] < emy[1] + 60:
                        try:
                            bullet_xy.remove(bxy)
                            pass
                        except:
                            pass
                        emy[6] -= 10
                        if emy[6] < 0:
                            try:
                                enemy_txy[i][0] = enemy[2]
                                pass
                            except:
                                pass
                            pass
                        enemy_txy[i][6] = emy[6]
                        pass
                    pass
                for i, mtr in enumerate(meteor_txy):
                    if bxy[1] > mtr[2] and bxy[1] < mtr[2] + 30 and bxy[0] > mtr[1] - 40 and bxy[0] < mtr[1] + 40:
                        try:
                            bullet_xy.remove(bxy)
                            pass
                        except:
                            pass
                        pass
                    pass
                if bxy[1] <= -80:
                    try:
                        bullet_xy.remove(bxy)
                        pass
                    except:
                        pass
                    pass
                pass
            pass

        if not len(bullet_enemy_xy) == 0:
            for i, bxy in enumerate(bullet_enemy_xy):
                bxy[1] += 15
                bullet_enemy_xy[i][1] = bxy[1]
                if bxy[1] > player_y and bxy[1] < player_y + 40 and bxy[0] > player_x - 60 and bxy[0] < player_x + 60:
                    try:
                        bullet_enemy_xy.remove(bxy)
                        pass
                    except:
                        pass
                    player_health -= 10
                    pass
                for i, mtr in enumerate(meteor_txy):
                    if bxy[1] > mtr[2] and bxy[1] < mtr[2] + 30 and bxy[0] > mtr[1] - 40 and bxy[0] < mtr[1] + 40:
                        try:
                            bullet_enemy_xy.remove(bxy)
                            pass
                        except:
                            pass
                        pass
                    pass
                if bxy[1] > pad_width:
                    try:
                        bullet_enemy_xy.remove(bxy)
                        pass
                    except:
                        pass
                    pass
                pass
            pass
        
        if not len(meteor_txy) == 0:
            for i, mtr in enumerate(meteor_txy):
                mtr[2] += speed * 1.5
                meteor_txy[i][2] = mtr[2]
                if mtr[2] >= pad_height:
                    meteor_txy.remove(mtr)
                    pass
                if mtr[2] > player_y and mtr[2] < player_y + 60 and mtr[1] > player_x - 60 and mtr[1] < player_x + 60:
                    try:
                        meteor_txy.remove(mtr)
                        pass
                    except:
                        pass
                    player_health -= 50
                    pass
                pass
            pass

        if not len(enemy_txy) == 0:
            for i, emy in enumerate(enemy_txy):
                if emy[0] == enemy[2]:
                        emy[7] += 1
                        pass
                if emy[7] > 15:
                    enemy_txy.remove(emy)
                    pass
                if not emy[3]:
                    emy[2] += emy[5]
                    enemy_txy[i][2] = emy[2]
                    if emy[2] >= pad_height / 10:
                        enemy_txy[i][3] = True
                        pass
                    pass
                else:
                    emy_attack = random.randrange(1,150)
                    emy_x_change = random.randrange(1,100)
                    emy_y_change = random.randrange(1,100)

                    if emy_attack == 1 and not emy[0] == enemy[2]:
                        bullet_enemy_xy.append([emy[1] + 10, emy[2] + 15])
                        pass

                    if emy_x_change == 1:
                        emy[4] = random.randrange(-speed, speed) / 5
                        pass
                    if emy_y_change == 1:
                        emy[5] = random.randrange(-speed, speed) / 5
                        pass
                    emy[1] += emy[4]
                    emy[2] += emy[5]
                    if emy[1] < 80:
                        emy[1] = 80
                        emy[4] = random.randrange(-speed, speed) / 5
                        pass
                    elif emy[1] > pad_height / 2 - 80:
                        emy[1] = pad_height / 2 - 80
                        emy[4] = random.randrange(-speed, speed) / 5
                        pass
                    if emy[2] < 0:
                        emy[2] = 0
                        emy[5] = random.randrange(-speed, speed) / 5
                        pass
                    elif emy[2] > pad_width - 80:
                        emy[2] = pad_width - 80
                        emy[5] = random.randrange(-speed, speed) / 5
                        pass
                    pass
                pass
            pass
                
        gamepad.fill((6,17,39))

        drawObject(background1,0,background1_y)
        drawObject(background2,0,background2_y)

        if not len(bullet_xy) == 0:
            for bx, by in bullet_xy:
                drawObject(bullet,bx,by)
                pass
            pass

        if not len(bullet_enemy_xy) == 0:
            for bx, by in bullet_enemy_xy:
                drawObject(bullet_enemy,bx,by)
                pass
            pass
        
        if not len(meteor_txy) == 0:
            for mt, mx, my in meteor_txy:
                drawObject(mt,mx,my)
                pass
            pass

        if not len(enemy_txy) == 0:
            for et, ex, ey, eb, exc, exy, ehtl, ecnt in enemy_txy:
                drawObject(et,ex,ey)
                pass
            pass
        
        drawObject(player, player_x, player_y)
        
        pygame.display.update()
        clock.tick(60)
        pass
    
    pygame.quit()
    quit()
    pass

initGame()
