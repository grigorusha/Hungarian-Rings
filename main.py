import pygame
from pygame import *

import pygame_widgets
from pygame_widgets.button import Button

import math
from math import sqrt,cos,sin,pi
from scipy.interpolate import CubicSpline

import random
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
                   [(50, 200, 250, 255), (0, 50, 50, 255)], [(0, 160, 160, 255), (0, 50, 50, 255)],        # 8 голубой 9 бирюзовый
                   [(190, 140, 140, 255), (50, 30, 30, 255)], [(250, 120, 190, 255), (70, 30, 50, 255)],   # 10 коричневый 11 розовый
                   [(200, 130, 250, 255), (50, 30, 70, 255)], [(0, 250, 0, 255), (0, 70, 00, 255)],        # 12 сиреневый 13 лайм
                   [(200, 200, 200, 255), (50, 50, 50, 255)] ]                                             # 14 серый

WIN_WIDTH, WIN_HEIGHT = 470, 300
PANEL = 33*3
BORDER = 20

filename = ""

BTN_CLICK = False
BTN_CLICK_STR = ""

def button_Button_click(button_str):
    global BTN_CLICK, BTN_CLICK_STR
    BTN_CLICK_STR = button_str
    BTN_CLICK = True

def typeof(your_var):
    if (isinstance(your_var, int)):
        return 'int'
    elif (isinstance(your_var, list)):
        return 'list'
    elif (isinstance(your_var, bool)):
        return 'bool'
    elif (isinstance(your_var, str)):
        return 'str'
    else:
        return "type is unknown"

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
    cos = round(x/rad,8)
    if -1 <= cos <= 1:
        angle = math.acos(round(cos,10))
        grad = angle*180/pi
        if y<0:
            grad = 360 - grad
            angle = 2*pi - angle
    else: angle = grad = 0
    return angle, round(grad,2)

def check_circle(center_x,center_y, x,y, rad):
    x,y = x-center_x,y-center_y
    length = sqrt(x*x+y*y)
    return (length<rad,length/rad)

def compare_xy(x,y,rr):
    return round(x,rr)==round(y,rr)

