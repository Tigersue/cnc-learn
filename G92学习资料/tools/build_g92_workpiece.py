from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math


OUT = Path(__file__).resolve().parents[1]
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
W, H = 1500, 1200
BG = '#FFFFFF'
INK = '#153348'
MUTED = '#506879'
GRID = '#BDCCD6'
METAL = '#E8EEF2'
BLUE = '#166F9C'
PALE = '#DCEEF8'
ORANGE = '#AE561B'


def font(size):
    return ImageFont.truetype(FONT, size)


def text(draw, xy, value, size=28, fill=INK, anchor=None):
    draw.text(xy, value, font=font(size), fill=fill, anchor=anchor)


def line(draw, points, fill=INK, width=3):
    draw.line(points, fill=fill, width=width, joint='curve')


def arrow(draw, a, b, fill=INK, width=2, head=12):
    line(draw, [a, b], fill, width)
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    draw.polygon([b, (b[0] - head * ux - .4 * head * uy, b[1] - head * uy + .4 * head * ux),
                  (b[0] - head * ux + .4 * head * uy, b[1] - head * uy - .4 * head * ux)], fill=fill)


def dashed(draw, a, b, fill=GRID, width=2, dash=13, gap=8):
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    for k in range(0, int(dist), dash + gap):
        t, u = k / dist, min(k + dash, dist) / dist
        line(draw, [(a[0] + t * dx, a[1] + t * dy),
                    (a[0] + u * dx, a[1] + u * dy)], fill, width)


def x(z):
    return 1160 - z * 80


def part(draw, cy, threaded=False):
    # Z0 at the right end; +Z is left. Radial scale differs from axial scale.
    r8, r6, r5 = 100, 75, 62.5
    left = 250
    pts = [(left, cy-r8), (x(8), cy-r8), (x(8), cy-r6),
           (x(.5), cy-r6), (x(0), cy-r5), (x(0), cy+r5),
           (x(.5), cy+r6), (x(8), cy+r6), (x(8), cy+r8), (left, cy+r8)]
    draw.polygon(pts, fill=METAL)
    if threaded:
        # Tint only the region marked as threaded in the original figure.
        # Thin lines identify a schematic thread; they do not set a root diameter.
        draw.polygon([(x(6), cy-r6), (x(.5), cy-r6), (x(0), cy-r5),
                      (x(0), cy+r5), (x(.5), cy+r6), (x(6), cy+r6)], fill=PALE)
    line(draw, pts, INK, 4)
    # Broken left boundary indicates continuing bar stock rather than a cut-off part.
    line(draw, [(left, cy-r8), (left-11, cy-65), (left+11, cy-30),
                (left-11, cy+5), (left+11, cy+40), (left-11, cy+75), (left, cy+r8)], INK, 3)
    dashed(draw, (left-35, cy), (x(0)+42, cy), MUTED, 2, 20, 9)
    if threaded:
        thin = 54
        line(draw, [(x(6), cy-thin), (x(0), cy-thin)], BLUE, 2)
        line(draw, [(x(6), cy+thin), (x(0), cy+thin)], BLUE, 2)
        line(draw, [(x(6), cy-r6), (x(6), cy+r6)], BLUE, 2)
    text(draw, (375, cy+33), '棒料继续', 25, MUTED, anchor='mm')
    text(draw, (1235, cy+100), 'Z0', 29, INK, anchor='mm')


def diameter(draw, xx, cy, half_h, label, edge_x):
    for yy in [cy-half_h, cy+half_h]:
        line(draw, [(xx-10, yy), (edge_x, yy)], GRID, 2)
    arrow(draw, (xx, cy), (xx, cy-half_h), MUTED, 2, 10)
    arrow(draw, (xx, cy), (xx, cy+half_h), MUTED, 2, 10)
    text(draw, (xx-20, cy), label, 30, INK, anchor='rm')


def length_dim(draw, zleft, zright, y, from_y, label, label_color=INK):
    a, b = x(zleft), x(zright)
    for xx in [a, b]:
        line(draw, [(xx, from_y), (xx, y+12)], GRID, 2)
    mid = (a+b)/2
    arrow(draw, (mid-40, y), (a, y), MUTED, 2, 11)
    arrow(draw, (mid+40, y), (b, y), MUTED, 2, 11)
    draw.rectangle((mid-170, y-25, mid+170, y+25), fill=BG)
    text(draw, (mid, y), label, 29, label_color, anchor='mm')


im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)
text(d, (58, 35), '实例：φ8 棒料右端加工 M6×1', 43)
text(d, (60, 101), '主轴侧 · 单位 mm · 右端面 Z0 · X 按直径编程', 27, MUTED)
line(d, [(60, 149), (1440, 149)], GRID, 2)

text(d, (60, 178), '① 螺纹加工前：先车出 φ6 外圆', 32)
cy1 = 350
part(d, cy1)
diameter(d, 197, cy1, 100, 'φ8', 250)
diameter(d, 1325, cy1, 75, 'φ6', x(.5))
text(d, (855, cy1-20), '这段外圆将用螺纹刀加工', 28, INK, anchor='mm')
length_dim(d, 8, 0, 499, cy1+100, '外车阶长 8')

text(d, (60, 571), '② 螺纹加工后：端部车成 M6×1', 32)
cy2 = 748
part(d, cy2, threaded=True)
diameter(d, 197, cy2, 100, 'φ8', 250)
text(d, (870, cy2-17), 'M6×1', 40, BLUE, anchor='mm')
text(d, (870, cy2+28), '公称直径 6 · 螺距 1', 27, INK, anchor='mm')
text(d, (1305, cy2-12), '入口倒角', 27, MUTED, anchor='mm')
arrow(d, (1252, cy2-36), (x(.25)+3, cy2-65), MUTED, 2, 10)
length_dim(d, 6, 0, 907, cy2+75, '螺纹段 6', BLUE)
length_dim(d, 8, 0, 975, cy2+100, '外车阶长 8')

arrow(d, (1390, 955), (1240, 955), INK, 3, 12)
text(d, (1315, 986), '+Z', 29, INK, anchor='mm')
text(d, (60, 1037), 'G92 逐刀切深的是牙槽；牙顶来自前序 φ6 外圆。', 29, BLUE)
text(d, (60, 1086), '螺纹段 6 按原图标注；螺纹简化示意，非牙型尺寸。', 26, MUTED)
text(d, (60, 1129), '教学重绘｜轴向与径向可非同比例｜后肩过渡与刀尖圆弧未展开', 24, MUTED)
text(d, (60, 1166), '依据：§7.9.1(2)，纸面 7-65（原PDF第333页）', 22, MUTED)

dest = OUT / 'g92-M6x1工件加工前后.png'
im.save(dest)
print(dest)
