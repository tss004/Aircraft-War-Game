from sys import exit
from pygame.locals import *
from Strategy import *
import random
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Aircraft War Game')
bullet_shot = pygame.mixer.Sound('image/sound/bullet.wav')
oppenent_t = pygame.mixer.Sound('image/sound/opponent1_down.wav')
game_over_s = pygame.mixer.Sound('image/sound/game_over.wav')
bullet_shot.set_volume(0.3)
oppenent_t.set_volume(0.3)
game_over_s.set_volume(0.3)
pygame.mixer.music.load('image/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

GAME_BACKGROUND = pygame.image.load('image/image/background.png').convert()
GAME_OVER = pygame.image.load('image/image/gameover.png')
filename = 'image/image/aircraft_shooter.png'
AIRCRAFT_IMAGES = pygame.image.load(filename)

player_par= []
player_par.append(pygame.Rect(0, 99, 102, 126)) 
player_par.append(pygame.Rect(165, 360, 102, 126))
player_par.append(pygame.Rect(165, 234, 102, 126))  
player_par.append(pygame.Rect(330, 624, 102, 126))
player_par.append(pygame.Rect(330, 498, 102, 126))
player_par.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
OPPONENT = Opponent(AIRCRAFT_IMAGES, player_par, player_pos)

acr_bullet = pygame.Rect(1004, 987, 9, 21)
bullet_img = AIRCRAFT_IMAGES.subsurface(acr_bullet)

OPPONENT1 = pygame.Rect(534, 612, 57, 43)
op_img = AIRCRAFT_IMAGES.subsurface(OPPONENT1)
op_down_img = []
op_down_img.append(AIRCRAFT_IMAGES.subsurface(pygame.Rect(267, 347, 57, 43)))
op_down_img.append(AIRCRAFT_IMAGES.subsurface(pygame.Rect(873, 697, 57, 43)))
op_down_img.append(AIRCRAFT_IMAGES.subsurface(pygame.Rect(267, 296, 57, 43)))
op_down_img.append(AIRCRAFT_IMAGES.subsurface(pygame.Rect(930, 697, 57, 43)))

ch_1 = pygame.sprite.Group()
ch_down = pygame.sprite.Group()
shoot_dis = 0
ch_dis = 0
op_down_idx = 16
score = 0
clock = pygame.time.Clock()
game_running = True

while game_running:
    
    clock.tick(60)
    if not OPPONENT.is_hit:
        if shoot_dis % 15 == 0:
            bullet_shot.play()
            OPPONENT.shoot(bullet_img)
        shoot_dis += 1
        if shoot_dis >= 15:
            shoot_dis = 0
    if shoot_dis % 50 == 0:
        ch_1_pos = [random.randint(0, SCREEN_WIDTH - OPPONENT1.width), 0]
        chall_1 = Challenger(op_img, op_down_img, ch_1_pos)
        ch_1.add(chall_1)
    ch_dis += 1
    if ch_dis >= 100:
        ch_dis = 0

    for bullet in OPPONENT.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            OPPONENT.bullets.remove(bullet)

    
    for C in ch_1:
        C.move()
        if pygame.sprite.collide_circle(C, OPPONENT):
            ch_down.add(C)
            ch_1.remove(C)
            OPPONENT.is_hit = True
            game_over_s.play()
            break
        if C.rect.top > SCREEN_HEIGHT:
            ch_1.remove(C)
    ch_1_DOWN = pygame.sprite.groupcollide(ch_1, OPPONENT.bullets, 1, 1)
    for C in ch_1_DOWN:
        ch_down.add(C)

    screen.fill(0)
    screen.blit(GAME_BACKGROUND, (0, 0))

    if not OPPONENT.is_hit:
        screen.blit(OPPONENT.image[OPPONENT.img_index], OPPONENT.rect)
        OPPONENT.img_index = shoot_dis // 8
    else:
        OPPONENT.img_index = op_down_idx // 8
        screen.blit(OPPONENT.image[OPPONENT.img_index], OPPONENT.rect)
        op_down_idx += 1
        if op_down_idx > 47:
            game_running = False

    
    for C in ch_down:
        if C.down_index == 0:
            oppenent_t.play()
        if C.down_index > 7:
            ch_down.remove(C)
            score += 1000
            continue
        screen.blit(C.down_imgs[C.down_index // 2], C.rect)
        C.down_index += 1

    OPPONENT.bullets.draw(screen)
    ch_1.draw(screen)

    score_FONT = pygame.font.Font(None, 36)
    score_TXT = score_FONT.render(str(score), True, (255, 255, 0))
    tt_aircraft = score_TXT.get_rect()
    tt_aircraft.topleft = [10, 10]
    screen.blit(score_TXT, tt_aircraft)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_press = pygame.key.get_pressed()
    if not OPPONENT.is_hit:
        if key_press[K_r] or key_press[K_UP]:
            OPPONENT.moveUp()
        if key_press[K_f] or key_press[K_DOWN]:
            OPPONENT.moveDown()
        if key_press[K_d] or key_press[K_LEFT]:
            OPPONENT.moveLeft()
        if key_press[K_g] or key_press[K_RIGHT]:
            OPPONENT.moveRight()

FONT = pygame.font.Font(None, 60)
TXT = FONT.render('score: ' + str(score), True, (255, 255, 0))
tt_aircraft = TXT.get_rect()
tt_aircraft.centerx = screen.get_rect().centerx
tt_aircraft.centery = screen.get_rect().centery + 24
screen.blit(GAME_OVER, (0, 0))
screen.blit(TXT, tt_aircraft)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
