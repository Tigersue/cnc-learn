from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / '图解'
ANIM = ROOT / '动图'
FIG.mkdir(exist_ok=True)
ANIM.mkdir(exist_ok=True)
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
W, H = 1100, 760
BG = '#FBFCFE'
INK = '#173849'
MUTED = '#536D7D'
GRID = '#CBD7DF'
METAL = '#DDE7EC'
CUT = '#0A779F'
RAPID = '#B86218'
GREEN = '#157657'
RED = '#B24947'
OLD = '#9CB7C8'


def ft(n):
    return ImageFont.truetype(FONT, n)


def txt(d, p, s, n=24, fill=INK, anchor=None):
    d.text(p, s, font=ft(n), fill=fill, anchor=anchor)


def line(d, a, b, fill=GRID, width=2, dash=9, gap=7):
    dx, dy = b[0]-a[0], b[1]-a[1]
    dist = math.hypot(dx, dy)
    if not dist:
        return
    for k in range(0, int(dist), dash+gap):
        lo, hi = k/dist, min(k+dash, dist)/dist
        d.line([(a[0]+lo*dx, a[1]+lo*dy), (a[0]+hi*dx, a[1]+hi*dy)], fill=fill, width=width)


def arrow(d, a, b, fill=INK, width=3, head=10, both=False):
    d.line([a, b], fill=fill, width=width)
    def head_at(start, end):
        dx, dy = end[0]-start[0], end[1]-start[1]
        length = math.hypot(dx, dy)
        if length < 1:
            return
        ux, uy = dx/length, dy/length
        d.polygon([end, (end[0]-head*ux-head*.45*uy, end[1]-head*uy+head*.45*ux),
                   (end[0]-head*ux+head*.45*uy, end[1]-head*uy-head*.45*ux)], fill=fill)
    head_at(a, b)
    if both:
        head_at(b, a)


def header(d, title, sub):
    txt(d, (38, 24), title, 33)
    txt(d, (40, 73), sub, 21, MUTED)
    d.line([(40, 112), (1060, 112)], fill=GRID, width=2)


def comparison():
    im = Image.new('RGB', (1100, 790), BG)
    d = ImageDraw.Draw(im)
    header(d, '内牙与外牙：材料在刀尖哪一侧？', '轴向剖面简图｜上侧 +X 刀尖｜X 按直径给值｜只比较径向动作')
    # External: metal toward the centre. Cutting heads toward decreasing X.
    txt(d, (40, 138), '外螺纹：在棒料外面切', 27)
    d.rectangle((200, 231, 660, 332), fill=METAL)
    d.line([(200, 231), (660, 231), (660, 332)], fill=INK, width=2)
    txt(d, (230, 289), '材料在表面内侧', 22, MUTED)
    line(d, (170, 355), (700, 355))
    txt(d, (180, 359), '轴线', 19, MUTED)
    for i, y in enumerate((244, 267, 286)):
        d.line([(250, y), (625, y)], fill=[OLD, CUT, GREEN][i], width=3)
    d.polygon([(425, 263), (409, 213), (441, 213)], fill=CUT)
    arrow(d, (714, 196), (714, 285), CUT, 5)
    txt(d, (744, 210), '切深增加 → X 变小', 25, CUT)
    arrow(d, (978, 287), (978, 188), RAPID, 5)
    txt(d, (744, 260), '退刀向外 → X 变大', 25, RAPID)
    txt(d, (40, 394), '内螺纹：在孔里面切', 27)
    # Internal: metal away from the centre. Cutting heads toward increasing X.
    d.rectangle((200, 455, 660, 548), fill=METAL)
    d.line([(200, 455), (200, 548), (660, 548), (660, 455)], fill=INK, width=2)
    txt(d, (235, 462), '材料在孔壁外侧', 22, MUTED)
    for i, y in enumerate((535, 513, 493)):
        d.line([(250, y), (625, y)], fill=[OLD, CUT, GREEN][i], width=3)
    d.polygon([(425, 513), (409, 575), (441, 575)], fill=CUT)
    d.rectangle((422, 574, 655, 598), fill=CUT)
    txt(d, (225, 605), '孔内空腔；刀杆从孔口伸入', 21, MUTED)
    line(d, (170, 652), (700, 652))
    txt(d, (180, 656), '轴线', 19, MUTED)
    arrow(d, (714, 597), (714, 486), CUT, 5)
    txt(d, (744, 494), '切深增加 → X 变大', 25, CUT)
    arrow(d, (978, 486), (978, 597), RAPID, 5)
    txt(d, (744, 548), '退刀向心 → X 变小', 25, RAPID)
    txt(d, (40, 722), '记忆：内牙往孔壁里挖，牙底离轴线更远。', 27, GREEN)
    txt(d, (40, 761), '示意不按比例；线条为刀尖切削包络，未画真实螺旋牙面。', 19, MUTED)
    im.save(FIG/'内外螺纹对照.png')