def init_ring():
    init = """
        Name: Golovolomka-8 (Головоломка-8) - 12+13
        Link: https://twistypuzzles.com/cgi-bin/puzzle.cgi?pkey=4395
        
        Scale: 3
        Speed: 3
        Flip: rotate
        
        # 1-circle, 0-not circle
        OrbitFormat: 1
        
        # ball radius, marker font size
        BallsFormat: 10.3, 10
        
        # Variables
        Param: pos_ball1, 40+20*sqrt(2) # 68.28427125
        Param: pos_ball2, 45+20*sqrt(2) # 73.28427125
        
        # ring number, center coordinates x y, radius, number of balls in the ring
        Ring: 1, 40,          45, 40,          12
        Ring: 2, 100.21061364,45, 42.65315156, 13
        
        # colors: 0 white, 1 black, 2 red, 3 green, 4 blue, 5 yellow, 6 purple
        # colors: 7 orange, 8 light blue, 9 teal, 10 brown, 11 pink, 12 lilac, 13 lime
        
        # ring number, ball number, ball center x y coordinates, color, marker, intersection flag
        Ball: 1,  1, pos_ball1, pos_ball2, 0, -, 1
        Ball: 1,  2, next_ring, 0, -, 0
        Ball: 1,  3, next_ring, 0, -, 0
        Ball: 1,  4, next_ring, 0, -, 1
        Ball: 1,  5, next_ring, 2, -, 0
        Ball: 1,  6, next_ring, 2, -, 0
        Ball: 1,  7, next_ring, 2, -, 0
        Ball: 1,  8, next_ring, 2, -, 0
        Ball: 1,  9, next_ring, 2, -, 0
        Ball: 1, 10, next_ring, 2, -, 0
        Ball: 1, 11, next_ring, 2, -, 0
        Ball: 1, 12, next_ring, 2, -, 0
        
        Ball: 2,  1, pos_ball1, pos_ball2, 0, -, 1
        Ball: 2,  2, next_ring, 4, -, 0
        Ball: 2,  3, next_ring, 4, -, 0
        Ball: 2,  4, next_ring, 4, -, 0
        Ball: 2,  5, next_ring, 4, -, 0
        Ball: 2,  6, next_ring, 4, -, 0
        Ball: 2,  7, next_ring, 4, -, 0
        Ball: 2,  8, next_ring, 4, -, 0
        Ball: 2,  9, next_ring, 4, -, 0
        Ball: 2, 10, next_ring, 4, -, 0
        Ball: 2, 11, next_ring, 0, -, 1
        Ball: 2, 12, next_ring, 0, -, 0
        Ball: 2, 13, next_ring, 0, -, 0
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

def centroid(input_x,input_y):
    x, y = 0, 0
    n = len(input_x)
    signed_area = 0
    for i in range(n):
        x0, y0 = input_x[i], input_y[i]
        x1, y1 = input_x[(i + 1) % n], input_y[(i + 1) % n]
        # shoelace formula
        area = (x0 * y1) - (x1 * y0)
        signed_area += area
        x += (x0 + x1) * area
        y += (y0 + y1) * area
    signed_area *= 0.5
    if signed_area!=0:
        x /= 6 * signed_area
        y /= 6 * signed_area
    return x, y

def get_ring_num(orbit_format, ring_rings, ring_lines, ring_num):
    if orbit_format==1:
        for ring in ring_rings:
            if ring[0]==ring_num:
                return ring, []
    else:
        for ring in ring_rings:
            if ring[0]==ring_num:
                return ring, []
        for line in ring_lines:
            if line[0]==ring_num:
                return [], line
    return [], []

def read_file(fl,init=""):
    global filename, BORDER, WIN_WIDTH, WIN_HEIGHT

    flip_y = flip_x = flip_rotate = False
    ring_name, ring_author, ring_scale, ring_speed, orbit_format = "", "", 1, 3, 1
    param_calc, ring_ballsformat, ring_rings, ring_lines, ring_balls, ring_link, solved_ring, orbit_mas = [], [], [], [], [], [], [], []

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
        elif command == "Author":
            ring_author = params
        elif command == "Link":
            ring_link.append(params)
        elif command == "Scale":
            ring_scale = float(params)
        elif command == "Speed":
            ring_speed = float(params)
        elif command == "OrbitFormat":
            orbit_format = int(params)
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
            for param in param_calc:
                if param_mas[1].find(param[0])!=-1:
                    param_mas[1] = param_mas[1].replace(param[0],str(param[1]))
            param_mas[1] = eval(param_mas[1])
            param_calc.append([param_mas[0], param_mas[1]])

        elif command == "Ring":
            if orbit_format==1:
                if len(param_mas) != 5: return ""
                param_mas[1],param_mas[2],param_mas[3] = calc_param(param_mas[1],param_calc), calc_param(param_mas[2],param_calc), calc_param(param_mas[3],param_calc)
                angle_sector = pi*2/int(param_mas[4])
                ring_rings.append( [ int(param_mas[0]),param_mas[1],param_mas[2],param_mas[3],int(param_mas[4]),angle_sector ] )
            else:
                if len(param_mas) != 7: return ""
                param_mas[2],param_mas[3],param_mas[4] = calc_param(param_mas[2],param_calc), calc_param(param_mas[3],param_calc), calc_param(param_mas[4],param_calc)
                ring_rings.append( [ int(param_mas[1]),param_mas[2],param_mas[3],param_mas[4],int(param_mas[5]),0,int(param_mas[0]),int(param_mas[6]) ] )

        elif command == "Line":
            if orbit_format != 1:
                if len(param_mas) != 4: return ""
                param_mas[2],param_mas[3] = calc_param(param_mas[2],param_calc), calc_param(param_mas[3],param_calc)
                ring_lines.append( [ int(param_mas[1]),param_mas[2],param_mas[3],0,0,int(param_mas[0]) ] )

        elif command == "Ball":
            if orbit_format==1:
                if len(param_mas)==7:
                    param_mas[2],param_mas[3],param_mas[0] = calc_param(param_mas[2],param_calc),calc_param(param_mas[3],param_calc),int(param_mas[0])
                    ring_balls.append( [ param_mas[0],int(param_mas[1]),param_mas[2],param_mas[3],int(param_mas[4]),param_mas[5],int(param_mas[6]),[] ] )
                elif len(param_mas) == 6 and (param_mas[2] == "next_ring"):
                    param_mas[0], param_mas[1] = int(param_mas[0]), int(param_mas[1])
                    ring_balls.append( [ param_mas[0], param_mas[1], param_mas[2], param_mas[2], int(param_mas[3]), param_mas[4], int(param_mas[5]), []])
                else: return ""
            else:
                if len(param_mas)==8:
                    param_mas[3],param_mas[4],param_mas[1] = calc_param(param_mas[3],param_calc),calc_param(param_mas[4],param_calc),int(param_mas[1])
                    ring_balls.append( [ param_mas[1],int(param_mas[2]),param_mas[3],param_mas[4],int(param_mas[5]),param_mas[6],int(param_mas[7]),[],int(param_mas[0]) ] )
                elif len(param_mas) == 7 and (param_mas[3] == "next_ring" or param_mas[3] == "next_line"):
                    param_mas[1], param_mas[2] = int(param_mas[1]), int(param_mas[2])
                    ring_balls.append( [ param_mas[1], param_mas[2], param_mas[3], param_mas[3], int(param_mas[4]), param_mas[5], int(param_mas[6]), [],int(param_mas[0]) ])
                else: return ""

    # заполним расчетные параметры
    angle, grad, num = 0, 0, 0
    for nn,ball in enumerate(ring_balls):
        ring_num = ball[0]
        ring, line = get_ring_num(orbit_format, ring_rings, ring_lines, ring_num)

        if typeof(ball[2])!="str":
            if len(ring)>0:
                angle,grad = calc_angle(ring[1],ring[2], ball[2],ball[3], ring[3])
            pos_x, pos_y = ball[2], ball[3]
            num = 0

        if ball[2] == "next_ring":
            num += 1
            angle_sector = ring[5]

            if angle_sector==0:
                kol, pos, fl_orbit = 1, nn, False
                while True:
                    pos += 1
                    kol += 1
                    if pos==len(ring_balls):
                        break
                    ball_next = ring_balls[pos]
                    if typeof(ball_next[2])!="str":
                        if ball[8] == ball_next[8]:
                            fl_orbit = True
                        break
                    if ball[0] != ball_next[0]:
                        break
                if not fl_orbit:
                    for ball_next in ring_balls:
                        if ball[8] == ball_next[8]:
                            break
                angle2, grad2 = calc_angle(ring[1],ring[2], ball_next[2],ball_next[3], ring[3])
                if angle2>angle:
                    angle_sector, grad_sector = abs((angle-angle2+2*pi)/kol), abs((grad-grad2+360)/kol)
                else:
                    angle_sector, grad_sector = abs((angle-angle2)/kol), abs((grad-grad2)/kol)
                ring[5] = angle_sector

            radius = ring[3]
            center_x, center_y = ring[1], ring[2]
            ang = angle - angle_sector * num
            angle_cos, angle_sin = cos(ang), sin(ang)
            xx, yy = angle_cos * radius + center_x, angle_sin * radius + center_y
            ball[2], ball[3] = xx,yy
        elif ball[2] == "next_line":
            num += 1
            angle_line = line[3]
            len_line = line[4]

            if angle_line == 0 and len_line == 0:
                kol, pos, fl_orbit = 1, nn, False
                while True:
                    pos += 1
                    kol += 1
                    if pos == len(ring_balls):
                        break
                    ball_next = ring_balls[pos]
                    if typeof(ball_next[2]) != "str":
                        if ball[8] == ball_next[8]:
                            fl_orbit = True
                        break
                    if ball[0] != ball_next[0]:
                        break
                if not fl_orbit:
                    for ball_next in ring_balls:
                        if ball[8] == ball_next[8]:
                            break
                len_line = sqrt( (pos_x-ball_next[2])**2+(pos_y-ball_next[3])**2 )
                angle_line, grad = calc_angle(pos_x,pos_y, ball_next[2], ball_next[3], len_line)
                len_line = len_line / kol
                line[3], line[4] = angle_line, len_line

            angle_cos, angle_sin = cos(angle_line), sin(angle_line)
            xx, yy = angle_cos * len_line * num + pos_x, angle_sin * len_line * num + pos_y
            ball[2], ball[3] = xx,yy

    # учтем масштаб
    if ring_scale != 1 and ring_scale != 0:
        ring_ballsformat[0] = ring_ballsformat[0]*ring_scale
        shift = ring_ballsformat[0]+BORDER
        for ring in ring_rings:
            ring[1] = ring[1] * ring_scale + shift
            ring[2] = ring[2] * ring_scale + shift
            ring[3] = ring[3] * ring_scale
        for line in ring_lines:
            line[1] = line[1] * ring_scale + shift
            line[2] = line[2] * ring_scale + shift
            line[4] = line[4] * ring_scale + shift
        for ball in ring_balls:
            ball[2] = ball[2] * ring_scale + shift
            ball[3] = ball[3] * ring_scale + shift

    ball_radius = ring_ballsformat[0]
    ball_offset = (-int(ball_radius / 3), -int(ball_radius / 3))

    # изменим размеры окна
    WIN_WIDTH, WIN_HEIGHT = 0, 0
    # if orbit_format == 1:
    for ring in ring_rings:
        if orbit_format == 0:
            if ring[7]==0: continue
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
        for line in ring_lines:
            line[1] = WIN_WIDTH - line[1]
        for ball in ring_balls:
            ball[2] = WIN_WIDTH - ball[2]
    if flip_y:
        vek_mul = -1 * vek_mul
        for ring in ring_rings:
            ring[2] = WIN_HEIGHT - ring[2]
        for line in ring_lines:
            line[2] = WIN_HEIGHT - line[2]
        for ball in ring_balls:
            ball[3] = WIN_HEIGHT - ball[3]
    if flip_rotate:
        vek_mul = -1 * vek_mul
        for ring in ring_rings:
            ring[1],ring[2] = ring[2],ring[1]
        for line in ring_lines:
            line[1],line[2] = line[2],line[1]
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
    for ball in ring_balls:
        if ball[6] == 0: continue
        for ball_sec in ring_balls:
            if ball == ball_sec: continue
            if ball_sec[6] == 0: continue
            if compare_xy(ball[2],ball_sec[2],2) and compare_xy(ball[3],ball_sec[3],2): # ball[2] == ball_sec[2] and ball[3] == ball_sec[3]
                if len(ball[7])==0:
                    ball[7].append( ball_sec[0] )  # номер перекрестного кольца, номер шарика в нем
                    ball[7].append( ball_sec[1] )
                    if orbit_format==0:
                        ball[7].append(ball_sec[8]) # номер орбиты
                if len(ball_sec[7])==0:
                    ball_sec[7].append( ball[0] )
                    ball_sec[7].append( ball[1] )
                    if orbit_format == 0:
                        ball_sec[7].append(ball[8])
                ball_sec[4], ball_sec[5] = ball[4], ball[5]

    ###########################################################################
    # построение орбит
    orbit_mas = []
    if orbit_format==0:
        orbit_kol = 0
        for ring in ring_rings:
            if ring[6]>orbit_kol:
                orbit_kol = ring[6]
        for line in ring_lines:
            if line[5]>orbit_kol:
                orbit_kol = line[5]

        for nom in range(1,orbit_kol+1):
            input_x, input_y, = [], []
            for ball in ring_balls:
                if ball[8]==nom:
                    input_x.append(ball[2])
                    input_y.append(ball[3])
            input_x.append(input_x[0])
            input_y.append(input_y[0])

            xx,yy = centroid(input_x, input_y)

            step = len(input_x)
            theta, pos = [], []
            for nn in range(0, step):
                angle, grad = nn*(2*pi/step), nn*(360/step)
                theta.append(angle)
                pos.append([input_x[nn], input_y[nn]])
            cs = CubicSpline(theta, pos, bc_type='periodic')

            input_x.pop()
            input_y.pop()
            orbit_mas.append( [ nom,step-1, [xx,yy], [input_x, input_y], cs ] )

    solved_ring = copy.deepcopy(ring_balls)

    return ring_name,ring_author, ring_link, ring_scale,ring_speed, orbit_format, orbit_mas, ring_ballsformat,ring_rings,ring_lines,ring_balls, ball_radius,ball_offset, solved_ring, WIN_WIDTH,WIN_HEIGHT, vek_mul

def main():
    global BTN_CLICK,BTN_CLICK_STR, WIN_WIDTH,WIN_HEIGHT, BORDER, filename

    file_ext = False

    ball_radius = 100 # ring_ballsformat[0]
    offset = (-int(ball_radius / 3), -int(ball_radius / 3))

    ring_name = ring_author = ring_link = ""
    ring_scale, ring_speed, orbit_format = 1, 3, 1
    ring_ballsformat, ring_rings, ring_lines, ring_balls, orbit_mas = [], [], [], [], []
    vek_mul = -1
    solved_ring = []
    fl_reset = False

    # основная инициализация
    random.seed()
    pygame.init()  # Инициация PyGame
    font = pygame.font.SysFont('Verdana', 18)
    font2 = pygame.font.SysFont('Verdana', 12)
    font_button = pygame.font.SysFont("ArialB",18)
    timer = pygame.time.Clock()
    Tk().withdraw()

    icon = os.path.abspath(os.curdir) + "\\Hungarian Rings.ico"
    if os.path.isfile(icon):
        pygame.display.set_icon(pygame.image.load(icon))

    ################################################################################
    ################################################################################
    # перезапуск программы при смене параметров
    while True:
        if not file_ext:
            fil = init_ring()
            ring_name, ring_author, ring_link, ring_scale, ring_speed, orbit_format, orbit_mas, ring_ballsformat, ring_rings, ring_lines, ring_balls, ball_radius, ball_offset, solved_ring, WIN_WIDTH, WIN_HEIGHT, vek_mul = fil

        DISPLAY = (WIN_WIDTH, WIN_HEIGHT+PANEL)  # Группируем ширину и высоту в одну переменную
        HELP = (WIN_WIDTH//3, WIN_HEIGHT//3)
        GAME = (WIN_WIDTH, WIN_HEIGHT)
        # инициализация окна

        if not fl_reset:
            screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
            game_scr = Surface(GAME)
        win_caption = ring_name if ring_name != "" else "Hungarian Rings Simulator"
        if ring_author != "":
            win_caption += " ("+ring_author.strip()+")"
        pygame.display.set_caption(win_caption)  # Пишем в шапку
        font_marker = pygame.font.SysFont('Verdana', ring_ballsformat[1])

        scramble_move = scramble_move_all = scramble_move_first = ring_num_pred = kol_step = 0
        moves_stack = []
        moves = 0
        solved = True

        mouse_xx, mouse_yy = 0, 0

        help = False
        help_gen = True

        # инициализация кнопок
        if True:
            button_y1 = WIN_HEIGHT + 20
            button_Reset = Button(screen, 10, button_y1, 45, 20, text='Reset', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=GREEN_COLOR, hoverColour=GREEN_COLOR, pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("reset"))
            button_Scramble = Button(screen, button_Reset.textRect.right+10, button_y1, 70, 20, text='Scramble', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=GREEN_COLOR, hoverColour=GREEN_COLOR, pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("scramble"))
            button_Undo = Button(screen, button_Scramble.textRect.right+10, button_y1, 40, 20, text='Undo', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=GREEN_COLOR, hoverColour=GREEN_COLOR, pressedColour=(0, 200, 20),
                            onClick = lambda: button_Button_click("undo"))

            button_Info = Button(screen, button_Undo.textRect.right+20, button_y1, 100, 20, text='Puzzle Photo ->', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=BLUE_COLOR, hoverColour=BLUE_COLOR, pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("info"))
            button_About = Button(screen, button_Info.textRect.right+10, button_y1, 60, 20, text='About ->', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=BLUE_COLOR, hoverColour=BLUE_COLOR, pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("about"))

            button_y2 = button_y1 + 25
            button_Open = Button(screen, 10, button_y2, 45, 20, text='Open', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=GREEN_COLOR, hoverColour=GREEN_COLOR, pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("open"))

            button_Help = Button(screen, button_Open.textRect.right+10, button_y2, 80, 20, text='Solved State', fontSize=20, font=font_button, margin=5, radius=3,
                            inactiveColour=GREEN_COLOR, hoverColour=GREEN_COLOR, pressedColour=(0, 200, 20),
                            onClick=lambda: button_Button_click("help"))

            button_y3 = button_y2 + 30
        button_set = [button_Reset, button_Scramble, button_Undo, button_Open, button_Info, button_Help, button_About]

        ################################################################################
        ################################################################################
        # Основной цикл программы
        while True:
            undo = False
            mouse_x, mouse_y, mouse_left, mouse_right, ring_move = 0, 0, False, False, 0
            if kol_step==0:
                ring_num = vek = orbit_num = 0

            if scramble_move == 0:
                timer.tick(10)

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
                    if (ev.type == KEYDOWN and ev.key == K_F4):
                        BTN_CLICK = True
                        BTN_CLICK_STR = "scramble"

                    if BTN_CLICK_STR=="info" and not help:
                        for link in ring_link:
                            if link!="":
                                webbrowser.open(link, new=2, autoraise=True)
                    if BTN_CLICK_STR=="about" and not help:
                        webbrowser.open("https://github.com/grigorusha/Hungarian-Rings", new=2, autoraise=True)
                        webbrowser.open("https://twistypuzzles.com/forum/viewtopic.php?p=422931#p422931", new=2, autoraise=True)
                    if BTN_CLICK_STR=="help":
                        help = not help

                    if ev.type == MOUSEMOTION:
                        mouse_xx = ev.pos[0]
                        mouse_yy = ev.pos[1]

                    if (ev.type == KEYDOWN and ev.key == K_SPACE):
                        BTN_CLICK = True
                        BTN_CLICK_STR = "undo"
                    if ev.type == MOUSEBUTTONDOWN and (ev.button == 2 or ev.button == 6 or ev.button == 7):
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

                    ################################################################################
                    # обработка нажатия на кнопки
                    if BTN_CLICK:
                        if BTN_CLICK_STR=="reset" and not help:
                            if not file_ext:
                                fl_break = fl_reset = True
                            else:
                                fil = read_file("reset")
                                if fil != "":
                                    ring_name, ring_author, ring_link, ring_scale, ring_speed, orbit_format, orbit_mas, ring_ballsformat, ring_rings, ring_lines, ring_balls, ball_radius, ball_offset, solved_ring, WIN_WIDTH, WIN_HEIGHT, vek_mul = fil
                                    fl_break = file_ext = fl_reset = True
                        if BTN_CLICK_STR=="open" and not help:
                            fl_break = False
                            fil = read_file("open")
                            if fil != "":
                                file_ext = fl_break = True
                                ring_name,ring_author,ring_link, ring_scale, ring_speed, orbit_format, orbit_mas, ring_ballsformat, ring_rings, ring_lines, ring_balls, ball_radius,ball_offset, solved_ring, WIN_WIDTH,WIN_HEIGHT, vek_mul = fil
                                fl_reset = False

                        if BTN_CLICK_STR=="scramble" and not help:
                            fl_break = False

                            pos = ball_kol = 0
                            if orbit_format == 1:
                                for ring in ring_rings:
                                    if ring[0]>pos:
                                        pos += 1
                                        ball_kol += ring[4]
                            else:
                                for orbit in orbit_mas:
                                    if orbit[0]>pos:
                                        pos += 1
                                        ball_kol += orbit[1]
                            scramble_move = ball_kol * 15
                            mul = 2 if ball_kol<100 else 1
                            scramble_move_all = scramble_move_first = ball_kol * mul
                            ring_num_pred = kol_step = 0

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
                # обработка перемещения и нажатия в игровом поле
                if mouse_xx + mouse_yy > 0 and not help:
                    if mouse_xx<WIN_WIDTH and mouse_yy<WIN_HEIGHT:
                        ring_pos = []
                        for ring in ring_rings:
                            if orbit_format == 0:
                                if ring[7] == 0: continue
                            pos = check_circle(ring[1], ring[2], mouse_xx, mouse_yy, ring[3]+ball_radius)
                            if pos[0]:
                                if orbit_format==1:
                                    ring_pos.append( (ring[0], pos[1]) )
                                else:
                                    ring_pos.append((ring[0], pos[1], ring[6]))
                        if len(ring_pos)>0: # есть внутри круга
                            rr = 999999
                            for ring_info in ring_pos:
                                if ring_info[1]<rr:
                                    rr = ring_info[1]
                                    ring_move = ring_info[0]
                                    if orbit_format != 1:
                                        orbit_num = ring_info[2]
                            if mouse_x + mouse_y > 0: # есть клик
                                vek = -1 if mouse_left else 1 if mouse_right else vek
                                vek = vek * vek_mul
                                ring_num = ring_move

            else:
                ################################################################################
                # обработка рандома для Скрамбла
                if kol_step>0:
                    kol_step -= 1
                else:
                    vek = random.choice([-1,1])
                    while True:
                        ring_num = random.randint(1, len(ring_rings))
                        kol_step = random.randint(1, ring_rings[ring_num-1][4]//2)
                        if orbit_format != 1:
                            orbit_num = ring_rings[ring_num-1][6]
                        if ring_num_pred != ring_num:
                            ring_num_pred = ring_num
                            break

            ################################################################################
            # логика игры - выполнение перемещений
            if ring_num>0:

                # анимация
                if (scramble_move==0 or scramble_move_first>0):
                    if scramble_move_all != 0:
                        scramble_move_first -= 1
                        if (scramble_move_first<(3*scramble_move_all//10)):
                            speed_mul = 9
                        elif (scramble_move_first<(5*scramble_move_all//10)):
                            speed_mul = 7
                        elif (scramble_move_first<(8*scramble_move_all//10)):
                            speed_mul = 5
                        else:
                            speed_mul = 3
                    else:
                        speed_mul = 1

                    if orbit_format==1:
                        angle_sector = ring_rings[ring_num - 1][5]
                        radius = ring_rings[ring_num - 1][3]
                        step = ball_radius*2
                        step = step / (ring_speed*speed_mul)

                        for count in range(int(step)):
                            timer.tick(300)
                            events = pygame.event.get()
                            game_scr.fill(Color(GRAY_COLOR))

                            for ring in ring_rings:
                                draw.circle(game_scr, GRAY_COLOR2, (ring[1], ring[2]), ring[3] - ball_radius, 1)
                                if ring[0] == ring_move:
                                    draw.circle(game_scr, WHITE_COLOR, (ring[1], ring[2]), ring[3] + ball_radius + 3, 3)
                                else:
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
                                    angle_cos, angle_sin = cos(ang), sin(ang)
                                    xx, yy = angle_cos * radius + center_x, angle_sin * radius + center_y
                                    game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset), (xx-ball_radius, yy-ball_radius))
                                    print_marker(game_scr, font_marker, ball[5], xx, yy, ball[4])

                            screen.blit(game_scr, (0, 0))
                            pygame_widgets.update(events)
                            pygame.display.update()

                    else:
                        step = ball_radius*2
                        step = step / (ring_speed*speed_mul)

                        for count in range(1,int(step)):
                            timer.tick(300)
                            events = pygame.event.get()
                            game_scr.fill(Color(GRAY_COLOR))

                            for ring in ring_rings:
                                if ring[7] == 0: continue
                                draw.circle(game_scr, GRAY_COLOR2, (ring[1], ring[2]), ring[3] - ball_radius, 1)
                                if ring[0] == ring_move:
                                    draw.circle(game_scr, WHITE_COLOR, (ring[1], ring[2]), ring[3] + ball_radius + 3, 3)
                                else:
                                    draw.circle(game_scr, GRAY_COLOR2, (ring[1], ring[2]), ring[3] + ball_radius + 3, 2)
                            for ball in ring_balls:
                                ball_x,ball_y = ball[2],ball[3]
                                if ball[8]!=orbit_num:
                                    if ball[6]==0:
                                        game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset),(ball_x - ball_radius, ball_y - ball_radius))
                                        print_marker(game_scr, font_marker, ball[5], ball_x, ball_y, ball[4])
                                    elif len(ball[7])==3 and ball[7][2]!=orbit_num:
                                        game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset),(ball_x - ball_radius, ball_y - ball_radius))
                                        print_marker(game_scr, font_marker, ball[5], ball_x, ball_y, ball[4])
                                else:
                                    # if ball[1]!=4: continue

                                    orbit_len = orbit_mas[ball[8]-1][1]
                                    for pos in range(orbit_len):
                                        if orbit_mas[ball[8]-1][3][0][pos]==ball_x and orbit_mas[ball[8]-1][3][1][pos]==ball_y:
                                            break
                                    orbit_len += 1
                                    cs = orbit_mas[ball[8]-1][4]
                                    angle, grad = pos*(2*pi/orbit_len), pos*(360/orbit_len)
                                    angle_step = (2*pi/orbit_len)*(count/int(step))
                                    xx = cs(angle+vek*vek_mul*angle_step)[0]
                                    yy = cs(angle+vek*vek_mul*angle_step)[1]
                                    game_scr.blit(gradient_circle(ball_radius, GRADIENT_COLOR[ball[4]], True, 1, offset=ball_offset),(xx - ball_radius, yy - ball_radius))
                                    print_marker(game_scr, font_marker, ball[5], xx, yy, ball[4])

                            screen.blit(game_scr, (0, 0))
                            pygame_widgets.update(events)
                            pygame.display.update()

                #############################################################################
                # перемещение
                for ring in ring_rings:
                    if ring[0]==ring_num:
                        ball_kol = ring[4]
                        break
                for nn,ball in enumerate(ring_balls):
                    if orbit_format == 1:
                        if ball[0] != ring_num: continue
                    else:
                        if ball[8] != orbit_num: continue

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
                                if ball_next[6]==1:
                                    if ball_next[0] == ball[7][0] and ball_next[1] == ball[7][1]:
                                        ball_next[4], ball_next[5] = ball[4], ball[5]

                    if not undo:
                        moves += 1
                        moves_stack.append([ring_num, vek])
                    break

            # скрамбл
            if scramble_move != 0:
                scramble_move -= 1
                if scramble_move == 0:
                    moves_stack = []
                    moves = ring_num = vek = scramble_move_all = kol_step = 0
                continue # отрисовка не нужна

            # проверка на решенное состояние
            solved = True
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
            text_moves_place = text_moves.get_rect(topleft=(button_Help.textRect.right + 18, button_y2-3))
            screen.blit(text_moves, text_moves_place) # Пишем количество перемещений
            if solved:
                text_solved = font.render('Solved', True, WHITE_COLOR)
            else:
                text_solved = font.render('not solved', True, RED_COLOR)
            text_solved_place = text_solved.get_rect(topleft=(text_moves_place.right + 10, button_y2-3))
            screen.blit(text_solved, text_solved_place) # Пишем статус
            text_info = font2.render('Use: mouse wheel - ring rotate, space button - undo', True, GREEN_COLOR)
            text_info_place = text_solved.get_rect(topleft=(10, button_y3-3))
            screen.blit(text_info, text_info_place)

            ############################################
            game_scr.fill(Color(GRAY_COLOR))
            # отрисовка контуров
            # if orbit_format==1:
            for ring in ring_rings:
                if orbit_format==0:
                    if ring[7]==0: continue
                draw.circle(game_scr,GRAY_COLOR2,(ring[1],ring[2]), ring[3]-ball_radius, 1)
                if ring[0]==ring_move:
                    draw.circle(game_scr, WHITE_COLOR, (ring[1], ring[2]), ring[3] + ball_radius + 3, 3)
                else:
                    draw.circle(game_scr,GRAY_COLOR2,(ring[1],ring[2]), ring[3]+ball_radius+3, 2)
            # else:
            #     for orbit in orbit_mas:
            #         orbit_len = orbit[1]
            #         cen_x,cen_y = orbit[2]
            #         cs = orbit[4]
            #         mul = 20
            #         for nn in range(0, orbit_len * mul):
            #             angle = 2 * math.pi * nn / (orbit_len * mul)
            #             angle2 = 2 * math.pi * (nn+1) / (orbit_len * mul)
            #             xx,yy,xx2,yy2, = cs(angle)[0],cs(angle)[1],cs(angle2)[0],cs(angle2)[1]
            #             draw.line(game_scr, GRAY_COLOR2, (xx, yy), (xx2, yy2), 2)
                        # dx,dy,dx2,dy2 = xx-cen_x, yy-cen_y,xx2-cen_x, yy2-cen_y
                        # rad,rad2 = sqrt(dx**2+dy**2),sqrt(dx2**2+dy2**2)
                        # xx_,yy_,xx2_,yy2_ = xx*(rad+ball_radius)/rad,yy*(rad+ball_radius)/rad,xx2*(rad2+ball_radius)/rad2,yy2*(rad2+ball_radius)/rad2
                        # draw.line(game_scr, GRAY_COLOR2, (xx_, yy_), (xx2_, yy2_), 3)

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
            if help:
                screen.blit(help_screen, (GAME[0]-HELP[0]-BORDER//3,BORDER//3))
                draw.rect(screen, Color("#B88800"), (GAME[0]-HELP[0]-2*(BORDER//3), 0, HELP[0]+2*(BORDER//3), HELP[1]+2*(BORDER//3)), BORDER // 3)

            #####################################################################################
            pygame_widgets.update(events)
            pygame.display.update()  # обновление и вывод всех изменений на экран

        # удаляем кнопки
        for btn in button_set:
            btn.hide()

main()
