#letters.py
from gcode import mov



def test(pas):
    print(pas)

example_motions = [(0,0),(1,0),(1,1),(0,1),(0,0)]

class letter():
    def __init__(self,motion):
        self.motions = motion
    def write(off):
        for m in motions:
            mov(m[0]+off.x,m[1]+off.y)
