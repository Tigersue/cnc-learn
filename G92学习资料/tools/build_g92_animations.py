from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parents[1] / '动图'
OUT.mkdir(exist_ok=True)
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
W, H = 1080, 760
BG = '#FAFCFE'
INK = '#153348'
MUTED = '#526878'
GRID = '#CFDCE3'
METAL = '#E0E8ED'
CUT = '#1672A3'
RAPID = '#BF691F'
GREEN = '#167C60'
HISTORY = '#9BB5C6'


def font(n):
    return ImageFont.truetype(FONT, n)


def text(d, xy, s, size=24, fill=INK, anchor=None):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor)


def dashed(d, a, b, fill=GRID, width=2, dash=9, gap=7):
    dx, dy = b[0] - a[0], b[1] - a[1]
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    for k in range(0, int(distance), dash + gap):
        t, u = k / distance, min(k + dash, distance) / distance
        d.line([(a[0] + t * dx, a[1] + t * dy), (a[0] + u * dx, a[1] + u * dy)], fill=fill, width=width)


def arrow(d, a, b, fill=INK, width=3, head=10):
    d.line([a, b], fill=fill, width=width)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    if length < head:
        return
    ux, uy = dx / length, dy / length
    d.polygon([b, (b[0] - head * ux - head * .45 * uy, b[1] - head * uy + head * .45 * ux), (b[0] - head * ux + head * .45 * uy, b[1] - head * uy - head * .45 * ux)], fill=fill)


# Screen is a side view: +Z left, +X up. X labels are diameter values;
# drawing height uses a deliberately expanded radial scale.
def pos(x, z):
    return (860 - 68 * (z + 2), 230 + (7 - x) * 105)


def point(d, p, label, offset=(0, 0), fill=INK):
    d.ellipse((p[0]-5, p[1]-5, p[0]+5, p[1]+5), fill=fill)
    text(d, (p[0]+offset[0], p[1]+offset[1]), label, 24, fill)


def segment_points(x):
    return [pos(7, -2), pos(x, -2), pos(x, 6.5), pos(7, 6.5), pos(7, -2)]


STEPS = ['① 快速接近 A → B', '② 同步切削 B → C', '③ 快速退出 C → D', '④ 快速返回 D → A']
NOTES = ['端面前到达本刀 X，尚未沿 Z 切入工件', '主轴每转 1 圈，沿 +Z 前进 1 mm', '沿 +X 退回 X7，离开工件表面', '在 X7 返回 Z−2；本刀循环完成']


def base(title, subtitle, x, active, p, pass_index=None, done=0, t=0):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    text(d, (45, 26), title, 35)
    text(d, (46, 78), subtitle, 22, MUTED)
    d.line([(45, 118), (1035, 118)], fill=GRID, width=2)
    # Nominal blank envelope. This is not a real thread profile.
    top = pos(6, 0)[1]
    left, right = pos(6, 8.7)[0], pos(6, 0)[0]
    d.rectangle((left, top, right, 570), fill=METAL)
    d.line([(left, top), (right, top), (right, 570)], fill=INK, width=2)
    text(d, (left+14, 548), '原始材料包络 φ6', 23, MUTED)
    dashed(d, (right, 195), (right, 585), fill=GRID)
    text(d, (right-2, 585), '右端面 Z0', 22, MUTED, anchor='mt')
    # Axis key.
    axis_origin=(1005, 590)
    arrow(d, axis_origin, (1005, 550), INK, 3)
    arrow(d, axis_origin, (935, 590), INK, 3)
    text(d, (1005, 532), '+X', 24, anchor='mm')
    text(d, (927, 590), '+Z', 24, anchor='rm')
    text(d, (985, 620), 'X为直径值', 20, MUTED, anchor='mm')
    # Previous pass lines show commanded tip envelopes, not tooth geometry.
    if pass_index is not None:
        for previous_x in [5.40, 4.96, 4.70, 4.60, 4.60][:done]:
            d.line([pos(previous_x, 0), pos(previous_x, 6.5)], fill=HISTORY, width=3)
    pts = segment_points(x)
    for i in range(4):
        dashed(d, pts[i], pts[i+1], fill=GRID, width=2)
    # Completed portions of the current pass.
    for i in range(active):
        d.line([pts[i], pts[i+1]], fill=CUT if i == 1 else RAPID, width=4)
    d.line([pts[active], p], fill=CUT if active == 1 else RAPID, width=6)
    # Direction marks remain readable even while a segment is beginning.
    for i in range(4):
        a, b = pts[i], pts[i+1]
        aa=(a[0]+.38*(b[0]-a[0]),a[1]+.38*(b[1]-a[1]))
        bb=(a[0]+.62*(b[0]-a[0]),a[1]+.62*(b[1]-a[1]))
        arrow(d, aa, bb, CUT if i == 1 else RAPID, 3, 9)
    point(d, pts[0], 'A  X7 / Z−2', (12,-41))
    point(d, pts[1], f'B  X{x:.2f} / Z−2', (10,6))
    point(d, pts[2], f'C  X{x:.2f} / Z6.5', (-46,14))
    point(d, pts[3], 'D  X7 / Z6.5', (-45,-41))
    # A small pointed tool indicates the actual commanded tip.
    fill = CUT if active == 1 else RAPID
    d.polygon([(p[0],p[1]),(p[0]-12,p[1]-27),(p[0]+12,p[1]-27)], fill=fill)
    d.ellipse((p[0]-6,p[1]-6,p[0]+6,p[1]+6),fill=fill)
    text(d, (46, 630), STEPS[active], 29, fill)
    text(d, (46, 673), NOTES[active], 23)
    text(d, (46, 722), '教学慢放与简化｜刀尖相对工件运动｜径向放大｜未展开末端修牙', 20, MUTED)
    return im


