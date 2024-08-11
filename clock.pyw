import pygame
import random
from datetime import datetime
import math
import pyautogui
import time

def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000:
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000

    tmp_internal = colour_temperature / 100.0

    # red
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red

    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green

    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue

    return red, green, blue

subsec=False

#clockColor=(255,255,240)
#print(math.sin(float(str(datetime.now()).split(":")[2].split(".")[0])))
clockColor=(207, 185, 145)#(255, 234, 141)#(255, 119, 0)#convert_K_to_RGB(2800)
kearning=20
colonKerning=200
scrollindex = 0

display_width=round(3840 / 2)
display_height=math.floor(display_width * 9 / 16)

seven_slant=40#math.floor(70 * display_height / 3840)
seven_ratio=1/7
seven_len=math.floor(400 * display_height / 3840)
dis_width=math.floor(350 * display_height / 3840)
spacess=math.floor(10 * display_height / 3840)

side_space=math.floor(14 * display_height / 3840)
dis_height=2*seven_len+spacess
funny_height=math.floor(30 * display_height / 3840)
seven_dimension= (display_height, display_width)

pygame.init()
pygame.mouse.set_visible(False)
pygame.mouse.get_rel()

if subsec:
    kearning*=0.5
    colonKerning*=0.5
    seven_slant*=0.5
    seven_ratio=1/10
    seven_len*=0.5
    dis_width*=0.5
    spacess*=0.5
    side_space*=0.5
    dis_height*=0.5
    funny_height*=0.5
    seven_dimension= (display_height, display_width)

clockSurface = pygame.Surface((display_width,display_height))

clock=pygame.time.Clock()

mainDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)

def top(s):
    wacky_coefficient=round(seven_slant*seven_ratio)
    ofx=2*(seven_slant)+seven_len*seven_ratio+seven_slant*spacess/seven_len-wacky_coefficient

    ofy=0


    #print(wacky_coefficient)
    points=[(ofx+side_space,ofy+seven_len*seven_ratio),(ofx+dis_width-seven_len*seven_ratio-side_space,ofy+seven_len*seven_ratio),(ofx+wacky_coefficient+dis_width-seven_len*seven_ratio-side_space,ofy),(ofx+side_space+wacky_coefficient,ofy)]  ##tr
    pygame.draw.polygon(s,clockColor,points)
def bottom(s):
    ofx=seven_len*seven_ratio
    ofy=seven_len*2-ofx+spacess #+ 2*spacess# + funny_height/2

    wacky_coefficient=round(seven_slant*seven_ratio)
    #print(wacky_coefficient)
    points=[(ofx+side_space,ofy+seven_len*seven_ratio),(ofx+dis_width-seven_len*seven_ratio-side_space,ofy+seven_len*seven_ratio),(ofx+wacky_coefficient+dis_width-seven_len*seven_ratio-side_space,ofy),(ofx+side_space+wacky_coefficient,ofy)]  ##tr
    pygame.draw.polygon(s,clockColor,points)
def tr(s):
    ofx=dis_width+seven_slant+seven_slant*spacess/seven_len
    ofy=15+15
    points=[(ofx,0+seven_len),(ofx+round(seven_len*seven_ratio),0+seven_len),(ofx+round(seven_len*seven_ratio)+seven_slant,0),(ofx+seven_slant,0)]  ##tr
    pygame.draw.polygon(s,clockColor,points)
def tl(s):
    ofx=seven_slant+seven_slant*spacess/seven_len
    ofy=15+15
    points=[(ofx,0+seven_len),(ofx+round(seven_len*seven_ratio),0+seven_len),(ofx+round(seven_len*seven_ratio)+seven_slant,0),(ofx+seven_slant,0)]  ##tr
    pygame.draw.polygon(s,clockColor,points)
