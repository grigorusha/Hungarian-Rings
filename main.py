import pygame
from pygame import *

import pygame_widgets
from pygame_widgets.button import Button

import random
from math import sqrt
import math
import copy

import webbrowser
from tkinter import Tk
from tkinter import filedialog as fd
import os

BACKGROUND_COLOR = "#000000"
GRAY_COLOR, GRAY_COLOR2, BLACK_COLOR = "#808080", "#C0C0C0", "#000000"
WHITE_COLOR, RED_COLOR, GREEN_COLOR, BLUE_COLOR = "#FFFFFF", "#FF0000", "#008000", "#0000FF"
GRADIENT_COLOR = [ [(255, 255, 255, 255), (120, 120, 120, 255)], [(70, 70, 70, 255), (0, 0, 0, 255)],      # 0 белый   1 черный
                   [(255, 50, 50, 255), (50, 0, 0, 255)], [(70, 180, 70, 255), (0, 50, 0, 255)],           # 2 красный 3 зеленый
                   [(50, 50, 255, 255), (0, 0, 50, 255)], [(250, 250, 50, 255), (50, 50, 0, 255)],         # 4 синий   5 желтый
                   [(200, 50, 200, 255), (50, 0, 50, 255)], [(250, 170, 50, 255), (70, 50, 0, 255)],       # 6 фиолетовый 7 оранжевый
                   [(50, 200, 250, 255), (0, 50, 50, 255)], [(0, 160, 160, 255), (0, 50, 50, 255)],       # 8 голубой 9 бирюзовый
                   [(190, 140, 140, 255), (50, 30, 30, 255)], [(250, 120, 190, 255), (70, 30, 50, 255)],   # 10 коричневый 11 розовый
                   [(200, 130, 250, 255), (50, 30, 70, 255)], [(0, 250, 0, 255), (0, 70, 00, 255)] ]       # 12 сиреневый 13 лайм

WIN_WIDTH, WIN_HEIGHT = 470, 300
PANEL = 33*2
BORDER = 20

filename = ""

BTN_CLICK = False
BTN_CLICK_STR = ""

def button_Button_click(button_str):
    global BTN_CLICK, BTN_CLICK_STR
    BTN_CLICK_STR = button_str
    BTN_CLICK = True

def gradient_circle(radius, color, cir, inv, offset=(0, 0)):
    radius = int(radius)
    diameter = radius * 2
    startcolor, endcolor = color

    bigSurf = pygame.Surface((diameter, diameter)).convert_alpha()
    bigSurf.fill((0, 0, 0, 0))
    dd = -1.0 / diameter
    sr, sg, sb, sa = endcolor
    er, eg, eb, ea = startcolor
    rm, gm, bm, am = (er - sr) * dd, (eg - sg) * dd, (eb - sb) * dd, (ea - sa) * dd

    draw_circle = pygame.draw.circle
    for rad in range(diameter, 0, -1):
        draw_circle(bigSurf, (er + int(rm * rad), eg + int(gm * rad), eb + int(bm * rad), ea + int(am * rad)),
                    (radius + inv*offset[0], radius + inv*offset[1]), rad, 2)

    for rad in range(radius, diameter, 1):
        draw_circle(bigSurf, (0, 0, 0, 0), (radius, radius), rad, 2)

    if cir:
        draw_circle(bigSurf, (0, 0, 0, 255), (radius, radius), radius-1, 1)

    return bigSurf

def calc_param(eval,param_calc):
    for param in param_calc:
        if param[0]==eval:
            eval = param[1]
            break
    eval = float(eval)
    return eval

def calc_angle(center_x,center_y, x,y, rad):
    x,y = x-center_x,y-center_y
    cos = x/rad
    if -1 <= cos <= 1:
        angle = math.acos(round(cos,10))
        grad = angle*180/math.pi
        if y<0:
            grad = 360 - grad
            angle = 2*math.pi - angle
    else: angle = grad = 0
    return angle,grad

def check_circle(center_x,center_y, x,y, rad):
    x,y = x-center_x,y-center_y
    length = sqrt(x*x+y*y)
    return (length<rad,length/rad)

def compare_xy(x,y,rr):
    return round(x,rr)==round(y,rr)

