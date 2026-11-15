from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
BG, INK, MUTED = '#ffffff', '#183344', '#526977'
BLUE, GOLD, GRID = '#176f96', '#c05f29', '#d8e1e6'
im = Image.new('RGB', (1440, 880), BG)
d = ImageDraw.Draw(im)

def text(x, y, s, size=28, color=INK, anchor=None):
    d.text((x,y), s, fill=color, font=ImageFont.truetype(FONT,size), anchor=anchor)

text(62, 36, 'M6×1 手册原例：X 直径差 ÷ 2 = 单边切入量', 39)
text(64, 99, '前序外圆 φ6｜循环起点 X7、Z−2｜各刀终点 Z6.5｜导程 F1.0', 26, MUTED)
d.line((64,151,1370,151), fill=GRID, width=2)

x0, x1 = 360, 1020
def sx(depth): return x0+(x1-x0)*depth/.70
text(65,185,'刀次 / X 指令',25,MUTED)
text(360,185,'从 φ6 外圆累计向内切入（单边，mm）',25,MUTED)
text(1130,185,'本刀新增',25,MUTED)
for h in [0,.1,.2,.3,.4,.5,.6,.7]:
    x=sx(h)
    d.line((x,240,x,698), fill=GRID, width=1)
    text(x,720,f'{h:.1f}',25,MUTED,'mt')

xs=[5.40,4.96,4.70,4.60,4.60]
last=0
for i,x in enumerate(xs):
    depth=round((6-x)/2, 2)
    inc=round(depth-last,2)
    y=268+i*94
    text(65,y,f'第 {i+1} 刀   X{x:.2f}',29,INK,'lm')
    if last>0:
        d.rectangle((x0,y-20,sx(last),y+20), fill='#cfe2eb')
    if inc>0:
        d.rectangle((sx(last),y-20,sx(depth),y+20), fill=BLUE)
    else:
        d.line((sx(depth),y-25,sx(depth),y+25), fill=GOLD,width=6)
    text(sx(depth)+14,y,f'{depth:.2f}',26,INK,'lm')
    text(1130,y,f'{inc:.2f} mm'+('  重复一刀' if inc==0 else ''),26,GOLD if inc==0 else INK,'lm')
    last=depth

text(65,785,'第一刀：(6.00 − 5.40) ÷ 2 = 0.30 mm；起点 X7 的空隙不计入切深。',27)
text(65,831,'按程序名义坐标推算；X4.60 是原例指令值，不代表所有 M6×1 的合格底径。',24,MUTED)
im.save(OUT/'g92-M6x1分刀图.png')

# 由已核实坐标直接绘制第一刀；非等比例，相对刀路而非整机结构。
import math
im = Image.new('RGB', (1440, 880), BG)
d = ImageDraw.Draw(im)
text(62,36,'G92 一刀的四段动作：最后回到起点 A',39)
text(64,99,'G00 X16.0 Z−2.0 → G92 X12.0 Z10.0 F1.0｜坐标写作 (X, Z)，单位 mm',26,MUTED)
d.line((64,151,1370,151), fill=GRID,width=2)
left,right,top,bottom=300,1150,278,558
z0=right-(right-left)*2/12
for y in range(200,700,20): d.line((z0,y,z0,y+10),fill=GRID,width=2)
text(z0,705,'Z0 右端面',25,MUTED,'mt')
def arrow(a,b,color=BLUE,width=5):
    d.line((a,b),fill=color,width=width)
    dx,dy=b[0]-a[0],b[1]-a[1]
    l=math.hypot(dx,dy); ux,uy=dx/l,dy/l
    d.polygon([b,(b[0]-16*ux+7*uy,b[1]-16*uy-7*ux),(b[0]-16*ux-7*uy,b[1]-16*uy+7*ux)],fill=color)
arrow((right,top),(right,bottom),MUTED)
arrow((right,bottom),(left,bottom),BLUE)
arrow((left,bottom),(left,top),MUTED)
arrow((left,top),(right,top),MUTED)
for x,y,s,anc in [(right,top,'A (16, −2)','rb'),(left,top,'D (16, 10)','lb')]:
    text(x,y-24,s,29,INK,anc)
for x,y,s,anc in [(right,bottom,'B (12, −2)','rt'),(left,bottom,'C (12, 10)','lt')]:
    text(x,y+24,s,29,INK,anc)
for x,y in [(left,top),(right,top),(left,bottom),(right,bottom)]:
    d.ellipse((x-6,y-6,x+6,y+6),fill=INK)
text(1200,385,'① 快速',27,MUTED)
text(1200,425,'沿 X 切入',27,MUTED)
text(725,510,'② 沿 +Z 螺纹同步切削，F1.0',29,BLUE,'mm')
text(85,385,'③ 快速',27,MUTED)
text(85,425,'沿 X 退刀',27,MUTED)
text(725,320,'④ 快速沿 Z 返回 A',28,MUTED,'mm')
arrow((140,700),(140,590),INK,3)
arrow((140,700),(65,700),INK,3)
text(145,565,'+X',26,INK,'mm')
text(65,738,'+Z',26,INK,'mm')
text(245,685,'X 为直径坐标',26,MUTED)
text(245,726,'+Z 向左进入工件',26,MUTED)
text(64,800,'刀尖相对工件的上侧示意，非等比例；原图画在工件下侧。',25,MUTED)
text(64,839,'按手册矩形路线简化，未展开末端修牙；实际末端可能有 X/Z 联动。',25,MUTED)
im.save(OUT/'g92-四段刀路.png')
