from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(__file__).resolve().parent
S = 2
W, H = 1600, 1160
im = Image.new('RGB', (W*S, H*S), '#ffffff')
d = ImageDraw.Draw(im)
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
INK, MUTED, BLUE, PALE, LINE, ORANGE = '#172b3a', '#536776', '#176c9e', '#e9f2f7', '#aebfc9', '#a85e16'

def p(q): return tuple(round(v*S) for v in q)
def line(points, fill=INK, width=2): d.line([p(q) for q in points], fill=fill, width=width*S)
def text(x,y,txt,size=28,fill=INK,anchor='mm'):
    d.text(p((x,y)),txt,font=ImageFont.truetype(FONT,size*S),fill=fill,anchor=anchor)
def arrow(a,b,fill=INK,width=2,head=11):
    line([a,b],fill,width)
    ang=math.atan2(b[1]-a[1],b[0]-a[0])
    pts=[b,(b[0]-head*math.cos(ang-.38),b[1]-head*math.sin(ang-.38)),(b[0]-head*math.cos(ang+.38),b[1]-head*math.sin(ang+.38))]
    d.polygon([p(q) for q in pts],fill=fill)
def dashed(a,b,fill=LINE,width=1,dash=9):
    dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy)
    for t in range(0,math.ceil(L),dash*2):
        u,v=t/L,min(t+dash,L)/L
        line([(a[0]+u*dx,a[1]+u*dy),(a[0]+v*dx,a[1]+v*dy)],fill,width)

scale, x0, y0 = 31.0, 1320.0, 540.0
def xy(z,r): return x0-scale*z, y0-scale*r
L=30.2
profile=[(L,8),(15.2,8),(15.2,6),(12,6),(12,8),(8,8),(7,7),(7,5),(0,5),(0,-5),(7,-5),(7,-7),(8,-8),(12,-8),(12,-6),(15.2,-6),(15.2,-8),(L,-8)]
points=[p(xy(z,r)) for z,r in profile]
d.polygon(points,fill=PALE)
line([xy(z,r) for z,r in profile]+[xy(*profile[0])],INK,3)
dashed((330,y0),(1460,y0),MUTED,1,12)

text(70,55,'先定基准，再沿长度算Z',size=40,anchor='lm')
text(70,116,'右端面 Z0  ·  向图左为 +Z（本轮教学约定）  ·  X为直径值',size=27,fill=MUTED,anchor='lm')
text(70,160,'凸台C1已展开；其余C / R及孔、螺纹未展开。实体比例按 r = X / 2。',size=24,fill=MUTED,anchor='lm')

text(*xy(22.7,9.15),'φ16',size=30)
text(*xy(13.6,7.0),'φ12 槽底',size=25)
text(*xy(9.5,6.5),'φ16',size=30)
text(*xy(3.5,6.2),'φ10',size=30)
line([xy(7.5,7.5),(1180,281),(1255,281)],ORANGE,2)
text(1265,281,'C1',size=25,fill=ORANGE,anchor='lm')

# Positive axis directions are relative to the displayed workpiece.
arrow((1425,535),(1425,362),BLUE,3)
text(1425,330,'+X',size=27,fill=BLUE)
text(1425,574,'直径值',size=24,fill=BLUE)
arrow((1270,540),(1105,540),BLUE,3)
text(1185,509,'+Z',size=28,fill=BLUE)
d.ellipse([p((x0-6,y0-6)),p((x0+6,y0+6))],fill=BLUE)
text(1360,623,'Z0',size=30,fill=BLUE)
text(1360,660,'右端成品面',size=23,fill=MUTED)

# Dimension origin: the outer tangent of the right groove fillet.
xt,yt=xy(11.5,8)
d.ellipse([p((xt-5,yt-5)),p((xt+5,yt+5))],fill=ORANGE)
line([(xt,yt),(xt-45,205),(795,205)],ORANGE,2)
text(785,205,'R0.50 外圆切点：Z11.50',size=24,fill=ORANGE,anchor='rm')
line([(x0,355),(x0,235)],LINE,1)
line([(xt,278),(xt,235)],ORANGE,1)
arrow((xt,249),(x0,249),ORANGE,2,8)
arrow((x0,249),(xt,249),ORANGE,2,8)
text((xt+x0)/2,224,'11.50',size=24,fill=ORANGE)

def dimension(za,zb,y,label):
    xa,xb=xy(za,0)[0],xy(zb,0)[0]
    arrow((xa,y),(xb,y),INK,2,9)
    arrow((xb,y),(xa,y),INK,2,9)
    text((xa+xb)/2,y-29,label,size=26)

stations=[(30.2,'30.20'),(15.2,'15.20'),(12,'12.00'),(7,'7.00'),(0,'0')]
for z,label in stations:
    xx=xy(z,0)[0]
    bottom=xy(z,-8 if z>=7 else -5)[1]
    line([(xx,bottom+8),(xx,904)],LINE,1)
    text(xx,909 if z==12 else 939,'Z'+label,size=25,fill=BLUE)
dimension(30.2,15.2,865,'15.00')
dimension(15.2,12,865,'3.20')
dimension(12,7,865,'5.00')
dimension(7,0,865,'7.00')

for z in (30.2,0):
    xx=xy(z,0)[0]
    line([(xx,971),(xx,1016)],LINE,1)
dimension(30.2,0,1006,'总长 30.20')

text(70,1070,'槽右壁 Z = 11.50 + 0.50 = 12.00；其余台阶以这道壁面连接尺寸链。',size=25,anchor='lm')
text(70,1115,'C1端点：(X14,Z7) → (X16,Z8)；底孔有效孔深10，钻尖另算。',size=23,fill=MUTED,anchor='lm')

im.save(OUT/'坐标基准与尺寸链.png')
print(OUT/'坐标基准与尺寸链.png')
