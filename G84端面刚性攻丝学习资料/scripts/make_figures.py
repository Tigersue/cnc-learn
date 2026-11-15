from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
FONT = '/System/Library/Fonts/PingFang.ttc'
INK = '#183040'
MUTED = '#536878'
BLUE = '#23779A'
BLUE_LIGHT = '#D8EBF2'
ORANGE = '#BA7018'
ORANGE_LIGHT = '#EFCB8B'
GREEN = '#277E63'
GRAY = '#D8E0E6'
BG = '#FFFFFF'

def font(size):
    return ImageFont.truetype(FONT, size)

def txt(d, xy, s, size=26, fill=INK, anchor=None):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor)

def line(d, points, fill=MUTED, width=2):
    d.line(points, fill=fill, width=width)

def dashed(d, xy, fill=GRAY, dash=10, gap=7, width=2):
    x1,y1,x2,y2=xy
    length=math.hypot(x2-x1,y2-y1)
    if length == 0: return
    for a in range(0,int(length),dash+gap):
        b=min(a+dash,length)
        d.line((x1+(x2-x1)*a/length,y1+(y2-y1)*a/length,
                x1+(x2-x1)*b/length,y1+(y2-y1)*b/length),fill=fill,width=width)

def arrow(d, p1, p2, fill=BLUE, width=4, head=12):
    d.line([p1,p2],fill=fill,width=width)
    a=math.atan2(p2[1]-p1[1],p2[0]-p1[0])
    d.polygon([p2,(p2[0]-head*math.cos(a-.5),p2[1]-head*math.sin(a-.5)),
                 (p2[0]-head*math.cos(a+.5),p2[1]-head*math.sin(a+.5))],fill=fill)

def dimension(d,x1,x2,y,label,color=INK):
    for x in [x1,x2]:line(d,(x,y-10,x,y+10),color,2)
    line(d,(x1,y,x2,y),color,2)
    if x2-x1>40:
        arrow(d,(x1+20,y),(x1,y),color,2,8)
        arrow(d,(x2-20,y),(x2,y),color,2,8)
    txt(d,((x1+x2)/2,y-16),label,24,color,'ms')

def machine(d,cy,z,tip=830,scale=30,angle=0,small=False):
    """Actual sliding-head motion: workpiece face moves +X on paper as Z1 grows."""
    face=tip+z*scale
    barlen=400 if not small else 340
    left=face-barlen
    spindle_left=left-150
    # Main spindle housing translates together with the workpiece.
    d.rounded_rectangle((spindle_left,cy-73,left+10,cy+73),10,fill='#E6EDF1',outline=MUTED,width=2)
    d.rectangle((left-22,cy-57,left+22,cy+57),fill='#95ACB9',outline=MUTED,width=2)
    # A cutaway of the pre-drilled workpiece; bore extends beyond the illustrated tapping limit.
    d.rectangle((left,cy-48,face,cy+48),fill=BLUE_LIGHT,outline=BLUE,width=3)
    bore_left=face-(310 if not small else 255)
    d.rectangle((bore_left,cy-20,face+2,cy+20),fill=BG)
    line(d,(bore_left,cy-20,face,cy-20),BLUE,2)
    line(d,(bore_left,cy+20,face,cy+20),BLUE,2)
    line(d,(bore_left,cy-20,bore_left,cy+20),BLUE,2)
    # Hatch marks on the material only.
    for x in range(int(left+12),int(face-12),28):
        line(d,(x,cy-45,x+20,cy-24),'#A9CAD8',1)
        line(d,(x,cy+24,x+20,cy+45),'#A9CAD8',1)
    # Stationary tool holder and left-pointing tap.
    thread_end=tip+(275 if not small else 245)
    holder_left=thread_end+70
    d.rectangle((thread_end,cy-14,holder_left+30,cy+14),fill='#CCD4D9',outline=MUTED,width=2)
    d.polygon([(tip,cy-7),(tip+42,cy-17),(thread_end,cy-17),(thread_end,cy+17),
               (tip+42,cy+17),(tip,cy+7)],fill=ORANGE_LIGHT,outline=ORANGE,width=2)
    # Thread tooth marks remain fixed; only the workpiece turns.
    for x in range(int(tip+40),int(thread_end-8),14):
        line(d,(x,cy-17,x+10,cy+17),ORANGE,2)
    line(d,(tip+15,cy,thread_end,cy),'#A36114',2)
    d.rounded_rectangle((holder_left,cy-51,holder_left+110,cy+51),7,fill='#DCE2E7',outline=MUTED,width=2)
    d.rectangle((holder_left+38,cy+51,holder_left+75,cy+79),fill='#AAB9C3',outline=MUTED,width=2)
    # Programmed center line X0.
    dashed(d,(spindle_left-15,cy,holder_left+128,cy),'#9BAEB9',dash=12,gap=8,width=1)
    # Rotation marker is a small end-view inset in the spindle housing.
    cx=spindle_left+65
    rr=31
    d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=BG,outline=BLUE,width=3)
    px=cx+24*math.cos(angle); py=cy+24*math.sin(angle)
    line(d,(cx,cy,px,py),BLUE,4)
    d.ellipse((px-4,py-4,px+4,py+4),fill=BLUE)
    return dict(face=face,left=left,spindle_left=spindle_left,holder_left=holder_left)

