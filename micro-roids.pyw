import cv2
import numpy as np
from math import floor, cos, sin, pi
from keyboard import is_pressed, read_key
from random import randint
from tkinter import Tk, Canvas, PhotoImage, NW
from PIL import Image, ImageTk
from time import sleep
import ctypes

import timeit

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

root = Tk()


# Canvas


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_CUBIC)
  return result

shipsize = 13

xw = screensize[0]
yw = screensize[1]

root.attributes('-transparentcolor','#f0f0f0')
canvas = Canvas(root, width=xw, height=yw)
canvas.pack()
root.overrideredirect(True)
root.geometry("{x}x{y}+{xo}+{yo}".format(x=xw,y=yw,xo=0,yo=0))
sp = np.array([[0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0],[0,0,0,1,1,0,1,1,0,0,0], [0,0,0,1,0,0,0,1,0,0,0], [0,0,1,1,0,0,0,1,1,0,0], [0,0,1,0,0,0,0,0,1,0,0], [0,1,1,0,0,1,0,0,1,1,0], [0,1,0,1,1,0,1,1,0,1,0], [0,1,1,1,0,0,0,1,1,1,0]])
sp = np.array([[0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,1,1,1,1,1,0,0,0], [0,0,0,1,1,0,1,1,0,0,0], [0,0,1,1,1,0,1,1,1,0,0], [0,0,1,1,0,1,0,1,1,0,0], [0,1,1,0,1,1,1,0,1,1,0], [0,1,1,1,1,1,1,1,1,1,0], [0,1,1,1,0,0,0,1,1,1,0]])

ship = np.zeros((shipsize,shipsize))
ship[1:12,1:12] += sp
#ship=ship.astype("bool")
#cv2.imshow("arr",ship)
#cv2.waitKey(0)
sc = (floor(xw/2),floor(yw/2))
sr = 0
sv = (0,0)
dt = 0.5
decay = 0.9999
bv = 5
slew = 20
bullets = []
asteroids = []
ba = 40
acc = 1.2

av = 15
points = 0

def dist(t1,t2):
    return ((t1[0]-t2[0])**2+(t1[1]-t2[1])**2)

class bullet:

    def __init__(self, loc, angle, relvel):
        self.location = loc
        self.x = -cos(-angle * pi/180 + pi/2) * bv + relvel[0] * dt
        self.y = -sin(-angle * pi/180 + pi/2) * bv + relvel[1] * dt
        bullets.append(self)
        self.age = 0
    def update(self):

        self.location = (self.location[0] + self.x, self.location[1] + self.y)
        self.age += 1
        if self.age > ba:
            bullets.remove(self)
        if self.location[0] >= xw - 1:
            self.location = (3, self.location[1])
        if self.location[0] <= 1:
            self.location = (xw - 3, self.location[1])

        if self.location[1] >= yw - 1:
            self.location = (self.location[0], 3)
        if self.location[1] <= 1:
            self.location = (self.location[0], yw - 3)
        return (floor(self.location[1]), floor(self.location[0]))

class asteroid:
    global points
    def __init__(self, ship_location, rad = 0, tl = 0, v = (0,0)):
        if rad == 0:
            self.rad = randint(3,10)
        else: self.rad = rad
        if tl == 0:
            tl = (randint(0,xw),randint(0,yw))
            while dist(tl, ship_location) < 400 + self.rad**2:
                 tl = (randint(0,xw),(0,yw))
        self.location = tl

        self.velocity = (av*randint(-1000,1000)/1000, av*randint(-1000,1000)/1000)

        asteroids.append(self)
    def update(self):
        global points
        self.location = (self.location[0] + self.velocity[0] * dt, self.location[1] + self.velocity[1] * dt)


        for i in bullets:
            if dist(i.location,self.location) < self.rad**2:
                try:
                    asteroids.remove(self)
                except: pass
                if self.rad > 5:
                    asteroid((sc),floor(self.rad/2),self.location, ())
                    asteroid((sc),floor(self.rad/2),self.location, ())
                bullets.remove(i)
                points += self.rad
        if self.location[0] < 0 or self.location[0] > xw or self.location[1] > yw or self.location[1] < 0:
            try:
                asteroids.remove(self)
            except:
                pass
            return (0,0)
        return (floor(self.location[0]), floor(self.location[1]))
