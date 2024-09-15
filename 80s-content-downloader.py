from random import randint
year = randint(1980,1992) #range of years youd like to experience
month = randint(1,12) #i guess you can specify the month too?
results = 3 #number of things you want to download. keep this number low because if you get bored halfway through it will corrupt files
searchfor = "commercial" #type of content you want

filepath = "C:/Users/~" #main directory for your slopfolder (it will build its own subdirectories for year and month)

from internetarchive import download, search_items #internetarchive bindings (not necessary to play just for downloading)
import os

year = str(year)
month = str(month)

day2 = "30"
if int(month) == 2:
    day2 = "28"
if int(month) < 10:
    month = "0" + month
year += "/"
month += "/"
savepath = filepath + year + month

if not os.path.exists(savepath):
    os.makedirs(savepath)


searchQuery = f'title:({searchfor}) AND mediatype:(movies) date:[{year}-{month}-01 TO {year}-{month}-{day2} AND item_size:["1000" TO "1000000"]]'
items = [i["identifier"] for i in search_items(searchQuery)]

for i in range(min(results, len(items))):
    print(year, month, items[i][0:50],"\n\n",savepath)
    download(items[i], destdir = savepath, dry_run=False, ignore_existing=True, ignore_errors = True, glob_pattern='*.ia.mp4')
