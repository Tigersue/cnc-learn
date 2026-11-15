from math import atan2, cos, sin, pi
from pathlib import Path
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path.cwd()
OUT = ROOT / "output/pdf/S205A_主副轴对接_图解.pdf"
for name, weight in [("CN", "Light"), ("CB", "Medium")]:
    pdfmetrics.registerFont(TTFont(name, f"/System/Library/Fonts/STHeiti {weight}.ttc", subfontIndex=1))
pdfmetrics.registerFont(TTFont("CODE", "/System/Library/Fonts/Menlo.ttc", subfontIndex=0))

W, H = A4
M = 42
F = W - 2*M
C = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
C.setTitle("S205A 主副轴对接图解")
C.setAuthor("加工工序学习")
C.setSubject("O0659 与 O0658 的接料、同步、切断与退回")

INK = "#152B3B"
DIM = "#4C6474"
SUBTLE = "#6A8190"
LINE = "#D6E3E9"
BG = "#F4F8FA"
BLUE = "#126DAB"
BLUE_L = "#DDEFFC"
ORANGE = "#AE511A"
ORANGE_L = "#FCE8D8"
GREEN = "#00765C"
GREEN_M = "#29BB90"
GREEN_L = "#DFF5EC"
PURPLE = "#71409C"
PURPLE_L = "#F1E8F8"
TOOL = "#AC3761"
GRAY = "#8598A4"
GRAY_L = "#CBD8DF"

def co(x):
    return HexColor(x) if isinstance(x, str) else x

def r(x,y,w,h,fill,stroke=None,rad=0):
    C.setFillColor(co(fill))
    if stroke:
        C.setStrokeColor(co(stroke))
        C.setLineWidth(.7)
    if rad:
        C.roundRect(x,H-y-h,w,h,rad,stroke=int(bool(stroke)),fill=1)
    else:
        C.rect(x,H-y-h,w,h,stroke=int(bool(stroke)),fill=1)

def t(x,y,s,sz=12,color=INK,font="CN",align="left", limit=None):
    width = pdfmetrics.stringWidth(s, font, sz)
    if limit and width > limit:
        raise ValueError(f"oversize {width:.1f}>{limit}: {s}")
    C.setFillColor(co(color))
    C.setFont(font,sz)
    base = H-y-sz*.84
    if align == "center":
        C.drawCentredString(x,base,s)
    elif align == "right":
        C.drawRightString(x,base,s)
    else:
        C.drawString(x,base,s)

def lines(x,y,ss,sz=12,leading=18,color=DIM,font="CN",limit=None):
    for i,s in enumerate(ss):
        t(x,y+i*leading,s,sz,color,font,limit=limit)

def rule(x1,x2,y,col=LINE,weight=1):
    C.setStrokeColor(co(col))
    C.setLineWidth(weight)
    C.line(x1,H-y,x2,H-y)

def pill(x,y,s,bg=GREEN_L,fg=GREEN,sz=11):
    width=pdfmetrics.stringWidth(s,"CB",sz)+20
    r(x,y,width,22,bg,rad=7)
    t(x+10,y+5,s,sz,fg,"CB")
    return width

def page(num,tag,title,sub):
    r(0,0,W,H,white)
    r(M,39,22,4,GREEN_M,rad=2)
    t(M+31,34,f"S205A  /  对接图解  /  {tag}",11,GREEN,"CB")
    t(M,65,title,29,INK,"CB",limit=F)
    t(M,109,sub,12.3,DIM,limit=F)
    rule(M,W-M,798)
    t(M,810,"津上 S205A  /  O0659 + O0658  /  学习用侧视示意，非比例",9,SUBTLE,limit=F-56)
    t(W-M,810,f"{num:02d} / 06",9,SUBTLE,"CB",align="right")
    C.bookmarkPage(f"p{num}")
    C.addOutlineEntry(f"{num:02d}  {title}",f"p{num}",level=0)

def box(y,label,ss,bg=GREEN_L,fg=GREEN,h=72):
    r(M,y,F,h,bg,rad=10)
    r(M+13,y+15,3,16,fg,rad=1.5)
    t(M+23,y+13,label,12.3,fg,"CB",limit=F-46)
    lines(M+23,y+34,ss,11.5,16.8,INK,limit=F-46)

