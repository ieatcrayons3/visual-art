#### g code py

import math
import os
import vectormath as vmath
import pygame
from random import randint
import numpy as np
import cv2

#from letters import *

path="////////" #save path of gcode
path2="/////////" #removable drive path
name="_handwriting" #file ending (used TXT writing source file name as prefix)
ext=".gcode" #file suffix
renderscale=3
wed=2

kerning=0.45
spacing=0.1
line_spacing=1.25
point=1
letter_height=1
letter_width=1
page_margins=10
handwritten=True
extremity=0.25


writeheight=3.8
upheight=writeheight+0.8
feedrate=3000
rapid=3000

#units are in MM
saftey_margins = 10
zmargin=100


MINX=0+saftey_margins
MINY=0+saftey_margins
MINZ=0.2
MAXX=220-saftey_margins
MAXY=220-saftey_margins
MAXZ=250-zmargin

right_page_edge=191.9
left_page_edge=14.2

left_margin=left_page_edge+page_margins
right_margin=right_page_edge-page_margins

offset=vmath.Vector2(left_margin+0.1,MAXY-(letter_height*point)-line_spacing-saftey_margins-0.1)

operations=[]
ops_num=0
output=""
running=vmath.Vector2(0,0)
toobig=False
#print(running)

def image(target,scale):

    img = cv2.imread(target, cv2.IMREAD_GRAYSCALE)

    # Initialize output
    out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Median blurring to get rid of the noise; invert image
    img = 255 - cv2.medianBlur(img, 3)
    edges = cv2.Canny(img, 20, 30)
    #cv2.imshow(edges)
    # Detect and draw lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength=2, maxLineGap=1)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(out, (x1, y1), (x2, y2), (0, 0, 255), 1)
            mov(x1*scale+MINX,y1*scale+MINY,0)
            mov(x2*scale+MINX,y2*scale+MINY)
    cv2.imshow('out',out)







def display(words):
    return 0
    operation = "M117 " + str(words)
    operations.append(operation)

def mov(x,y,p=1):
    global running
    global toobig
    global handwritten
    global extremity
    if handwritten:
        x+=extremity*(randint(0,1)-0.5)*(1+randint(0,1000)/10000000)
        y+=extremity*(randint(0,1)-0.5)*(1+randint(0,1000)/10000000)
    if p == 1:
        operations.append("G1 Z" + str(writeheight) +  " F3000")
        operations.append("G1 F"+ str(feedrate))
    else:

        operations.append("G1 Z" + str(upheight) +  " F3000")
        operations.append("G1 F3000")
        running=(x,MAXY-y)


    pygame.draw.line(lineSurface,(255,255,255),(running[0]*renderscale,running[1]*renderscale),(x*renderscale,(MAXY-y)*renderscale),width=wed)
    #toobig=True
    if x > MAXX:
        print("\n\nX value exceeded")
        quit(-1)
    elif x < MINX:
        print("\n\nX value too low")
        quit(-1)
    elif y > MAXY:
        print("\n\nY value exceeded")
        quit(-1)
    elif y < MINY:
        print("\n\nY value too low")
        toobig=True
        #quit(-1)
        pass
    #print('mov')
    else:

        operation = "G1 X" + str(x) + " Y" + str(y)
        operations.append(operation)
    running=(x,MAXY-y)
    #return run

def arc_to_arc(x,y,d,r,sr,cw=0):


    if r==4:
        x2=0
        y2=0.5
    if r==1:
        x2=0.5
        y2=1
    if r==3:
        y2=0
        x2=0.5
    if r==2:
        x2=1
        y2=0.5


    return 0
def Cmov(x2,y2,d,p=1):
    if p == 1:
        operations.append("G1 Z" + str(writeheight) +  " F3000")
        operations.append("G1 F"+ str(feedrate))
    else:
        operations.append("G1 Z" + str(upheight) +  " F3000")
        operations.append("G1 F3000")

    if x > MAXX:
        print("\n\nX value exceeded")
        quit(-1)
    if x < MINX:
        print("\n\nX value too low")
        quit(-1)
    if y > MAXY:
        print("\n\nY value exceeded")
        quit(-1)
    if y < MINY:
        print("\n\nY value too low")
        quit(-1)


    operation = "G1 X" + str(x) + " Y" + str(y)
    operations.append(operation)

