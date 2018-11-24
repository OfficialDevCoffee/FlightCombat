#flightcombat.py
__author__ = 'stdio.chem@gmail.com'

import pygame, random
import color

pad_width = 480
pad_height = 720
caption = "Flight Combat"

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj,(x,y))
    pass

def initGame():
    global gamepad, clock, background1, background2
    global player, enemy, meteor, bullet

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
    meteor.append(pygame.image.load("image/meteor_a.png"))
    meteor.append(pygame.image.load("image/meteor_b.png"))
    bullet = pygame.image.load("image/bullet.png")
    
    clock = pygame.time.Clock()
    runGame()
    pass

def runGame():
    global gamepad, clock, background1, background2
    global player, enemy, meteor, bullet

    enemy_txy = []
    meteor_txy = []
    bullet_xy = []
    
    speed = 5
    
    background1_y = 0
    background2_y = -pad_height
    
    player_x = 200
    player_y = 620
    player_x_change = 0
    player_y_change = 0

    crashed = False
    while not crashed:
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
                if bxy[1] <= -80:
                    bullet_xy.remove(bxy)
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

        if not len(meteor_txy) == 0:
            for mt, mx, my in meteor_txy:
                drawObject(mt,mx,my)
                pass
            pass
        
        drawObject(player, player_x, player_y)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
    pass

initGame()
