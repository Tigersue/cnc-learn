from pathlib import Path
import math
import re
import json

OUT = Path(__file__).resolve().parent.parent
TAN = math.tan(math.pi / 8)
QR = 0.2 * TAN / math.sqrt(2)
QL = 0.4 * TAN / math.sqrt(2)

# One motion dataset drives both language editions.
# Points are X diameter, Z; circle centres are Z, physical radius.
SECTIONS = [
    dict(id='B', n=100, start=(8.12, 0),
         cn='小端C0.94、R0.20、φ10、肩根R0.60', en='SMALL END AND SHOULDER',
         entry_cn='已粗车；理想尖刀已到X8.120 Z0.000；外圆刀参考点，不是刀尖圆心',
         entry_en='PRE-ROUGHED; IDEAL POINT TOOL AT X8.120 Z0.000',
         exit_cn='出口X11.200 Z7.000；同一理想刀可在几何上接C段',
         exit_en='EXIT X11.200 Z7.000; C MAY FOLLOW GEOMETRICALLY',
         moves=[
             ('G01', (10 - 2 * QR, .94 - QR), None, None,
              '沿45度倒角；q=0.0585786，X=10-2q，Z=0.94-q', 'C0.94 LINE TO R0.20'),
             ('G03', (10, .94 + .2 * TAN), .2, (.94 + .2 * TAN, 4.8),
              'R0.20接φ10；Z=0.94+0.20*tan22.5度；R是成品半径', 'R0.20 TO OD10'),
             ('G01', (10, 6.4), None, None,
              'φ10直外圆；肩面Z7减R0.60，切点Z=6.40', 'OD10 TO SHOULDER ROOT'),
             ('G02', (11.2, 7), .6, (6.4, 5.6),
              '肩根R0.60；X=10+2*0.60=11.20，Z=7', 'R0.60 TO SHOULDER'),
         ]),
    dict(id='C', n=200, start=(11.2, 7),
         cn='肩面、凸台C1、φ16外圆', en='SHOULDER C1 AND OD16',
         entry_cn='理想尖刀已在X11.200 Z7.000；可接B的出口',
         entry_en='IDEAL POINT TOOL AT X11.200 Z7.000',
         exit_cn='出口X16.000 Z11.500；D段须换成适用槽刀并重新到达其入口',
         exit_en='EXIT X16.000 Z11.500; D NEEDS ITS OWN GROOVE TOOL',
         moves=[
             ('G01', (14, 7), None, None,
              '肩面到C1起点；X=16-2*1=14，Z仍为7', 'SHOULDER TO C1 START'),
             ('G01', (16, 8), None, None,
              'C1斜线；直径增2即径向增1，Z增1；两轴必须联动', 'C1 CHAMFER'),
             ('G01', (16, 11.5), None, None,
              'φ16直外圆；直段长11.50-8=3.50，到槽口R切点', 'OD16 TO GROOVE TANGENT'),
         ]),
    dict(id='D', n=300, start=(16, 11.5),
         cn='环槽精加工：仅1.50宽理想零R槽刀参考轨迹', en='GROOVE WIDTH1.50 ZERO CORNER R',
         entry_cn='槽已粗加工；低Z刃角已在X16.000 Z11.500，刀宽向正Z覆盖1.50',
         entry_en='GROOVE PRE-ROUGHED; LOW-Z EDGE AT X16.000 Z11.500',
         exit_cn='参考角出口X16.000 Z14.200；另一刃在Z15.700；绝不直接接E1',
         exit_en='REF EXIT X16.000 Z14.200; FAR EDGE Z15.700; DO NOT JOIN E1',
         moves=[
             ('G03', (15, 12), .5, (11.5, 7.5),
              '低Z刃加工右槽口R0.50；X=16-2*0.50，Z=11.50+0.50', 'NEAR EDGE RIGHT MOUTH R0.50'),
             ('G01', (13, 12), None, None,
              '低Z刃沿右壁下降；槽底φ12加径向R0.50，故X=13', 'RIGHT WALL'),
             ('G02', (12, 12.5), .5, (12.5, 6.5),
              '低Z刃加工右槽底R0.50；终点Z=12+0.50', 'NEAR EDGE RIGHT ROOT R0.50'),
             ('G01', (12, 13.2), None, None,
              '槽底横移0.70；远刃到Z14.70，参考Z=14.70-1.50=13.20', 'FLOOR; FAR EDGE Z14.700'),
             ('G02', (13, 13.7), .5, (13.2, 6.5),
              '切换远刃控制左槽底R；参考Z=15.20-1.50=13.70', 'FAR EDGE LEFT ROOT R0.50'),
             ('G01', (15, 13.7), None, None,
              '远刃沿左壁上升；实际左壁15.20，参考角仍在13.70', 'LEFT WALL; FAR EDGE Z15.200'),
             ('G03', (16, 14.2), .5, (14.2, 7.5),
              '远刃加工左槽口R；实际切点15.70减刀宽1.50=参考14.20', 'FAR EDGE LEFT MOUTH R0.50'),
         ]),
    dict(id='E1', n=400, start=(16, 15.7),
         cn='左φ16直外圆', en='LEFT OD16',
         entry_cn='已用适用外圆刀重新到X16.000 Z15.700；此处不提供换刀及接近动作',
         entry_en='OD TOOL RE-ESTABLISHED AT X16.000 Z15.700',
         exit_cn='出口X16.000 Z29.154；与E2仅几何相接，实际大端C/R计划背面完成',
         exit_en='EXIT X16.000 Z29.154; E2 IS GLOBAL GEOMETRY ONLY',
         moves=[
             ('G01', (16, 30.2 - .88 - .4 * TAN), None, None,
              '到左R0.40的外圆切点；Z=30.20-0.88-0.40*tan22.5度', 'OD16 TO LEFT R0.40 TANGENT'),
         ]),
    dict(id='E2', n=500, start=(16, 30.2 - .88 - .4 * TAN),
         cn='左端R0.40与C0.88：全局成品几何对照段', en='LEFT END GLOBAL GEOMETRY ONLY',
         entry_cn='全局几何起点X16.000 Z29.154；本段不是实际副轴通道代码',
         entry_en='GLOBAL START X16.000 Z29.154; NOT SUB-SPINDLE CODE',
         exit_cn='出口全局X14.240 Z30.200；实际背面局部坐标及圆弧码须另核',
         exit_en='GLOBAL EXIT X14.240 Z30.200; BACK AXIS CONVERSION REQUIRED',
         moves=[
             ('G03', (16 - 2 * QL, 30.2 - .88 + QL), .4,
              (30.2 - .88 - .4 * TAN, 7.6),
              '左R0.40接倒角；q=0.1171573，X=16-2q，Z=29.32+q', 'LEFT R0.40 TO CHAMFER'),
             ('G01', (14.24, 30.2), None, None,
              'C0.88到左端面；X=16-2*0.88=14.24，Z=总长30.20', 'C0.88 TO LEFT FACE'),
         ]),
]

