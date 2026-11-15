from pathlib import Path
from math import hypot
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / '图解'
ANI = ROOT / '动图'
FIG.mkdir(exist_ok=True)
ANI.mkdir(exist_ok=True)
FONT = '/System/Library/Fonts/PingFang.ttc'
BG = '#FFFFFF'
INK = '#172C42'
MUTED = '#52677D'
BLUE = '#096DAD'
ORANGE = '#B95018'
TEAL = '#067C70'
PALE = '#EDF4F8'
GRID = '#BDCDD9'

@lru_cache(maxsize=32)
def f(size): return ImageFont.truetype(FONT, size)
def text(d, xy, txt, size=30, fill=INK, anchor=None):
    d.text(xy, txt, font=f(size), fill=fill, anchor=anchor)
def line(d, pts, fill=INK, width=3): d.line(pts, fill=fill, width=width)
def arrow(d, a, b, fill=BLUE, width=4, head=12, both=False):
    line(d, [a,b], fill, width)
    def ah(p,q):
        x,y=p; dx=q[0]-x;dy=q[1]-y; ll=hypot(dx,dy)
        if not ll:return
        ux,uy=dx/ll,dy/ll
        d.polygon([(x,y),(x+ux*head-uy*head*.45,y+uy*head+ux*head*.45),
                   (x+ux*head+uy*head*.45,y+uy*head-ux*head*.45)],fill=fill)
    ah(b,a)
    if both:ah(a,b)
def dash(d,a,b,fill=GRID,width=2,dlen=14):
    dx,dy=b[0]-a[0],b[1]-a[1];ll=hypot(dx,dy)
    if not ll:return
    for n in range(0,int(ll),dlen*2):
        p=n/ll;q=min(n+dlen,ll)/ll
        line(d,[(a[0]+dx*p,a[1]+dy*p),(a[0]+dx*q,a[1]+dy*q)],fill,width)
def hdim(d,x1,x2,y,ext_y,label,fill=INK):
    for x in (x1,x2):line(d,[(x,ext_y),(x,y+12)],GRID,2)
    arrow(d,(x1,y),(x2,y),fill,2,10,True)
    w=d.textlength(label,font=f(29))
    d.rectangle((min(x1,x2)+(abs(x2-x1)-w)/2-7,y-21,min(x1,x2)+(abs(x2-x1)+w)/2+7,y+20),fill=BG)
    text(d,((x1+x2)/2,y),label,29,fill,anchor='mm')
def vdim(d,x,y1,y2,ext_x,label,fill=INK):
    for y in (y1,y2):line(d,[(ext_x,y),(x+12,y)],GRID,2)
    arrow(d,(x,y1),(x,y2),fill,2,10,True)
    text(d,(x-17,(y1+y2)/2),label,29,fill,anchor='rm')
def dot(d,x,y,r=6,fill=ORANGE):d.ellipse((x-r,y-r,x+r,y+r),fill=fill)