def local_rect(x,y,w,h,fill,rad=0):
    C.setFillColor(co(fill))
    if rad:
        C.roundRect(x,y,w,h,rad,stroke=0,fill=1)
    else:
        C.rect(x,y,w,h,stroke=0,fill=1)

def poly(points,fill):
    p=C.beginPath()
    p.moveTo(*points[0])
    for xy in points[1:]: p.lineTo(*xy)
    p.close()
    C.setFillColor(co(fill))
    C.drawPath(p,fill=1,stroke=0)

def ltext(x,y,s,sz=10,color=INK,center=False):
    C.setFillColor(co(color))
    C.setFont("CB",sz)
    if center: C.drawCentredString(x,y,s)
    else: C.drawString(x,y,s)

def lline(x1,y1,x2,y2,fill,weight=1,dash=None):
    C.setStrokeColor(co(fill))
    C.setLineWidth(weight)
    if dash: C.setDash(dash)
    C.line(x1,y1,x2,y2)
    if dash: C.setDash()

def arrow(x1,y1,x2,y2,col,weight=2):
    lline(x1,y1,x2,y2,col,weight)
    a=atan2(y2-y1,x2-x1)
    poly([(x2,y2),(x2-7*cos(a-pi/6),y2-7*sin(a-pi/6)),
          (x2-7*cos(a+pi/6),y2-7*sin(a+pi/6))],col)

def part(x0,tip,cy,fill=GREEN_M):
    # Profile steps are schematic. The far right straight section is the grip land.
    pts=[(x0,cy-10),(x0+22,cy-10),(x0+22,cy-14),(tip-31,cy-14),
         (tip-31,cy-8),(tip,cy-8),(tip,cy+8),(tip-31,cy+8),
         (tip-31,cy+14),(x0+22,cy+14),(x0+22,cy+10),(x0,cy+10)]
    poly(pts,fill)
    lline(x0+2,cy+5,tip-2,cy+5,white,.7)

def scene(x,y,w,h,mode):
    C.saveState()
    C.translate(x,H-y-h)
    C.scale(w/480,h/108)
    cy=51
    cut=232
    tip=338
    closed=mode in ("grip","cut","out","old")
    split=mode in ("cut","out")
    dx=48 if mode=="out" else 0
    face={"ready":398,"sync":398,"near":371,"grip":311,"cut":311,
          "out":359,"old":415}[mode]
    # Headstock and back-spindle bodies; facing jaw profiles indicate open/closed.
    local_rect(16,cy-25,106,50,BLUE_L,6)
    local_rect(16,cy-25,11,50,BLUE,3)
    local_rect(face+22,cy-25,42,50,ORANGE_L,6)
    local_rect(face+53,cy-25,11,50,ORANGE,3)
    lline(26,cy,461,cy,SUBTLE,.7,[4,4])
    local_rect(23,cy-9,cut-23-(3 if split else 0),18,GRAY_L)
    for s in [-1,1]:
        poly([(100,cy+s*25),(134,cy+s*19),(134,cy+s*9),(100,cy+s*9)],BLUE)
    part(cut+dx+(3 if split else 0),tip+dx,cy)
    if mode=="old":
        part(face-69,face+27,cy,PURPLE)
    gap = 8 if closed else 16
    for s in [-1,1]:
        poly([(face,cy+s*gap),(face+30,cy+s*gap),
              (face+30,cy+s*24),(face,cy+s*20)],ORANGE)
    ltext(79,11,"主夹头 · 夹紧",10.2,BLUE,True)
    ltext(face+28,11,"副夹头 · "+("夹紧" if closed else "张开"),10.2,ORANGE,True)
    if mode=="cut":
        poly([(cut-8,102),(cut+10,102),(cut+10,66),(cut,52),(cut-8,67)],TOOL)
        arrow(cut-24,101,cut-24,72,TOOL)
        ltext(cut+16,91,"T08 切断刀",10.5,TOOL)
        ltext(cut-38,80,"X1",8.7,TOOL)
        lline(cut,44,cut,20,TOOL,1,[2,2])
        ltext(cut,9,"切断面",9.3,TOOL,True)
    elif mode=="out":
        arrow(307,92,398,92,ORANGE)
        ltext(352,99,"Z2 持件退回",10.6,ORANGE,True)
        ltext(269,11,"已分离",9.8,GREEN,True)
    elif mode=="near":
        arrow(424,93,349,93,ORANGE)
        ltext(386,100,"Z2 向工件靠近",10.2,ORANGE,True)
        ltext(237,15,"工件还连着棒料",9.8,GREEN,True)
    elif mode=="grip":
        lline(125,88,331,88,GREEN,1.5)
        lline(125,81,125,89,GREEN,1.5)
        lline(331,81,331,89,GREEN,1.5)
        ltext(228,94,"两只夹头同时夹住一根料",10.4,GREEN,True)
    elif mode=="sync":
        for bx,col,light in [(70,BLUE,BLUE_L),(411,ORANGE,ORANGE_L)]:
            local_rect(bx-39,83,78,19,light,6)
            ltext(bx,88,"转速已到达",9.5,col,True)
        ltext(241,88,"副轴仍在接料待机位",10,GREEN,True)
    elif mode=="old":
        ltext(275,85,"本轮新件",10.4,GREEN,True)
        ltext(405,85,"副轴持上一件",10.4,PURPLE,True)
    else:
        ltext(281,85,"将要接走的部分",10.6,GREEN,True)
        lline(cut,40,cut,22,TOOL,.9,[2,2])
        ltext(cut,11,"预定切断面",9.2,TOOL,True)
    C.restoreState()