def mid(s):

    funny_height=seven_len*seven_ratio
    wacky_coefficient=round(seven_slant*funny_height/seven_len)

    funny_height=seven_len*seven_ratio
    ofx=seven_slant+seven_len*seven_ratio+seven_slant*spacess/2/seven_len-wacky_coefficient/2
    ofy=seven_len-(funny_height/2)+spacess/2

        #print(wacky_coefficient)
    points=[(ofx+side_space,ofy+seven_len*seven_ratio),(ofx+dis_width-seven_len*seven_ratio-side_space,ofy+seven_len*seven_ratio),(ofx+wacky_coefficient+dis_width-seven_len*seven_ratio-side_space,ofy),(ofx+side_space+wacky_coefficient,ofy)]  ##tr
    pygame.draw.polygon(s,clockColor,points)
def br(s):
    ofx=dis_width#+seven_len*seven_ratio#+2*side_space
    ofy=seven_len+spacess
    points=[(ofx,ofy+seven_len),(ofx+round(seven_len*seven_ratio),ofy+seven_len),(ofx+round(seven_len*seven_ratio)+seven_slant,ofy),(ofx+seven_slant,ofy)] ##br
    pygame.draw.polygon(s,clockColor,points)
def bl(s):
    ofx=0
    ofy=seven_len+spacess
    points=[(ofx,ofy+seven_len),(ofx+round(seven_len*seven_ratio),ofy+seven_len),(ofx+round(seven_len*seven_ratio)+seven_slant,ofy),(ofx+seven_slant,ofy)]  ##bl
    pygame.draw.polygon(s,clockColor,points)

def msgcScroll(x,y, message):
    x -= (dis_width + 2 * kearning) * len(message) / 2
    for i in message:
        seven_seg(x,y,i)
        x += dis_width + 2 * kearning
        #print(i)


def clockGenerate(z,h,w):
    tm = "test message         "

    clockSurface.fill((0,0,0))
    t=datetime.now()
    d,t=str(t).split()
    t,m=t.split(".")
    m=m[0:2]
    scrollindex = m[-1]

    t=t.split(":")
    if int(t[0])>12:
        t[0]=int(t[0])-12
        t[0]=str(t[0])
    if len(t[0]) < 2:
        t[0]="0"+t[0]
        #print(t[0])
    tl=""
    g=[]
    for i in t:
        tl+=i
    tl+=str(m)
    g=[char for char in tl]
    for i in range(len(g)):
        g[i]=int(g[i])
    tm2 = ""
        #g[i]=chr(i+96)
    #print(g,end="\r")
    ox=display_width-6*(dis_width+kearning+colonKerning/2)
    ox*=0.5
    oy=display_height/2-dis_height/2
    if subsec:
        ox=display_width-8*(dis_width+kearning+colonKerning/2)-1000
        ox*=0.5

    p0=ox+2*(dis_width+side_space+seven_len*seven_ratio+kearning)
    points=[(p0,oy),(p0+seven_ratio*seven_len,oy),(p0+seven_ratio*seven_len,oy+seven_ratio*seven_len),(p0,oy+seven_ratio*seven_len)]

    seven_seg(ox,oy,g[0])
    seven_seg(ox+(dis_width+side_space+seven_len*seven_ratio+kearning),oy,g[1])

    #pygame.draw.polygon(clockSurface,(50,50,50),points)

    seven_seg(ox+2*(dis_width+side_space+seven_len*seven_ratio+kearning)+colonKerning,oy,g[2])
    seven_seg(ox+3*(dis_width+side_space+seven_len*seven_ratio+kearning)+colonKerning,oy,g[3])
    seven_seg(ox+4*(dis_width+side_space+seven_len*seven_ratio+kearning)+2*colonKerning,oy,g[4])
    seven_seg(ox+5*(dis_width+side_space+seven_len*seven_ratio+kearning)+2*colonKerning,oy,g[5])
    if subsec:
        seven_seg(ox+6*(dis_width+side_space+seven_len*seven_ratio+kearning)+3*colonKerning,oy,g[6])
        seven_seg(ox+7*(dis_width+side_space+seven_len*seven_ratio+kearning)+3*colonKerning,oy,g[7])
    #print("day: " + d,"time: "+t)
    #msgcScroll(display_width/2,1000,tm2)