def init_ring():
    init = """
    Name: Golovolomka-8 (Головоломка-8)
    Link: https://twistypuzzles.com/cgi-bin/puzzle.cgi?pkey=4395
    
    Scale: 3
    Speed: 3
    Flip: rotate
    
    # радиус шариков, размер маркера
    BallsFormat: 10.3, 10
    
    # Переменные
    Param: pos_ball1, 40+20*sqrt(2) # 68.28427125
    Param: pos_ball2, 45+20*sqrt(2) # 73.28427125
    
    # номер кольца, координаты x y, радиус, количество шариков в кольце, направление заполнения, кольцо круглое
    Ring: 1, 40,          45, 40,          12, -1, 1
    Ring: 2, 100.21061364,45, 42.65315156, 13, -1, 1
    
    # цвета: 0 белый, 1 черный, 2 красный, 3 зеленый, 4 синий, 5 желтый, 6 фиолетовый
    # цвета: 7 оранжевый, 8 голубой, 9 бирюзовый, 10 коричневый, 11 розовый, 12 сиреневый, 13 лайм
    # номер кольца, номер шарика, координаты x y, цвет, метка, флаг пересечения
    Ball: 1,  1, pos_ball1, pos_ball2, 0, -, 1
    Ball: 1,  2, next, 0, -, 0
    Ball: 1,  3, next, 0, -, 0
    Ball: 1,  4, next, 0, -, 1
    Ball: 1,  5, next, 2, -, 0
    Ball: 1,  6, next, 2, -, 0
    Ball: 1,  7, next, 2, -, 0
    Ball: 1,  8, next, 2, -, 0
    Ball: 1,  9, next, 2, -, 0
    Ball: 1, 10, next, 2, -, 0
    Ball: 1, 11, next, 2, -, 0
    Ball: 1, 12, next, 2, -, 0
    
    Ball: 2,  1, pos_ball1, pos_ball2, 0, -, 1
    Ball: 2,  2, next, 4, -, 0
    Ball: 2,  3, next, 4, -, 0
    Ball: 2,  4, next, 4, -, 0
    Ball: 2,  5, next, 4, -, 0
    Ball: 2,  6, next, 4, -, 0
    Ball: 2,  7, next, 4, -, 0
    Ball: 2,  8, next, 4, -, 0
    Ball: 2,  9, next, 4, -, 0
    Ball: 2, 10, next, 4, -, 0
    Ball: 2, 11, next, 0, -, 1
    Ball: 2, 12, next, 0, -, 0
    Ball: 2, 13, next, 0, -, 0
    """.strip('\n')

    fil = read_file("init",init)
    return fil

def print_marker(game_scr,font_marker,txt,ball_x,ball_y, ball_color):
    if len(txt) > 0 and txt != "-":
        if ball_color != 1:
            text_marker = font_marker.render(txt, True, BLACK_COLOR)
        else:
            text_marker = font_marker.render(txt, True, WHITE_COLOR)
        text_marker_place = text_marker.get_rect(center=(ball_x, ball_y))
        game_scr.blit(text_marker, text_marker_place)  # Пишем маркет

