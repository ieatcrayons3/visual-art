from time import sleep
import vlc
import os
from random import randint, shuffle


commercialPath = "C:/Users/~/OneDrive/Desktop/Personal/Dev/" #main slopfolder (see other script)
contentpath = "C:/Users/~/Videos/NGE/" #where you put the stuff you actually wanna watch (currently doesnt support serialized content, Sorry!)

do_commercials = True #this is the optimal configuration
do_content = False



def recursivewalk(path2walk):
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path2walk)) for f in fn]

def PlayVideo(video_path, medreturn = None):
    my_media = vlc.MediaPlayer(video_path)
    my_media.toggle_fullscreen()
# playing video
    my_media.play()
    sleep(1.5)
    duration = my_media.get_length() / 1000
    sleep(3.5)
    if medreturn != None:
        medreturn.stop()
    sleep(duration-5)
    return my_media

def commercialbreak(medreturn = None, ym = None):
    if ym == None:
        year = str(randint(1980, 1992)) + "/"
        month = str(randint(1,12))
    else:

        year = str(ym[0])
        month = str(ym[1])
    print(f"YEAR: {year}, MONTH: {month}")
    if int(month) < 10:
        month = "0" + month
    month += "/"
    workingPath = commercialPath + year + month
    commercials = recursivewalk(workingPath)
    #while len(commercials) == 0:
    if len(commercials) == 0:
        print(f"no content from {year} {month}") #if youre getting this message a ton and nothing is playing you dont have content downloaded into the commercial folder
        #ym = (int(year.replace("/","")),int(month.replace("/","")))
        #if ym[1] == 12:
        #    ym = (ym[0]+1,1)
        #if ym[0] > 1992:
        medreturn = commercialbreak(medreturn)
        #else:
        #medreturn = commercialbreak(medreturn, (ym[0], ym[1]+1))
    else:
        shuffle(commercials)
        #for i in commercials[0:min(randint(3,5),len(commercials))]:
        for i in commercials[0:min(10000,len(commercials))]:
            medreturn = PlayVideo(i, medreturn)
            print(i)
    return medreturn

def playcontent(path, medreturn, unplayed):
    titles = os.listdir(path)
    shuffle(titles)
    while titles[0] in unplayed:
        titles.pop(0)
    medreturn = PlayVideo(path + titles[0])
    return medreturn, unplayed


medreturn = None
unplayed = []
while True:
    if do_commercials:
        medreturn = commercialbreak(medreturn)
    if do_content:
        medreturn, unplayed = playcontent(contentpath, medreturn, unplayed)