HEADER_CN = '''详细中文注释版｜分段轮廓教学代码｜不可整份运行
本文件为分段阅读资料，不是带完整入口、退让、夹持和刀具补偿的生产程序。
本稿保持草案约定：右端Z0，向图纸左侧为正Z，X直径，单位毫米。
圆弧采用津上手册纸7-31第299页第一组、T04至T08等效编程示意。
该视图旋转180度后正Z向左、正X向上；不把它冒充已确认的现场刀台。
不适用于未经核实的镜像、其他刀台或实际Z反向；不能只改Z符号而不核圆弧。
每段执行前均须已建立：公制、G18、X直径、适用工件坐标及刀具补正、G40。
G40是本教学假设；B/C/E采用理想零刀尖R，真实圆刀尖必须另做补偿。
D段只采用1.50宽、两刃零R且允许侧向车槽的理想刀具，低Z刃角对刀。
进给模式及适用F、主轴/冷却状态须事先正确建立；本稿不虚构S、F、T。
每段仅从注明的入口开始，出口均不含退刀；段间换刀和快速定位不在本稿中。
不按文件从上到下连跑。所有N行是已定几何代码，其余文字为阅读说明。
数值统一四舍五入到0.001 mm；不代替公差判定或控制器验证。
中文为UTF-8学习注释，未验证现场控制器字符兼容性。
'''
HEADER_EN = '''ENGLISH SHORT NOTES | SEGMENTED TEACHING CODE | NOT A RUNNABLE PROGRAM
RIGHT FACE Z0; +Z LEFT ON DRAWING; X DIAMETER; MM.
ARC VIEW: TSUGAMI MANUAL P7-31 / ORIGINAL PDF299, T04-T08 EQUIVALENT.
ACTUAL TURRET / Z DIRECTION / MIRROR STATE NOT CONFIRMED.
PREREQS PER BLOCK: METRIC, G18, X DIAMETER, CORRECT DATUM / OFFSETS, G40.
B/C/E: IDEAL ZERO NOSE R. D: WIDTH1.50, ZERO CORNER R, SIDE-TURN CAPABLE.
D REFERENCE: LOW-Z EDGE; TOOL EXTENDS +Z BY1.50.
FEED MODE / F / SPINDLE / COOLANT MUST ALREADY BE SET CORRECTLY.
NO INVENTED T / S / F / APPROACH / RETRACT / CLAMP CODES.
INDEPENDENT FRAGMENTS: START AT STATED ENTRY; DO NOT RUN AS ONE FILE.
N LINES ARE CODE; OTHER LINES ARE READING NOTES. VALUES ROUNDED TO0.001MM.
'''

