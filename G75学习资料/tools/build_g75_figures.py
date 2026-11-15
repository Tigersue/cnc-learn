from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(__file__).resolve().parents[1]
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
BG = '#f8fafc'
INK = '#172735'
MUTED = '#526574'
LINE = '#b8c8d1'
METAL = '#d6e0e5'
BLUE = '#126b9b'
ORANGE = '#ba5420'
GREEN = '#14735e'
PALE = '#e7f3f3'

def f(n):
    return ImageFont.truetype(FONT, n)

def txt(d, xy, s, size=27, color=INK, anchor=None):
    d.text(xy, s, font=f(size), fill=color, anchor=anchor)

def line(d, p, color=INK, width=3):
    d.line(p, fill=color, width=width)

def arrow(d, a, b, color=INK, width=3, head=12):
    line(d, [a,b], color, width)
    dx,dy = b[0]-a[0],b[1]-a[1]
    ln = math.hypot(dx,dy)
    if ln == 0: return
    ux,uy = dx/ln,dy/ln
    px,py = -uy,ux
    d.polygon([b,(b[0]-head*ux+head*.42*px,b[1]-head*uy+head*.42*py),(b[0]-head*ux-head*.42*px,b[1]-head*uy-head*.42*py)], fill=color)

def dashed(d,a,b,color=LINE,width=2,dash=9,gap=7):
    dx,dy=b[0]-a[0],b[1]-a[1]
    ln=math.hypot(dx,dy)
    if ln==0: return
    for k in range(0,int(ln),dash+gap):
        t=k/ln; u=min(k+dash,ln)/ln
        line(d,[(a[0]+t*dx,a[1]+t*dy),(a[0]+u*dx,a[1]+u*dy)],color,width)

def dim(d, a, b, label, vertical=False, color=MUTED, size=25):
    arrow(d,a,b,color,2,9); arrow(d,b,a,color,2,9)
    if vertical:
        txt(d,(a[0]-18,(a[1]+b[1])/2),label,size,color,anchor='rm')
    else:
        txt(d,((a[0]+b[0])/2,a[1]-12),label,size,color,anchor='mb')

def banner(d, title, subtitle, width=1600):
    txt(d,(70,44),title,43)
    txt(d,(72,111),subtitle,25,MUTED)
    line(d,[(70,159),(width-70,159)],LINE,2)

