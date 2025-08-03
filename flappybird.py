import pygame, sys, random

#lặp sàn
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
#xử lí va chạm
def check_collision(pipes,lasers,sa):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            sa-=1
            if sa==0:
                hitsound.play()
                return 0
    for alaser in lasers:
        if bird_rect.colliderect(alaser):
            sa-=1
            if sa==0:
                hitsound.play()
                return 0
    if bird_rect.top<=-78:
        diesound.play()
        return 0
    if bird_rect.bottom>=650:
        diesound.play()
        return 0
    return sa 
#chim bay
def rotate_bird(birds):
    new_bird=pygame.transform.rotozoom(birds,-bird_movement*4,1)
    return new_bird
#animation of bird
def bird_animation():
    new_bird=bird_list[index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect
#display
def score_display(active): 
    logo_suface=logo_font.render(logo_list[idx_logo],True,(255,250,100))
    logo_rect=logo_suface.get_rect(center=(logo_x_pos,logo_y_pos))
    screen.blit(logo_suface,logo_rect)
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
#tính điểm
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
    y=random.randint(150,350)
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

    

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.font.init()
#setting
WIDTH = 432
HEIGHT = 768
screen= pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
gravity = 0.2
bird_movement = 0

game_active =True
game_font=pygame.font.Font('04B_19.TTF',43)
new_font=pygame.font.SysFont('',25)
logo_font=pygame.font.SysFont('',30)
#chèn background
bg = pygame.image.load('background-night.png').convert()
bg = pygame.transform.scale2x(bg)

#chèn sàn
floor = pygame.image.load('floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos=0

#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('yellowbird-upflap.png').convert_alpha())
bird_list=[bird_down,bird_mid,bird_up]
index=2
bird = bird_list[index]
bird_rect=bird.get_rect(center = (100,350))
#timer of bird
birdflap = pygame.USEREVENT +1
pygame.time.set_timer(birdflap,200)

#tạo ống
pipe_surface= pygame.image.load('pipe-green.png').convert()
pipe_surface= pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#timer of pipe
newpipe= pygame.USEREVENT
pygame.time.set_timer(newpipe,1500)

#Ending
game_over_surface=pygame.transform.scale2x(pygame.image.load('message.png').convert_alpha())
game_over_rect=game_over_surface.get_rect(center = (100,350))

pipe_height=[]
for i in range(300,450):
    pipe_height.append(i)

#sound
flapsound=pygame.mixer.Sound('sfx_wing.wav')
diesound=pygame.mixer.Sound('sfx_die.wav')
hitsound=pygame.mixer.Sound('sfx_hit.wav')
pointsound=pygame.mixer.Sound('sfx_point.wav')
swooshingsound=pygame.mixer.Sound('sfx_swooshing.wav')

#thiên thạch
meteorite=pygame.image.load('meteo34x34.png').convert_alpha()
meteorite=pygame.transform.scale2x(meteorite)
meteo_list=[]

#timer
newmeteo= pygame.USEREVENT+3
pygame.time.set_timer(newmeteo,1000)

#LASER - Sử dụng file laser.png
WARNING_DISTANCE = 50  # Khoảng cách từ mép phải màn hình để hiện "!"
warning_font = pygame.font.SysFont(None, 50)  # font mặc định, cỡ 50
warning_color = (255, 0, 0)  # đỏ chói

laser = pygame.image.load('laser.png').convert_alpha()
laser_animation_frames = None
laser_animation_index = 0

laser_list=[]
#timer
lasertime= pygame.USEREVENT+4
pygame.time.set_timer(lasertime,4000)
#điểm
score =0
best = 0

#kỉ lục mới
new_high_score=False

#tăng tốc bay
game_speed = 80
speed_point = [5,10,15,20,25,30]
index_speed = 0
end_index_speed = len(speed_point)-1

#khoảng cách ống
dis_pipes=[690,710,720,740]
logo_list=['Great','Nice','Keep going']
idx_logo=0
logo_x_pos=-100
logo_y_pos=20
increase_x_logo=2
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
    screen.blit(bg,(0,0))
    screen.blit(game_over_surface,(70,200))
    pygame.display.update()

still_alive=3
#main
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement = -4.3
                    flapsound.play()
                else:
                    #logo_x_pos=-100
                    #logo_y_pos=20
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
                    still_alive=3
        if event.type == newpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            index=(index+1)%len(bird_list)
            bird, bird_rect=bird_animation()
        if event.type== newmeteo:
            meteo_list.append(create_meteo())
        if event.type== lasertime:
            laser_list.append(create_laser())




    screen.blit(bg,(0,0))
    if game_active:
        #meteo
        meteo_list=move_meteo(meteo_list)
        draw_meteo(meteo_list) 

        #chim
        bird_movement+=gravity
        new_bird= rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(new_bird,bird_rect)
        still_alive=check_collision(pipe_list,laser_list,still_alive)

        #ống
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)
        #game_active=True // no die

        #laser
        laser_list=move_laser(laser_list)
        draw_laser(laser_list)

        #score
        x=cal(score)
        if x>score:
            pointsound.play()
        score=x
        if best<score:
            new_high_score=True
        best=max(best,score)
        game_active= (still_alive!=0)
        score_display(game_active)

    score_display(game_active)

    #sàn
    floor_x_pos-=1
    draw_floor()
    if(floor_x_pos<=-432):
        floor_x_pos=0
    logo_x_pos+=increase_x_logo
    if(logo_x_pos>=700 or logo_x_pos <=-450):
        increase_x_logo*=-1
        idx_logo=(idx_logo+1)%len(logo_list)
        #logo_x_pos=-100
        logo_y_pos+=15
        if logo_y_pos>70:
            logo_y_pos=20

        
    pygame.display.update()
    clock.tick(game_speed)
    if index_speed<= end_index_speed:
        if speed_point[index_speed]==int(score):
            swooshingsound.play()
            index_speed+=1
            game_speed+=5
    