PENDING_CN = '''
未生成动作的工序及原因：
A 端面/粗车：缺毛坯、刀具、粗精余量和切削条件，不编粗车分刀和超程。
F 接料/切断：缺实际夹持、刀宽、端面余量、同步及完成反馈条件，不编M码或切断终点。
G 背面：s是局部深度，s0为左成品面，正s入孔；全局Z=30.20-s。
  左端面外缘X14.240 s0；斜面切点X15.765685 s0.762843；圆柱切点X16 s1.045685。
  s不是已确认的NC地址，不将E2直接作为副轴程序，也不猜副轴G02/G03。
H 底孔：有效全直径深10，完整孔底全局Z20.20。
  d为实际底孔直径、theta为钻尖角：h=d/2/tan(theta/2)。
  钻尖局部深10+h，全局Z20.20-h；缺d和theta，不编数字终点。
H 双头内螺纹：M10、P1、2头、导程2；两头相位差180度。
  缺完整有效牙长、刀具类型/几何、孔底空间和实际通道能力，不编G84/G92/G76。
  有效孔深10不等于完整有效牙深10；普通单头M10x1丝锥不能代替。
核查状态：已做算术/圆弧/刀宽核查及双版本一致性比较；未做控制器仿真、空运行或首件。
'''
PENDING_EN = '''
NOT GENERATED:
A FACE / ROUGH: STOCK, TOOLS, ALLOWANCE AND CUTTING DATA MISSING.
F PICKOFF / PART: CLAMP, WIDTH, ALLOWANCE, SYNC / FEEDBACK MISSING.
G BACK: LOCAL DEPTH s; GLOBAL Z=30.20-s. s IS NOT A VERIFIED NC ADDRESS.
  LEFT FACE X14.240 s0; CHAMFER TANGENT X15.765685 s0.762843; OD TANGENT X16 s1.045685.
  E2 IS NOT SUB-SPINDLE CODE; VERIFY BACK COORDS / ARC DIRECTION.
H DRILL: FULL-DIAMETER DEPTH10; GLOBAL FULL BORE END Z20.20.
  h=d/2/tan(theta/2); TIP DEPTH=10+h; GLOBAL TIP Z=20.20-h.
  DRILL DIAMETER / POINT ANGLE MISSING; NO NUMERIC DRILL END.
H THREAD: M10 P1 TWO STARTS; LEAD2; PHASE180DEG.
  FULL THREAD LENGTH / TOOL / BOTTOM SPACE / CHANNEL CAPABILITY MISSING.
  NO G84 / G92 / G76 GENERATED. HOLE DEPTH10 IS NOT FULL THREAD LENGTH10.
  A SINGLE-START M10x1 TAP DOES NOT MATCH.
CHECKED: GEOMETRY / ARC / TOOL WIDTH / CN-EN CODE IDENTITY.
NOT VERIFIED: CONTROLLER SIMULATION / MACHINE DRY RUN / FIRST ARTICLE.
'''