def basic_profile(x0, x1, y_crest, y_root, pitch=105):
    pts=[]
    # Basic ISO internal form: crest flat P/4, root flat P/8.
    # Two flank axial projections 5P/16 each. Difference is radially exaggerated.
    x=x0
    while x<x1:
        for frac,y in ((0,y_crest),(.25,y_crest),(.5625,y_root),(.6875,y_root),(1,y_crest)):
            xx=min(x+frac*pitch,x1)
            pts.append((xx,y))
            if xx==x1:
                return pts
        x+=pitch
    return pts


def dimensions():
    im = Image.new('RGB', (1100, 840), BG)
    d=ImageDraw.Draw(im)
    header(d, '内螺纹尺寸：牙顶最靠轴线，牙底最远', 'M10×1 单头公制内螺纹｜基本牙型示意｜径向差异放大，非等比例')
    top=basic_profile(115,625,270,182)
    bottom=[(x,800-y) for x,y in top]
    d.polygon([(115,146),(625,146)]+list(reversed(top)), fill=METAL)
    d.polygon(bottom+[(625,654),(115,654)],fill=METAL)
    d.line(top,fill=INK,width=3)
    d.line(bottom,fill=INK,width=3)
    line(d,(80,400),(650,400),fill=MUTED)
    txt(d,(125,406),'轴线',20,MUTED)
    for y,fill in ((182,GREEN),(270,CUT),(235,MUTED),(618,GREEN),(530,CUT),(565,MUTED)):
        line(d,(90,y),(650,y),fill=fill,width=1,dash=8,gap=5)
    txt(d,(120,150),'材料',20,MUTED)
    txt(d,(300,324),'孔内空腔',24,MUTED)
    # Diameter labels beside the axial section, not radius labels.
    for x,yt,yb,label,fill in ((70,182,618,'D',GREEN),(670,235,565,'D2',MUTED),(710,270,530,'D1',CUT)):
        arrow(d,(x,yt),(x,yb),fill,2,8,both=True)
        txt(d,(x,391),label,23,fill,anchor='mm')
    # Leaders identify physical roots/crests.
    arrow(d,(550,690),(556,618),GREEN,2,8)
    txt(d,(180,684),'牙底 → 大径 D：离轴线最远',23,GREEN)
    arrow(d,(540,120),(548,270),CUT,2,8)
    txt(d,(60,120),'牙顶 → 小径 D1：离轴线最近',23,CUT)
    # End-view reference circles: dashed circumferences are theoretical envelopes.
    cx,cy=900,344
    d.ellipse((cx-142,cy-142,cx+142,cy+142),fill=METAL,outline=INK,width=2)
    d.ellipse((cx-114,cy-114,cx+114,cy+114),fill=BG)
    for radius,fill in ((114,GREEN),(105,MUTED),(95,CUT)):
        for angle in range(0,360,14):
            d.arc((cx-radius,cy-radius,cx+radius,cy+radius),angle,angle+8,fill=fill,width=3)
    line(d,(cx-165,cy),(cx+165,cy))
    line(d,(cx,cy-165),(cx,cy+165))
    txt(d,(900,146),'端视参考圆',24,anchor='mt')
    txt(d,(900,518),'D = 10.000 mm',24,GREEN,anchor='mt')
    txt(d,(900,556),'D2 ≈ 9.350 mm',24,MUTED,anchor='mt')
    txt(d,(900,594),'D1 ≈ 8.917 mm',24,CUT,anchor='mt')
    txt(d,(760,638),'D2 是中径参考圆，',20,MUTED)
    txt(d,(760,667),'不是孔里的实体台阶。',20,MUTED)
    txt(d,(40,745),'基本尺寸 ≠ 成品公差极限；教学底孔 φ9.00 也不等于基本小径 8.917。',23,RED)
    txt(d,(40,790),'完整螺旋牙面在不同截面相位不同；端视只画直径包络参考圆。',21,MUTED)
    im.save(FIG/'内螺纹三径.png')