def fig_width():
    im=Image.new('RGB',(1600,1200),BG);d=ImageDraw.Draw(im)
    banner(d,'宽槽怎样算：刀具参考点 + 刀宽','教学假设｜主轴外圆 φ20 → 槽底 φ14；槽壁 Z10～Z16；刀宽 2 mm')
    # Isometric physical section: z increases to screen left.
    scale=37; x0=1350; cy=527
    X=lambda z:x0-z*scale
    Y=lambda r:cy-r*scale
    p=[(X(0),Y(10)),(X(10),Y(10)),(X(10),Y(7)),(X(16),Y(7)),(X(16),Y(10)),(X(26),Y(10)),(X(26),Y(-10)),(X(16),Y(-10)),(X(16),Y(-7)),(X(10),Y(-7)),(X(10),Y(-10)),(X(0),Y(-10))]
    # Main figure is cropped symmetrically in height to show upper half only.
    # Entire section at 0.6 vertical scale preserves diameter labels explicitly.
    sy=.61
    Y=lambda r:cy-r*scale*sy
    p=[(X(0),Y(10)),(X(10),Y(10)),(X(10),Y(7)),(X(16),Y(7)),(X(16),Y(10)),(X(26),Y(10)),(X(26),Y(-10)),(X(16),Y(-10)),(X(16),Y(-7)),(X(10),Y(-7)),(X(10),Y(-10)),(X(0),Y(-10))]
    d.polygon(p,fill=METAL,outline=INK,width=3)
    # Removed envelopes highlighted outside final contour.
    for r1,r2 in [(7,10),(-10,-7)]:
        box=(X(16),Y(r2),X(10),Y(r1))
        d.rectangle(box,fill=PALE)
        for xx in range(int(X(16))-80,int(X(10)),19):
            ax=max(xx,X(16));bx=min(xx+65,X(10))
            if bx>ax:
                y1=box[3]-(ax-xx);y2=box[3]-(bx-xx)
                # clip hatches to removal rectangle using a separate image mask below.
        # Simpler clipped hatch overlay.
        patch=Image.new('RGB',(int(box[2]-box[0])+1,int(box[3]-box[1])+1),PALE)
        q=ImageDraw.Draw(patch)
        for xx in range(-100,patch.width+100,19):q.line([(xx,patch.height),(xx+patch.height,0)],fill='#b2d4d1',width=2)
        im.paste(patch,(int(box[0]),int(box[1])))
    d.line(p+[p[0]],fill=INK,width=3)
    dashed(d,(X(27),cy),(X(-1.3),cy),MUTED,2)
    txt(d,(X(26),cy+18),'工件中心线',23,MUTED)
    txt(d,(X(0)+10,Y(10)-40),'右端面 Z0',25)
    dashed(d,(X(0),Y(11.5)),(X(0),Y(-11.5)),LINE,2)
    # Final blade at Z14 to Z16; reference is low-Z corner, screen right.
    zref=14
    d.rectangle((X(zref+2),Y(13.4),X(zref),Y(7)),fill=BLUE,outline=INK,width=2)
    d.ellipse((X(zref)-7,Y(7)-7,X(zref)+7,Y(7)+7),fill=ORANGE)
    arrow(d,(1100,228),(X(zref)+2,Y(7)-1),ORANGE,3)
    txt(d,(1110,198),'刀具参考点 Z14',26,ORANGE)
    txt(d,(1110,235),'低 Z 侧切刃角',23,MUTED)
    txt(d,(X(16)-18,Y(13.4)-30),'刀宽 2',25,BLUE)
    # Dimensional annotations.
    for z in [10,16]:line(d,[(X(z),Y(-10)-1),(X(z),823)],LINE,2)
    dim(d,(X(16),810),(X(10),810),'成槽宽 6 mm')
    txt(d,(X(16)-3,836),'Z16 槽壁',25,anchor='mt')
    txt(d,(X(10)+3,836),'Z10 槽壁',25,anchor='mt')
    dim(d,(X(26)-45,Y(10)),(X(26)-45,Y(-10)),'φ20',True)
    txt(d,(X(20),cy-35),'保留材料',27,MUTED,anchor='mm')
    txt(d,(X(13),cy),'槽底 φ14',25,anchor='mm')
    # Axis keys, relative paths only.
    arrow(d,(1440,555),(1440,426),INK,3)
    arrow(d,(1440,555),(1300,555),INK,3)
    txt(d,(1440,399),'+X',27,anchor='mm')
    txt(d,(1290,588),'+Z',27,anchor='mm')
    txt(d,(1430,625),'X 用直径值',23,MUTED,anchor='mm')
    txt(d,(73,898),'刀具覆盖范围',29)
    txt(d,(430,900),'步距 1.5、1.5、1.0（末步缩短）；前两次重叠 0.5 mm',25,MUTED)
    # Coverage lanes; z10..16 increases to left and labels split to the right.
    xref=1130; s=86; l=lambda z:xref-(z-10)*s
    ytop=955
    refs=[10,11.5,13,14]
    for i,z in enumerate(refs):
        yy=ytop+i*43
        d.rectangle((l(16),yy,l(10),yy+25),fill='#edf1f4')
        d.rectangle((l(z+2),yy,l(z),yy+25),fill=BLUE)
        d.ellipse((l(z)-4,yy+8,l(z)+4,yy+16),fill=ORANGE)
        txt(d,(1180,yy+12),f'第 {i+1} 列：Z{z:g}～Z{z+2:g}',24,anchor='lm')
        txt(d,(74,yy+12),f'参考点 Z{z:g}',25,anchor='lm')
    txt(d,(74,1140),'|Z终点 14 − Z起点 10| + 刀宽 2 = 槽宽 6 mm',30,BLUE)
    txt(d,(1530,1172),'侧视剖面纵向压缩示意；尖角为名义轮廓；刀具相对工件运动',21,MUTED,anchor='rb')
    im.save(OUT/'g75-槽宽与刀具基准.png')