def panel(y,height,tag,title,mode,caption):
    r(M,y,F,height,BG,LINE,rad=11)
    pw=pill(M+13,y+10,tag)
    t(M+22+pw,y+12,title,14,INK,"CB",limit=F-pw-39)
    scene(M+13,y+37,F-26,height-65,mode)
    t(M+15,y+height-22,caption,11.4,DIM,limit=F-30)

def steps(y,items):
    gap=8
    width=(F-gap*(len(items)-1))/len(items)
    for i,(tag,desc) in enumerate(items):
        x=M+i*(width+gap)
        r(x,y,width,51,BG,LINE,8)
        t(x+width/2,y+8,tag,12,GREEN,"CB","center",width-10)
        t(x+width/2,y+29,desc,10,DIM,"CN","center",width-7)

# 01: the story before the codes.
page(1,"先看动作","主副轴怎么把工件交过去？","想象两只手交接：右手先抓稳，左边再切开，右手才拿走。")
x=M
for s,bg,fg in [("蓝：主夹头",BLUE_L,BLUE),("橙：副夹头",ORANGE_L,ORANGE),
                ("灰：棒料",BG,DIM),("绿：本轮工件",GREEN_L,GREEN)]:
    x+=pill(x,137,s,bg,fg)+8
panel(174,151,"01","主轴夹住棒料，副轴开口等候","ready",
      "绿色部分已经做过正面加工，但它和灰色棒料仍连在一起。")
panel(337,151,"02","副轴靠近并夹紧，两边同时抓住","grip",
      "主夹头继续夹棒料；副夹头抓住将要切下的那一段。")
panel(500,151,"03","切断后，副轴带着工件退走","out",
      "灰色余料留在主轴，绿色工件留在副轴。主轴不必为交件而松夹。")
box(676,"先记住这四个动作",["靠近  →  夹紧  →  切断  →  持件退回",
    "两只夹头的位置、工件形状及间隙均为示意；图不用于定尺寸。"],h=77)
C.showPage()

# 02: why the receiving spindle may initially be occupied.
page(2,"接料前","先清空副轴，再对上转速","连续加工时，副轴手里可能还夹着上一个循环接下来的工件。")
steps(146,[("M90658","启动副程序"),("M500","两边先会合"),("M501","主轴让位"),
           ("M502","副轴准备好"),("M503","允许靠近")])
panel(215,160,"M501","主轴让位，副轴先处理上一件","old",
      "副轴先做上一件背面，再停转、排料、退让；本轮新件仍在主轴。")
panel(390,160,"M56 / M53","副轴仍在待机位，两边对转速","sync",
      "副轴空夹准备好，双方通过 M502；主轴备好切断刀，再做同步。")