def part_drawing():
    im=Image.new('RGB',(1800,1210),BG);d=ImageDraw.Draw(im)
    text(d,(70,45),'G76 实例工件｜M10×1.5 单头外螺纹',48)
    text(d,(72,114),'主轴侧 · 轴向侧视 · 刀尖相对工件 · 单位：mm · X 为直径值',28,MUTED)
    x=lambda z:1350-37*z
    cy=610;sr=34
    y=lambda dia:cy-dia*sr/2
    # 工程简化外形：螺纹大径、牙底细线、入口倒角、退刀槽及继续连接棒材。
    pts=[(x(26),y(12)),(x(18),y(12)),(x(18),y(7.8)),(x(15),y(7.8)),
         (x(15),y(10)),(x(.5),y(10)),(x(0),y(9)),
         (x(0),2*cy-y(9)),(x(.5),2*cy-y(10)),(x(15),2*cy-y(10)),
         (x(15),2*cy-y(7.8)),(x(18),2*cy-y(7.8)),(x(18),2*cy-y(12)),(x(26),2*cy-y(12))]
    d.polygon(pts,fill=PALE)
    line(d,pts,INK,5)
    # 左边棒材采用断裂线，表示不在此切断。
    lx=x(26)
    line(d,[(lx,y(12)),(lx-12,cy-75),(lx+12,cy-35),(lx-12,cy+15),(lx+12,cy+65),(lx,2*cy-y(12))],INK,4)
    for sgn in (-1,1):
        line(d,[(x(14.8),cy+sgn*8.16*sr/2),(x(.65),cy+sgn*8.16*sr/2)],BLUE,2)
    dash(d,(260,cy),(1540,cy),MUTED,2,18)
    text(d,(270,cy+15),'工件轴线',25,MUTED)
    # 程序参考点。
    ax,ay=x(-3),y(12);cx,ty=x(16.5),y(8.16)
    dot(d,ax,ay,8,ORANGE);dot(d,cx,ty,8,ORANGE)
    dash(d,(ax,ay),(ax,cy),ORANGE,2,10)
    text(d,(1510,352),'A 循环起点',29,ORANGE)
    text(d,(1510,392),'X12 / Z−3',29,ORANGE)
    arrow(d,(1500,410),(ax,ay),ORANGE,2,9)
    text(d,(785,675),'终点 D：X8.160 / Z16.5',29,ORANGE)
    line(d,[(865,670),(865,635),(cx,635),(cx,ty+10)],ORANGE,2)
    # 顶部尺寸。
    hdim(d,x(15),x(0),268,y(10),'螺纹部位 15')
    hdim(d,x(18),x(15),337,y(7.8),'3')
    text(d,(x(16.5),292),'退刀槽',29,TEAL,anchor='mm')
    hdim(d,x(0),x(-3),870,cy,'3')
    text(d,(x(-1.5),917),'空中导入',28,MUTED,anchor='mm')
    hdim(d,x(18),x(0),960,2*cy-y(12),'肩位 Z18')
    # 径向与工艺标注。
    vdim(d,310,y(12),2*cy-y(12),lx,'φ12')
    vdim(d,1420,y(10),2*cy-y(10),x(.5),'φ10')
    text(d,(475,855),'棒材 / 夹持段',29)
    text(d,(475,897),'向左继续连接',26,MUTED)
    line(d,[(620,880),(620,805)],MUTED,2)
    text(d,(760,1020),'槽底 φ7.8；槽范围 Z15～Z18',30,TEAL)
    line(d,[(745,1035),(690,1035),(690,790),(cx,790),(cx,2*cy-y(7.8)+8)],TEAL,2)
    text(d,(1450,730),'C0.5',30)
    line(d,[(1445,760),(1380,760),(1380,475),(x(.25),y(9.5))],INK,2)
    text(d,(x(0)-12,812),'右端面 Z0',27,MUTED,anchor='rm')
    text(d,(1110,196),'M10×1.5',36,BLUE,anchor='mm')
    text(d,(1110,237),'牙型角 60°',27,BLUE,anchor='mm')
    line(d,[(1100,285),(1100,365),(1040,y(10))],BLUE,2)
    # 坐标箭头，+Z向左，与普通教程常见方向不同。
    ox,oy=1660,1020
    arrow(d,(ox,oy),(ox-170,oy),BLUE,4,15)
    arrow(d,(ox,oy),(ox,oy-145),BLUE,4,15)
    text(d,(ox-180,oy+8),'+Z',30,BLUE,anchor='ra')
    text(d,(ox+12,oy-145),'+X',30,BLUE)
    text(d,(70,1100),'牙底参考：φ8.160，来自自拟教学切深 h=0.920；未指定公差等级，不是验收尺寸。',27,ORANGE)
    text(d,(70,1145),'螺纹采用工程简化画法；Z26 仅为显示范围，不代表零件总长；有效完整牙长另核首尾不完整牙。',26,MUTED)
    im.save(FIG/'g76-M10x1.5工件图.png')

def radius_diagram():
    im=Image.new('RGB',(1800,1050),BG);d=ImageDraw.Draw(im)
    text(d,(70,45),'X 是直径｜P、Q 和精加工余量 R 是径向量',44)
    text(d,(70,115),'本图以公制最小输入增量 0.001 mm 为假设；不是所有机床都采用这一输入单位。',28,MUTED)
    cx,cy=460,550;r0=285;r1=r0*8.16/10
    d.ellipse((cx-r0,cy-r0,cx+r0,cy+r0),fill=PALE,outline=INK,width=5)
    d.ellipse((cx-r1,cy-r1,cx+r1,cy+r1),outline=BLUE,width=5)
    dash(d,(100,cy),(840,cy),MUTED,2,12)
    dash(d,(cx,205),(cx,910),MUTED,2,12)
    dot(d,cx,cy,5,INK)
    text(d,(cx,cy+40),'轴心',29,MUTED,anchor='mm')
    arrow(d,(cx,cy-r0),(cx,cy-r1),ORANGE,4,12,True)
    line(d,[(cx+10,cy-r0),(765,cy-r0)],ORANGE,2)
    line(d,[(cx+10,cy-r1),(765,cy-r1)],ORANGE,2)
    text(d,(775,cy-(r0+r1)/2),'h = 0.920',30,ORANGE,anchor='lm')
    vdim(d,110,cy-r0,cy+r0,cx,'φ10')
    text(d,(cx,885),'蓝圈：教学牙底参考 φ8.160',28,BLUE,anchor='mm')
    # 数值区不使用拥挤尺寸标注。
    x0=970
    text(d,(x0,245),'程序终点',28,MUTED)
    text(d,(x0,285),'X8.160',49,BLUE)
    text(d,(x0,390),'直径减少',28,MUTED)
    text(d,(x0,430),'10.000 − 8.160 = 1.840 mm',34)
    text(d,(x0,535),'单边径向切深',28,MUTED)
    text(d,(x0,575),'h = 1.840 ÷ 2 = 0.920 mm',34,ORANGE)
    text(d,(x0,680),'第二行牙高 P',28,MUTED)
    text(d,(x0,720),'0.920 ÷ 0.001 → P920',34,ORANGE)
    text(d,(70,970),'记忆：直径变化除以 2，才是单边切入。P920 不是直径减少 0.920，也不是切入 920 mm。',29)
    im.save(FIG/'g76-直径与径向切深.png')

