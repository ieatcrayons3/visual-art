import cv2
import numpy as np
from random import randint,shuffle
from math import exp, sqrt, pow, floor

def tdiv(p,s):
    return (p[0]/s,p[1]/s,p[2]/s)

lenboard = 44
widthboard = 11
res = 100
xrs = lenboard*res
yrs = widthboard*res
tape = np.zeros((xrs, yrs,3))

pallate = [(255,0,255),(255,255,0)]
#pallate = [(250,206,91),(184,169,245),(255,255,255)]
#pallate = [(51,53,188),(45,125,208),(57,172,205),(255,255,255)]

pallate = [tdiv(i,255) for i in pallate]

def drawTri(points):
    shuffle(pallate)
    triangle_cnt = np.array(points)
    cv2.drawContours(tape, [triangle_cnt], 0, pallate[0], -1)
    cv2.drawContours(tape, [triangle_cnt], 0, (0,0,0), 5)

def tadd(p1,p2):
    return (p1[0]+p2[0],p1[1]+p2[1])

def norm(x):

     a=exp(-pow(x,2))
    # print(a)
     return a


s = 15
while True:
    tape = np.zeros((xrs, yrs,3))
    for i in range(150):
        s = floor(250*norm(randint(0,1000)/1000))
        p1 = (randint(0,yrs),randint(0,xrs))
        p2 = tadd(p1,(randint(-s,s),randint(-s,s)))
        p3 = tadd(p1,(randint(-s,s),randint(-s,s)))
        drawTri([p1,p2,p3])

    dim = (lenboard * 20, widthboard * 20)
    resized = cv2.resize(tape, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("frame",resized)
    if cv2.waitKey(1) == ord("q"):
        break
cv2.waitKey(0)
