from pathlib import Path
import math
import re
import sys
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
files = list(BASE.glob('*.nc.txt'))
main = (BASE/'O0001_主轴_教学待填.nc.txt').read_text()
sub = (BASE/'O0100_重复切槽_刀尖R0.1教学.nc.txt').read_text()
back = (BASE/'O0002_副轴_教学待填.nc.txt').read_text()
notes = []

def record(msg):
    notes.append('通过：' + msg)

def clean(text):
    return re.sub(r'\([^)]*\)', '', text)

for p in files:
    s = p.read_text()
    s.encode('ascii')
    assert s.count('(') == s.count(')')
    for line in clean(s).splitlines():
        assert not (re.search(r'\bT\d+', line) and re.search(r'\bM0[01]\b', line))
record('三文件为ASCII程序文本，注释括号配对，T与M00/M01未同段。')

waits = lambda s: re.findall(r'^M(50[1-6])$', clean(s), re.M)
assert waits(main) == waits(back) == ['501','502','503','504','505','506']
assert main.index('M56') < main.index('M53') < main.index('M503') < main.index('M504') < main.index('G99 G01 X-2.0')
assert main.index('M57') < main.index('M505') < main.index('M506')
assert back.index('M20') < back.index('M504') < back.index('M505') < back.index('N100')
assert back.index('N400') < back.index('N500') < back.index('M506')
assert not re.search(r'GOTO', clean(back))
record('M501～M506两通道顺序一致；夹紧在切断前，同步解除在副轴带件退回前，背面和排出在M506前。')

assert len(re.findall(r'^M98 P0100$', main, re.M)) == 4
assert len(re.findall(r'^G00 W5\.0$', main, re.M)) == 3
assert 'M90002' in main and re.search(r'^O0002\b', back, re.M)
record('重复槽子程序调用四次、槽距移动三次，主轴M90002与副轴O0002对应。')

# Interpret the subprogram W and X endpoints rather than relying on a stated sum.
z, r = 0.0, 9.0
arc_ends = []
g75_return = None
rough_columns = []
for line in clean(sub).splitlines():
    w = re.search(r'\bW(-?\d+(?:\.\d+)?)', line)
    x = re.search(r'\bX(-?\d+(?:\.\d+)?)', line)
    before = (z, r)
    if line.startswith('G75'):
        if not x:
            assert not w and not re.search(r'\b[ZQP]', line)
            g75_return = float(re.search(r'\bR(\d+(?:\.\d+)?)', line)[1])
            continue
        assert not re.search(r'\b[ZWQ]', line)
        depth = int(re.search(r'\bP(\d+)\b', line)[1]) * .001
        relief = float(re.search(r'\bR(-?\d+(?:\.\d+)?)', line)[1])
        target = float(x[1])/2
        assert g75_return is not None and 0 < g75_return < depth
        assert relief == 0 and target < r and depth > 0
        initial_r = r
        peaks = []
        while r > target + 1e-12:
            r = max(target, r-depth)
            peaks.append(r)
        assert all(target-1e-12 <= v < initial_r for v in peaks)
        assert all(a > b for a,b in zip(peaks,peaks[1:]))
        rough_columns.append((z,target,depth,g75_return,peaks))
        # Single column: R0 and omitted Z/W/Q mean no axial motion.
        # Cycle returns radially; the following G00 X18 also states this exit.
        r = initial_r
        continue
    if w:
        z += float(w[1])
    if x:
        r = float(x[1])/2
    if line.startswith('G02'):
        rad = float(re.search(r'\bR(\d+(?:\.\d+)?)', line)[1])
        chord = math.dist(before, (z,r))
        assert abs(chord - rad*math.sqrt(2)) < 1e-10
        arc_ends.append((before,(z,r),rad))
assert abs(z) < 1e-12 and abs(r-9) < 1e-12
assert len(arc_ends) == 2
record('解析子程序后，Z净增量为零、出口X18；两段圆弧均满足R0.6的90°弦长。')

assert len(rough_columns) == 2
assert all(abs(c[0]-zref)<1e-12 for c,zref in zip(rough_columns,[.1,.9]))
assert all(abs(c[1]-6.1)<1e-12 and abs(c[2]-.3)<1e-12 and abs(c[3]-.1)<1e-12 for c in rough_columns)
assert all(len(c[4]) == 10 and abs(c[4][-2]-c[4][-1]-.2)<1e-10 for c in rough_columns)
assert all(abs((c[4][0]+c[3])-8.8)<1e-12 for c in rough_columns)
covered = sorted((zref,zref+1.5) for zref,*_ in rough_columns)
assert abs(covered[0][0]-.1)<1e-12 and abs(covered[-1][1]-2.4)<1e-12
assert abs(covered[0][1]-covered[1][0]-.7)<1e-12
assert abs(6.1-6.0-.1)<1e-12
record('两列G75均省略Z/W/Q且底部R0；刀宽覆盖A+0.1～B−0.1、重叠0.7、底部径向余量0.1；各有10次最深进刀目标，末次0.2mm。')

