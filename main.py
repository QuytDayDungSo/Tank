import pgzrun
import random
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

tank_speed = 2
WIDTH = 1000
HEIGHT = 600
size_tank = 40
walls = []
bullets = []
gameover_image = Actor("gameover")
gamewin_image = Actor("win")
gameover_image.pos = (WIDTH // 2 , HEIGHT // 2)
enemy_bullets = []
bullet_delay = 0
bullet_delay_enemy = 0
speed_bullet = 10
enemyTanks = []
game_over = False
game_win = False
enemy_move_count = 0
bullet_delay_AI = 0
start_delay = 180
score = 0  
board = Actor("board")
board.pos = (900, 300)
excited = Actor("excited")
excited.pos =(900,200)
education = Actor("education")
education.pos = (900, 100)
button_newgame = Actor("newgame")
button_newgame.pos=(900,300)
button_newgame_press = Actor("newgame-press")  # Hình ảnh trạng thái được nhấn
button_newgame.pos = (900, 300)  # Vị trí ban đầu
button_newgame_press.pos = (900, 300)  # Vị trí ban đầu
button_newgame_active = True  # Trạng thái nút

  


button_startgame= Actor("startgame")
button_startgame.pos = (900,350)
button_startgame_active = True
start_check = False
button_startgame_press = Actor("startgame-press")
button_startgame_press.pos = (900,350)

button_pausegame = Actor("pausegame")
button_pausegame.pos = (900,400)
button_pausegame_press = Actor("pausegame-press")
button_pausegame_press.pos = (900,400)
button_pausegame_active=True

button_stopgame = Actor("stopgame")
button_stopgame.pos = (900,450)
button_stopgame_press = Actor("stopgame_press")
button_stopgame_press.pos = (900,450)
button_stopgame_active = True 

speeds = []
bullet_items = []
bomb_item = []

with open("score.txt", "r") as file:
    max  = int(file.read())


# Create my Tank
myTank = Actor("mytank")
myTank.pos = (size_tank*4, HEIGHT - size_tank)
count_tank_enemy = 5



 


# Setup background 
background = Actor("background")  # Set initial position at the center

# Wall

map_data = [["1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1"],
            ["1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1","0","0","1"],
            ["1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],
            ["1","0","1","1","2","2","2","1","1","1","1","1","2","2","2","1","1","0","1"],
            ["1","0","1","0","0","0","0","0","0","1","0","0","0","0","0","0","1","0","1"],
            ["1","0","1","0","1","1","1","0","0","1","0","0","1","1","1","0","1","0","1"],
            ["1","0","1","0","0","1","0","0","0","0","0","0","0","1","0","0","1","0","1"],
            ["1","0","1","3","3","3","3","3","3","3","3","3","3","3","3","3","1","0","1"],
            ["1","0","1","0","0","1","1","0","1","0","1","0","1","1","0","0","1","0","1"],
            ["1","0","1","0","0","0","0","0","1","1","1","0","0","0","0","0","1","0","1"],
            ["1","0","1","1","2","2","2","1","1","1","1","1","2","2","2","1","1","0","1"],
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
 
 # Create enemy Tank
def create_enemy_tank(x, y):
    enemyTank = Actor("enemytank")
    enemyTank.x = x     
    enemyTank.y = y
    enemyTank.angle = 180
    enemyTanks.append(enemyTank)   
for i in range(2,15,3):
    create_enemy_tank(i*40,40)           
def tank_set():
    global tank_speed,speed_bullet,enemyTanks
    original_x = myTank.x
    original_y = myTank.y

    if keyboard.left or keyboard.A:
        myTank.x = myTank.x - tank_speed
        myTank.angle = 90

    elif keyboard.right or keyboard.D:
        myTank.x = myTank.x + tank_speed
        myTank.angle = 270
    elif keyboard.up or keyboard.W:
        myTank.y = myTank.y - tank_speed
        myTank.angle = 0
    elif keyboard.down or keyboard.S:
        myTank.y = myTank.y + tank_speed
        myTank.angle = 180

    if myTank.collidelist(walls) != -1 or myTank.collidelist(enemyTanks) != -1:
        myTank.x = original_x
        myTank.y = original_y   
    if myTank.collidelist(speeds) !=-1:
        del speeds[myTank.collidelist(speeds)]
        tank_speed = tank_speed - 1

    if myTank.collidelist(bullet_items) !=-1:
        del bullet_items[myTank.collidelist(bullet_items)]
        speed_bullet  = speed_bullet + 5
    if myTank.collidelist(bomb_item) !=-1:
        del bomb_item[myTank.collidelist(bomb_item)]
        enemyTanks.clear()
        enemy_bullets.clear()
        for i in range(2,15,3):
            create_enemy_tank(i*40,40)  
    
        

    if (
        myTank.x < size_tank
        or myTank.x > (WIDTH - 200) - size_tank
        or myTank.y < size_tank
        or myTank.y > HEIGHT - size_tank
    ):
        myTank.x = original_x
        myTank.y = original_y

def tank_bullit_set():
    global bullet_delay,start_delay,score,game_win
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

    for bullet in bullets:  
        wall_index = bullet.collidelist(walls)
        if wall_index != -1:
            sounds.fire.play()
            choise  = random.randint(0,15)
            if choise == 4:
                speed  = Actor("speed")
                speed.pos = walls[wall_index].pos
                speeds.append(speed)
            elif choise == 5:
                wall = walls[wall_index]
                bullet_item = Actor("bullet_item")
                bullet_item.pos = wall.pos  
                bullet_items.append(bullet_item)
            elif choise == 6:
                wall = walls[wall_index]
                bomb = Actor("bomb")    
                bomb.pos = wall.pos
                bomb_item.append(bomb)
                          
            del walls[wall_index]
            bullets.remove(bullet)
        if bullet.x < 0 or bullet.x > (WIDTH - 200) or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

        enemy_index = bullet.collidelist(enemyTanks)
        if enemy_index != -1:
            sounds.bang.play()
            score = score +1
            # if score ==5:
            #     game_win = True
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


# Hàm tính khoảng cách Manhattan từ một ô (x,y) đến ô (x2, y2)
def manhattan_distance(x, y, x2, y2):
    return abs(x-x2) + abs(y-y2)

# Hàm kiểm tra một ô (x,y) có nằm trong map_data hay không
def is_valid(x, y, map_data):
    return 0 <= x < len(map_data) and 0 <= y < len(map_data[x])

# Hàm tìm đường đi từ ô xuất phát đến ô đích bằng thuật toán A*
def a_star(map_data, start, end):
    # Khởi tạo hàng đợi ưu tiên Q và tập hợp S
    Q = [(start[0], start[1], manhattan_distance(*start, *end), None)]
    S = set()
    # Lặp cho đến khi Q rỗng hoặc tìm được đích
    while Q:
        # Lấy ra một ô u có chi phí f nhỏ nhất khỏi Q và thêm vào S
        u = Q.pop(0)
        S.add((u[0], u[1]))
        # Nếu u là đích, trả về đường đi từ xuất phát đến u
        if (u[0], u[1]) == end:
            path = []
            while u:
                path.append((u[0], u[1]))
                u = u[3]
            return path[::-1]
        # Nếu không, duyệt qua các ô kề với u
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            v_x = u[0] + dx
            v_y = u[1] + dy
            # Nếu v hợp lệ và không phải là ô có giá trị 1
            if is_valid(v_x, v_y, map_data) and map_data[v_x][v_y] != "1":
                # Tính chi phí g, h, f của v
                v_g = u[2] - manhattan_distance(u[0], u[1], *end) + 1
                v_h = manhattan_distance(v_x, v_y, *end)
                v_f = v_g + v_h
                # Nếu v đã nằm trong Q, so sánh và cập nhật f của v nếu cần
                for i in range(len(Q)):
                    if Q[i][:2] == (v_x, v_y):
                        if Q[i][2] > v_f:
                            Q[i] = (v_x, v_y, v_f, u)
                            Q.sort(key=lambda x: x[2])
                        break
                else:
                    # Nếu v chưa nằm trong Q và S, thêm vào Q
                    if (v_x, v_y) not in S:
                        Q.append((v_x, v_y, v_f, u))
                        Q.sort(key=lambda x: x[2])
    # Nếu không tìm được đường đi, trả về None
    return None






def tank_enemy_set():
    global bullet_delay, bullet_delay_AI, enemyTanks, map_data,enemy_move_count

    for tank in enemyTanks:
    # tank = enemyTanks[0]
        original_x = tank.x
        original_y = tank.y  
        target = (round(int(myTank.x // size_tank)),round(int( myTank.y // size_tank)))  # Vị trí của người chơi
        # Tính toán đường dẫn sử dụng thuật toán A*
        path = a_star(map_data, (round(int(tank.x // size_tank)), round(int(tank.y // size_tank))), target)
        
        if path!=None:
            path = path[1]
            target_x, target_y = path[0] * size_tank, path[1] * size_tank
            
            if target_x > tank.x:
                tank.angle = 270
                tank.x += 2
            elif target_x < tank.x:
                
                tank.angle = 90
                tank.x -= 2
            elif target_y > tank.y:
                tank.angle = 180
                tank.y += 2
            elif target_y < tank.y:
                tank.angle = 0
                tank.y -= 2
        else:
            original_enemy_x = tank.x
            original_enemy_y = tank.y
            
            enemy_collision_index = tank.collidelist(enemyTanks)
            wall_collision_index = tank.collidelist(walls)

            if wall_collision_index != -1:
                tank.x = original_enemy_x
                tank.y = original_enemy_y
                enemy_move_count = 0
                
            elif enemy_collision_index != -1 and enemy_collision_index != enemyTanks.index(tank):
                tank.x = original_enemy_x
                tank.y = original_enemy_y
                enemy_move_count = 0
                # print("Xe tăng địch chạm nhau")
                
            if tank.colliderect(myTank):
                tank.x = original_enemy_x
                tank.y = original_enemy_y
                enemy_move_count = 0
            
            
            choise = random.randint(0,3)
            
            if enemy_move_count>0:
                enemy_move_count = enemy_move_count -1
                if tank.angle == 270:
                    tank.x += 2
                elif tank.angle == 90:
                    tank.x -= 2
                elif tank.angle == 180:
                    tank.y += 2
                elif tank.angle == 0:
                    tank.y -= 2

                
                enemy_collision_index = tank.collidelist(enemyTanks)
                wall_collision_index = tank.collidelist(walls)

                if wall_collision_index != -1:
                    tank.x = original_enemy_x 
                    tank.y = original_enemy_y
                    tank.angle = (tank.angle + 180) % 360
                    enemy_move_count = 0
                    
                if enemy_collision_index != -1 and enemy_collision_index != enemyTanks.index(tank):
                    tank.x = original_enemy_x
                    tank.y = original_enemy_y
                    tank.angle = (tank.angle + 180) % 360
                    
                    
                    enemy_move_count = 0
                            
                if (
                    tank.x < size_tank
                    or tank.x > (WIDTH - 200) - size_tank
                    or tank.y < size_tank
                    or tank.y > HEIGHT - size_tank
                ):
                    tank.x = original_enemy_x
                    tank.y = original_enemy_y
                    tank.angle = (tank.angle + 180) % 360
                    enemy_move_count = 0
            elif choise == 0:
                enemy_move_count = 200
            elif choise == 1:# Đổi hướng
                tank.angle=random.randint(0,3)*90
            else:
                if bullet_delay == 0:
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
                    bullet_delay = speed_bullet
                else:
                    bullet_delay = bullet_delay - 1        
                    
        
        if tank.collidelist(walls) != -1:
            tank.x = original_x
            tank.y = original_y

        enemy_collision_index = tank.collidelist(enemyTanks)
        if enemy_collision_index != -1 and enemy_collision_index != enemyTanks.index(tank):
            tank.x = original_x
            tank.y = original_y
        
        if tank.colliderect(myTank):
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
            bullet_delay_AI = random.randint(100, 200)
        else:
            bullet_delay_AI = bullet_delay_AI - 1


    
    
                
def tank_enemy_bullet():
    global enemyTanks,game_over,map_data
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
            x, y = walls[wall_index].pos # Lấy tọa độ của tường
            try:
               
                map_data[int(x //size_tank)][int(y //size_tank)] = "0"  # Thay đổi giá trị của tường trong map_data thành "0"
            except:
                pass
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
     
        if bullet.collidelist(bullets)!=-1:
            sounds.fire.play()
            bullets.remove(bullets[bullet.collidelist(bullets)])
            enemy_bullets.remove(bullet)
 
def on_mouse_down(pos):
    global start_check, game_over,button_newgame_active,button_startgame_active,button_stopgame_active,button_pausegame_active
    if button_newgame_active and button_newgame.collidepoint(pos):
        sounds.hit.play()
        reset_game()
        button_newgame_active = False
    if button_startgame_active and button_startgame.collidepoint(pos):
        sounds.hit.play()
        start_check = True
        button_startgame_active = False
    if button_pausegame_active and button_pausegame.collidepoint(pos):
        sounds.hit.play()
        start_check = False
        button_pausegame_active = False
    if button_stopgame_active and button_stopgame.collidepoint(pos):
        sounds.hit.play()
        button_stopgame_active = False
        game_over = True 
        

def on_mouse_up(pos):
    global start_check, game_over,button_newgame_active,button_startgame_active,button_stopgame_active,button_pausegame_active
    button_newgame_active = True  # Trả về trạng thái bình thường
    button_startgame_active = True  
    button_pausegame_active = True  
    button_stopgame_active = True 


def reset_game():
    global start_check,myTank,game_over,speed_bullet,tank_speed
    speed_bullet = 10
    tank_speed = 2
    enemyTanks.clear()
    enemy_bullets.clear()
    bullets.clear()
    start_check = False
    game_over = False
    del myTank 
    bomb_item.clear()
    speeds.clear()
    bullet_items.clear()
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
    for i in range(2,15,3):
        create_enemy_tank(i*40,40)  
    myTank = Actor("mytank")
    myTank.pos = (size_tank*4, HEIGHT - size_tank)

def update():
    if game_over==False and game_win == False and start_check !=False:
        tank_set()
        tank_bullit_set()
        tank_enemy_set()
        tank_enemy_bullet()
    else:
        if max < score:
            with open("score.txt", "w") as file:
                file.write(str(score))


def draw():
    if game_over:
        gameover_image.draw()
    elif game_win:
        gamewin_image.draw()
    # elif start_check == False:
    #     pass
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
        for speed in speeds:
            speed.draw()
        for bomb in bomb_item:
            bomb.draw()
        for bullet_item in bullet_items:
            bullet_item.draw()
        home.draw()
        board.draw()
        education.draw()
        # Thay "customfont" bằng tên của font tùy chỉnh bạn đã thêm vào dự án
        screen.draw.text(f"Score: {score}\nTop: {max}", (850, 50), color="white", fontname="alumnisanscollegiaterne.ttf", fontsize=30)


        excited.draw()
        if button_newgame_active:
            button_newgame.draw()
        else:
            button_newgame_press.draw()
        if button_startgame_active:
            button_startgame.draw()
        else:
            button_startgame_press.draw()
        if button_pausegame_active:
            button_pausegame.draw()
        else:
            button_pausegame_press.draw()
        if button_stopgame_active:
            button_stopgame.draw()
        else:
            button_stopgame_press.draw()
        
pgzrun.go()