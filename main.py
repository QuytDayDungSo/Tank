import pgzrun
import random
speed = 2
WIDTH = 1000
HEIGHT = 600
size_tank = 40
walls = []
bullets = []
gameover_image = Actor("gameover")
gamewin_image = Actor("win")
gameover_image.pos = (WIDTH // 2, HEIGHT // 2)
enemy_bullets = []
bullet_delay = 0
bullet_delay_enemy = 0
speed_bullet = 10
enemyTanks = []
game_over = False
enemy_move_count = 0
bullet_delay_AI = 0
start_delay = 180
score = 0  
board = Actor("board")
board.pos = (900, 300)


# Create my Tank
myTank = Actor("mytank")
myTank.pos = (size_tank*4, HEIGHT - size_tank)
fire = Actor("fire")
count_tank_enemy = 5


# Create enemy Tank
def create_enemy_tank(x, y):
    enemyTank = Actor("enemytank")
    enemyTank.x = x
    enemyTank.y = y
    enemyTank.angle = 180
    enemyTanks.append(enemyTank)
    
for i in range(2,15,3):
    create_enemy_tank(i*40,40)

# Setup background 
background = Actor("background")  # Set initial position at the center

# Wall

map_data = [["1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1"],
            ["1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1"],
            ["1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],
            ["1","0","1","1","2","2","2","1","1","1","1","1","2","2","2","1","1","","1"],
            ["1","0","1","0","0","0","0","0","0","1","0","0","0","0","0","0","1","0","1"],
            ["1","0","1","0","1","1","1","0","0","1","0","0","1","1","1","0","1","0","1"],
            ["1","0","1","0","0","1","0","0","0","0","0","0","0","1","0","0","1","0","1"],
            ["1","0","1","3","3","3","3","3","3","3","3","3","3","3","3","3","1","","1"],
            ["1","0","1","0","0","1","1","0","1","0","1","0","1","1","0","0","1","0","1"],
            ["1","0","1","0","0","0","0","0","1","1","1","0","0","0","0","0","1","0","1"],
            ["1","0","1","1","2","2","2","1","1","1","1","1","2","2","2","1","1","","1"],
            ["1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],
            ["1","0","0","0","1","1","1","0","1","1","1","0","1","1","1","0","0","0","1"],
            ["1","0","0","0","0","0","0","0","1","4","1","0","0","0","0","0","0","0","1"],
           
       ]

walls = []
trees = []
waves = []

for x in range(len(map_data[0])):
    for y in range(len(map_data)):
        if map_data[y][x] == "1":
            wall = Actor("wall")
            wall.x = (x+1)*40
            wall.y = (y+1)*40
            walls.append(wall)
        if map_data[y][x] =="2":
            tree = Actor("tree")
            tree.x = (x+1)*40 
            tree.y = (y+1)*40 
            trees.append(tree)
        if map_data[y][x] =="3":
            wave= Actor("wave")
            wave.x = (x+1)*40 
            wave.y = (y+1)*40 
            waves.append(wave)
        if map_data[y][x] =="4":
            home = Actor("home")
            home.x = (x+1)*40
            home.y = (y+1)*40
            


def tank_set():
    original_x = myTank.x
    original_y = myTank.y

    if keyboard.left or keyboard.A:
        myTank.x = myTank.x - speed
        myTank.angle = 90

    elif keyboard.right or keyboard.D:
        myTank.x = myTank.x + speed
        myTank.angle = 270
    elif keyboard.up or keyboard.W:
        myTank.y = myTank.y - speed
        myTank.angle = 0
    elif keyboard.down or keyboard.S:
        myTank.y = myTank.y + speed
        myTank.angle = 180

    if myTank.collidelist(walls) != -1 or myTank.collidelist(enemyTanks) != -1:
        myTank.x = original_x
        myTank.y = original_y

    if (
        myTank.x < size_tank
        or myTank.x > (WIDTH - 200) - size_tank
        or myTank.y < size_tank
        or myTank.y > HEIGHT - size_tank
    ):
        myTank.x = original_x
        myTank.y = original_y

def tank_bullit_set():
    global bullet_delay,start_delay,score
    if start_delay > 0:
        start_delay -= 1
    if bullet_delay == 0:
        if keyboard.J:
            sounds.gunfire.play()
            bullet = Actor("bullet")
            bullet.angle = myTank.angle
            if bullet.angle == 90:  # LEFT
                bullet.pos = (myTank.x - size_tank, myTank.y)
            if bullet.angle == 270:  # RIGHT
                bullet.pos = (myTank.x + size_tank, myTank.y)
            if bullet.angle == 0:  # UP
                bullet.pos = (myTank.x, myTank.y - size_tank)
            if bullet.angle == 180:  # Down
                bullet.pos = (myTank.x, myTank.y + size_tank)
            bullets.append(bullet)
            bullet_delay = speed_bullet
    else:
        bullet_delay = bullet_delay - 1

    for bullet in bullets:
        if bullet.angle == 90:  # LEFT
            bullet.x = bullet.x - 5
        if bullet.angle == 270:  # RIGHT
            bullet.x = bullet.x + 5
        if bullet.angle == 0:  #
            bullet.y = bullet.y - 5
        if bullet.angle == 180:  #
            bullet.y = bullet.y + 5

    for bullet in bullets:  # Setup bullet destros wall
        wall_index = bullet.collidelist(walls)
        if wall_index != -1:
            # print(wall_index)
            
            fire.pos = bullet.pos
            sounds.fire.play()
            del walls[wall_index]
            bullets.remove(bullet)
        if bullet.x < 0 or bullet.x > (WIDTH - 200) or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

        enemy_index = bullet.collidelist(enemyTanks)
        if enemy_index != -1:
            sounds.bang.play()
            score = score +1
            del enemyTanks[enemy_index]
            bullets.remove(bullet)
            for i in range(2,15,3):
                point = Actor("enemytank")  # Actor ảo để kiểm tra va chạm
                point.x = i*40
                point.y = 40
                tank_index = point.collidelist(enemyTanks)
                if tank_index == -1: 
                    create_enemy_tank(i*40,40)
                    break
        # if bullet.collidelist(enemy_bullets)!=-1:
        #     sounds.bang.play()
        #     bullets.remove(bullet)




def tank_enemy_set():
    global enemy_move_count,bullet_delay,bullet_delay_AI
    # Tank AI
    try:
        tank= enemyTanks[0]
    
        original_x = tank.x
        original_y = tank.y  
        target  = (myTank.x, myTank.y)

        if target[0] > tank.x:
            tank.angle = 270
            tank.x += 2
            
        elif target[0] < tank.x:
            tank.angle = 90
            tank.x -= 2              
            
        elif target[1] > tank.y:
            tank.angle = 180
            tank.y += 2           

        elif target[1] < tank.y:
            tank.angle = 0
            tank.y -= 2
            
        if tank.collidelist(walls) != -1 :
            tank.x = original_x
            tank.y = original_y
            
        enemy_collision_index = tank.collidelist(enemyTanks)
        if enemy_collision_index != -1 and enemy_collision_index != enemyTanks.index(tank):
            tank.x = original_x
            tank.y = original_y
            # enemy_move_count = 0
        
        if  tank.colliderect(myTank):
            tank.x = original_x
            tank.y = original_y

                    
        if (
            tank.x < size_tank
            or tank.x > (WIDTH - 200) - size_tank
            or tank.y < size_tank
            or tank.y > HEIGHT - size_tank
        ):
            tank.x = original_x
            tank.y = original_y
        if bullet_delay_AI == 0:
            sounds.gunfire.play()
            bullet = Actor("bullet")
            bullet.angle = tank.angle
            if bullet.angle == 90:  # LEFT
                bullet.pos = (tank.x - size_tank, tank.y)
            if bullet.angle == 270:  # RIGHT
                bullet.pos = (tank.x + size_tank, tank.y)
            if bullet.angle == 0:  # UP
                bullet.pos = (tank.x, tank.y - size_tank)
            if bullet.angle == 180:  # Down
                bullet.pos = (tank.x, tank.y + size_tank)
            enemy_bullets.append(bullet)
            bullet_delay_AI = random.randint(100,200)
        else:
            bullet_delay_AI = bullet_delay_AI - 1
        
        
            
            
        
        
        ####################################################################################################3
            
            # Tank bot
        
        for enemy_tank in enemyTanks[1:]:
            original_enemy_x = enemy_tank.x
            original_enemy_y = enemy_tank.y
            
            enemy_collision_index = enemy_tank.collidelist(enemyTanks)
            wall_collision_index = enemy_tank.collidelist(walls)

            if wall_collision_index != -1:
                enemy_tank.x = original_enemy_x
                enemy_tank.y = original_enemy_y
                enemy_move_count = 0
                
            elif enemy_collision_index != -1 and enemy_collision_index != enemyTanks.index(enemy_tank):
                enemy_tank.x = original_enemy_x
                enemy_tank.y = original_enemy_y
                enemy_move_count = 0
                # print("Xe tăng địch chạm nhau")
                
            if enemy_tank.colliderect(myTank):
                enemy_tank.x = original_enemy_x
                enemy_tank.y = original_enemy_y
                enemy_move_count = 0
            
            
            choise = random.randint(0,3)
            if enemy_move_count>0:
                enemy_move_count = enemy_move_count -1
                if enemy_tank.angle == 270:
                    enemy_tank.x += 2
                elif enemy_tank.angle == 90:
                    enemy_tank.x -= 2
                elif enemy_tank.angle == 180:
                    enemy_tank.y += 2
                elif enemy_tank.angle == 0:
                    enemy_tank.y -= 2

                
                enemy_collision_index = enemy_tank.collidelist(enemyTanks)
                wall_collision_index = enemy_tank.collidelist(walls)

                if wall_collision_index != -1:
                    enemy_tank.x = original_enemy_x 
                    enemy_tank.y = original_enemy_y
                    enemy_tank.angle = (enemy_tank.angle + 180) % 360
                    enemy_move_count = 0
                    
                if enemy_collision_index != -1 and enemy_collision_index != enemyTanks.index(enemy_tank):
                    enemy_tank.x = original_enemy_x
                    enemy_tank.y = original_enemy_y
                    enemy_tank.angle = (enemy_tank.angle + 180) % 360
                    
                    
                    enemy_move_count = 0
                            
                if (
                    enemy_tank.x < size_tank
                    or enemy_tank.x > (WIDTH - 200) - size_tank
                    or enemy_tank.y < size_tank
                    or enemy_tank.y > HEIGHT - size_tank
                ):
                    enemy_tank.x = original_enemy_x
                    enemy_tank.y = original_enemy_y
                    enemy_tank.angle = (enemy_tank.angle + 180) % 360
                    enemy_move_count = 0
                    
            elif choise == 0:
                enemy_move_count = 200
            elif choise == 1:# Đổi hướng
                enemy_tank.angle=random.randint(0,3)*90
            else:
                if bullet_delay == 0:
                    sounds.gunfire.play()
                    bullet = Actor("bullet")
                    bullet.angle = enemy_tank.angle
                    if bullet.angle == 90:  # LEFT
                        bullet.pos = (enemy_tank.x - size_tank, enemy_tank.y)
                    if bullet.angle == 270:  # RIGHT
                        bullet.pos = (enemy_tank.x + size_tank, enemy_tank.y)
                    if bullet.angle == 0:  # UP
                        bullet.pos = (enemy_tank.x, enemy_tank.y - size_tank)
                    if bullet.angle == 180:  # Down
                        bullet.pos = (enemy_tank.x, enemy_tank.y + size_tank)
                    enemy_bullets.append(bullet)
                    bullet_delay = speed_bullet
                else:
                    bullet_delay = bullet_delay - 1
    except:
        print("Bạn Win")
                

                
                    

                                

                    
                        
                
        

def tank_enemy_bullet():
    global enemyTanks,game_over
    for bullet in enemy_bullets:
        if bullet.angle == 90:  # LEFT
            bullet.x = bullet.x - 5
        if bullet.angle == 270:  # RIGHT
            bullet.x = bullet.x + 5
        if bullet.angle == 0:  #
            bullet.y = bullet.y - 5
        if bullet.angle == 180:  #
            bullet.y = bullet.y + 5
            
        wall_index = bullet.collidelist(walls)
        if wall_index != -1:
            sounds.fire.play()
            del walls[wall_index]
            enemy_bullets.remove(bullet)
            
        if bullet.x < 0 or bullet.x > (WIDTH - 200) or bullet.y < 0 or bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)
        try:
            if bullet.collidelist(enemyTanks)!=-1:
                enemy_bullets.remove(bullet)
        except:
            pass

        if bullet.colliderect(myTank):
            game_over = True
        
        if bullet.colliderect(home):
            game_over = True
            # enemyTanks = []
        fire.draw()
        # for bullet2 in bullets:         
        if bullet.collidelist(bullets)!=-1:
            sounds.fire.play()
            bullets.remove(bullets[bullet.collidelist(bullets)])
            enemy_bullets.remove(bullet)
            

  

def update():
    if game_over==False:
        tank_set()
        tank_bullit_set()
        tank_enemy_set()
        tank_enemy_bullet()

    



def draw():
    if game_over :
        screen.fill((0,0,0))
        # screen.draw.text("YOU LOSS",(260,250),color = (255,255,255),fontsize =100)
        gameover_image.draw()
    elif score >= 3:
        gamewin_image.draw()
    else:
        gameover_image.draw()
        background.draw()
        for wave in waves:
            wave.draw()
        myTank.draw()

        for wall in walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw()
        for enemyTank in enemyTanks:
            enemyTank.draw()
        for enemy_bullet in enemy_bullets:
            enemy_bullet.draw()
        for wall in walls:
            wall.draw()
        for tree in trees:
            tree.draw()
        home.draw()
        board.draw()
        screen.draw.text(f"Score: {score}", (850, 70), color="white", fontsize=30)

pgzrun.go()