def start(feedrate):

    operation = "G21 ;metric values\nG90 ;absolute positioning\nM82 ;set extruder to absolute mode\nM107 ;start with the fan off\nG28 X0 Y0 ;move X/Y to min endstops\nG28 Z0 ;move Z to min endstops\nG1 Z15.0 F3000 ;move the extruder up 15mm" #\nM117 Homing X/Y ...
    operations.append(operation)
    operation="G1 F" + str(feedrate)

def sum(out=output):
    global ops_num
    ops_num=len(operations)
    for ops in operations:
        out += ops
        out += ";\n"

    print(out)
    print("\n")
    print("code generated")
    return out
def save(data):
    print("saving...")
    try:
        try:
            os.remove(path2+name+ext)
        except:
            pass

        file=open(path2+name+".txt","w")
        file.write(data)
        file.close()
        os.rename(path2+name+".txt",path2+name+ext)
        print("saved to removable drive")
    except:
        try:
            os.remove(path+name+ext)
        except:
            pass

        file=open(path+name+".txt","w")
        file.write(data)
        file.close()
        os.rename(path+name+".txt",path+name+ext)
        print("saved to disk")

class letter():
    def __init__(self,motion,width):
        self.motions = motion
        self.width=width
    def write(self,off):
        #mov(motions[0][0]+off.x,motions[0][1]+off.y,0)
        for mot in self.motions:
            #print(mot)
            try:
                mot[2]
                #print("tried!")
                mov(point*letter_width*mot[0]+off.x,point*letter_height*mot[1]+off.y,0)
                #print("sucked")
            except:
                mov(point*letter_width*mot[0]+off.x,point*letter_height*mot[1]+off.y)
        return self.width

a=letter([(1,0.33,0),(0.66,0),(0.33,0),(0,0.33),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,0)],1)
b=letter([(0,0.66,0),(0.33,1),(0.66,1),(1,0.66),(1,0.33),(0.66,0),(0.33,0),(0,0.33),(0,2)],1)
c=letter([(0.66,0,0),(0.33,0),(0,0.33),(0,0.66),(0.33,1),(0.66,1)],0.66)
d=letter([(1,0.66,0),(0.66,1),(0.33,1),(0,0.66),(0,0.33),(0.33,0),(0.66,0),(1,0.33),(1,2)],1)
e=letter([(1,0.33,0),(0.66,0),(0.33,0),(0,0.33),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,0.5),(0,0.5)],1)
f=letter([(0.25,0,0),(0.25,1),(0.205,1.33),(0.66,1),(0,0.66,0),(0.66,0.66)],0.66)
g=letter([(1,0.33,0),(0.66,0),(0.33,0),(0,0.33),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,-0.5),(0.66,-0.83),(0.33,-0.83),(0,-0.5)],1)
h=letter([(0,2,0),(0,0),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,0.33),(1,0)],1)
i=letter([(0.2,1.25,0),(0,1.25),(0.1,1.35,0),(0.1,1.15),(0.1,0.6,0),(0.1,0)],0.2)
j=letter([(0.7,1.25,0),(0.5,1.25),(0.6,1.35,0),(0.6,1.15),(0.6,1,0),(0.6,-0.5),(0.3,-0.83),(0,-0.83)],0.7)
k=letter([(0,1.33,0),(0,0),(0.33,0.66,0),(0,0.33),(0.33,0)],0.33)
l=letter([(0,0,0),(0,1.33)],0.1)
m=letter([(0,0,0),(0,0.75),(0.25,1),(0.5,0.75),(0.5,0),(0.5,0.75),(0.75,1),(1,0.75),(1,0)],1)
n=letter([(0,0,0),(0,0.75),(0.25,1),(0.5,1),(0.75,0.75),(0.75,0)],0.75)
o=letter([(0,0.33,0),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,0.33),(0.66,0),(0.33,0),(0,0.33)],1)
p=letter([(0,-0.83,0),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,0.33),(0.66,0),(0.33,0),(0,0.33)],1)
q=letter([(1,0.33,0),(0.66,0),(0.33,0),(0,0.33),(0,0.66),(0.33,1),(0.66,1),(1,0.66),(1,-0.83)],1)
r=letter([(0,0,0),(0,0.66),(0.33,1),(0.5,1)],0.75)
s=letter([(0,0,0),(1,0),(1,0.5),(0,0.5),(0,1),(1,1)],1)
t=letter([(0.33,0,0),(0.33,1.25),(0,1,0),(0.66,1)],0.66)
u=letter([(0,1,0),(0,0.33),(0.33,0),(0.66,0),(1,0.33),(1,1)],1)
v=letter([(0,1,0),(0.33,0),(0.66,1)],0.66)
w=letter([(0,1,0),(0,0.25),(0.25,0),(0.5,0.25),(0.5,1),(0.5,0.25),(0.75,0),(1,0.25),(1,1)],1)
x=letter([(0,1,0),(1,0),(0,0,0),(1,1)],1)
y=letter([(0,1,0),(0.5,0),(1,1,0),(0,-0.83)],0.5)
z=letter([(0,1,1),(1,1),(0,0),(1,0)],1)

