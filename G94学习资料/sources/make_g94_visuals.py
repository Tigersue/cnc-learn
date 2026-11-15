from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
BG = '#F8FAFC'
INK = '#182936'
MUTED = '#526674'
STEEL = '#D5E0E6'
STEEL_LINE = '#9CAFBA'
RAPID = '#2563A5'
FEED = '#B44B1A'
HILITE = '#F8DFC7'
GRID = '#D2DCE3'

def font(size):
    return ImageFont.truetype(FONT, size)

def text(d, xy, value, size=20, color=INK, anchor=None):
    # Hiragino Sans GB lacks Latin Ø; Greek phi is the familiar diameter mark.
    d.text(xy, value.replace('Ø', 'φ'), font=font(size), fill=color, anchor=anchor)

def dashed(d, p, q, color, width=2, dash=8, gap=5):
    dx, dy = q[0]-p[0], q[1]-p[1]
    length = math.hypot(dx,dy)
    if length == 0: return
    for k in range(0, int(length), dash+gap):
        a,b = k/length, min(length,k+dash)/length
        d.line((p[0]+a*dx,p[1]+a*dy,p[0]+b*dx,p[1]+b*dy),fill=color,width=width)

def arrow(d,p,q,color,width=3,dash=False,head=10):
    if dash: dashed(d,p,q,color,width)
    else: d.line((p,q),fill=color,width=width)
    a=math.atan2(q[1]-p[1],q[0]-p[0])
    d.polygon([q,(q[0]-head*math.cos(a-.5),q[1]-head*math.sin(a-.5)),(q[0]-head*math.cos(a+.5),q[1]-head*math.sin(a+.5))],fill=color)

def tool(d,p):
    # Only the ideal cutting tip is dimensioned; this triangular glyph is schematic.
    x,y=p
    d.polygon([(x,y),(x+20,y-23),(x+35,y-4)],fill=INK)
    d.ellipse((x-4,y-4,x+4,y+4),fill=FEED,outline=BG,width=1)

def hatch_stock(im, poly):
    layer=Image.new('RGB',im.size,STEEL)
    ld=ImageDraw.Draw(layer)
    for k in range(-im.height,im.width,19):
        ld.line((k,0,k+im.height,im.height),fill=STEEL_LINE,width=1)
    mask=Image.new('L',im.size)
    ImageDraw.Draw(mask).polygon(poly,fill=255)
    im.paste(layer,(0,0),mask)
    ImageDraw.Draw(im).line(poly+[poly[0]],fill=MUTED,width=2)

def profile(z0,cy,unit,prev,current,cut_r,half=True):
    def p(z,r):return (z0-z*unit,cy-r*unit)
    # Rightmost portion was cut to r=4 in prior passes. The current layer is
    # progressively reduced from r=8 to r=4, as an ideal swept-volume projection.
    upper=[p(18,8),p(current,8),p(current,cut_r),p(prev,cut_r),p(prev,4),p(0,4)] if prev or cut_r < 8 else [p(18,8),p(0,8)]
    if half:return upper+[p(0,0),p(18,0)]
    lower=[(x,2*cy-y) for x,y in reversed(upper)]
    return upper+lower