def seven_seg(x,y,n):






    seven_surface = pygame.Surface(seven_dimension)

    seven_surface.fill(pygame.Color(0,0,0))
    if n == 1:
        br(seven_surface)
        tr(seven_surface)
    if n==2:
        bl(seven_surface)
        tr(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if n==3:
        top(seven_surface)
        mid(seven_surface)
        bottom(seven_surface)
        tr(seven_surface)
        br(seven_surface)
    if n==4:
        mid(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
    if n==5:
        br(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if n==6:
        bl(seven_surface)
        br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if n==7:
        br(seven_surface)
        tr(seven_surface)
        top(seven_surface)
    if n==8:
        bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if n==9:
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if n==0:
        bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)



    if str(n).lower() == "a":
        bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        #bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "c":
        bl(seven_surface)
        #br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "d":
        bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        #tl(seven_surface)
        #top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "e":
        tl(seven_surface)
        bl(seven_surface)
        top(seven_surface)
        mid(seven_surface)
        bottom(seven_surface)
    if str(n).lower() == "f":
        bl(seven_surface)
        #br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        #bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "g":
        #bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "h":
        bl(seven_surface)
        br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        #top(seven_surface)
        #bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "i":
        #bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        #tl(seven_surface)
        #top(seven_surface)
        #bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "j":
        bl(seven_surface)
        br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        #top(seven_surface)
        bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "l":
        bl(seven_surface)
        #br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        #top(seven_surface)
        bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "o":
        bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "p":
        bl(seven_surface)
        #br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        #bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "r":
        bl(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "s":
        #bl(seven_surface)
        br(seven_surface)
        #tr(seven_surface)
        tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "t":
        #bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        #tl(seven_surface)
        top(seven_surface)
        #bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "u":
        bl(seven_surface)
        br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        #top(seven_surface)
        bottom(seven_surface)
        #mid(seven_surface)
    if str(n).lower() == "y":
        bl(seven_surface)
        #br(seven_surface)
        tr(seven_surface)
        tl(seven_surface)
        #top(seven_surface)
        #bottom(seven_surface)
        mid(seven_surface)
    if str(n).lower() == "z":
        bl(seven_surface)
        #br(seven_surface)
        tr(seven_surface)
        #tl(seven_surface)
        top(seven_surface)
        bottom(seven_surface)
        mid(seven_surface)





    seven_surface.set_colorkey((0,0,0))
    pygame.Surface.blit(clockSurface,seven_surface,(x,y))

z=0
r=255
g=187
b=78


r,g,b=255,255,200
w, h = pygame.display.get_surface().get_size()
d2=0
while True:
    #print()
    #clockColor = convert_K_to_RGB(3000+ 1200 * math.sin(0.1 * float(str(datetime.now()).split(":")[2].split(".")[0])))
    x,y = pygame.mouse.get_rel()
    if abs(x + y) > 0:
        quit()
    dt=str(datetime.now()).split(":")[2].split(".")[0]
    if False:#dt !=d2 :
        a=random.randint(0,2)
        if a<1:
            r=random.randint(0,255)
        elif a>1:
            g=random.randint(0,255)
        else:
            b=random.randint(0,255)
        d2=dt
        #r=random.randint(0,255)
        #g=random.randint(0,255)
        #b=random.randint(0,255)
        clockColor=(r,g,b)
    w, h = pygame.display.get_surface().get_size()
    #print(w,h)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            quit()
    #time.sleep(0.05)
    clockGenerate(z,h,w)
    #seven_seg(100,100,k)
    time.sleep(0.1)
    #colors=random.randint(0,100)
    #clockSurface.fill((0,0,0))






    pygame.Surface.blit(mainDisplay,clockSurface,(0,0))
    pygame.display.update()
    #break
#clock.show()