# X is DIAMETER; radial differences deliberately expanded.
# +Z points left, right front face is Z0. Tube is Z0..6; Z8 is past exit.
def pos(x,z):
    return (885 - 65*(z+2), 395 - 118*(x-8.4))


def points(x):
    return [pos(8.4,-2),pos(x,-2),pos(x,8),pos(8.4,8),pos(8.4,-2)]


STEPS=['① 端面前靠向孔壁 A → B','② 主轴同步车螺纹 B → C','③ 出口外收刀 C → D','④ 在孔内间隙返回 D → A']
NOTES=['X8.40 → 本刀 X；Z 仍为 −2，刀尖在孔口外',
       '沿 +Z 切削；单头 P1.0 时，每转轴向前进 1 mm',
       '沿 −X 收回 X8.40；内螺纹收刀方向朝孔中心',
       '保持 X8.40，回 Z−2；一行 G92 的完整循环结束']
PASS_X=[9.36,9.62,9.80,9.92,10.,10.]
ADD=[.18,.13,.09,.06,.04,0.]


def draw_frame(x,stage,t,k=None,all_routes=False):
    im=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(im)
    title='内螺纹 G92：一刀先向外，退刀再向心' if k is None else '内螺纹分刀：X 越大，刀尖越深入孔壁'
    sub='教学第一刀｜G92 X9.36 Z8.0 F1.0｜通孔长度6 mm'
    if k is not None:
        sub=f'第{k+1}/6刀｜X{x:.2f}｜新增单边{ADD[k]:.2f} mm｜累计{(x-9)/2:.2f} mm'
    header(d,title,sub)
    if k is not None:
        txt(d,(40,130),'切削 X',21,MUTED)
        for i,val in enumerate(PASS_X):
            xx=180+i*139
            if i==k:
                d.rounded_rectangle((xx-10,124,xx+95,160),radius=5,fill='#DBEDF4')
            txt(d,(xx,129),f'{val:.2f}',22,CUT if i==k else MUTED)
    else:
        txt(d,(40,133),'刀尖在上侧孔壁；材料在孔壁外侧',22,MUTED)
    left,right=pos(9,6)[0],pos(9,0)[0]
    wall=pos(9,0)[1]
    d.rectangle((left,183,right,wall),fill=METAL)
    d.line([(left,183),(left,wall),(right,wall),(right,183)],fill=INK,width=2)
    line(d,(right,165),(right,527),fill=GRID)
    line(d,(left,165),(left,527),fill=GRID)
    txt(d,(right,535),'孔口 Z0',22,MUTED,anchor='mt')
    txt(d,(left,535),'出口 Z6',22,MUTED,anchor='mt')
    # Previous envelopes (these are not the geometry of the entire bore).
    if k is not None:
        for old in PASS_X[:k]:
            line(d,pos(old,0),pos(old,6),fill=OLD,width=2,dash=7,gap=4)
    pts=points(x)
    for j in range(4):
        line(d,pts[j],pts[j+1],fill=GRID,width=2)
    for j in range(stage):
        d.line([pts[j],pts[j+1]],fill=CUT if j==1 else RAPID,width=4)
    p=(pts[stage][0]+t*(pts[stage+1][0]-pts[stage][0]),pts[stage][1]+t*(pts[stage+1][1]-pts[stage][1]))
    d.line([pts[stage],p],fill=CUT if stage==1 else RAPID,width=5)
    for j in range(4):
        a,b=pts[j],pts[j+1]
        m1=(a[0]+.40*(b[0]-a[0]),a[1]+.40*(b[1]-a[1]))
        m2=(a[0]+.62*(b[0]-a[0]),a[1]+.62*(b[1]-a[1]))
        arrow(d,m1,m2,CUT if j==1 else RAPID,3,9)
    # Boring bar body is wholly inside the original bore, even at max X.
    # Radially long tip accommodates the deliberately expanded radial scale.
    # Drawing is an abstract tip/body, not a tool catalogue outline.
    tool_fill=CUT if stage==1 else RAPID
    sy=p[1]+155
    end=1050
    d.rectangle((p[0],sy,p[0]+max(22,end-p[0]),sy+21),fill=tool_fill)
    d.polygon([p,(p[0]-11,sy+21),(p[0]+12,sy+21)],fill=tool_fill)
    d.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5),fill=tool_fill)
    txt(d,(905,494),'刀杆缩略',20,MUTED)
    # A-D point labels located clear of stock and tool.
    labels=[('A 8.40 / −2',pts[0],(13,-4)),(f'B {x:.2f} / −2',pts[1],(10,-35)),
            (f'C {x:.2f} / 8',pts[2],(-72,-35)),('D 8.40 / 8',pts[3],(-110,12))]
    for lab,pp,off in labels:
        d.ellipse((pp[0]-4,pp[1]-4,pp[0]+4,pp[1]+4),fill=INK)
        txt(d,(pp[0]+off[0],pp[1]+off[1]),lab,20)
    # Axis key and center line. Positioning is schematic (not physical scale).
    line(d,(55,517),(1040,517),fill=MUTED)
    txt(d,(58,522),'轴线方向（径向非等比例）',19,MUTED)
    arrow(d,(105,335),(105,275),INK,3)
    arrow(d,(105,335),(50,335),INK,3)
    txt(d,(105,250),'+X',22,anchor='mt')
    txt(d,(40,335),'+Z',22,anchor='rm')
    txt(d,(40,582),STEPS[stage],28,CUT if stage==1 else RAPID)
    txt(d,(40,626),NOTES[stage],23)
    txt(d,(40,673),'坐标 (X / Z)，单位mm；X为直径值；底孔 φ9.00；刀尖相对工件的轨迹。',20,MUTED)
    txt(d,(40,705),'刀体简化、径向放大；未展开螺旋牙形、末端修牙和加减速。',20,MUTED)
    txt(d,(40,735),'X8.40 为回程刀尖示意，整把刀的间隙须另核；分刀数值仅供理解。',19,RED)
    return im