# Draw the distinction as two readable cards.
for i,(tag,ttl,ss) in enumerate([
    ("M56","开启旋转同步",["让主、副轴的旋转匹配。","此时副轴仍在待机位。"]),
    ("M53","确认速度到达",["确认两边转速到达要求。","随后经 M503 放行靠近。"])]):
    xx=M+i*(F/2+6)
    ww=F/2-6
    r(xx,570,ww,101,GREEN_L,rad=9)
    p=pill(xx+12,583,tag,GREEN,white)
    t(xx+22+p,586,ttl,13.5,INK,"CB",limit=ww-p-34)
    lines(xx+13,613,ss,11.4,17,DIM,limit=ww-26)
box(692,"转速相配和副轴向前走，是两件事",[
    "M56 / M53 管旋转；M503 是这份模板允许 Z2 接近的会合点。",
    "需要特定角度时才另外核对位相同步。此图未规定主副轴旋向。"],h=74)
C.showPage()

# 03: the actual grip.
page(3,"接到工件","先靠近，再夹紧","想象右手张开、套到握持位置，再合拢。绿色部分此时还没有切断。")
panel(158,164,"M503 以后","张开的副夹头沿 Z2 靠近","near",
      "示意图中副轴向左接近；图上的箭头不代表机床坐标正负。")
panel(340,164,"M20 / M504","到位后副轴夹紧，主轴仍夹着棒料","grip",
      "副轴核对夹紧完成，再走到 M504。两边会合后才允许切断。")
r(M,525,F,125,INK,rad=10)
t(M+15,537,"把图和副轴程序对上",13,white,"CB")
for i,(code,desc) in enumerate([
    ("G98 G00 Z50.0","快移到材料外的接近点"),
    ("G01 Z20.0 F3000","按每分钟进给到夹持位置"),
    ("M20   /   M504","先发夹紧指令，核对完成后再会合")]):
    yy=566+i*24
    t(M+16,yy,code,11.5,"#8EE3C8","CODE",limit=180)
    t(M+210,yy,desc,11.5,white,limit=F-225)
box(671,"Z20.0 是目标坐标，夹了多深要另算",[
    "模板候选值从 Z50.0 到 Z20.0，坐标变化是 -30 mm。",
    "这段行程包含靠近时的空程。夹入深度还取决于夹头端面和工件伸出。"],h=76)
C.showPage()

# 04: cutting and exit.
page(4,"交接完成","切开以后，副轴才能拿走","切断刀沿 X1 进刀；副轴退出时沿 Z2 移动。看清这两个方向。")
panel(158,170,"M504 以后","T08 从外侧向中心切断","cut",
      "切断前两边都夹紧；切开后主轴留灰色棒料，副轴留绿色工件。")
panel(345,164,"M505 以后","副轴保持夹紧，停转并带件退回","out",
      "副轴走完已验证的退回路径，才到 M506；本轮工件还没排出。")
steps(532,[("M42","检测切断"),("M57","解除同步"),("M505","放行退出"),
           ("M105","副轴停转"),("M506","退出会合")])
box(603,"M505 是准许离开，M506 是已经退到位",[
    "主轴过了 M505，不能假定副轴已经离开；应等 M506 再做余料检查。",
    "M42 是差速式切断检测选配。本机是否安装及有效，须另行核实。"],h=78)
box(693,"看图自查：退回时能不能先松副夹头？",[
    "不能。刚切下的工件只由副轴夹持，应带件退出，留待下一轮或末件收尾。"],
    bg=BLUE_L,fg=BLUE,h=59)
C.showPage()