def fig_peck():
    im=Image.new('RGB',(1600,1130),BG);d=ImageDraw.Draw(im)
    banner(d,'P 与 R：径向走 0.5，X 直径减 1.0','教学假设｜公制 IS-B：P500 = 0.500 mm；第一行 R0.2 = 径向回退 0.200 mm')
    left,right,top,bot=130,1110,230,800
    xx=lambda i:left+i/16*(right-left)
    yy=lambda v:bot-(v-14)/8*(bot-top)
    for v in range(14,23):
        line(d,[(left,yy(v)),(right,yy(v))],LINE,1)
        txt(d,(left-18,yy(v)),f'{v:.0f}',24,MUTED,anchor='rm')
    d.rectangle((left,yy(20),right,yy(14)),fill='#f3e6dc')
    for v in range(14,21):line(d,[(left,yy(v)),(right,yy(v))],LINE,1)
    dashed(d,(left,yy(20)),(right,yy(20)),ORANGE,3)
    txt(d,(right-20,yy(20)-18),'外圆 φ20',25,ORANGE,anchor='rb')
    arrow(d,(left,bot+3),(left,top-20),INK,3)
    arrow(d,(left,bot),(right+25,bot),INK,3)
    txt(d,(74,187),'X直径 / mm',27)
    txt(d,((left+right)/2,bot+50),'动作顺序（横向不是机床 Z 运动）',25,MUTED,anchor='mm')
    pts=[(0,22)]
    cur=22
    for i,target in enumerate(range(21,13,-1)):
        k=2*i+1
        a=(xx(k-1),yy(cur));b=(xx(k),yy(target))
        col=BLUE if target>=20 else ORANGE
        arrow(d,a,b,col,4,11)
        d.ellipse((b[0]-5,b[1]-5,b[0]+5,b[1]+5),fill=col)
        txt(d,(b[0]-5,b[1]+23),f'{target}',23,anchor='mt')
        if target>14:
            c=(xx(k+1),yy(target+.4))
            arrow(d,b,c,GREEN,3,10)
            cur=target+.4
    # Explanatory block, no data marks hidden by prose.
    txt(d,(1190,300),'看这一组',30)
    txt(d,(1190,359),'X19.0',33,ORANGE)
    txt(d,(1190,410),'↓ 快退 R0.2',26,GREEN)
    txt(d,(1190,460),'X19.4',33,GREEN)
    txt(d,(1190,511),'↓ 下一次进给',26,ORANGE)
    txt(d,(1190,561),'X18.0',33,ORANGE)
    txt(d,(1190,635),'回退：ΔX = +0.4',24)
    txt(d,(1190,677),'新深度：ΔX = −1.0',24)
    txt(d,(1190,732),'本次进给走 0.7 mm',24)
    txt(d,(1190,769),'= 重走 0.2 + 新增 0.5',23,MUTED)
    txt(d,(130,913),'● 前两次到 X21、X20：只走起点与毛坯之间的间隙',27,BLUE)
    txt(d,(130,963),'● 以后每次新增单边 0.5 mm，直到 X14；到槽底后快退至 X22',27,ORANGE)
    txt(d,(130,1013),'● 第二行 R0：本例槽底不作 Z 向让刀；它与第一行 R0.2 含义不同',27)
    txt(d,(1530,1092),'实线箭头 = 进给；绿色上行箭头 = 快速回退；运动顺序示意，非时间比例',23,MUTED,anchor='rb')
    im.save(OUT/'g75-P与R分步.png')