# Reconstruct the finished surface from each physical nose circle.
rn, part_R = .1, .5
centers = [(-.5,7.5),(3.0,7.5)]
for j, (start,end,ref_R) in enumerate(arc_ends):
    nose_z_offset = rn if j == 0 else 1.5-rn
    p0 = (start[0]+nose_z_offset, start[1]+rn)
    p1 = (end[0]+nose_z_offset, end[1]+rn)
    c = centers[j]
    for p in (p0,p1):
        dist = math.dist(p,c)
        assert abs(dist-(part_R+rn)) < 1e-10
        surface = (p[0] - rn*(p[0]-c[0])/dist, p[1] - rn*(p[1]-c[1])/dist)
        assert abs(math.dist(surface,c)-part_R) < 1e-10
    v0,v1 = (p0[0]-c[0],p0[1]-c[1]),(p1[0]-c[0],p1[1]-c[1])
    assert v0[0]*v1[1]-v0[1]*v1[0] < 0
record('用刀片两端不同圆心偏移重建成品，两处凸圆角均为R0.5，Z-X平面参考轨迹为G02；槽底内角R0.1单独保留。')

starts = [16.4+5*i for i in range(4)]
assert all(abs(a-b)<1e-10 for a,b in zip(starts,[16.4,21.4,26.4,31.4]))
assert abs(1.1+4*2.5+3*2.5-18.6)<1e-12
assert abs((35-11.4)-18.6-5)<1e-12
assert abs(37.2-2-35.2)<1e-12
assert 11.7 < 11.9 < 15.7 < 15.9
assert abs(35-15.7-19.3)<1e-12
assert abs(10.27-1.385-8.885)<1e-12
record('35mm总长、四槽位置、切断刀宽及背面0.2余量、夹持带与两侧倒角/圆角避让、45°尺寸链相符。')

h = 4.4/math.tan(math.radians(59))
full = 12.644-h
assert 10 <= full < 10.001
assert 8 < 10
record(f'φ8.8/118°钻尖高{h:.6f}mm；钻尖12.644mm时全径深{full:.6f}mm；螺纹刀终点8mm早于全径孔底。')

fields = sorted(set(re.findall(r'<([A-Z0-9_]+)>', main+back)))
assert fields == ['EJECT_X','EJECT_Z','G300_STROKE','PICKUP_CLAMP_Z','PICKUP_FAST_Z']
notes += ['', '仍待现场填写：' + '、'.join(fields),
          '未验证：真实刀具补偿、螺纹牙型/量规、整刀与夹具干涉、控制器执行、夹持强度、材料切削条件。',
          '以上校核是几何与程序文本核查，不是控制器仿真或上机验证。']
(BASE/'计算校核记录.txt').write_text('\n'.join(notes)+'\n')

names=['O0001_主轴_教学待填.nc.txt','O0100_重复切槽_刀尖R0.1教学.nc.txt','O0002_副轴_教学待填.nc.txt']
preamble=('三程序合并阅读版（教学待填稿，单槽粗切已改G75）\n\n'
          '本文件只供阅读，不要整份输入机床。三个O程序须按各自通道分别存储。\n'
          '包含5个尖括号现场待填项，且外形及螺纹仍需真实刀具补偿。\n'
          '已核查名义几何与等待顺序，未做控制器仿真或上机验证。\n'
          '详细前提见《程序说明与坐标表.md》。\n\n')
(BASE/'完整程序_合并阅读.txt').write_text(preamble+'\n\n'.join(name+'\n'+(BASE/name).read_text() for name in names))
if '--check-only' in sys.argv:
    print('\n'.join(notes))
    raise SystemExit(0)

# Exact geometric sketches; no generated bitmap geometry.
font_path='/System/Library/Fonts/PingFang.ttc'
def font(size):
    return ImageFont.truetype(font_path,size)

W,H=2200,1200
im=Image.new('RGB',(W,H),'#f6f8fc'); d=ImageDraw.Draw(im)
ink='#18283f'; blue='#1866b0'; green='#16835c'; orange='#b96013'; grey='#6b7890'
d.text((70,35),'S205A 练习件｜成品坐标与副轴夹持候选方案',font=font(45),fill=ink)
d.text((70,100),'按 Z1 递增展开：M6 成品端面 Z1=0，+Z1 向右进入工件；与原图左右相反。单位 mm',font=font(27),fill=grey)
sx,sy,ox,cy=55,28,125,450
xy=lambda z,r:(ox+sx*z,cy-sy*r)
profile=[(0,2.5),(.5,3),(5.885,3),(6.885,2),(8.885,2),(10.27,3.385),(10.27,6)]
def curve(cz,cr,rad,t0,t1,n=32):
    return [(cz+rad*math.cos(t0+(t1-t0)*i/n),cr+rad*math.sin(t0+(t1-t0)*i/n)) for i in range(1,n+1)]
