from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT=Path(__file__).resolve().parents[1]
FONT='/System/Library/Fonts/PingFang.ttc'
INK='#173244'
MUTED='#566C79'
BLUE='#27799A'
BLUELIGHT='#DCECF3'
ORANGE='#B86B13'
AMBER='#F0CD91'
GREEN='#2D8067'
GRAY='#DDE5EB'
BG='#FFFFFF'

def f(size):return ImageFont.truetype(FONT,size)
def text(d,xy,s,size=26,fill=INK,anchor=None):d.text(xy,s,font=f(size),fill=fill,anchor=anchor)
def line(d,xy,fill=MUTED,width=2):d.line(xy,fill=fill,width=width)
def dashed(d,xy,fill=GRAY,width=2,dash=10,gap=7):
    x1,y1,x2,y2=xy
    L=math.hypot(x2-x1,y2-y1)
    for a in range(0,int(L),dash+gap):
        b=min(a+dash,L)
        d.line((x1+(x2-x1)*a/L,y1+(y2-y1)*a/L,x1+(x2-x1)*b/L,y1+(y2-y1)*b/L),fill=fill,width=width)
def arrow(d,a,b,color=BLUE,width=4):
    line(d,(a,b),color,width)
    t=math.atan2(b[1]-a[1],b[0]-a[0]);H=12
    d.polygon([b,(b[0]-H*math.cos(t-.5),b[1]-H*math.sin(t-.5)),(b[0]-H*math.cos(t+.5),b[1]-H*math.sin(t+.5))],fill=color)

def assembly(d,x,base,p,angle,axis,drive,holder,phase,static=False):
    """Local section only: horizontal work axis, vertical hole axis.

    The diagram deliberately does not assert machine-wide X/Y orientation.
    p is a normalized illustration state, never a real coordinate or dimension.
    """
    top=base+165
    bottom=top+125
    holebottom=bottom-18
    wx1=x-330;wx2=x+185
    # Stationary workpiece, held at a fixed angular position.
    d.rectangle((wx1,top,wx2,bottom),fill=BLUELIGHT,outline=BLUE,width=3)
    for xx in range(int(wx1+10),int(wx2-10),24):
        if not (x-38<xx<x+22):
            line(d,(xx,top+3,xx+20,top+23),'#B5D0DC',1)
            line(d,(xx,bottom-23,xx+20,bottom-3),'#B5D0DC',1)
    # Pre-drilled blind side hole, deeper than the illustrated tapping end plane.
    d.polygon([(x-23,top-1),(x+23,top-1),(x+23,holebottom),(x,holebottom+15),(x-23,holebottom)],fill=BG)
    line(d,[(x-23,top),(x-23,holebottom),(x,holebottom+15),(x+23,holebottom),(x+23,top)],BLUE,2)
    # The clamp is a symbol for the stated holding spindle, not a machine layout.
    d.rectangle((wx1-70,top-14,wx1+40,bottom+14),fill='#E2E9EE',outline=MUTED,width=2)
    d.rectangle((wx1+20,top-14,wx1+50,top+30),fill='#9CB2BF',outline=MUTED,width=2)
    d.rectangle((wx1+20,bottom-30,wx1+50,bottom+14),fill='#9CB2BF',outline=MUTED,width=2)
    dashed(d,(wx1-92,top+63,wx2+35,top+63),'#9AB0BD',width=1)
    dashed(d,(x,base-20,x,holebottom+34),'#9AB0BD',width=1)
    # Tap and powered holder move along the hole axis.
    tip=top-31+p*100
    bodytop=tip-150
    d.rounded_rectangle((x-47,bodytop,x+47,bodytop+75),8,fill='#E4EAEE',outline=MUTED,width=2)
    d.rectangle((x-18,bodytop+75,x+18,tip-70),fill='#C6D0D7',outline=MUTED,width=2)
    d.polygon([(x-20,tip-79),(x+20,tip-79),(x+20,tip-25),(x+9,tip),(x-9,tip),(x-20,tip-25)],fill=AMBER,outline=ORANGE,width=2)
    # Rotation can be read both from this end-view marker and the moving flute.
    cx=x;cy=bodytop+37;rr=25
    d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=BG,outline=ORANGE,width=2)
    px=cx+19*math.cos(angle);py=cy+19*math.sin(angle)
    line(d,((cx,cy),(px,py)),ORANGE,4)
    d.ellipse((px-3,py-3,px+3,py+3),fill=ORANGE)
    for yy in range(int(tip-75),int(tip-23),10):
        shift=math.sin(angle)*5
        line(d,(x-19,yy,x+19,yy+8),ORANGE,2)
        line(d,(x+shift,yy,x+shift,yy+8),'#8B5012',2)
    text(d,(x+75,bodytop+10),drive+' 旋转丝锥',25,ORANGE)
    text(d,(x+75,bodytop+47),'旋转标记（端视）',20,MUTED)
    # The axis arrow indicates local feed only, without asserting + or -.
    ax=x-90
    if phase in ('同步攻入','起始'):
        arrow(d,(ax,top-100),(ax,top-12),BLUE)
    elif phase=='反向同步退出':
        arrow(d,(ax,top-12),(ax,top-100),GREEN)
    else:
        line(d,(ax-10,top-63,ax+10,top-63),MUTED,3)
        line(d,(ax-10,top-53,ax+10,top-53),MUTED,3)
    text(d,(ax-20,top-93),axis,27,BLUE,'rs')
    text(d,(ax-20,top-57),'孔轴进退',22,MUTED,'rs')
    text(d,(wx1-16,bottom+30),holder+'夹持工件',25,BLUE)
    text(d,(wx1-16,bottom+67),'工件保持角度，不随攻丝连续旋转',23,MUTED)
    text(d,(wx2+20,top+70),'工件轴线',21,MUTED,'ls')
    # This label remains out of the moving holder's path.
    text(d,(x+34,holebottom+12),'预制侧孔',22,MUTED)