def static():
    im=Image.new('RGB',(1500,1150),BG);d=ImageDraw.Draw(im)
    txt(d,(65,35),'主轴端面刚性攻丝：实际动的是工件',44)
    txt(d,(65,99),'侧视剖面示意  ·  左侧主轴夹持工件  ·  右侧丝锥固定、不旋转',26,MUTED)
    arrow(d,(545,160),(760,160),BLUE)
    txt(d,(545,145),'Z1＋：主轴箱与工件向右',24,BLUE,'ls')
    txt(d,(1130,165),'固定刀座',24,MUTED)
    for i,(cy,z,title,sub) in enumerate([
            (320,-1,'① 起始：Z－1.0','端面在丝锥尖端左侧 1 mm'),
            (590,0,'② 接触：Z0','端面与丝锥尖端对齐'),
            (860,6,'③ 终点：Z6.0','名义插入端面以内 6 mm')]):
        if i%2==0:d.rectangle((45,cy-112,1455,cy+129),fill='#F6F9FB')
        txt(d,(65,cy-113),title,29)
        pos=machine(d,cy,z)
        # Left-side labels are below the diagram to keep the end-view marker clear.
        txt(d,(pos['spindle_left']+65,cy+84),'主轴箱',23,MUTED,'mt')
        txt(d,(pos['left']+175,cy+64),'工件（预制底孔）',23,BLUE,'mt')
        txt(d,(1175,cy+86),'丝锥始终固定',23,ORANGE,'mt')
        if z==6:
            dimension(d,830,pos['face'],cy-78,'名义 6 mm')
        if z==-1:
            # Tiny clearance is directly labeled with a leader.
            line(d,(815,cy-4,815,cy-62,925,cy-62),INK,2)
            txt(d,(935,cy-79),'间隙 1 mm',24)
        if z==0:
            line(d,(830,cy-55,830,cy-83),INK,2)
            txt(d,(830,cy-90),'端面接触',24,INK,'ms')
    txt(d,(65,1022),'X0：丝锥与主轴中心线重合。  从 Z－1 到 Z6 的轴向总行程为 7 mm。',27)
    txt(d,(65,1070),'教学假设：端面为 Z0、刀补正确；示意非比例。完整牙深受丝锥切削锥影响，底孔需另留余量。',23,MUTED)
    im.save(ROOT/'图片'/'G84主轴端面攻丝_三个位置.png')