A=letter([(0,0,0),(0.5,2),(1,0),(0.1,0.4,0),(0.9,0.4)],1)
B=letter([(0,0,0),(0,2),(0.66,2),(1,1.66),(1,1.33),(0.66,1),(0,1),(0.66,1),(1,0.66),(1,0.33),(0.66,0),(0,0)],1)
C=letter([(1,0,0),(0.33,0),(0,0.33),(0,1.66),(0.33,2),(1,2)],1)
D=letter([(0,0,0),(0,2),(0.66,2),(1,1.66),(1,0.33),(0.66,0),(0,0)],1)
E=letter([(1,0,0),(0,0),(0,2),(1,2),(0,1,0),(1,1)],1)
F=letter([(0,0,0),(0,2),(1,2),(0,1,0),(1,1)],1)
G=letter([(1,2,0),(0.33,2),(0,1.66),(0,0.33),(0.33,0),(1,0),(1,1),(0.66,1)],1)
H=letter([(0,0,0),(0,2),(1,0,0),(1,2),(0,1,0),(1,1)],1)
I=letter([(0,0,0),(0.66,0),(0,2,0),(0.66,2),(0.33,0,0),(0.33,2)],0.66)
J=letter([(0,2,0),(1,2),(1,0.33),(0.66,0),(0.33,0),(0,0.33)],1)
K=letter([(0,0,0),(0,2),(1,2,0),(0,1),(1,0)],1)
L=letter([(0,2,0),(0,0),(0,1)],1)
M=letter([(0,0,0),(0.33,2),(0.66,0),(1,2),(1.33,0)],1.33)
N=letter([(0,0,0),(0,2),(0.66,0),(0.66,2)],0.66)
O=letter([(0,0.33,0),(0,1.66),(0.33,2),(0.66,2),(1,1.66),(1,0.33),(0.66,0),(0.33,0),(0,0.33)],1)
P=letter([(0,0,0),(0,2),(0.66,2),(1,1.66),(1,1.33),(0.66,1),(0,1)],1)
Q=letter([(0,0.33,0),(0,1.66),(0.33,2),(0.66,2),(1,1.66),(1,0.33),(0.66,0),(0.33,0),(0,0.33),(0.5,1,0),(1,0)],1)
R=letter([(0,0,0),(0,2),(0.66,2),(1,1.66),(1,1.33),(0.66,1),(0,1),(1,0)],1)
S=letter([(1,2,0),(0.33,2),(0,1.66),(0,1.33),(0.33,1),(0.66,1),(1,0.66),(1,0.33),(0.66,0),(0,0)],1)
T=letter([(0,2,0),(1,2),(0.5,2,0),(0.5,0)],1)
U=letter([(0,2,0),(0,0.33),(0.33,0),(0.66,0),(1,0.33),(1,2)],1)
V=letter([(0,2,0),(0.5,0),(1,2)],1)
W=letter([(0,2,0),(0.33,0),(0.66,2),(1,0),(1.33,2)],1.33)
X=letter([(0,2,0),(1,0),(0,0,0),(1,2)],1)
Y=letter([(0,2,0),(0.5,1.33),(1,2),(0.5,1.33,0),(0.5,0)],1)
Z=letter([(0,2,0),(1,2),(0,0),(1,0)],1)