profile += curve(10.77,6,.5,math.pi,math.pi/2)
profile += [(11.4,6.5),(11.4,7.7),(11.7,8)]
for a in starts:
    b=a+2.5
    profile += [(a-.5,8)] + curve(a-.5,7.5,.5,math.pi/2,0)
    profile += [(a,6),(b,6),(b,7.5)] + curve(b+.5,7.5,.5,math.pi,math.pi/2)
profile += [(35,8)]
outline=[xy(z,r) for z,r in profile]+[xy(z,-r) for z,r in profile[::-1]]
d.polygon(outline,fill='#dce6f1',outline=ink,width=3)
for x in range(90,W-60,24): d.line((x,cy,x+12,cy),fill='#a7b2c3',width=2)
for z in [0,5.885,11.4,16.4,21.4,26.4,31.4,35]:
    x,_=xy(z,0); d.line((x,710,x,727),fill=ink,width=2)
    d.text((x-25,736),f'{z:g}',font=font(24),fill=ink)
d.line((ox,718,ox+35*sx,718),fill=ink,width=2)
d.text((ox+35*sx-20,778),'+Z1 →',font=font(27),fill=ink)
d.text((xy(1,0)[0],300),'M6×1',font=font(28),fill=blue)
d.text((xy(7,0)[0]-20,320),'φ4，长2',font=font(25),fill=blue)
d.text((xy(22,0)[0],195),'φ16 / 槽底 φ12',font=font(28),fill=blue)
d.text((xy(18,0)[0],800),'四槽宽2.5，槽距5.0，八个槽口R0.5',font=font(27),fill=blue)
# Indicate the candidate grip band without claiming a force/fixture validation.
x1,x2=xy(11.9,0)[0],xy(15.7,0)[0]
for y in [cy-8*sy,cy+8*sy]: d.line((x1,y,x2,y),fill=green,width=15)
d.line((x1,175,x2,175),fill=green,width=3)
d.line((x1,165,x1,190),fill=green,width=3); d.line((x2,165,x2,190),fill=green,width=3)
d.text((x1-10,129),'夹持带 11.9～15.7',font=font(26),fill=green)
d.text((80,845),'夹持说明',font=font(31),fill=green)
d.text((80,901),'φ16 软夹头接触带约3.8；内部让开 M6、φ4 与φ13。口端在Z1=15.7，成品外伸19.3。',font=font(27),fill=ink)
d.text((80,953),'夹持力、抗滑移和整夹头干涉未验证；图上的15.7不是可直接输入的副轴机床Z坐标。',font=font(27),fill=ink)
d.text((80,1030),'精度边界：名义成品图；槽底R0.1及真实刀具补偿另见程序说明。教学稿尚未上机验证。',font=font(26),fill=orange)
im.save(BASE/'工件坐标与夹持方案.png')

# Bore-depth sketch to explain the user's A choice.
im=Image.new('RGB',(1800,900),'#f6f8fc');d=ImageDraw.Draw(im)
d.text((70,40),'A方案｜直孔壁深10，钻头尖端到12.644',font=font(42),fill=ink)
d.text((70,105),'φ8.8，顶角118°；螺纹刀切到8不等于8mm完整牙长。',font=font(28),fill=grey)
ox,cy,sx,sy=240,450,85,30
x=lambda v:ox+v*sx
y=lambda v:cy+v*sy
d.rectangle((x(0),y(-6),x(15),y(6)),fill='#dce6f1',outline=ink,width=3)
d.polygon([(x(0),y(-4.4)),(x(10),y(-4.4)),(x(12.644),y(0)),(x(10),y(4.4)),(x(0),y(4.4))],fill='white',outline=blue,width=4)
for pos,label,col,yy in [(8,'螺纹刀终点 8',green,250),(10,'全径孔深 10',blue,680),(12.644,'钻尖总深 12.644',orange,760)]:
    d.line((x(0),yy,x(pos),yy),fill=col,width=3)
    for xx in (x(0),x(pos)):d.line((xx,yy-10,xx,yy+10),fill=col,width=3)
    d.text((x(0)+20,yy-43),label,font=font(28),fill=col)
d.text((70,795),'轴向剖面示意；孔内从背面成品Z2=0向负Z2进入。钻尖角改变时必须重算。',font=font(25),fill=grey)
im.save(BASE/'底孔深度A方案.png')

print('\n'.join(notes))