def read_file(fl,init=""):
    global filename, BORDER, WIN_WIDTH, WIN_HEIGHT

    flip_y = flip_x = flip_rotate = False
    ring_name, ring_scale, ring_speed = "", 1, 3
    param_calc, ring_ballsformat, ring_rings, ring_balls, ring_link, solved_ring = [], [], [], [], [], []

    if fl == "init":
        lines = init.split("\n")
    else:
        if fl=="open" or filename=="":
            dir = os.path.abspath(os.curdir)
            if os.path.isdir(dir+"\\Rings"):
                dir = dir+"\\Rings"
            filetypes = (("Text file", "*.txt"),("Any file", "*"))
            filename = fd.askopenfilename(title="Open Level", initialdir=dir,filetypes=filetypes)
            if filename=="":
                return ""
        lines = []
        with open(filename,'r') as f:
            lines = f.readlines()

    # прочитаем файл
    for nom,stroka in enumerate(lines):
        stroka = stroka.replace('\n','')
        stroka = stroka.strip()
        if stroka == "": continue

        if stroka[0] == "#": continue
        pos = stroka.find("#")
        if pos >= 0:
            stroka = stroka[0:pos]

        pos = stroka.find(":")
        if pos == -1: continue
        if pos == len(stroka)-1: continue

        command = stroka[0:pos].strip()
        params =  stroka[pos+1:].strip()
        param_mas = params.split(",")
        for num,par in enumerate(param_mas):
            param_mas[num] = par.strip()

        if command == "Name":
            ring_name = params
        elif command == "Link":
            ring_link.append(params)
        elif command == "Scale":
            ring_scale = float(params)
        elif command == "Speed":
            ring_speed = float(params)
        elif command == "Flip":
            if params.lower().find("y")>=0:
                flip_y = True
            if params.lower().find("x")>=0:
                flip_x = True
            if params.lower().find("rotate") >= 0:
                flip_rotate = True
        elif command == "BallsFormat":
            if len(param_mas) != 2: return ""
            ring_ballsformat = [float(param_mas[0]), int(param_mas[1])]
        elif command == "Param":
            if len(param_mas) != 2: return ""
            param_mas[1] = eval(param_mas[1])
            param_calc.append([param_mas[0], param_mas[1]])
        elif command == "Ring":
            if len(param_mas) != 7: return ""
            param_mas[1],param_mas[2],param_mas[3] = calc_param(param_mas[1],param_calc), calc_param(param_mas[2],param_calc), calc_param(param_mas[3],param_calc)
            angle_sector = math.pi*2/int(param_mas[4])
            ring_rings.append( [ int(param_mas[0]),param_mas[1],param_mas[2],param_mas[3],int(param_mas[4]),int(param_mas[5]),angle_sector,int(param_mas[6]) ] )
        elif command == "Ball":
            if len(param_mas)==7:
                param_mas[2],param_mas[3],param_mas[0] = calc_param(param_mas[2],param_calc),calc_param(param_mas[3],param_calc),int(param_mas[0])
                if int(param_mas[1])==1:
                    angle,grad = calc_angle(ring_rings[param_mas[0]-1][1],ring_rings[param_mas[0]-1][2], param_mas[2],param_mas[3], ring_rings[param_mas[0]-1][3])
                ring_balls.append( [ param_mas[0],int(param_mas[1]),param_mas[2],param_mas[3],int(param_mas[4]),param_mas[5],int(param_mas[6]),[] ] )
            elif len(param_mas)==6 and param_mas[2]=="next":
                param_mas[0],param_mas[1] = int(param_mas[0]),int(param_mas[1])
                angle_sector = ring_rings[param_mas[0]-1][6]
                vekt = ring_rings[param_mas[0]-1][5]
                radius = ring_rings[param_mas[0]-1][3]
                center_x, center_y = ring_rings[param_mas[0]-1][1], ring_rings[param_mas[0]-1][2]
                num = param_mas[1] - 1
                ang = angle + vekt*angle_sector*num
                angle_cos, angle_sin = math.cos(ang), math.sin(ang)
                xx, yy = angle_cos*radius+center_x, angle_sin*radius+center_y
                ring_balls.append( [ param_mas[0],param_mas[1],xx,yy,int(param_mas[3]),param_mas[4],int(param_mas[5]),[] ] )
            else: return ""

    # учтем масштаб
    if ring_scale != 1 and ring_scale != 0:
        ring_ballsformat[0] = ring_ballsformat[0]*ring_scale
        shift = ring_ballsformat[0]+BORDER
        for ring in ring_rings:
            ring[1] = ring[1] * ring_scale + shift
            ring[2] = ring[2] * ring_scale + shift
            ring[3] = ring[3] * ring_scale
        for ball in ring_balls:
            ball[2] = ball[2] * ring_scale + shift
            ball[3] = ball[3] * ring_scale + shift

    ball_radius = ring_ballsformat[0]
    ball_offset = (-int(ball_radius / 3), -int(ball_radius / 3))

    # изменим размеры окна
    WIN_WIDTH, WIN_HEIGHT = 0, 0
    for ring in ring_rings:
        if ring[7]!=0:
            xx = ring[1] + ring[3] + ball_radius + BORDER
            WIN_WIDTH = xx if xx > WIN_WIDTH else WIN_WIDTH
            yy = ring[2] + ring[3] + ball_radius + BORDER
            WIN_HEIGHT = yy if yy > WIN_HEIGHT else WIN_HEIGHT
    for ball in ring_balls:
        xx = ball[2] + ball_radius + BORDER
        WIN_WIDTH = xx if xx > WIN_WIDTH else WIN_WIDTH
        yy = ball[3] + ball_radius + BORDER
        WIN_HEIGHT = yy if yy > WIN_HEIGHT else WIN_HEIGHT

    # учтем повороты
    vek_mul = -1
    if flip_x:
        vek_mul = -1 * vek_mul
        for ring in ring_rings:
            ring[1] = WIN_WIDTH - ring[1]
        for ball in ring_balls:
            ball[2] = WIN_WIDTH - ball[2]
    if flip_y:
        vek_mul = -1 * vek_mul
        for ring in ring_rings:
            ring[2] = WIN_HEIGHT - ring[2]
        for ball in ring_balls:
            ball[3] = WIN_HEIGHT - ball[3]
    if flip_rotate:
        vek_mul = -1 * vek_mul
        for ring in ring_rings:
            ring[1],ring[2] = ring[2],ring[1]
        for ball in ring_balls:
            ball[2],ball[3] = ball[3],ball[2]
        WIN_WIDTH, WIN_HEIGHT = 0, 0
        for ring in ring_rings:
            xx = ring[1] + ring[3] + ball_radius + BORDER
            WIN_WIDTH = xx if xx > WIN_WIDTH else WIN_WIDTH
            yy = ring[2] + ring[3] + ball_radius + BORDER
            WIN_HEIGHT = yy if yy > WIN_HEIGHT else WIN_HEIGHT

    ###########################################################################
    # установка перекрестных ссылок
    for ring in ring_rings:
        for ball in ring_balls:
            if ball[6] == 0: continue

            fl_break = False
            for ring_sec in ring_rings:
                if ring_sec[0]==ball[0]: continue

                fl_break = False
                for ball_sec in ring_balls:
                    if ring_sec[0] != ball_sec[0]: continue
                    if ball_sec[6] == 0: continue

                    if compare_xy(ball[2],ball_sec[2],2) and compare_xy(ball[3],ball_sec[3],2): # ball[2] == ball_sec[2] and ball[3] == ball_sec[3]
                        if len(ball[7])==0:
                            ball[7].append( ball_sec[0] )  # номер перекрестного кольца, номер шарика в нем
                            ball[7].append( ball_sec[1] )
                        if len(ball_sec[7])==0:
                            ball_sec[7].append( ball[0] )
                            ball_sec[7].append( ball[1] )
                        ball_sec[4], ball_sec[5] = ball[4], ball[5]
                        fl_break = True

                    if fl_break: break
                if fl_break: break

    solved_ring = copy.deepcopy(ring_balls)

    return ring_name,ring_link, ring_scale,ring_speed, ring_ballsformat,ring_rings,ring_balls, ball_radius,ball_offset, solved_ring, WIN_WIDTH,WIN_HEIGHT, vek_mul