SPACE=letter([(0,0,0)],spacing)
EXC=letter([(0.1,1,0),(0.1,0.2),(0.1,0.1,0),(0.1,0),(0,0.1,0),(0.2,0.1)],0.2)
PER=letter([(0.1,0.1,0),(0.1,0),(0,0.1,0),(0.2,0.1)],0.2)
COMMA=letter([(0,-0.2,0),(0.1,0)],0.1)
QUESTION=letter([(0.23,0.1,0),(0.43,0.1),(0.33,0,0),(0.33,0.2),(0.33,0.4,0),(0.33,0.66),(0.66,1),(0.33,1.33)],0.66)
QUOT=letter([(0,1,0),(0,1.2)],0.1)
QUOTQUOT=letter([(0,1,0),(0,1.2),(0.2,1,0),(0.2,1,2)],0.2)
DASH=letter([(0,0.5,0),(0.33,0.5)],0.335)
COLON=letter([(0,0.5,0),(0.2,0.5),(0.1,0.4,0),(0.1,0.6),(0,1.5,0),(0.2,1.5),(0.1,1.4,0),(0.1,1.6)],0.2)
LPAREN=letter([(0.5,0,0),(0.25,0),(0,0.25),(0,1.66),(0.25,2),(0.5,2)],0.25)
RPAREN=letter([(0,0,0),(0.25,0),(0.5,0.25),(0.5,1.66),(0.25,2),(0,2)],0.25)



ONE=letter([(0,1.5,0),(0.25,1.75),(0.33,0)],0.25)
TWO=letter([(0,1.5,0),(0.33,1.75),(0.66,1.75),(1,1.5),(1,1.25),(0,0),(1,0)],1)
THREE=letter([(1,0.25,0),(0.75,0),(0.25,0),(0,0.25),(0,0.5),(0.25,0.75),(0.5,0.75),(0.25,0.75),(0,1),(0,1.25),(0.25,1.5),(0.75,1.5),(1,1.25)],1)
FOUR=letter([(0.75,0,0),(0.75,1.5),(0,0.66),(1,0.66)],1)
FIVE=letter([(1,1.5,0),(0,1.5),(0,0.75),(0.25,1),(0.75,1),(1,0.75),(1,0.25),(0.75,0),(0.25,0),(0,0.25)],1)
SIX=letter([(1,1.25,0),(0.75,1.5),(0.25,1.5),(0,1.25),(0,0.25),(0.25,0),(0.75,0),(1,0.25),(1,0.75),(0.75,1),(0.25,1),(0,0.75)],1)
SEVEN=letter([(0,1.5,0),(1,1.5),(0,0)],1)
EIGHT=letter([(0.25,0,0),(0.75,0),(1,0.25),(1,0.5),(0.75,0.75),(1,1),(1,1.25),(0.75,1.5),(0.25,1.5),(0,1.25),(0,1),(0.25,0.75),(0,0.5),(0,0.25),(0.25,0)],1)
NINE=letter([(1,0,0),(1,1.25),(0.75,1.5),(0.25,1.5),(0,1.25),(0,1),(0.25,0.75),(0.75,0.75),(1,1)],1)
ZERO=letter([(0,0.33,0),(0,1.66),(0.33,2),(0.66,2),(1,1.66),(1,0.33),(0.66,0),(0.33,0),(0,0.33)],1)