def rounded_point(pt):
    return tuple(float(f'{v:.3f}') for v in pt)

def render(lang):
    cn = lang == 'cn'
    lines = [(HEADER_CN if cn else HEADER_EN).rstrip(), '']
    for s in SECTIONS:
        lines += [f"[{s['id']}] {s['cn'] if cn else s['en']}",
                  s['entry_cn'] if cn else s['entry_en']]
        if s['id'] == 'D':
            lines.append('只给有限刀宽参考轨迹，不再重复给单点槽轮廓作为另一套切削。' if cn
                         else 'FINITE WIDTH REF PATH ONLY; NO SECOND POINT-PROFILE CUT.')
        lines.append(f"N{s['n']} G18")
        for i, (g, pt, rad, center, note_cn, note_en) in enumerate(s['moves'], 1):
            note = note_cn if cn else note_en
            code = f"N{s['n'] + i*10} {g} X{pt[0]:.3f} Z{pt[1]:.3f}"
            if rad is not None:
                code += f' R{rad:.3f}'
            if cn:
                lines += [f'（{note}）', code]
            else:
                lines.append(f'{code} ({note})')
        lines += [s['exit_cn'] if cn else s['exit_en'], '']
    lines.append((PENDING_CN if cn else PENDING_EN).strip())
    return '\n'.join(lines) + '\n'

cn_path = OUT / '分段刀路_详细中文注释.nc.txt'
en_path = OUT / 'Segmented_Toolpaths_EN.nc.txt'
cn_path.write_text(render('cn'), encoding='utf-8')
en_path.write_text(render('en'), encoding='utf-8')

def code_lines(path):
    return [re.sub(r'\s*\([^)]*\)', '', line).strip()
            for line in path.read_text().splitlines() if re.match(r'^N\d+\s', line)]

assert code_lines(cn_path) == code_lines(en_path), 'CN/EN code differs'

def solve_arc(start_xz, end_xz, radius, g):
    p = (start_xz[1], start_xz[0]/2)
    q = (end_xz[1], end_xz[0]/2)
    chord = math.dist(p, q)
    assert 0 < chord <= 2*radius + 1e-12
    m = ((p[0]+q[0])/2, (p[1]+q[1])/2)
    off = math.sqrt(max(0, radius**2-(chord/2)**2))
    perp = (-(q[1]-p[1])/chord, (q[0]-p[0])/chord)
    # Manual view: G02 is CCW, G03 CW in numerical Z-right/r-up plot.
    for sign in [1, -1]:
        c = (m[0]+sign*off*perp[0], m[1]+sign*off*perp[1])
        a = math.atan2(p[1]-c[1], p[0]-c[0])
        b = math.atan2(q[1]-c[1], q[0]-c[0])
        sweep = (b-a) % (2*math.pi) if g == 'G02' else -((a-b) % (2*math.pi))
        if abs(sweep) <= math.pi + 1e-10:
            return c, a, sweep
    raise AssertionError('No minor R arc')