def palette_frames(frames):
    # Use one stable palette for clean lettering and no animation color flicker.
    colors=frames[0].quantize(colors=192, method=Image.Quantize.MEDIANCUT)
    return [frame.quantize(palette=colors, dither=Image.Dither.NONE) for frame in frames]


def four_moves():
    frames, durations = [], []
    x=5.4
    pts=segment_points(x)
    counts=[18,64,18,28]
    for step,count in enumerate(counts):
        for i in range(count+1):
            t=i/count
            p=(pts[step][0]+t*(pts[step+1][0]-pts[step][0]),pts[step][1]+t*(pts[step+1][1]-pts[step][1]))
            im=base('G92：一行程序，完成四段动作', '手册 M6×1 第一刀｜G92 X5.40 Z6.5 F1.0', x,step,p,t=t)
            frames.append(im)
            durations.append(650 if i==0 else (850 if i==count else 70))
    frames[0].save(OUT/'g92-four-moves-first.png')
    frames[52].save(OUT/'g92-four-moves-cutting.png')
    frames[-1].save(OUT/'g92-four-moves-end.png')
    pf=palette_frames(frames)
    pf[0].save(OUT/'g92-four-moves.gif',save_all=True,append_images=pf[1:],duration=durations,loop=0,optimize=True,disposal=2)
    return sum(durations)


def five_passes():
    frames,durations=[],[]
    xs=[5.40,4.96,4.70,4.60,4.60]
    add=[.30,.22,.13,.05,0]
    for k,x in enumerate(xs):
        pts=segment_points(x)
        for step,count in enumerate([6,20,6,10]):
            for i in range(count+1):
                t=i/count
                p=(pts[step][0]+t*(pts[step+1][0]-pts[step][0]),pts[step][1]+t*(pts[step+1][1]-pts[step][1]))
                desc=f'第{k+1}/5刀  X{x:.2f}｜新增单边 {add[k]:.2f} mm｜累计 {(6-x)/2:.2f} mm'
                im=base('G92：每行 X，都再走一整刀',desc,x,step,p,pass_index=k,done=k,t=t)
                d=ImageDraw.Draw(im)
                text(d,(46,143),'切削 X',23,MUTED)
                for n,val in enumerate(xs):
                    xx=182+n*142
                    label=f'{val:.2f}'
                    if n==k:
                        d.rounded_rectangle((xx-13,137,xx+91,177),radius=8,fill='#E3F1F8')
                    text(d,(xx,143),label,24,CUT if n==k else MUTED)
                if k==4:
                    text(d,(46,598),'最后重复 X4.60：相同深度再走一刀，新增名义切深为 0',23,GREEN)
                frames.append(im)
                durations.append(250 if i==0 else (400 if i==count else 100))
    frames[0].save(OUT/'g92-five-passes-first.png')
    frames[len(frames)//2].save(OUT/'g92-five-passes-middle.png')
    frames[-1].save(OUT/'g92-five-passes-end.png')
    pf=palette_frames(frames)
    pf[0].save(OUT/'g92-five-passes.gif',save_all=True,append_images=pf[1:],duration=durations,loop=0,optimize=True,disposal=2)
    return sum(durations)


if __name__=='__main__':
    durations={'four_moves_ms':four_moves(),'five_passes_ms':five_passes()}
    print(durations)
    for p in sorted(OUT.glob('*.gif')):
        im=Image.open(p)
        total=sum(im.seek(i) or im.info.get('duration',0) for i in range(im.n_frames))
        print(p.name, p.stat().st_size, 'bytes', im.n_frames, 'frames', total,'ms')