def static_image():
    im=Image.new('RGB',(1200,1130),BG);d=ImageDraw.Draw(im)
    text(d,(46,26),'G94：一条指令，走完四段刀路',36)
    text(d,(46,78),'津上 S205A/S206A 手册原例｜单位 mm｜上半轴向剖面，理想刀尖相对工件运动',20,MUTED)
    text(d,(46,121),'G00 X16.6 Z-1.0;    G94 X8.0 Z4.0 F0.05;',25)
    z0,cy,u=970,495,32
    def p(z,x): return (z0-z*u,cy-x/2*u)
    # first-pass stock after cutting; faint envelope records the original Ø16 blank
    hatch_stock(im,profile(z0,cy,u,0,4,4))
    d=ImageDraw.Draw(im)
    for a,b in [(p(18,16),p(0,16)),(p(0,16),p(0,0))]:dashed(d,a,b,STEEL_LINE,2)
    text(d,(396,280),'原始 Ø16 毛坯',20,MUTED)
    text(d,(809,408),'保留 Ø8',20)
    dashed(d,p(19,0),p(-3,0),MUTED,2,12,6)
    arrow(d,(1070,555),(330,555),INK,2)
    text(d,(332,574),'+Z 向左（进入材料）',20)
    arrow(d,(1102,495),(1102,188),INK,2)
    text(d,(1074,165),'+X',21)
    for x in (0,8,16):
        y=p(0,x)[1]
        d.line((1096,y,1108,y),fill=INK,width=2)
        text(d,(1112,y-12),f'X{x}',18)
    for z in (0,4,8,12,16):
        xx=p(z,0)[0]
        d.line((xx,548,xx,562),fill=INK,width=2)
        text(d,(xx,517),str(z),19,anchor='mt')
    text(d,(1005,520),'Z / mm',18)
    A,B,C,D=p(-1,16.6),p(4,16.6),p(4,8),p(-1,8)
    arrow(d,A,B,RAPID,4,True)
    arrow(d,B,C,FEED,4)
    arrow(d,C,D,FEED,4)
    arrow(d,D,A,RAPID,4,True)
    for label,pt,offset in [('A',A,(11,-29)),('B',B,(-28,-29)),('C',C,(-27,7)),('D',D,(10,5))]:
        d.ellipse((pt[0]-4,pt[1]-4,pt[0]+4,pt[1]+4),fill=INK)
        text(d,(pt[0]+offset[0],pt[1]+offset[1]),label,24)
    text(d,(875,190),'① R',23,RAPID)
    text(d,(776,305),'② F',23,FEED)
    text(d,(875,396),'③ F',23,FEED)
    text(d,(1030,305),'④ R',23,RAPID)
    text(d,(45,200),'A 起点',23)
    text(d,(45,238),'X16.6 / Z-1.0',21)
    text(d,(45,300),'C 切削终点',23)
    text(d,(45,338),'X8.0 / Z4.0',21)
    text(d,(45,400),'R：快速（虚线）',21,RAPID)
    text(d,(45,437),'F：进给（实线）',21,FEED)
    text(d,(45,514),'X 为直径量',21)
    text(d,(45,550),'图中实体半径 = X ÷ 2',20,MUTED)
    # Four explicit operations: keeps the less obvious third feed unmistakable.
    yy=635
    steps=[('① Z 快速靠近','X16.6 / Z4.0',RAPID),('② X 径向切削','X8.0 / Z4.0',FEED),('③ Z 进给退回','X8.0 / Z-1.0',FEED),('④ X 快速返回','X16.6 / Z-1.0',RAPID)]
    for i,(title,coords,col) in enumerate(steps):
        xx=45+i*291
        text(d,(xx,yy),title,22,col)
        text(d,(xx,yy+37),coords,19)
    d.line((45,722,1155,722),fill=GRID,width=2)
    text(d,(45,747),'连续三刀后的形状',27)
    z0,cy,u=500,941,16
    hatch_stock(im,profile(z0,cy,u,12,12,4,False))
    d=ImageDraw.Draw(im)
    dashed(d,(190,cy),(540,cy),MUTED,2,10,5)
    arrow(d,(500,854),(308,854),INK,2,False,7)
    arrow(d,(308,854),(500,854),INK,2,False,7)
    text(d,(405,820),'12',21,anchor='mt')
    arrow(d,(550,cy-64),(550,cy+64),INK,2,False,7)
    arrow(d,(550,cy+64),(550,cy-64),INK,2,False,7)
    text(d,(563,cy-12),'Ø8',22)
    text(d,(640,821),'Z4.0;  →  Z8.0;  →  Z12.0;',26)
    text(d,(640,868),'每一行，都从 A 出发并回到 A。',23)
    text(d,(640,911),'X8.0 仍然保留 Ø8 轴颈，未车到中心。',21)
    text(d,(640,954),'16.6 → 8.0：实际径向行程为 4.3 mm。',21)
    text(d,(45,1083),'依据 §7.5.7.3，纸面 7-43（原 PDF 第311页）。教学示意；原例数值非切削条件推荐。',18,MUTED)
    path=ROOT/'静态刀路图.png';im.save(path)
    return path

