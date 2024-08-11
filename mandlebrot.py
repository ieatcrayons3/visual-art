#mandlebrot


from numba import jit
import math
import numpy as np
import cv2

x=1000
y=1000
ix=1/x
iy=1/y
#effort=1000
#ie=1/effort

frame=np.zeros((y,x))


for i in range(x):
    for j in range(y):
        frame[i,j]=i/x





def progress(s,f,title=None):
    f1=round(f/(f*0.05))
    s1=round(s/(f*0.05))
    pgb=""
    pgb+=title
    pgb+="|"
    for i in range(s1):
        pgb+="█"
    for i in range(f1-s1):
        pgb+=" "
    pgb+="|"+str(s)+"/"+str(f)
    print(pgb,end="\r")
    if s==(f-1):
        pgb=""
        pgb+=title
        pgb+="|"
        for i in range(s1):
            pgb+="█"
        for i in range(f1-s1):
            pgb+=" "
        pgb+="|"+str(s+1)+"/"+str(f)
        print(pgb,end="\r")
        print("\n")













@jit(nopython=True)
def testpoint(xx,yy,effort,ie):
    xx1=0
    yy1=0
    for i in range(effort):
        xx2=xx1*xx1-yy1*yy1+xx
        yy2=2*xx1*yy1+yy
        xx1=xx2
        yy1=yy2
        if xx1**2 > 4 or yy1**2 > 2:
            return 1-i*ie

#@jit
def iterates(ef):
    effort=ef
    ie=1/effort
    for xx in range(x):
        for yy in range(y):
            frame[yy,xx]=testpoint((xx*ix*3-2),(yy*iy*3-1.5),effort,ie)
            #for k in range(3):
                #frame[yy,xx,k]=t
#frame=np.multiply(frame,255)

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 3,(y,x),False)
for i in range(15):

    iterates(1+i)

    cv2.imshow('img',frame)
    #out.write(frame)
    #progress(i,400,"Progress: ")
    if cv2.waitKey(1)==ord('q'):
        break
#out.release()
cv2.destroyAllWindows()