def word(word,offset):
    letters=[]
    letters[:]=word

    for jay in letters: #this is not my proudest moment, but made it easy to implement custom functions in letters, such as custom kerning around punctuation
        skip_override=0
        if jay == " ":
            width=SPACE.write(offset)
        elif jay == "!":
            width=EXC.write(offset)
        elif jay == ".":
            width=PER.write(offset)
        elif jay == ",":
            width=COMMA.write(offset)
        elif jay =="?":
            width=QUESTION.write(offset)
        elif jay =="\'":
            width=QUOT.write(offset)
        elif jay =="\"":
            width=QUOTQUOT.write(offset)
        elif jay =="-":
            width=DASH.write(offset)
        elif jay ==":":
            width=COLON.write(offset)
        elif jay =="(":
            width=LPAREN.write(offset)
        elif jay==")":
            width=RPAREN.write(offset)


        elif jay =="1":
            width=ONE.write(offset)
        elif jay =="2":
            width=TWO.write(offset)
        elif jay =="3":
            width=THREE.write(offset)
        elif jay =="4":
            width=FOUR.write(offset)
        elif jay =="5":
            width=FIVE.write(offset)
        elif jay =="6":
            width=SIX.write(offset)
        elif jay =="7":
            width=SEVEN.write(offset)
        elif jay =="8":
            width=EIGHT.write(offset)
        elif jay =="9":
            width=NINE.write(offset)
        elif jay =="0":
            width=ZERO.write(offset)

        elif jay =="_":
            offset.x = left_margin
            offset.y += -(line_spacing+letter_height)*point
            skip_override=1
            #return offset

        else:
            width=eval(jay).write(offset)

        if skip_override==0:
            offset+=(kerning*point+letter_width*width*point,0)
            if offset.x > right_margin:
                offset.x = left_margin
                offset.y += -(line_spacing+letter_height)*point
    offset.y += -(line_spacing+letter_height)*point
    offset.x = left_margin
    pygame.Surface.blit(mainDisplay,lineSurface,(0,0))
    pygame.display.update()
    pygame.event.get()
    return offset





pygame.init()
lineSurface=pygame.Surface((MAXX*renderscale,MAXY*renderscale))
mainDisplay = pygame.display.set_mode((MAXX*renderscale,MAXY*renderscale))



start(100)
#display("writing...")


#image('soy2.png',0.2)
#output=sum()

#save(output)
#quit()
letter_number=0
fsz=input("font size?\n")
if fsz!="MAX":
    point=float(fsz)
    print("type your sentance\n")
    flag=0
    linessss=""
    while flag==0:
        holding=input()
        if holding == "done":
            flag=1
            print("message recieved!")
        else:

            offset=word(str(holding),offset)





    display("done")
    operations.append("G1 Y"+str(MAXY)+" Z15 F"+str(rapid))
    output=sum()
    save(output)
    print("done")
else:
    point=1
    while toobig==False:
        operations=[]
        output=""
        running=vmath.Vector2(0,0)
        point*=1.1
        print(point)
        print("type your sentance\n")
        flag=0
        linessss=""
        while flag==0:
            holding=input()
            if holding == "done":
                flag=1
                print("message recieved!")
            else:

                offset=word(str(holding),offset)






        display("done")
        operations.append("G1 Y"+str(MAXY)+" Z15 F"+str(rapid))
        output=sum()
    point*=0.9
    print("size found: "+str(point5))
    print("type your sentance\n")
    flag=0
    linessss=""
    while flag==0:
        holding=input()
        if holding == "done":
            flag=1
            print("message recieved!")
        else:

            offset=word(str(holding),offset)






    display("done")
    operations.append("G1 Y"+str(MAXY)+" Z15 F"+str(rapid))
    output=sum()


    save(output)
    print("done")



#def codeify(fsz,)



while(True):
    #time.sleep(1)
    pygame.event.get()