def p_diagram():
    im=Image.new('RGB',(1800,820),BG);d=ImageDraw.Draw(im)
    text(d,(70,45),'第一行 P020060｜按两位一组读取',45)
    text(d,(70,115),'G76 P020060 Q50 R0.05',34,MUTED)
    positions=[410,900,1390]
    vals=['02','00','60']
    labels=['m：精加工次数','r：末端倒角量','a：刀尖角度']
    details=['最后按精加工目标切 2 次','00 × 0.1 × 导程 = 0','60°牙型刀尖角']
    for px,v,lab,det in zip(positions,vals,labels,details):
        text(d,(px,270),v,110,BLUE,anchor='mm')
        arrow(d,(px,350),(px,400),BLUE,3,12)
        text(d,(px,450),lab,34,anchor='mm')
        text(d,(px,510),det,27,MUTED,anchor='mm')
    text(d,(70,610),'m=02 的第一刀通常还会切掉精加工余量；不能把它说成“2 次都不吃刀”。',31,ORANGE)
    text(d,(70,675),'r=00 不等于不退刀：本例在预先加工的退刀槽内退出；它只是没有设定末端倒角长度。',29)
    text(d,(70,735),'a=60 不是“60°斜进刀”；标准单侧进刀几何可按半角理解，实控切削方式另核。',29)
    im.save(FIG/'g76-P020060拆解.png')

