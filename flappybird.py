from this import d
from numpy import append
import pygame, sys, random

# Ngắt đoạn sự kiện create
PIPE_INTERVAL = 1500        # 1.5s sinh ống
METEO_INTERVAL = 1000       # 1s sinh thiên thạch
LASER_INTERVAL = 4000       # 4s sinh laser
HEART_INTERVAL = 15000      # 15s sinh tim 

# =============================== DEF ===============================

#vẽ sàn
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
#tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    random_pipe_dis = random.choice(dis_pipes)
    bot_pipe = pipe_surface.get_rect( midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect( midtop = (500,random_pipe_pos-random_pipe_dis))
    return bot_pipe, top_pipe
#dịch ống
def move_pipe(pipes):
    if len(pipes)>0:
        while pipes[0].centerx<-500:
            pipes.pop(0)
            if len(pipes)==0:
                break 
    for pipe in pipes:
        pipe.centerx-=5
    return pipes
#vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=700:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)   

#va chạm chướng ngại vật
def check_collision(pipes, lasers, hp):
    global last_hit_sound_time
    current_time = pygame.time.get_ticks()
    hit_this_frame = False

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hp -= 1
            hit_this_frame = True

    for laser in lasers:
        if bird_rect.colliderect(laser):
            hp -= 1
            hit_this_frame = True

    # Va chạm với trần hoặc sàn => chết luôn
    if bird_rect.top <= -78 or bird_rect.bottom >= 650:
        diesound.play()
        return 0

    # Chỉ phát âm thanh nếu va chạm và đã qua 300ms từ lần cuối
    if hit_this_frame and current_time - last_hit_sound_time >= hit_sound_delay:
        hitsound.play()
        last_hit_sound_time = current_time

    return hp

#chim bay
def rotate_bird(birds):
    new_bird=pygame.transform.rotozoom(birds,-bird_movement*4,1)
    return new_bird
#animation of bird
def bird_animation():
    new_bird=bird_list[index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect
#thanh máu
def draw_hp_bar(hp, max_hp=100):
    # Vị trí và kích thước thanh máu
    bar_x = 60
    bar_y = 20
    bar_width = 60
    bar_height = 20

    # Phần trăm máu còn lại
    hp_percent = max(hp / max_hp, 0)

    # Khung thanh máu (trắng)
    pygame.draw.rect(screen, (255, 255, 255), (bar_x-2, bar_y-2, bar_width+4, bar_height+4))
    # Thanh máu nền (xám)
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    # Thanh máu còn lại (đỏ)
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, int(bar_width*hp_percent), bar_height))

    # Chữ "HP" bên trái
    hp_label = small_font.render("HP", True, (255, 255, 255))
    hp_label_rect = hp_label.get_rect(midright=(bar_x-10, bar_y+bar_height//2))
    screen.blit(hp_label, hp_label_rect)

    # Số HP bên phải
    hp_text = small_font.render(str(hp), True, (255,255,255))
    hp_rect = hp_text.get_rect(midleft=(bar_x+bar_width+10, bar_y+bar_height//2))
    screen.blit(hp_text, hp_rect)

#hiển thị điểm và máu
def score_display(active): 

    # HP hiển thị góc trái trên
    draw_hp_bar(hp);

    score_surface=game_font.render('SCORE: '+str(int(score)),True,(0,204,0))
    score_rect=score_surface.get_rect(center=(215,100))
    screen.blit(score_surface,score_rect)


    if active==False:
        best_surface=game_font.render('BEST: '+str(int(best)),True,(255,0,0))
        best_rect=best_surface.get_rect(center=(215,150))
        screen.blit(best_surface,best_rect)
        screen.blit(game_over_surface,(70,200))
        if new_high_score:
            new_surface=new_font.render('NEW!',True,(255,255,102))
            new_surface=pygame.transform.rotozoom(new_surface,30,1)

            new_rect=new_surface.get_rect(center=(325,140))
            screen.blit(new_surface,new_rect)
    return best
#cộng điểm khi qua ống
def cal(scores):
    for pipe in pipe_list:
        if pipe.bottom<=700:
            if pipe.centerx==bird_rect.centerx:
                scores+=1
    return scores

#tạo meteo
def create_meteo():
    x=random.randint(100,500)
    y=random.randint(-50,0)
    meteoa = meteorite.get_rect( midtop = (x,y) )  
    return meteoa
#dịch meteo
def move_meteo(meteos):
    if len(meteos)>0:
        while meteos[0].centery>=500:
            meteos.pop(0)
            if len(meteos)==0:
                break 
    for meteoa in meteos:
       meteoa.centerx-=2
       meteoa.centery+=2
    return meteos
#vẽ meteo
def draw_meteo(meteos):
    for meteoa in meteos: 
            screen.blit(meteorite,meteoa) 

#tạo laser
def create_laser():
    x=random.randint(2000,2500)
    y=random.randint(50,450)
    alaser = laser.get_rect(midtop = (x,y)) 
    return alaser
#dịch laser
def move_laser(lasers):
    if len(lasers)>0:
        if lasers[0].centerx<=-200:
            lasers.pop(0)
    for lasera in lasers:
       lasera.centerx-=6
    return lasers   
#vẽ laser
def draw_laser(lasers):
    global laser_animation_index
    blink = (pygame.time.get_ticks() // 400) % 2
    for lasera in lasers:
        # Vẽ laser
        if laser_animation_frames is not None:
            current_frame = laser_animation_frames[laser_animation_index % len(laser_animation_frames)]
            screen.blit(current_frame, lasera)
        else:
            screen.blit(laser, lasera)
        if blink:  # Chỉ vẽ khi blink = 1
            distance_to_right = lasera.centerx - WIDTH
            if 200 <= distance_to_right <= 1000:
                warning_surface = warning_font.render("!", True, warning_color)
                warning_rect = warning_surface.get_rect(midleft=(WIDTH - 30, lasera.centery))
                screen.blit(warning_surface, warning_rect) 


    # Cập nhật animation index
    if laser_animation_frames is not None:
        laser_animation_index += 1

#tạo tim
def create_heart():
    x = random.randint(500, 600)
    y = random.randint(100, 400)
    return heart_img.get_rect(center=(x, y))
#dịch tim
def move_heart(hearts):
    for heart in hearts:
        heart.centerx -= 3
    # Xóa item đã bay khỏi màn hình
    hearts = [h for h in hearts if h.centerx > -50]
    return hearts
#vẽ tim
def draw_heart(hearts):
    for heart in hearts:
        screen.blit(heart_img, heart)
#check ăn tim
def check_heart_collision(hearts, hp, max_hp=100):
    for heart in hearts[:]:  # copy để xóa khi ăn
        if bird_rect.colliderect(heart):
            hp = min(max_hp, hp + random.randint(10,15))  # hồi random 10-15 HP, không quá max
            healingsound.play()
            hearts.remove(heart)
    return hp
   

# =============================== INIT ===============================
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.font.init()

WIDTH = 432
HEIGHT = 768
screen= pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
gravity = 0.2
bird_movement = 0

#đang chơi
game_active =True

#xử lí va chạm + âm thanh
last_hit_sound_time = 0
hit_sound_delay = 500

#font
game_font=pygame.font.Font('asset/font/04B_19.TTF',43)
small_font = pygame.font.Font('asset/font/04B_19.TTF', 20)
new_font=pygame.font.SysFont('',25)

#chèn background
bg = pygame.image.load('asset/img/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

#chèn sàn
floor = pygame.image.load('asset/img/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos=0

#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('asset/img/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('asset/img/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('asset/img/yellowbird-upflap.png').convert_alpha())
bird_list=[bird_down,bird_mid,bird_up]
index=2
bird = bird_list[index]
bird_rect=bird.get_rect(center = (100,350))
#timer of bird
birdflap = pygame.USEREVENT +1
pygame.time.set_timer(birdflap,200)

#tạo ống
pipe_surface= pygame.image.load('asset/img/pipe-green.png').convert()
pipe_surface= pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#timer of pipe
newpipe= pygame.USEREVENT
pygame.time.set_timer(newpipe,PIPE_INTERVAL)

#Ending
game_over_surface=pygame.transform.scale2x(pygame.image.load('asset/img/message.png').convert_alpha())
game_over_rect=game_over_surface.get_rect(center = (100,350))

#vị trí ống bên dưới
pipe_height=[]
for i in range(300,450):
    pipe_height.append(i)

#khoảng cách ống trên dưới
dis_pipes=[]
for i in range(680,700):
    dis_pipes.append(i)

#sound
flapsound=pygame.mixer.Sound('asset/sound/sfx_wing.wav')
diesound=pygame.mixer.Sound('asset/sound/sfx_die.wav')
hitsound=pygame.mixer.Sound('asset/sound/sfx_hit.wav')
pointsound=pygame.mixer.Sound('asset/sound/sfx_point.wav')
swooshingsound=pygame.mixer.Sound('asset/sound/sfx_swooshing.wav')
healingsound = pygame.mixer.Sound('asset/sound/health-pickup-6860.mp3')

#thiên thạch
meteorite=pygame.image.load('asset/img/meteo34x34.png').convert_alpha()
meteorite=pygame.transform.scale2x(meteorite)
meteo_list=[]

#timer
newmeteo= pygame.USEREVENT+3
pygame.time.set_timer(newmeteo,METEO_INTERVAL)

#LASER
WARNING_DISTANCE = 50  # Khoảng cách cảnh báo
warning_font = pygame.font.SysFont(None, 50)
warning_color = (255, 0, 0)  # đỏ

laser = pygame.image.load('asset/img/laser.png').convert_alpha()
laser_animation_frames = None
laser_animation_index = 0
laser_list=[]

#timer
lasertime= pygame.USEREVENT+4
pygame.time.set_timer(lasertime,LASER_INTERVAL) # 4s / laser

#điểm
score =0
best = 0

#kỉ lục mới
new_high_score=False

#tăng tốc game
game_speed = 80
speed_point = [5,10,15,20,25,30,50,100,200,300,400,500,600,700,800,900,1000]
index_speed = 0
end_index_speed = len(speed_point)-1

#thông báo nếu tăng tốc
speed_up_text = None
speed_up_rect = None
speed_up_active = False
speed_up_speed = 4  # tốc độ chạy ngang


#Màn hình chờ
key = True
while key:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    key=False 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    screen.blit(bg,(0,0))
    screen.blit(game_over_surface,(70,200))
    pygame.display.update()

#healing system
hp=100
heart_img = pygame.image.load('asset/img/heart_pixel_art_16x16.png').convert_alpha()
heart_img = pygame.transform.scale2x(heart_img)
heart_list = []

newheart = pygame.USEREVENT + 5
pygame.time.set_timer(newheart, HEART_INTERVAL) # 15s

# =============================== MAIN ===============================

#main
while True:
    # nhặt event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key== pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement = -4.3
                    flapsound.play()
                else:
                    game_active=True
                    pipe_list.clear()
                    meteo_list.clear()
                    laser_list.clear()
                    bird_rect.center = (100,350)
                    bird_movement=0
                    score=0
                    index_speed=0
                    game_speed=80
                    new_high_score=False
                    hp=100
        if event.type == newpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            index=(index+1)%len(bird_list)
            bird, bird_rect=bird_animation()
        if event.type== newmeteo:
            meteo_list.append(create_meteo())
        if event.type== lasertime:
            laser_list.append(create_laser())
            if score > 30:
                laser_list.append(create_laser())
            if score > 50:
                laser_list.append(create_laser())
            if score > 100:
                laser_list.append(create_laser())
            if score > 200:
                laser_list.append(create_laser())
            if score > 300:
                laser_list.append(create_laser())   
            if score > 500:
                laser_list.append(create_laser())

        if event.type == newheart:
            heart_list.append(create_heart())
            pygame.time.set_timer(newheart, random.randint(HEART_INTERVAL, HEART_INTERVAL+5000))


    # luôn vẽ background
    screen.blit(bg,(0,0))


    # tác động lên vật thể
    if game_active:
        # meteo
        meteo_list=move_meteo(meteo_list)
        draw_meteo(meteo_list) 

        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        new_bird= rotate_bird(bird)
        screen.blit(new_bird,bird_rect)

        # hp
        hp=check_collision(pipe_list,laser_list,hp)

        # ống
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)

        # laser
        laser_list=move_laser(laser_list)
        draw_laser(laser_list)

        #healing item
        heart_list = move_heart(heart_list)
        draw_heart(heart_list)
        hp = check_heart_collision(heart_list, hp)

        # speed up noti
        if speed_up_active:              
            speed_up_rect.centerx += speed_up_speed
            screen.blit(speed_up_text, speed_up_rect)

            # Nếu chạy ra khỏi màn hình bên phải thì tắt
            if speed_up_rect.left > WIDTH:
                speed_up_active = False


        # score
        x=cal(score)
        if x>score:
            pointsound.play()
        score=x
        if best<score:
            new_high_score=True
        best=max(best,score)
        game_active= (hp>0)

        # sàn
        floor_x_pos -= 1
        if floor_x_pos <= -432:
            floor_x_pos = 0

        # cơ chế tăng tốc
        if index_speed<= end_index_speed:
            if speed_point[index_speed]==int(score):
                swooshingsound.play()
                index_speed+=1
                if score < 100:
                    game_speed+=5
                else:
                    game_speed+=3

                # Tạo Speed Up text chạy ngang
                su_noti = "SPEED UP "
                for i in range(1,index_speed):
                    su_noti += "!!"
                speed_up_text = small_font.render(su_noti, True, (255, 255, 0))
                speed_up_rect = speed_up_text.get_rect(center=(-100, random.randint(50,200)))  # Bắt đầu ngoài màn hình bên trái
                speed_up_active = True

        #game_active=True # open to no die
        score_display(game_active)

    # luôn hiện điểm
    score_display(game_active)

    # luôn vẽ sàn
    draw_floor()

    pygame.display.update()
    clock.tick(game_speed)

    