arc_checks = []
max_point_rounding_error = 0.0
for s in SECTIONS:
    original = s['start']
    current = rounded_point(original)
    for i, (g, pt, r, expected_center, _, _) in enumerate(s['moves'], 1):
        target = rounded_point(pt)
        err = math.hypot((pt[0]-target[0])/2, pt[1]-target[1])
        max_point_rounding_error = max(max_point_rounding_error, err)
        if r is not None:
            # Exact mathematical geometry and code after 0.001 rounding.
            for p in (original, pt):
                assert abs(math.dist((p[1], p[0]/2), expected_center)-r) < 1e-10
            cc, aa, sw = solve_arc(current, target, r, g)
            deviation = math.dist(cc, expected_center)
            assert deviation < .001
            exact_start = math.atan2(original[0]/2-expected_center[1], original[1]-expected_center[0])
            exact_end = math.atan2(pt[0]/2-expected_center[1], pt[1]-expected_center[0])
            exact_sweep = ((exact_end-exact_start) % (2*math.pi) if g == 'G02'
                           else -((exact_start-exact_end) % (2*math.pi)))
            max_dev = 0.0
            for j in range(201):
                t = j / 200
                actual = (cc[0]+r*math.cos(aa+sw*t), cc[1]+r*math.sin(aa+sw*t))
                expected = (expected_center[0]+r*math.cos(exact_start+exact_sweep*t),
                            expected_center[1]+r*math.sin(exact_start+exact_sweep*t))
                max_dev = max(max_dev, math.dist(actual, expected))
            assert max_dev < .001
            arc_checks.append(dict(section=s['id'], line=s['n']+i*10, code=g,
                                   radius=r, sweep_degrees=math.degrees(sw),
                                   center_error_mm=deviation, path_error_mm=max_dev))
        original, current = pt, target

# Check the full ideal blade footprint against the finished groove profile.
def part_radius(z):
    if z < 11.5 or z > 15.7:
        return 8.0
    if z < 12:
        return 7.5 + math.sqrt(max(0, .25-(z-11.5)**2))
    if z < 12.5:
        return 6.5 - math.sqrt(max(0, .25-(z-12.5)**2))
    if z <= 14.7:
        return 6.0
    if z <= 15.2:
        return 6.5 - math.sqrt(max(0, .25-(z-14.7)**2))
    return 7.5 + math.sqrt(max(0, .25-(z-15.7)**2))

groove = next(s for s in SECTIONS if s['id'] == 'D')
current = groove['start']
min_clearance = float('inf')
for g, pt, r, _, _, _ in groove['moves']:
    arc = solve_arc(current, pt, r, g) if r else None
    for j in range(401):
        t = j/400
        if arc:
            c, a, sweep = arc
            z = c[0]+r*math.cos(a+sweep*t)
            rad = c[1]+r*math.sin(a+sweep*t)
        else:
            z = current[1]+(pt[1]-current[1])*t
            rad = (current[0]+(pt[0]-current[0])*t)/2
        for k in range(61):
            clearance = rad - part_radius(z + 1.5*k/60)
            min_clearance = min(min_clearance, clearance)
    current = pt
assert min_clearance > -1e-7
assert abs(SECTIONS[0]['moves'][-1][1][0]-SECTIONS[1]['start'][0]) < 1e-12
assert SECTIONS[0]['moves'][-1][1] == SECTIONS[1]['start']
assert SECTIONS[3]['moves'][-1][1] == SECTIONS[4]['start']
assert rounded_point(groove['moves'][-1][1]) == (16.0, 14.2)
assert SECTIONS[3]['start'] == (16, 15.7)  # Re-entry, not a direct D continuation.

report = dict(code_identity=True, code_line_count=len(code_lines(cn_path)),
              arc_count=len(arc_checks), arc_checks=arc_checks,
              max_point_rounding_error_mm=max_point_rounding_error,
              groove_min_blade_clearance_mm=min_clearance,
              controller_simulation=False, machine_validation=False)
(OUT/'校核'/'核查数据.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
