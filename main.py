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
GRAY_COLOR, GRAY_COLOR2 = "#808080", "#C0C0C0"
WHITE_COLOR, RED_COLOR, GREEN_COLOR, BLUE_COLOR = "#FFFFFF", "#FF0000", "#008000", "#0000FF"
GRADIENT_COLOR = [ [(255, 255, 255, 255), (120, 120, 120, 255)], [(70, 70, 70, 255), (0, 0, 0, 255)],      # 0 белый   1 черный
                   [(255, 50, 50, 255), (50, 0, 0, 255)], [(70, 180, 70, 255), (0, 50, 0, 255)],           # 2 красный 3 зеленый
                   [(50, 50, 255, 255), (0, 0, 50, 255)], [(250, 250, 50, 255), (50, 50, 0, 255)],         # 4 синий   5 желтый
                   [(200, 50, 200, 255), (50, 0, 50, 255)], [(250, 200, 50, 255), (50, 50, 0, 255)],       # 6 фиолетовый 7 оранжевый
                   [(50, 200, 250, 255), (0, 50, 50, 255)], [(50, 210, 200, 255), (0, 50, 50, 255)],       # 8 голубой 9 бирюзовый
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
    angle = math.acos(cos)
    grad = angle*180/math.pi
    return angle,grad

def check_circle(center_x,center_y, x,y, rad):
    x,y = x-center_x,y-center_y
    length = sqrt(x*x+y*y)
    return (length<rad,length)

def compare_xy(x,y,rr):
    return round(x,rr)==round(y,rr)

def read_file(fl):
    global filename, BORDER, WIN_WIDTH, WIN_HEIGHT

    if fl or filename=="":
        dir = os.path.abspath(os.curdir)
        filetypes = (("Text file", "*.txt"),("Any file", "*"))
        filename = fd.askopenfilename(title="Open Level", initialdir=dir,filetypes=filetypes)
        if filename=="":
            return ""

    flip_y = flip_x = flip_rotate = False
    ring_name, ring_scale = "", 1
    param_calc, ring_ballsformat, ring_rings, ring_balls, ring_link = [], [], [], [], []

    with open(filename,'r') as f:
        lines = f.readlines()
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
                if len(param_mas) != 6: return ""
                param_mas[1],param_mas[2],param_mas[3] = calc_param(param_mas[1],param_calc), calc_param(param_mas[2],param_calc), calc_param(param_mas[3],param_calc)
                angle_sector = math.pi*2/int(param_mas[4])
                ring_rings.append( [ int(param_mas[0]),param_mas[1],param_mas[2],param_mas[3],int(param_mas[4]),int(param_mas[5]),angle_sector ] )
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
                    angle_cos = math.cos(angle + vekt*angle_sector*num)
                    angle_sin = math.sin(angle + vekt*angle_sector*num)
                    xx, yy = angle_cos*radius+center_x, angle_sin*radius+center_y
                    ring_balls.append( [ param_mas[0],param_mas[1],xx,yy,int(param_mas[3]),param_mas[4],int(param_mas[5]),[] ] )
                else: return ""

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

    WIN_WIDTH, WIN_HEIGHT = 0, 0
    for ring in ring_rings:
        xx = ring[1] + ring[3] + ball_radius + BORDER
        WIN_WIDTH = xx if xx > WIN_WIDTH else WIN_WIDTH
        yy = ring[2] + ring[3] + ball_radius + BORDER
        WIN_HEIGHT = yy if yy > WIN_HEIGHT else WIN_HEIGHT

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

                    if compare_xy(ball[2],ball_sec[2],4) and compare_xy(ball[3],ball_sec[3],4): # ball[2] == ball_sec[2] and ball[3] == ball_sec[3]
                        if len(ball[7])==0:
                            ball[7].append( ball_sec[0] )  # номер перекрестного кольца, номер шарика в нем
                            ball[7].append( ball_sec[1] )
                        if len(ball_sec[7])==0:
                            ball_sec[7].append( ball[0] )
                            ball_sec[7].append( ball[1] )

                        fl_break = True

                    if fl_break: break
                if fl_break: break

    return ring_name,ring_link, ring_scale, ring_ballsformat,ring_rings,ring_balls, ball_radius,ball_offset, WIN_WIDTH,WIN_HEIGHT, vek_mul

def main():
    global BTN_CLICK,BTN_CLICK_STR, WIN_WIDTH,WIN_HEIGHT, BORDER, filename

    file_ext = False

    ball_radius = 100 # ring_ballsformat[0]
    offset = (-int(ball_radius / 3), -int(ball_radius / 3))

    ring_name = ring_link = ""
    ring_scale = 1
    ring_ballsformat, ring_rings, ring_balls = [], [], []
    vek_mul = -1

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
        DISPLAY = (WIN_WIDTH, WIN_HEIGHT+PANEL)  # Группируем ширину и высоту в одну переменную
        # инициализация окна
        screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        win_caption = ring_name if ring_name != "" else "Hungarian Rings Simulator"
        pygame.display.set_caption(win_caption)  # Пишем в шапку

        # инициализация окна с подсказкой
        HELP = (WIN_WIDTH//3+BORDER, WIN_HEIGHT//3+BORDER)
        GAME = (WIN_WIDTH, WIN_HEIGHT)
        game_scr = Surface(GAME)

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
            timer.tick(10)

            fl_break = False
            mouse_x, mouse_y, mouse_left, mouse_right = 0,0,False,False

            events = pygame.event.get()
            for ev in events:  # Обрабатываем события
                if (ev.type == QUIT):
                    return SystemExit, "QUIT"
                if (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                    help = False if help else help
                if (ev.type == KEYDOWN and ev.key == K_F2):
                    BTN_CLICK = True
                    BTN_CLICK_STR = "reset"
                if ev.type == MOUSEBUTTONDOWN:
                    but = ev.button
                if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                    help = False if help else help

                    mouse_x = ev.pos[0]
                    mouse_y = ev.pos[1]
                    mouse_left = True
                if ev.type == MOUSEBUTTONDOWN and ev.button == 3:
                    help = False if help else help

                    mouse_x = ev.pos[0]
                    mouse_y = ev.pos[1]
                    mouse_right = True
                if ev.type == MOUSEBUTTONDOWN and ev.button == 5:
                    BTN_CLICK = True
                    BTN_CLICK_STR = "undo"

                ################################################################################
                # обработка нажатия на кнопки
                if BTN_CLICK:
                    if BTN_CLICK_STR=="reset" and not help:
                        if not file_ext:
                            fl_break = True
                        else:
                            fil = read_file(False)
                            if fil != "":
                                file_ext = True
                                ring_name, ring_link, ring_scale, ring_ballsformat, ring_rings, ring_balls, ball_radius, ball_offset, WIN_WIDTH, WIN_HEIGHT, vek_mul = fil
                                fl_break = True
                    if BTN_CLICK_STR=="open" and not help:
                        fl_break = False
                        fil = read_file(True)
                        if fil != "":
                            file_ext = True
                            ring_name,ring_link, ring_scale, ring_ballsformat,ring_rings,ring_balls, ball_radius,ball_offset, WIN_WIDTH,WIN_HEIGHT, vek_mul = fil
                            fl_break = True

                    if BTN_CLICK_STR=="info" and not help:
                        for link in ring_link:
                            if link!="":
                                webbrowser.open(link, new=2, autoraise=True)
                    if BTN_CLICK_STR=="help":
                        help = not help

                    if BTN_CLICK_STR=="scramble" and not help:
                        pass
                    if BTN_CLICK_STR=="undo" and not help:
                        pass

                    BTN_CLICK = False
                    BTN_CLICK_STR = ""
            if fl_break: break

            ################################################################################
            # обработка нажатия в игровом поле
            ring_num = vek = 0
            if mouse_x + mouse_y > 0 and not help:
                if mouse_x<WIN_WIDTH and mouse_y<WIN_HEIGHT:
                    ring_pos = []
                    for ring in ring_rings:
                        pos = check_circle(ring[1], ring[2], mouse_x, mouse_y, ring[3])
                        if pos[0]:
                            ring_pos.append( (ring[0], pos[1]) )
                    if len(ring_pos)>0: # есть внутри круга
                        rr = 9999
                        for ring in ring_pos:
                            if ring[1]<rr:
                                ring_num = ring[0]
                        vek = -1 if mouse_left else 1 if mouse_right else vek
                        vek = vek * vek_mul

            ################################################################################
            # логика игры - выполнение перемещений
            if ring_num>0:
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

                    break

            #####################################################################################
            # отрисовка игрового поля
            screen.fill(BACKGROUND_COLOR)  # Заливаем поверхность сплошным цветом
            game_scr.fill(Color(GRAY_COLOR))

            pf = Surface((WIN_WIDTH, 10))
            pf.fill(Color("#B88800"))
            screen.blit(pf, (0, WIN_HEIGHT)) # Рисуем разделительную черту

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
            # отрисовка колец
            for ring in ring_rings:
                draw.circle(game_scr,GRAY_COLOR2,(ring[1],ring[2]), ring[3]-ball_radius, 2)
                draw.circle(game_scr,GRAY_COLOR2,(ring[1],ring[2]), ring[3]+ball_radius+3, 2)

            # отрисовка шариков
            for ball in ring_balls:
                ball_x,ball_y = ball[2],ball[3]
                game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset), (ball_x-ball_radius, ball_y-ball_radius))

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