def static():
    im=Image.new('RGB',(1500,1190),BG);d=ImageDraw.Draw(im)
    text(d,(55,30),'前驱、背驱横向刚性攻丝：丝锥旋转并进给',40)
    text(d,(55,94),'局部孔轴剖视，不代表刀座实际朝向；两图各自取景，非比例。',26,MUTED)
    for k,(code,drive,axis,holder,head) in enumerate([
        ('G184','CDF','X1','主轴','前驱 / 横向（前面）'),
        ('G186','BD','Y2','副主轴','背驱 / 背面横向')]):
        y=165+k*450
        if k==0:d.rectangle((40,y-5,1460,y+430),fill='#F7FAFB')
        text(d,(60,y+8),code+'  '+head,31)
        text(d,(60,y+62),'旋转对象：丝锥',25,ORANGE)
        text(d,(60,y+101),'进给轴：'+axis,25,BLUE)
        text(d,(60,y+150),'夹持对象：工件',25,BLUE)
        assembly(d,880,y+20,.72,.8,axis,drive,holder,'同步攻入',True)
    text(d,(55,1090),'共同动作：正转同步攻入 → 停止 / 延时 → 反向同步退出。',28)
    text(d,(55,1139),'每转前进一个导程，退出同样保持同步；图中箭头只表示各自孔轴方向，不标机床实际轴正负。',23,MUTED)
    im.save(ROOT/'图片'/'G184_G186_动力头与进给轴对照.png')

def frame(p,angle,phase,progress):
    im=Image.new('RGB',(1260,1120),BG);d=ImageDraw.Draw(im)
    text(d,(42,25),'横向刚性攻丝：工件定角度，动力头带丝锥转',34)
    text(d,(42,80),'局部孔轴剖视，不代表刀座实际朝向；两图各自取景，非比例。',23,MUTED)
    for k,(code,drive,axis,holder) in enumerate([('G184','CDF','X1','主轴'),('G186','BD','Y2','副主轴')]):
        y=137+k*399
        text(d,(42,y+3),code,31)
        text(d,(42,y+51),drive+' 旋转',25,ORANGE)
        text(d,(42,y+93),axis+' 同步进退',25,BLUE)
        assembly(d,705,y+5+(15 if k else 0),p,angle,axis,drive,holder,phase)
        if k==0:line(d,(42,y+393,1218,y+393),GRAY,2)
    color=BLUE if phase=='同步攻入' else GREEN if phase=='反向同步退出' else INK
    display_phase='正转同步攻入' if phase=='同步攻入' else '反转同步退出' if phase=='反向同步退出' else phase
    text(d,(42,977),display_phase,31,color)
    descriptor={
        '起始':'沿各自孔轴准备；工件保持夹紧和角度。',
        '同步攻入':'丝锥每转一圈，沿孔轴前进一个导程。',
        '停止 / 延时':'到攻丝底面，旋转和进给停止，执行延时。',
        '反向同步退出':'丝锥反转，沿已加工的螺纹同步退出。',
        '退回起点':'丝锥退出；工件始终保持角度。'
    }[phase]
    text(d,(340,985),descriptor,24)
    d.rectangle((42,1041,1218,1047),fill=GRAY)
    d.rectangle((42,1041,42+1176*progress,1047),fill=color)
    text(d,(42,1075),'教学慢放；无转速、尺寸和实际坐标设定。箭头仅表示各自孔轴的攻入 / 退出。',22,MUTED)
    return im

def animation():
    seq=[]
    for _ in range(8):seq.append((0,0,'起始'))
    for i in range(55):
        p=(i+1)/55
        seq.append((p,p*5*math.tau,'同步攻入'))
    for _ in range(12):seq.append((1,5*math.tau,'停止 / 延时'))
    for i in range(55):
        p=1-(i+1)/55
        seq.append((p,p*5*math.tau,'反向同步退出'))
    for _ in range(8):seq.append((0,0,'退回起点'))
    frames=[frame(p,a,phase,i/(len(seq)-1)) for i,(p,a,phase) in enumerate(seq)]
    for i,name in [(37,'G184_G186_同步攻入帧'),(67,'G184_G186_停止延时帧'),(102,'G184_G186_反向退出帧')]:
        frames[i].save(ROOT/'图片'/(name+'.png'))
    # A shared palette preserves colors and allows compact frame differences.
    probe=Image.new('RGB',(1260,3360),BG)
    for j,i in enumerate((0,37,102)):probe.paste(frames[i],(0,j*1120))
    palette=probe.quantize(colors=128,method=Image.Quantize.MEDIANCUT)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(ROOT/'动图'/'G184_G186_旋转丝锥同步进退.gif',save_all=True,
                   append_images=indexed[1:],duration=70,loop=0,optimize=True,disposal=1)
    print('Saved G184 / G186 figures to',ROOT)

if __name__=='__main__':static();animation()