def animation():
    W,H=1600,940
    x=lambda z:1230-38*z
    y=lambda dia:300+(10-dia)*55
    A=(x(-3),y(12)); endz=16.5
    depths=[.25,.62,.87,.92,.92]
    names=['粗切代表刀 ①','粗切代表刀 ②','粗切末段代表刀','精加工 ① / m=02','精加工 ② / m=02']
    Xs=[10-2*h for h in depths]
    frames=[];durations=[];preview={}
    def base(idx,phase,p,toolpos,trace):
        im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
        text(d,(55,30),'G76 自动分刀：切入 → 同步切削 → 退出 → 返回',40)
        text(d,(55,93),'主轴侧 · +Z 向左 · X 直径值 · 外圆上半部局部',27,MUTED)
        # Upper-half cropped material, radial exaggeration.
        pts=[(x(26),y(12)),(x(18),y(12)),(x(18),y(7.8)),(x(15),y(7.8)),
             (x(15),y(10)),(x(.5),y(10)),(x(0),y(9)),(x(0),590),(x(26),590)]
        d.polygon(pts,fill=PALE);line(d,pts[:7],INK,4)
        line(d,[(x(0),y(9)),(x(0),590)],INK,4)
        # Completed representative traces, not full actual pass distribution.
        for j in range(idx):
            yy=y(Xs[j])
            line(d,[(x(-.5),yy),(x(15),yy)],GRID,2)
        # Root reference and relief label.
        dash(d,(x(.5),y(8.16)),(x(14.8),y(8.16)),BLUE,2,12)
        text(d,(x(8),540),'M10×1.5 螺纹部位',29,anchor='mm')
        text(d,(x(16.5),610),'退刀槽',27,TEAL,anchor='mm')
        text(d,(x(16.5),648),'Z15～18',25,TEAL,anchor='mm')
        line(d,[(x(16.5),595),(x(16.5),y(7.8)+15)],TEAL,2)
        text(d,(x(22),615),'φ12 棒材',27,MUTED,anchor='mm')
        # Workpiece material cut at cropped bottom.
        dash(d,(x(26),590),(x(0),590),MUTED,2,12)
        for z in (0,15,18):
            yy=680
            line(d,[(x(z),610),(x(z),yy-7)],GRID,2)
            text(d,(x(z),yy),f'Z{z}',25,MUTED,anchor='ma')
        # Context path: deliberately schematic X/Z rectangles.
        B=(A[0],y(Xs[idx]));C=(x(endz),B[1]);D=(C[0],A[1])
        for aa,bb in ((A,B),(B,C),(C,D),(D,A)):dash(d,aa,bb,GRID,2,10)
        for aa,bb in trace:arrow(d,aa,bb,ORANGE if phase==1 else BLUE,4,12)
        dot(d,*A,6,BLUE)
        text(d,(A[0]+45,A[1]-67),'A 起点',26,BLUE)
        text(d,(A[0]+45,A[1]-34),'X12 / Z−3',24,BLUE)
        # V-shaped tool symbol. Tip is the relative programmed point.
        tx,ty=toolpos
        d.polygon([(tx,ty),(tx-25,ty-44),(tx+25,ty-44)],fill=ORANGE,outline=INK)
        dot(d,tx,ty,4,INK)
        if phase==1:
            arrow(d,(1100,465),(940,465),ORANGE,4,13)
            text(d,(1110,465),'+Z 切削',26,ORANGE,anchor='lm')
        else:
            text(d,(1090,465),['X 向切入','同步切削','在槽内退出','外侧返回'][phase],26,BLUE,anchor='lm')
        # Coordinate convention.
        arrow(d,(1490,625),(1390,625),BLUE,3,10)
        arrow(d,(1490,625),(1490,535),BLUE,3,10)
        text(d,(1380,625),'+Z',26,BLUE,anchor='rm')
        text(d,(1500,530),'+X',26,BLUE)
        # Selected state.
        label=names[idx]
        text(d,(55,755),f'{label}    累计单边深度 h={depths[idx]:.3f} mm    目标 X{Xs[idx]:.3f}',32,INK)
        end_label='④ 返回 A，整个 G76 循环完成' if idx==len(depths)-1 else '④ 返回 A，再自动安排下一刀'
        text(d,(55,807),['① 在端面前切入','② 按导程 F1.5 同步车螺纹','③ 在 Z16.5 退刀槽内退出',end_label][phase],30,ORANGE)
        # Stable footer with critical scope.
        text(d,(55,870),'仅取 5 个代表刀次，省略中间粗切；m=02 为两次精加工，不代表两次纯空刀。',25,MUTED)
        text(d,(55,907),'径向放大；斜向进刀的轴向微移、同步等待和加减速未展开，非实控仿真。',25,MUTED)
        return im
    # About 29 seconds. Phase duration is pedagogic, never machining time.
    steps=[8,20,8,14]
    for idx in range(len(depths)):
        B=(A[0],y(Xs[idx]));C=(x(endz),B[1]);D=(C[0],A[1]);v=[A,B,C,D,A]
        for phase,nn in enumerate(steps):
            for k in range(nn):
                p=(k+1)/nn;aa=v[phase];bb=v[phase+1]
                pos=(aa[0]+(bb[0]-aa[0])*p,aa[1]+(bb[1]-aa[1])*p)
                tr=[(v[j],v[j+1]) for j in range(phase)]+[(aa,pos)]
                im=base(idx,phase,p,pos,tr)
                # Moderate final size, optimized below.
                im=im.resize((1280,752),Image.Resampling.LANCZOS)
                frames.append(im);durations.append(90)
                if phase==1 and k==nn-1:preview[idx]=im.copy()
            # Mark return or completion with a brief pause.
            durations[-1]=300 if phase<3 else 850
    # Shared palette preserves stable colors; avoid flicker.
    palette=frames[0].quantize(colors=96)
    qframes=[fr.quantize(palette=palette,dither=Image.Dither.NONE) for fr in frames]
    qframes[0].save(ANI/'g76-粗切到精切-代表刀次.gif',save_all=True,append_images=qframes[1:],
                     duration=durations,loop=0,optimize=True,disposal=1)
    preview[3].save(ANI/'g76-动图预览.png')
    # Contact sheet to verify representative states.
    thumbs=[]
    for i in range(5):
        fr=preview[i].resize((768,451),Image.Resampling.LANCZOS)
        thumbs.append(fr)
        preview[i].save(ANI/f'g76-代表帧-{i+1}.png')
    sheet=Image.new('RGB',(1536,451*3),BG)
    for i,fr in enumerate(thumbs):sheet.paste(fr,((i%2)*768,(i//2)*451))
    sheet.save(ANI/'g76-代表帧检查.png')

if __name__=='__main__':
    part_drawing();radius_diagram();p_diagram();animation()
    for p in sorted(FIG.glob('*.png')):print(p)
    for p in sorted(ANI.glob('*.gif')):print(p,round(p.stat().st_size/1024/1024,2),'MB')
