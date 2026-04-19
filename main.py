from PIL import Image, ImageDraw
from numpy import *

# Задать в этом же файле функцию расчета евклидова расстояния и функции
# отрисовки точек
def dist(p1, p2):
    dx, dy=p1[0]-p2[0], p1[1]-p2[1]
    return sqrt(dx*dx+dy*dy)
def drawPt(x, y, ind, r=3):
    colors=('black', 'red', 'green', 'blue', 'violet')
    draw.ellipse((x-r, y-r, x+r, y+r), fill=colors[ind+1])
def drawCenter(x, y, ind, r=3):
    colors=('black', 'red', 'green', 'blue', 'violet')
    draw.rectangle((x-r, y-r, x+r, y+r), fill=colors[ind+1])

# Задать расположение точек данных на двумерной плоскости:   
pts=[
    [100,70, -1], [120,80,-1], [90,110,-1], [110,130,-1],
    [130,90,-1], [80,140,-1], [90,120,-1], [150,125,-1],
    [145,45,-1], [160,130,-1], [120,100,-1]
]

# Задать начальное расположение центров кластеров:
centers=[
    [90,80, 0], [150,80, 1], [60,120, 2]
]

# Реализовать функцию поиска ближайшего кластера к выбранной точке
def findNearestCenter(p):
    minDist=100500
    bestInd=0
    for ind in range(0, len(centers)):
        c = centers[ind]
        d = dist(p, c)
        if(d<minDist):
            minDist=d
            bestInd=ind
    return bestInd

# Реализовать такую же функцию для всего набора точек:
def assignPoints():
    for ind in range(0, len(pts)):
 # меняем цвет точки на цвет ближайшего кластера
        pts[ind][2]=findNearestCenter(pts[ind])

# Реализовать такую же функцию для всего набора точек:
def findCenterOfMass(ind):
    res=[0.0,0.0]
    cnt=0
    for i in range(0, len(pts)):
        p=pts[i]
        if(p[2]==ind):
            res[0]+=p[0]
            res[1]+=p[1]
            cnt+=1
    return [res[0]/cnt, res[1]/cnt]

# Реализовать функцию сдвига центров кластеров в направлении
# пересчитанных центров масс
def shiftCenters():
    global centers
    for ind in range(0, len(centers)):
        c=centers[ind]
        c_=findCenterOfMass(ind)
        centers[ind] = [c_[0], c_[1], c[2]]

w,h = 250, 200
im = Image.new('RGB', (w, h), (255, 255, 255))
draw = ImageDraw.Draw(im)

def drawAll():
    draw.rectangle((0, 0, w, h), fill='white') #clear
    for ind in range(0, len(pts)):
        p = pts[ind]
        drawPt(p[0], p[1], p[2])
    for ind in range(0, len(centers)):
        p = centers[ind]
        drawCenter(p[0], p[1], p[2])
        
for i in range(5):
    if i>0: shiftCenters()
    assignPoints()
    drawAll()
    im.save(f"img{i}.jpg", quality=95)