def animation_frame(z,angle,phase,code,idx,progress):
    im=Image.new('RGB',(1200,760),BG);d=ImageDraw.Draw(im)
    txt(d,(44,29),'G84：主轴旋转 + Z1 同步进退',37)
    txt(d,(44,85),'侧视剖面示意  ·  工件随主轴箱移动，丝锥保持固定',25,MUTED)
    txt(d,(44,142),f'当前 Z = {z:+.2f} mm',31)
    txt(d,(670,147),'S600  ·  F1.25 mm/rev',28)
    if phase=='同步攻入':
        arrow(d,(460,219),(610,219),BLUE)
        txt(d,(460,202),'Z1＋',24,BLUE,'ls')
    elif phase=='反转退出':
        arrow(d,(610,219),(460,219),GREEN)
        txt(d,(460,202),'Z1－',24,GREEN,'ls')
    else:
        txt(d,(460,202),'轴向停止',24,MUTED,'ls')
    pos=machine(d,345,z,tip=650,scale=22,angle=angle,small=True)
    txt(d,(pos['spindle_left']+65,443),'主轴箱',23,MUTED,'mt')
    txt(d,(pos['left']+170,417),'工件 / 底孔',23,BLUE,'mt')
    txt(d,(1040,443),'固定刀座',23,MUTED,'mt')
    txt(d,(850,251),'固定丝锥，不旋转',24,ORANGE,'mt')
    txt(d,(pos['spindle_left']+65,273),'旋转标记',21,BLUE,'ms')
    # Current stage is clear, and the animation deliberately avoids specifying a CW viewpoint.
    stage_color=BLUE if phase=='同步攻入' else GREEN if phase=='反转退出' else INK
    txt(d,(44,511),phase,33,stage_color)
    txt(d,(300,518),code,25)
    descriptors={
        '起始准备':'主轴与轴向暂时停止；起点 Z－1.0。',
        '同步攻入':'主轴正转，Z1 向右：每转 1 圈，轴向前进 1.25 mm。',
        '孔底延时':'攻入到 Z6.0，旋转与轴向停止；执行 P100 延时。',
        '反转退出':'主轴反转，Z1 向左：沿原螺纹同步退出。',
        '回到起点':'已退回 Z－1.0；随后 G80 取消攻丝循环。'
    }
    txt(d,(44,574),descriptors[phase],25)
    barx=44; bary=639; barw=1112
    d.rectangle((barx,bary,barx+barw,bary+6),fill='#E4EBEF')
    d.rectangle((barx,bary,barx+barw*progress,bary+6),fill=stage_color)
    txt(d,(44,682),'教学慢放：未模拟加减速；孔底延时仅作示意。尺寸和刀具外形非比例。',22,MUTED)
    txt(d,(44,716),'假设：端面 Z0、刀补正确；名义深度不等于完整牙有效深度。',22,MUTED)
    return im

def animation():
    seq=[]
    for i in range(10):seq.append((-1,0,'起始准备','M29 S600 → G84 Z6.0 P100 F1.25'))
    n=64
    for i in range(n):
        z=-1+7*(i+1)/n
        # Exactly 1.25 mm per revolution of the marker, including the air approach.
        angle=(z+1)/1.25*2*math.pi
        seq.append((z,angle,'同步攻入','G84 Z6.0 P100 F1.25'))
    maxangle=7/1.25*2*math.pi
    for i in range(12):seq.append((6,maxangle,'孔底延时','P100'))
    for i in range(n):
        z=6-7*(i+1)/n
        angle=(z+1)/1.25*2*math.pi
        seq.append((z,angle,'反转退出','G84 循环内部自动反转退回'))
    for i in range(10):seq.append((-1,0,'回到起点','G80'))
    frames=[animation_frame(z,a,p,c,i,i/(len(seq)-1)) for i,(z,a,p,c) in enumerate(seq)]
    frames[47].save(ROOT/'图片'/'G84攻丝动画_关键帧.png')
    frames[79].save(ROOT/'图片'/'G84攻丝动画_孔底帧.png')
    frames[0].save(ROOT/'动图'/'G84主轴端面刚性攻丝_同步攻入反转退出.gif',save_all=True,
                   append_images=frames[1:],duration=65,loop=0,optimize=True,disposal=2)
    print('Saved static figure, GIF, and review frames to',ROOT)

if __name__=='__main__':
    static();animation()