def main():
    global BTN_CLICK,BTN_CLICK_STR, WIN_WIDTH,WIN_HEIGHT, BORDER, filename

    file_ext = False

    ball_radius = 100 # ring_ballsformat[0]
    offset = (-int(ball_radius / 3), -int(ball_radius / 3))

    ring_name = ring_link = ""
    ring_scale, ring_speed = 1, 3
    ring_ballsformat, ring_rings, ring_balls = [], [], []
    vek_mul = -1
    solved_ring = []

    # основная инициализация
    random.seed()
    pygame.init()  # Инициация PyGame
    font = pygame.font.SysFont('Verdana', 18)
    font_button = pygame.font.SysFont("ArialB",18)
    timer = pygame.time.Clock()
    Tk().withdraw()

    ################################################################################
    ################################################################################
    # перезапуск программы при смене параметров
    while True:
        if not file_ext:
            fil = init_ring()
            ring_name, ring_link, ring_scale, ring_speed, ring_ballsformat, ring_rings, ring_balls, ball_radius, ball_offset, solved_ring, WIN_WIDTH, WIN_HEIGHT, vek_mul = fil

        DISPLAY = (WIN_WIDTH, WIN_HEIGHT+PANEL)  # Группируем ширину и высоту в одну переменную
        # инициализация окна
        screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        win_caption = ring_name if ring_name != "" else "Hungarian Rings Simulator"
        pygame.display.set_caption(win_caption)  # Пишем в шапку
        font_marker = pygame.font.SysFont('Verdana', ring_ballsformat[1])

        # инициализация окна с подсказкой
        HELP = (WIN_WIDTH//3+BORDER, WIN_HEIGHT//3+BORDER)
        GAME = (WIN_WIDTH, WIN_HEIGHT)
        game_scr = Surface(GAME)

        scramble_move = 0
        moves_stack = []
        moves = 0
        solved = True

        help = False
        help_gen = True

        # инициализация кнопок
        if True:
            button_y1 = WIN_HEIGHT + 10 + 10
            button_Reset = Button(screen, 10, button_y1, 45, 20, text='Reset', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("reset"))
            button_Scramble = Button(screen, button_Reset.textRect.right+10, button_y1, 70, 20, text='Scramble', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("scramble"))
            button_Undo = Button(screen, button_Scramble.textRect.right+10, button_y1, 40, 20, text='Undo', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("undo"))

            button_Open = Button(screen, button_Undo.textRect.right+20, button_y1, 45, 20, text='Open', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("open"))

            button_Info = Button(screen, button_Open.textRect.right+20, button_y1, 30, 20, text='Info', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("info"))
            button_Help = Button(screen, button_Info.textRect.right+8, button_y1, 35, 20, text='Help', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour="#008000", hoverColour="#008000", pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("help"))

            button_y3 = button_y1 + 30
        button_set = [button_Reset, button_Scramble, button_Undo, button_Open, button_Info, button_Help]

        ################################################################################
        ################################################################################
        # Основной цикл программы
        while True:
            undo = False
            mouse_x, mouse_y, mouse_left, mouse_right = 0, 0, False, False
            ring_num = vek = 0

            if scramble_move == 0:
                timer.tick(100)

                fl_break = False

                events = pygame.event.get()
                for ev in events:  # Обрабатываем события
                    if (ev.type == QUIT):
                        return SystemExit, "QUIT"
                    if (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                        help = False if help else help
                    if (ev.type == KEYDOWN and ev.key == K_F1):
                        BTN_CLICK = True
                        BTN_CLICK_STR = "help"
                    if (ev.type == KEYDOWN and ev.key == K_F2):
                        BTN_CLICK = True
                        BTN_CLICK_STR = "reset"
                    if (ev.type == KEYDOWN and ev.key == K_F3):
                        BTN_CLICK = True
                        BTN_CLICK_STR = "open"
                    if (ev.type == KEYDOWN and ev.key == K_SPACE):
                        BTN_CLICK = True
                        BTN_CLICK_STR = "undo"

                    if ev.type == MOUSEBUTTONDOWN and (ev.button == 1 or ev.button == 4) and not BTN_CLICK:
                        if not help:
                            mouse_x = ev.pos[0]
                            mouse_y = ev.pos[1]
                            mouse_left = True
                        help = False if help else help
                    if ev.type == MOUSEBUTTONDOWN and (ev.button == 3 or ev.button == 5) and not BTN_CLICK:
                        if not help:
                            mouse_x = ev.pos[0]
                            mouse_y = ev.pos[1]
                            mouse_right = True
                        help = False if help else help
                    # if ev.type == MOUSEBUTTONDOWN and ev.button == 5:
                    #     BTN_CLICK = True
                    #     BTN_CLICK_STR = "undo"

                    ################################################################################
                    # обработка нажатия на кнопки
                    if BTN_CLICK:
                        if BTN_CLICK_STR=="reset" and not help:
                            if not file_ext:
                                fl_break = True
                            else:
                                fil = read_file("reset")
                                if fil != "":
                                    file_ext = True
                                    ring_name, ring_link, ring_scale, ring_speed, ring_ballsformat, ring_rings, ring_balls, ball_radius, ball_offset, solved_ring, WIN_WIDTH, WIN_HEIGHT, vek_mul = fil
                                    fl_break = True
                        if BTN_CLICK_STR=="open" and not help:
                            fl_break = False
                            fil = read_file("open")
                            if fil != "":
                                file_ext = True
                                ring_name,ring_link, ring_scale, ring_speed, ring_ballsformat,ring_rings,ring_balls, ball_radius,ball_offset, solved_ring, WIN_WIDTH,WIN_HEIGHT, vek_mul = fil
                                fl_break = True

                        if BTN_CLICK_STR=="info" and not help:
                            for link in ring_link:
                                if link!="":
                                    webbrowser.open(link, new=2, autoraise=True)
                        if BTN_CLICK_STR=="help":
                            help = not help

                        if BTN_CLICK_STR=="scramble" and not help:
                            fl_break = False
                            scramble_move = 3000
                        if BTN_CLICK_STR=="undo" and not help:
                            fl_break = False
                            if len(moves_stack) > 0:
                                ring_num, vek = moves_stack.pop()
                                vek = -vek
                                moves -= 1
                                undo = True

                        BTN_CLICK = False
                        BTN_CLICK_STR = ""
                if fl_break: break

                ################################################################################
                # обработка нажатия в игровом поле
                if mouse_x + mouse_y > 0 and not help:
                    if mouse_x<WIN_WIDTH and mouse_y<WIN_HEIGHT:
                        ring_pos = []
                        for ring in ring_rings:
                            pos = check_circle(ring[1], ring[2], mouse_x, mouse_y, ring[3])
                            if pos[0]:
                                ring_pos.append( (ring[0], pos[1]) )
                        if len(ring_pos)>0: # есть внутри круга
                            rr = 999999
                            for ring in ring_pos:
                                if ring[1]<rr:
                                    rr = ring[1]
                                    ring_num = ring[0]
                            vek = -1 if mouse_left else 1 if mouse_right else vek
                            vek = vek * vek_mul

            else:
                ################################################################################
                # обработка рандома для Скрамбла
                vek = random.choice([-1,1])
                ring_num = random.randint(0, len(ring_rings))

            ################################################################################
            # логика игры - выполнение перемещений
            if ring_num>0:

                # анимация
                if scramble_move == 0 and ring_rings[ring_num - 1][7] != 0:
                    angle_sector = ring_rings[ring_num - 1][6]
                    radius = ring_rings[ring_num - 1][3]
                    step = int(radius*angle_sector)
                    # step_mul = 2 if step<20 else 3 if step<60 else 4 if step<100 else 5
                    step = step // ring_speed

                    for count in range(int(step)):
                        timer.tick(300)
                        game_scr.fill(Color(GRAY_COLOR))
                        for ring in ring_rings:
                            draw.circle(game_scr, GRAY_COLOR2, (ring[1], ring[2]), ring[3] - ball_radius, 2)
                            draw.circle(game_scr, GRAY_COLOR2, (ring[1], ring[2]), ring[3] + ball_radius + 3, 2)
                        for ball in ring_balls:
                            ball_x,ball_y = ball[2],ball[3]
                            if ring_num!=ball[0]:
                                if ball[6]==0:
                                    game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset),(ball_x - ball_radius, ball_y - ball_radius))
                                    print_marker(game_scr, font_marker, ball[5], ball_x, ball_y, ball[4])
                                elif ball[7][0]!=ring_num:
                                    game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset),(ball_x - ball_radius, ball_y - ball_radius))
                                    print_marker(game_scr, font_marker, ball[5], ball_x, ball_y, ball[4])
                            else:
                                center_x, center_y = ring_rings[ring_num-1][1], ring_rings[ring_num-1][2]
                                angle, grad = calc_angle(center_x,center_y, ball_x,ball_y, radius)
                                ang = round(angle + vek * vek_mul * count*angle_sector/step,10)
                                angle_cos, angle_sin = math.cos(ang), math.sin(ang)
                                xx, yy = angle_cos * radius + center_x, angle_sin * radius + center_y
                                game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset), (xx-ball_radius, yy-ball_radius))
                                print_marker(game_scr, font_marker, ball[5], xx, yy, ball[4])
                        screen.blit(game_scr, (0, 0))
                        pygame.display.update()

                #############################################################################
                # перемещение
                ball_kol = ring_rings[ring_num-1][4]
                for nn,ball in enumerate(ring_balls):
                    if ball[0] != ring_num: continue

                    if vek==-1:
                        ball_pred = copy.deepcopy(ball)
                        for kol in range(1,ball_kol):
                            ball = ring_balls[nn+kol-1]
                            ball_next = ring_balls[nn+kol]
                            ball[4],ball[5] = ball_next[4],ball_next[5]
                        ball_next = ring_balls[nn+ball_kol-1]
                        ball_next[4],ball_next[5] = ball_pred[4],ball_pred[5]
                    if vek==1:
                        ball = ring_balls[nn+ball_kol-1]
                        ball_pred = copy.deepcopy(ball)
                        for kol in range(ball_kol-1,0,-1):
                            ball = ring_balls[nn+kol]
                            ball_next = ring_balls[nn+kol-1]
                            ball[4],ball[5] = ball_next[4],ball_next[5]
                        ball_next = ring_balls[nn]
                        ball_next[4],ball_next[5] = ball_pred[4],ball_pred[5]
                    for kol in range(0,ball_kol):
                        ball = ring_balls[nn+kol]
                        if ball[6]==1:
                            for ball_next in ring_balls:
                                if ball_next[0] == ball[7][0] and ball_next[1] == ball[7][1]:
                                    ball_next[4], ball_next[5] = ball[4], ball[5]

                    if not undo:
                        moves += 1
                        moves_stack.append([ring_num, vek])

                    break

            # скрамбл
            if scramble_move != 0:
                scramble_move -= 1
                moves_stack = []
                moves = 0
                continue
                # отрисовка не нужна

            # проверка на решенное состояние
            solved = True
            if len(moves_stack) > 0:
                if ring_balls != solved_ring:
                    solved = False

            #####################################################################################
            # отрисовка игрового поля
            screen.fill(BACKGROUND_COLOR)  # Заливаем поверхность сплошным цветом
            pf = Surface((WIN_WIDTH, 10)) # Рисуем разделительную черту
            pf.fill(Color("#B88800"))
            screen.blit(pf, (0, WIN_HEIGHT))

            ################################################################################
            # text
            text_moves = font.render('Moves: ' + str(moves), True, RED_COLOR)
            text_moves_place = text_moves.get_rect(topleft=(10, button_y3-7))
            screen.blit(text_moves, text_moves_place) # Пишем количество перемещений
            if solved:
                text_solved = font.render('Solved', True, WHITE_COLOR)
            else:
                text_solved = font.render('not solved', True, RED_COLOR)
            text_solved_place = text_solved.get_rect(topleft=(text_moves_place.right + 10, button_y3-7))
            screen.blit(text_solved, text_solved_place) # Пишем статус

            ############################################

            game_scr.fill(Color(GRAY_COLOR))
            # отрисовка колец
            for ring in ring_rings:
                draw.circle(game_scr,GRAY_COLOR2,(ring[1],ring[2]), ring[3]-ball_radius, 2)
                draw.circle(game_scr,GRAY_COLOR2,(ring[1],ring[2]), ring[3]+ball_radius+3, 2)
            # отрисовка шариков
            for ball in ring_balls:
                ball_x,ball_y = ball[2],ball[3]
                game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset), (ball_x-ball_radius, ball_y-ball_radius))
                print_marker(game_scr,font_marker,ball[5],ball_x,ball_y, ball[4])

            screen.blit(game_scr, (0, 0))

            # окно помощи
            if help_gen:
                help_gen = False
                help_screen = pygame.transform.scale(game_scr, HELP)
                draw.rect(help_screen, Color("#B88800"), (0,0,HELP[0],HELP[1]), BORDER//3)
            if help:
                screen.blit(help_screen, (GAME[0]-HELP[0],0))

            #####################################################################################
            pygame_widgets.update(events)
            pygame.display.update()  # обновление и вывод всех изменений на экран

        # удаляем кнопки
        for btn in button_set:
            btn.hide()

main()
