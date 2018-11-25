#flightcombat.py
__author__ = 'stdio.chem@gmail.com'

import pygame, random
from time import sleep
import color

pad_width = 480
pad_height = 720
caption = "Flight Combat"
left = 0
center = 1
right = 2
score = 0

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj,(x,y))
    pass

def textObject(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def drawText(text, size, color, x, y, align):
    global gamepad
    textFont = pygame.font.Font('font/pixel.ttf', size)
    TextSurf, TextRect = textObject(text, textFont, color)
    if align == left:
        TextRect.midleft = (x, y)
        pass
    elif align == center:
        TextRect.center = (x, y)
        pass
    elif align == right:
        TextRect.midright = (x, y)
        pass
    gamepad.blit(TextSurf, TextRect)
    pass

def initGame():
    global gamepad, clock, background1, background2
    global player, enemy, meteor, bullet, bullet_enemy, item
    global shot_sound, shot_enemy_sound, explosion_sound, shield_activate_sound, crash_sound, recover_sound, select_sound, gameover_sound
    global energy_icon

    player = []
    enemy = []
    meteor = []
    item = []
    
    pygame.init()

    gamepad = pygame.display.set_mode((pad_width,pad_height))
    pygame.display.set_caption(caption)

    background1 = pygame.image.load('image/background.png')
    background2 = background1.copy()
    player.append(pygame.image.load('image/player_nomal.png'))
    player.append(pygame.image.load("image/player_damaged.png"))
    player.append(pygame.image.load("image/player_shield.png"))
    enemy.append(pygame.image.load("image/enemy_a.png"))
    enemy.append(pygame.image.load("image/enemy_b.png"))
    enemy.append(pygame.image.load("image/boom.png"))
    meteor.append(pygame.image.load("image/meteor_a.png"))
    meteor.append(pygame.image.load("image/meteor_b.png"))
    bullet = pygame.image.load("image/bullet.png")
    bullet_enemy = pygame.image.load("image/bullet_enemy.png")
    item.append(pygame.image.load("image/energy.png"))
    item.append(pygame.image.load("image/shield.png"))
    energy_icon = pygame.image.load("image/energy_icon.png")

    shot_sound = pygame.mixer.Sound("sound/laser.wav")
    shot_enemy_sound = pygame.mixer.Sound("sound/laser_enemy.wav")
    explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
    shield_activate_sound = pygame.mixer.Sound("sound/shield_activate.wav")
    crash_sound = pygame.mixer.Sound("sound/shield_crash.wav")
    recover_sound = pygame.mixer.Sound("sound/recover.wav")
    select_sound = pygame.mixer.Sound("sound/select.wav")
    gameover_sound = pygame.mixer.Sound("sound/gameover.wav")
    
    clock = pygame.time.Clock()
    mainScreen()
    pass
	
def mainScreen():
    global gamepad, clock, background1, background2, select_sound

    background1_y = 0
    background2_y = -pad_height
    
    i = 1
    msgDisp = False
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(select_sound)
                    runGame()
                    pass
                pass
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                pass
            pass
        if i % 30 == 0:
            if msgDisp:
                i = 0
                msgDisp = False
                pass
            else:
                msgDisp = True
                pass
            pass
        i += 1

        background1_y += 3
        background2_y += 3

        if background1_y > pad_height:
            background1_y = -pad_height
            pass
        if background2_y > pad_height:
            background2_y = -pad_height
            pass
        
        gamepad.fill((6,17,39))
        drawObject(background1,0,background1_y)
        drawObject(background2,0,background2_y)
        drawText("Flight Combat", 100, color.white, pad_width / 2, pad_height / 2 - 100, center)
        drawText("Copyright: Studio.Chem, 2018-2019 | stdio.chem@gmail.com", 30, color.lightgray, pad_width / 2, pad_height - 30, center)
        if msgDisp:
            drawText("Press Space To Start", 50, color.lightgray, pad_width / 2, pad_height / 2, center)
            pass
        pygame.display.update()
        clock.tick(60)
        pass
    pass

def gameOver():
    global gamepad, select_sound, gameover_sound
    pygame.mixer.music.stop()
    drawText("Game Over", 100, color.red, pad_width / 2, pad_height / 2 - 50, center)
    drawText("Your Score : " + str(score), 50, color.white, pad_width / 2, pad_height / 2 + 30, center)
    drawText("Replay? (Y/N)", 50, color.white, pad_width / 2, pad_height / 2 + 80, center)
    pygame.display.update()
    pygame.mixer.Sound.play(gameover_sound)
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.mixer.Sound.play(select_sound)
                    runGame()
                    pass
                elif event.key == pygame.K_n:
                    pygame.mixer.Sound.play(select_sound)
                    pygame.quit()
                    quit()
                    pass
                pass
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                pass
            pass
        pass
    pass
	
def runGame():
    global gamepad, clock, background1, background2
    global player, enemy, meteor, bullet, bullet_enemy, item, score
    global shot_sound, shot_enemy_sound, explosion_sound, shield_activate_sound, crash_sound, recover_sound
    global energy_icon

    pygame.mixer.music.load("sound/title.wav")
    pygame.mixer.music.play(-1)

    enemy_txy = []
    meteor_txy = []
    item_txy = []
    bullet_xy = []
    bullet_enemy_xy = []
    
    speed = 3
    enemy_max = 1
    
    background1_y = 0
    background2_y = -pad_height
    
    player_x = 200
    player_y = 620
    player_x_change = 0
    player_y_change = 0

    player_cooltime = 0
    player_damaged = False
    player_shieldtime = 0
    player_shielded = False

    player_health = 100

    kill_count = 0
    score = 0

    crashed = False
    while not crashed:
        if player_health <= 0:
            gameOver()
            pass
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_w]:
                player_y_change = -3 - speed * 0.1
                pass
            elif pygame.key.get_pressed()[pygame.K_s]:
                player_y_change = 3 + speed * 0.1
                pass
            else:
                player_y_change = 0
                pass
            if pygame.key.get_pressed()[pygame.K_a]:
                player_x_change = -3 - speed * 0.1
                pass
            elif pygame.key.get_pressed()[pygame.K_d]:
                player_x_change = 3 + speed * 0.1
                pass
            else:
                player_x_change = 0
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_xy.append([player_x+11,player_y])
                    pygame.mixer.Sound.play(shot_sound)
                    pass
                pass
            if event.type == pygame.QUIT:
                crashed = True
                pass
            pass

        speed = 3 + kill_count * 0.05
        enemy_max = 1 + kill_count * 0.02
        
        meteor_type = random.randrange(1,int(1000 / speed))
        if meteor_type == 1:
            meteor_txy.append([meteor[0],random.randrange(30, pad_width - 30),-100])
            pass
        elif meteor_type == 2:
            meteor_txy.append([meteor[1],random.randrange(30, pad_width - 30),-100])
            pass

        item_type = random.randrange(1,int(speed * 700))
        if item_type == 1:
            item_txy.append([item[0],random.randrange(30, pad_width - 30),-100])
            pass
        if item_type == 2:
            item_txy.append([item[1], random.randrange(30, pad_width - 30),-100])
            pass
        
        enemy_type = random.randrange(1,int(700 / speed))
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
                bxy[1] -= 10
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
                bxy[1] += 10
                bullet_enemy_xy[i][1] = bxy[1]
                if bxy[1] > player_y and bxy[1] < player_y + 40 and bxy[0] > player_x - 60 and bxy[0] < player_x + 60:
                    try:
                        bullet_enemy_xy.remove(bxy)
                        pass
                    except:
                        pass
                    if not player_shielded:
                        pygame.mixer.Sound.play(crash_sound)
                        player_damaged = True
                        player_health -= 10
                        pass
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
                if bxy[1] > pad_height:
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
                mtr[2] += speed * 1.25
                meteor_txy[i][2] = mtr[2]
                if mtr[2] >= pad_height:
                    meteor_txy.remove(mtr)
                    pass
                if mtr[2] > player_y and mtr[2] < player_y + 60 and mtr[1] > player_x - 60 and mtr[1] < player_x + 60:
                    pygame.mixer.Sound.play(crash_sound)
                    try:
                        meteor_txy.remove(mtr)
                        pass
                    except:
                        pass
                    if player_shielded:
                        player_shielded = False
                        player_shieldtime = 0
                        pass
                    else:
                        player_damaged = True
                        player_health -= 50
                        pass
                    pass
                pass
            pass

        if not len(item_txy) == 0:
            for i, itm in enumerate(item_txy):
                itm[2] += speed * 1.1
                item_txy[i][2] = itm[2]
                if itm[2] >= pad_height:
                    item_txy.remove(itm)
                    pass
                if itm[2] > player_y and itm[2] < player_y + 40 and itm[1] > player_x - 40 and itm[1] < player_x + 40:
                    if itm[0] == item[0]:
                        pygame.mixer.Sound.play(recover_sound)
                        player_health += 20 + int((speed-3) * 20)
                        pass
                    elif itm[0] == item[1]:
                        pygame.mixer.Sound.play(shield_activate_sound)
                        player_shielded = True
                    try:
                        item_txy.remove(itm)
                        pass
                    except:
                        pass
                    pass
                pass
            pass

        if not len(enemy_txy) == 0:
            for i, emy in enumerate(enemy_txy):
                if emy[0] == enemy[2]:
                        emy[7] += 1
                        pass
                if emy[7] > 15:
                    pygame.mixer.Sound.play(explosion_sound)
                    enemy_txy.remove(emy)
                    kill_count += 1
                    score += int(speed * 3.14)
                    pass
                if not emy[3]:
                    emy[2] += emy[5]
                    try:
                        enemy_txy[i][2] = emy[2]
                        pass
                    except:
                        pass
                    if emy[2] >= pad_height / 10:
                        try:
                            enemy_txy[i][3] = True
                            pass
                        except:
                            pass
                        pass
                    pass
                else:
                    emy_attack = random.randrange(1,int(700/speed))
                    emy_x_change = random.randrange(1,100)
                    emy_y_change = random.randrange(1,100)

                    if emy_attack == 1 and not emy[0] == enemy[2]:
                        bullet_enemy_xy.append([emy[1] + 10, emy[2] + 15])
                        pygame.mixer.Sound.play(shot_enemy_sound)
                        pass

                    if emy_x_change == 1:
                        emy[4] = random.randrange(int(-speed), int(speed)) / 5
                        pass
                    if emy_y_change == 1:
                        emy[5] = random.randrange(int(-speed), int(speed)) / 5
                        pass
                    emy[1] += emy[4]
                    emy[2] += emy[5]
                    if emy[1] < 80:
                        emy[1] = 80
                        emy[4] = random.randrange(int(-speed), int(speed)) / 5
                        pass
                    elif emy[1] > pad_height / 2 - 80:
                        emy[1] = pad_height / 2 - 80
                        emy[4] = random.randrange(int(-speed), int(speed)) / 5
                        pass
                    if emy[2] < 0:
                        emy[2] = 0
                        emy[5] = random.randrange(int(-speed), int(speed)) / 5
                        pass
                    elif emy[2] > pad_width - 80:
                        emy[2] = pad_width - 80
                        emy[5] = random.randrange(int(-speed), int(speed)) / 5
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

        if not len(item_txy) == 0:
            for it, ix, iy in item_txy:
                drawObject(it,ix,iy)
                pass
            pass

        if not len(enemy_txy) == 0:
            for et, ex, ey, eb, exc, exy, ehtl, ecnt in enemy_txy:
                drawObject(et,ex,ey)
                pass
            pass

        if player_cooltime == 10 and player_damaged:
            player_damaged = False
            player_cooltime = 0
            pass
        elif player_damaged:
            player_cooltime += 1
            pass

        if player_shieldtime == 300 and player_shielded:
            player_shielded = False
            player_shieldtime = 0
            pass
        elif player_shielded:
            player_shieldtime += 1
            pass

        if player_damaged:
            drawObject(player[1], player_x, player_y)
            pass
        elif player_shielded:
            drawObject(player[2], player_x, player_y)
        else:
            drawObject(player[0], player_x, player_y)
            pass
        
        if player_health < 0:
            player_health = 0
            pass
        drawObject(energy_icon, 10, 15)
        drawText(str(player_health), 50, color.orange, 35, 20, left)
        drawText(str(score), 50, color.white, pad_width - 10, 20, right)
        pygame.display.update()
        clock.tick(60)
        pass
    
    pygame.quit()
    quit()
    pass

if __name__ == '__main__':
        initGame()
        pass
    