# 05: the two NC lanes.
page(5,"对照程序","两条程序，各走各的","同号等待像约好的会合点：先到的一侧停在这里，等另一侧也到。")
t(M,143,"主轴 M90658 搜索并启动副轴 O0658，然后两侧各走各的程序。",12,INK,"CB",limit=F)
lx=M+13; mx=M+F/2; rx=M+F/2+55
r(M,174,F,33,INK,rad=7)
t(lx,184,"主轴 O0659",12,white,"CB")
t(mx,184,"会合",12,white,"CB","center")
t(rx,184,"副轴 O0658",12,white,"CB")
rows=[
    ("M500",["启动副程序后，等副轴到场"],["走到接料切断入口"]),
    ("M501",["主轴完成正面加工并让位"],["等待放行，之后处理上一件"]),
    ("M502",["等待副轴接料准备完成"],["上一件排出，机构收回；","空夹打开，接料位准备好"]),
    ("M503",["切断刀准备就绪；","M56 同步，M53 确认速度"],["等放行，之后 Z2 接近"]),
    ("M504",["等副轴夹紧后再切断"],["Z2 到位，M20 夹紧；","确认后到等待点"]),
    ("M505",["完成切断与检测，解除同步"],["保持夹紧；通过后停转退回"]),
    ("M506",["等副轴退出，再检查余料"],["已持件退回安全位"]),
    ("M599",["余料检查及本轮收尾完成"],["保留新件，等待本轮结束"]),
]
for i,(tag,aa,bb) in enumerate(rows):
    y=214+i*59
    r(M,y,F,53,BG if i%2==0 else "#FAFCFD",LINE,rad=6)
    green = i in [3,4,5,6]
    r(mx-36,y+13,72,27,GREEN if green else GREEN_L,rad=7)
    t(mx,y+20,tag,12,white if green else GREEN,"CB","center")
    for x,col,ss in [(lx,BLUE,aa),(rx,ORANGE,bb)]:
        lines(x,y+(13 if len(ss)>1 else 20),ss,11.2,15,col,"CB",limit=190)
box(697,"等待码传递的是“双方都走到了这里”",[
    "它不是夹紧、转速或位置传感器。前一段动作的真实完成条件仍要核实。",
    "例如 M20 是夹紧指令，M504 是夹紧段之后的双通道会合。"],h=75)
C.showPage()

# 06: part identity across cycles.
page(6,"三个循环场景","最后一件，不能漏掉背面","用两件工件举例：图里的 01、02 是工件编号，表示同一件如何接续。")

def token(cx,y,num,fill,fg):
    if num=="空夹":
        r(cx-29,y,58,31,BG,LINE,7)
        t(cx,y+7,num,11,DIM,"CB","center")
    else:
        r(cx-29,y,58,31,fill,rad=7)
        t(cx,y+7,num,13,fg,"CB","center")

scenarios=[
    ("首件","空夹","01","接住 01","副轴没有上一件，跳过旧件加工和排料。"),
    ("连续件","01","02","先排 01，再接 02","01 完成背面并排出；02 切下后留在副轴。"),
    ("末件收尾","02","空夹","加工并排出 02","主轴保持让位，不再送料或切下一件。"),
]
for i,(tag,a,b,mid,desc) in enumerate(scenarios):
    y=151+i*125
    r(M,y,F,112,BG,LINE,rad=10)
    pill(M+13,y+10,tag)
    t(M+91,y+14,desc,11.1,DIM,limit=F-107)
    xa=M+93; xb=M+F-93
    token(xa,y+46,a,PURPLE_L,PURPLE)
    token(xb,y+46,b,GREEN_L,GREEN)
    C.saveState()
    arrow(xa+43,H-y-70,xb-43,H-y-70,GREEN,1.65)
    C.restoreState()
    t((xa+xb)/2,y+45,mid,12.8,GREEN,"CB","center",xb-xa-85)
    t(xa,y+86,"本轮开始时副轴所持",9.8,SUBTLE,"CN","center")
    t(xb,y+86,"本轮结束时副轴所持",9.8,SUBTLE,"CN","center")

t(M,533,"末件单独收尾：两个通道都进入 N900",14,INK,"CB")
steps(557,[("M590","确认都走末件入口"),("M591","主轴让位后放行"),
           ("M599","背面与排料完成")])
box(624,"复习：完整成品什么时候出来？",[
    "切断时副轴刚接到工件。等它完成背面加工并排出，这件才做完。"],
    h=59)
rule(M,W-M,699)
t(M,710,"读图依据与使用范围",11,INK,"CB")
lines(M,729,[
    "程序：O0659 主轴、O0658 副轴审阅版；等待点按这对模板分配。",
    "津上 3281-LTQ0C-05：§7.4（纸面 7-16、7-24；原PDF 284、292页），",
    "§7.8 和 §7.9.6(4)（纸面 7-63、7-82；原PDF 331、350页）。",
    "图解用于理解顺序。坐标、补正、夹紧反馈、选配及退回路径仍需实机核对。"],
    9.8,14.4,DIM,limit=F)
C.showPage()
C.save()
print(OUT)