def gif_frame(pass_i,seg,t,complete=False,initial=False):
    im=Image.new('RGB',(1000,680),BG);d=ImageDraw.Draw(im)
    text(d,(35,21),'G94 端面切削循环',31)
    text(d,(35,65),'上半轴向剖面｜刀尖相对工件｜+Z 向左｜X 为直径量 / mm',18,MUTED)
    target=(4,8,12)[pass_i];prev=target-4
    if initial:
        code='G00 X16.6 Z-1.0;'
        status='起点 A：X16.6 / Z-1.0'
    else:
        code=('G94 X8.0 Z4.0 F0.05;','Z8.0;','Z12.0;')[pass_i]
        name=('① Z 快速靠近 R','② X 径向切削 F','③ Z 进给退回 F','④ X 快速返回 R')[seg]
        status=f'第 {pass_i+1} 刀 / {name}'
        if complete:status='三刀完成：Ø8 轴颈，长12 mm；刀尖回到 A'
    text(d,(35,104),code,24)
    if pass_i and not initial:text(d,(235,109),'继承 G94、X8.0、F0.05',18,MUTED)
    text(d,(35,146),status,21)
    z0,cy,u=795,505,31
    def p(z,x):return (z0-z*u,cy-x/2*u)
    A,B,C,D=p(-1,16.6),p(target,16.6),p(target,8),p(-1,8)
    pts=[A,B,C,D,A]
    start,end=pts[seg],pts[seg+1]
    q=(start[0]+(end[0]-start[0])*t,start[1]+(end[1]-start[1])*t)
    if initial:q=A;prev=0;target=4;cut_r=8
    elif seg==0:cut_r=8
    elif seg==1:cut_r=min(8,max(4,(cy-q[1])/u))
    else:cut_r=4
    if complete:cut_r=4;q=A
    # Conceptual removed volume: a circumferential sweep, not a chip simulation.
    if prev:
        d.rectangle((p(prev,16),p(0,8)),fill=HILITE)
    if cut_r<8:
        d.rectangle((p(target,16),p(prev,cut_r*2)),fill=HILITE)
    hatch_stock(im,profile(z0,cy,u,prev,target,cut_r))
    d=ImageDraw.Draw(im)
    dashed(d,p(18,16),p(0,16),STEEL_LINE,2)
    dashed(d,p(0,16),p(0,0),STEEL_LINE,2)
    text(d,(255,290),'余料 Ø16',20,MUTED)
    text(d,(255,326),'浅橙：已去除投影',17,MUTED)
    arrow(d,(874,cy),(175,cy),INK,2)
    text(d,(177,520),'+Z',18)
    arrow(d,(874,cy),(874,210),INK,2)
    text(d,(861,185),'+X',19)
    for x in (0,8,16):
        y=p(0,x)[1]
        d.line((868,y,880,y),fill=INK,width=2)
        text(d,(887,y-12),f'X{x}',17)
    for z in (0,4,8,12,16):
        xx=p(z,0)[0]
        d.line((xx,499,xx,511),fill=INK,width=2)
        text(d,(xx,520),str(z),18,anchor='mt')
    for i in range(4):
        color=RAPID if i in (0,3) else FEED
        arrow(d,pts[i],pts[i+1],color,2,i in(0,3),8)
    if not initial and not complete:
        arrow(d,start,q,RAPID if seg in(0,3) else FEED,5,seg in(0,3),9)
    for label,pt,off in [('A',A,(5,-46)),('B',B,(-24,-46)),('C',C,(-25,7)),('D',D,(7,7))]:
        d.ellipse((pt[0]-3,pt[1]-3,pt[0]+3,pt[1]+3),fill=INK)
        text(d,(pt[0]+off[0],pt[1]+off[1]),label,21)
    tool(d,q)
    xv=(cy-q[1])/u*2;zv=(z0-q[0])/u
    text(d,(35,568),f'刀尖：X{xv:.2f}   Z{zv:.2f}',21)
    text(d,(450,568),'R 快速（虚线）   F 进给（实线）',19)
    text(d,(35,613),'第三段仍按 F 进给；每一刀结束都回到同一起点 A。',18)
    text(d,(35,647),'教学投影；不含刀尖R、机构和碰撞校验。原例数值非切削条件推荐。',16,MUTED)
    return im

def animation():
    frames=[];durations=[]
    def add(im,ms):
        frames.append(im);durations.append(ms)
    add(gif_frame(0,0,0,initial=True),1000)
    for pass_i in range(3):
        for seg,dur in enumerate((800,2100,1400,700)):
            n=dur//100
            for j in range(1,n+1):add(gif_frame(pass_i,seg,j/n),100)
    add(gif_frame(2,3,1,complete=True),4500)
    # Quantize against one global palette to avoid text and background flicker.
    sample=Image.new('RGB',(1000,2040),BG)
    for i,k in enumerate((0,22,len(frames)-1)):
        sample.paste(frames[k],(0,i*680))
    palette=sample.quantize(colors=128)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    path=ROOT/'G94三刀循环.gif'
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=1)
    frames[22].save(ROOT/'sources/G94动图检查帧.png')
    frames[-1].save(ROOT/'sources/G94动图最终帧.png')
    return path,len(frames),sum(durations)

if __name__=='__main__':
    print(static_image())
    print(animation())