asteroid(sc)
while True:
    print(points, end="\r")
    if randint(0,10) == 0:
        asteroid(sc)
    if is_pressed("a"):
        sr += slew
    if is_pressed("d"):
        sr -= slew
    if is_pressed("w"):
        sv = (sv[0]-acc*sin(pi * sr / 180), sv[1] - acc*cos(pi * sr/180))
        #sp = np.array([[0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,1,1,1,1,1,0,0,0], [0,0,0,1,1,0,1,1,0,0,0], [0,0,1,1,1,0,1,1,1,0,0], [0,0,1,1,0,1,0,1,1,0,0], [0,1,1,0,1,1,1,0,1,1,0], [0,1,1,1,1,1,1,1,1,1,0], [0,1,1,1,1,1,1,1,1,1,0]])

    elif is_pressed("s"):
        sp = np.array([[0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,1,1,1,1,1,0,0,0], [0,0,0,1,1,0,1,1,0,0,0], [0,0,1,1,1,0,1,1,1,0,0], [0,0,1,1,0,1,0,1,1,0,0], [0,1,1,0,1,1,1,0,1,1,0], [0,1,1,1,1,1,1,1,1,1,0], [0,1,1,1,0,0,0,1,1,1,0]])
        bullet((sc[0]+shipsize/2,sc[1] + shipsize/2),sr, sv)
    #else:
        #sp = np.array([[0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,1,1,1,1,1,0,0,0], [0,0,0,1,1,0,1,1,0,0,0], [0,0,1,1,1,0,1,1,1,0,0], [0,0,1,1,0,1,0,1,1,0,0], [0,1,1,0,1,1,1,0,1,1,0], [0,1,1,1,1,1,1,1,1,1,0], [0,1,1,1,0,0,0,1,1,1,0]])

    if is_pressed("space"):
        quit()
    sc = (sc[0] + sv[0] * dt, sc[1]+sv[1] * dt)

    if sc[0] >= xw - 1- shipsize:
        sc = (3 + shipsize, sc[1])
    if sc[0] <= 1 + shipsize:
        sc = (xw - 3 - shipsize, sc[1])

    if sc[1] >= yw - 1 - shipsize:
        sc = (sc[0], 3 + shipsize)
    if sc[1] <= 1 + shipsize:
        sc = (sc[0], yw - 3 - shipsize)
    sv = (sv[0] * decay, sv[1] * decay)
    arr = np.zeros((yw,xw))

    arr[floor(sc[1]):floor(sc[1]+shipsize),floor(sc[0]):floor(sc[0]+shipsize)] += rotate_image(ship,sr)
    for i in bullets:
        arr[i.update()]=1
    for i in asteroids:
        cv2.circle(arr, (floor(i.location[0]),floor(i.location[1])), i.rad, 1, 1)
        if dist(sc, i.update())<i.rad**2:
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(arr,'GAME OVER',(floor(xw/2 - randint(140,160)),floor(yw/2 + randint(-15,5))), font, 4,(1),2,cv2.LINE_AA)
            cv2.putText(arr, str(points),(floor(xw/2+randint(20,30)),floor(yw/2+randint(50,60))), font, 3,(1),2,cv2.LINE_AA)
            img = Image.fromarray(np.ones((yw,xw))).convert('RGB')
            #print(type(img))
            img.putalpha(Image.fromarray(arr).convert('L'))
            img =  ImageTk.PhotoImage(image=img)

            canvas.create_image(0, 0, anchor=NW, image=img)

            # Starts the GUI]

            root.update_idletasks()
            root.update()

            sleep(3)
            asteroids = []
            bullets = []


            #cv2.imshow("game",arr)
            #cv2.waitKey(0)
            #quit()

    #arr[floor(sc[1]), floor(sc[0])] = 1



    # Image
    #img = PhotoImage(file="./images/panda.png")

    # Positioning the Image inside the canvas
    #arr = np.stack((arr,arr,arr))



    img = Image.fromarray(np.ones((yw,xw))).convert('RGB')
    #print(type(img))
    img.putalpha(Image.fromarray(arr).convert('L'))
    img =  ImageTk.PhotoImage(image=img)

    canvas.create_image(0, 0, anchor=NW, image=img)

    # Starts the GUI]

    root.update_idletasks()
    root.update()
    #sleep(0.006)
    #cv2.imshow("game",arr)
    #cv2.waitKey(6)