def animation():
    W,H=1200,780
    # Each motion has a caption, start/end X (diameter), and a pedagogic duration.
    seg=[(22,22,.8,'setup','循环起点：X22.0、Z10.0；单边间隙 1 mm')];cur=22
    for i,target in enumerate(range(21,13,-1)):
        seg.append((cur,target,0.95,'feed',f'第 {i+1} 次进给：目标 X{target:.1f}'))
        cur=target
        if target>14:
            seg.append((cur,cur+.4,0.45,'rapid',f'断屑快退：径向 0.2 mm，X 回升 0.4'))
            cur+=.4
    seg.append((14,22,1.25,'rapid','槽底到达 X14：快速退回循环起点 X22'))
    seg.append((22,22,4.0,'end','单槽完成：X22.0、Z10.0；实际槽宽 2 mm'))
    fps=12
    frames=[];deepest=22
    for a,b,dur,kind,caption in seg:
        for j in range(max(2,round(dur*fps))):
            t=(j+1)/max(2,round(dur*fps));x=a+(b-a)*t
            if kind=='feed':deepest=min(deepest,x)
            im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
            txt(d,(46,26),'G75 单槽啄切：X 是直径，P 是径向量',34)
            txt(d,(48,81),'教学设定：φ20 → φ14｜刀宽 2｜Z10｜P500｜R0.2｜第二行 R0',23,MUTED)
            line(d,[(46,125),(W-46,125)],LINE,2)
            # Physical upper half section. Z0 at right, +Z to left.
            sx=36;sy=30;origin=1030;cy=638
            X=lambda z:origin-z*sx
            Y=lambda r:cy-r*sy
            d.rectangle((X(24),Y(10),X(0),cy),fill=METAL,outline=INK,width=3)
            cutr=min(10,deepest/2)
            if cutr<10:
                d.rectangle((X(12),Y(10)-1,X(10),Y(cutr)),fill=BG)
                line(d,[(X(12),Y(10)),(X(12),Y(cutr)),(X(10),Y(cutr)),(X(10),Y(10))],INK,3)
            # Final nominal bottom and material surface.
            dashed(d,(X(13.3),Y(7)),(X(8.8),Y(7)),LINE,2)
            txt(d,(X(13.5),Y(7)),'槽底 φ14',23,MUTED,anchor='rm')
            txt(d,(X(24),Y(10)-21),'外圆 φ20',23,MUTED)
            dashed(d,(X(24.7),cy),(X(-.5),cy),MUTED,2)
            txt(d,(X(0)+15,cy),'Z0',24,anchor='lm')
            # Blade bottom, reference at low-Z/right corner.
            col=GREEN if kind in ('rapid','end') else ORANGE
            tipY=Y(x/2)
            d.rectangle((X(12),tipY-148,X(10),tipY),fill=BLUE,outline=INK,width=2)
            d.ellipse((X(10)-5,tipY-5,X(10)+5,tipY+5),fill=ORANGE)
            # Current direction arrow by blade.
            if kind not in ('end','setup'):
                ay=tipY-57 if kind=='feed' else tipY+44
                by=tipY+13 if kind=='feed' else tipY-26
                arrow(d,(X(10)+35,ay),(X(10)+35,by),col,4,11)
            txt(d,(810,187),f'X {x:05.2f}',43,col)
            txt(d,(812,247),'直径显示 / mm',22,MUTED)
            txt(d,(48,184),'进给切入' if kind=='feed' else ('已完成' if kind=='end' else ('循环起点' if kind=='setup' else '快速回退')),30,col)
            txt(d,(48,234),'刀尖相对工件运动',23,MUTED)
            # True small clearance radius dimension at start.
            txt(d,(X(10)+50,tipY),'参考点',22,ORANGE,anchor='lm')
            for z in (10,12):line(d,[(X(z),cy+10),(X(z),cy+42)],LINE,2)
            dim(d,(X(12),cy+35),(X(10),cy+35),'2 mm',False,size=22)
            txt(d,(X(10)+8,cy+68),'Z10',23,anchor='mt')
            txt(d,(X(12)-8,cy+68),'Z12',23,anchor='mt')
            arrow(d,(1030,575),(916,575),INK,3)
            txt(d,(910,580),'+Z',22,anchor='rt')
            arrow(d,(1095,576),(1095,469),INK,3)
            txt(d,(1095,450),'+X',22,anchor='mm')
            txt(d,(48,726),caption,27,col)
            txt(d,(1154,771),'动作示意，非真实速度；不代替 CNC 仿真',21,MUTED,anchor='rb')
            frames.append(im)
    # Single play; no GIF loop extension means it ends on the last frame.
    frames[0].save(OUT/'g75-单槽啄切.gif',save_all=True,append_images=frames[1:],duration=round(1000/fps),optimize=True,disposal=2)
    for idx,name in [(1,'start'),(len(frames)//2,'mid'),(len(frames)-1,'end')]:
        frames[idx].save(OUT/'tools'/f'gif-review-{name}.png')
    return len(frames)

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    fig_width();fig_peck();n=animation()
    print(f'Created 2 PNGs and {n} GIF frames in {OUT}')