def gif_save(frames,durations,path):
    pal=frames[0].quantize(colors=192,method=Image.Quantize.MEDIANCUT)
    imgs=[x.quantize(palette=pal,dither=Image.Dither.NONE) for x in frames]
    imgs[0].save(path,save_all=True,append_images=imgs[1:],duration=durations,loop=0,optimize=True,disposal=1)


def four_moves():
    frames,durations=[],[]
    for stage,count in enumerate([12,45,12,28]):
        for i in range(count+1):
            t=i/count
            frames.append(draw_frame(9.36,stage,t))
            durations.append(600 if i in (0,count) else 65)
    draw_frame(9.36,1,.56).save(FIG/'内螺纹G92四段.png')
    frames[0].save(ANIM/'内螺纹一刀_起始帧.png')
    draw_frame(9.36,1,.56).save(ANIM/'内螺纹一刀_切削帧.png')
    frames[-1].save(ANIM/'内螺纹一刀_结束帧.png')
    gif_save(frames,durations,ANIM/'内螺纹G92四段.gif')


def multi_pass():
    frames,durations=[],[]
    for k,x in enumerate(PASS_X):
        for stage,count in enumerate([3,12,3,6]):
            for i in range(count+1):
                frames.append(draw_frame(x,stage,i/count,k))
                durations.append(140 if i in (0,count) else 65)
    frames[0].save(ANIM/'内螺纹分刀_起始帧.png')
    draw_frame(9.92,1,.52,3).save(ANIM/'内螺纹分刀_中间帧.png')
    draw_frame(10.,1,.52,5).save(ANIM/'内螺纹分刀_同深光刀帧.png')
    frames[-1].save(ANIM/'内螺纹分刀_结束帧.png')
    gif_save(frames,durations,ANIM/'内螺纹逐刀加深.gif')


if __name__=='__main__':
    comparison()
    dimensions()
    four_moves()
    multi_pass()
    for p in sorted(ANIM.glob('*.gif')):
        im=Image.open(p)
        total=0
        for i in range(im.n_frames):
            im.seek(i)
            total+=im.info.get('duration',0)
        print(p.name,im.n_frames,'frames',total,'ms',p.stat().st_size,'bytes')
