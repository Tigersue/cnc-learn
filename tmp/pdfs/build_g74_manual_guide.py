from pathlib import Path
import json
import os
import subprocess
import sys
from xml.sax.saxutils import escape

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage

ROOT = Path('/Users/wanghu/Documents/ChatGPT/加工工序学习')
WORK = ROOT / 'tmp/pdfs/g74-manual'
ASSETS = ROOT / 'G74学习资料/手册原图'
OUT = ROOT / 'output/pdf/G74_手册原图与实例对照.pdf'
TROOT = Path('/Users/wanghu/.agents/skills/tsugami-s20a-machining')
TSRC = TROOT / 'assets/manual-excerpt.pdf'
FSRC = ROOT / 'G75学习资料/参考资料/FANUC_0i-F_车床操作手册_B-64604EN-1.pdf'
META = json.loads((TROOT / 'references/source.json').read_text())
TMAP = {p['original_pdf_page']: p['excerpt_page'] for p in META['pages']}
SOURCES = [
    ('fanuc-092', FSRC, 92, 'FANUC G74 格式原页｜纸面78，原PDF92'),
    ('fanuc-093', FSRC, 93, 'FANUC G74 刀路原页｜纸面79，原PDF93'),
    ('tsugami-293', TSRC, TMAP[293], '津上 G代码表｜纸面7-25，原PDF293'),
    ('tsugami-335', TSRC, TMAP[335], '津上 正面钻孔｜纸面7-67，原PDF335'),
    ('tsugami-344', TSRC, TMAP[344], '津上 深孔钻加工｜纸面7-76，原PDF344'),
    ('tsugami-342', TSRC, TMAP[342], '津上 正面割槽（T铣刀）｜纸面7-74，原PDF342'),
    ('tsugami-345', TSRC, TMAP[345], '津上 Z1/Z2同步例｜纸面7-77，原PDF345'),
]

def prepare():
    WORK.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    cache = WORK / 'fontcache'
    cache.mkdir(exist_ok=True)
    config = WORK / 'fonts.conf'
    config.write_text('<fontconfig><dir>/System/Library/Fonts</dir><dir>/System/Library/Fonts/Supplemental</dir><cachedir>' + str(cache) + '</cachedir></fontconfig>')
    env = dict(os.environ, FONTCONFIG_FILE=str(config), XDG_CACHE_HOME=str(cache))
    for name, source, page, label in SOURCES:
        output = ASSETS / name
        result = subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile', '-r', '160', '-png', str(source), str(output)], env=env, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr[-2000:])
        print(label)
    crops = [
        ('tsugami-335', 'tsugami-335-drilling', (0.12,0.08,0.88,0.54)),
        ('fanuc-093', 'fanuc-g74-path', (0.24,0.10,0.79,0.435)),
    ]
    for src, dest, box in crops:
        im = Image.open(ASSETS / (src + '.png'))
        rect = tuple(round(v*(im.width if i%2 == 0 else im.height)) for i,v in enumerate(box))
        im.crop(rect).save(ASSETS / (dest+'.png'))
    print('Original-page images and crops prepared.')

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont('CJK', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
    styles = {
        'title': ParagraphStyle('title', fontName='CJK', fontSize=23, leading=32, textColor=colors.HexColor('#143b51'), spaceAfter=15),
        'h': ParagraphStyle('h', fontName='CJK', fontSize=14, leading=21, textColor=colors.HexColor('#143b51'), spaceBefore=12, spaceAfter=6),
        'body': ParagraphStyle('body', fontName='CJK', fontSize=10.2, leading=16.2, wordWrap='CJK', spaceAfter=7),
        'small': ParagraphStyle('small', fontName='CJK', fontSize=8.8, leading=13, wordWrap='CJK', spaceAfter=4, textColor=colors.HexColor('#4a5560')),
        'code': ParagraphStyle('code', fontName='Courier', fontSize=9.2, leading=14, spaceAfter=1),
    }
    def p(txt, style='body'):
        return Paragraph(escape(txt).replace('\n','<br/>'), styles[style])
    def table(rows, widths):
        data = [[p(str(v), 'small' if j else 'body') for v in row] for j,row in enumerate(rows)]
        t=Table(data, colWidths=widths, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9f0f4')),
            ('LINEBELOW',(0,0),(-1,0),0.8,colors.HexColor('#a0b2bd')),
            ('LINEBELOW',(0,1),(-1,-1),0.3,colors.HexColor('#d6dfe4')),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ]))
        return t
    story=[]
    story += [p('G74 手册原图与实例对照','title'), p('津上 S205A/S206A × FANUC 车床控制器｜原图、原程序、中文讲解','small'), Spacer(1,12)]
    story += [p('核查结论','h'), p('津上手册的G代码表列有G74“端面切断循环”；本次检查的§7.9-7.10（原PDF332-366页）未找到直接调用G74的原程序或专属刀路图。FANUC控制器手册§4.2.5则有G74完整格式、参数表和刀路图。')]
    story += [p('最有用的组合读法','h'), p('先看FANUC原图理解循环动作，再对照津上§7.9.2的手写断屑钻孔，最后回到自拟环槽例计算刀宽和参考点。原文、解释和自拟例分别标明。')]
    story += [table([
        ['内容','来源定位','本册页'],
        ['G74格式与参数','FANUC §4.2.5；纸面78-79；原PDF92-93','4-5'],
        ['本机G74名称','津上 §7.5；纸面7-25；原PDF293','6'],
        ['分段断屑钻孔原例','津上 §7.9.2(1)；纸面7-67；原PDF335','7'],
        ['深孔装置与进退条件','津上 §7.9.4；纸面7-76；原PDF344','8'],
        ['T铣刀正面割槽辨析','津上 §7.9.3(4)；纸面7-74；原PDF342','9'],
        ['同步切槽刀例辨析','津上 §7.9.5；纸面7-77；原PDF345','10'],
    ],[145,285,55]), Spacer(1,10)]
    story += [p('第4-10页保留原页内容。津上“原PDF页”按485页上传文件映射；它与技能节选文件的页序不同。FANUC为B-64604EN-1/01（0i-F），用于格式对照；本机资料封面与前言存在版本差异，现场适用性仍须核对。','small')]
    story += [PageBreak(), p('把 G74 原图读成动作','title')]
    image_path=ASSETS/'fanuc-g74-path.png'
    im=Image.open(image_path)
    img_w=390; img_h=img_w*im.height/im.width
    story += [RLImage(str(image_path),width=img_w,height=img_h), p('原图：FANUC §4.2.5，纸面79（原PDF93）。括号(R)/(F)是运动类型；不是程序中的R地址。','small')]
    story += [table([
        ['原图符号','中文对应'],
        ['A / C / B','起点 / 首列切入终点 / 最后X与起始Z的交点'],
        ['e → 第一行R','Z向小回退；回退后直接工进至下一最深点'],
        ['Δk → Q','Z向相邻最深点增量；末啄Δk′可小于Q'],
        ['Δi → P','X向径向换列；末次Δi′可小于P'],
        ['Δd → 第二行R','槽底X向让刀，之后沿Z退出'],
        ['U/2 / W','参考点径向总跨度 / 轴向总跨度'],
    ],[135,350])]
    story += [p('方向须看原图：FANUC原图+Z向右，切入向左为-Z；津上前述教学例+Z向左入料。不能照抄符号。原图路径末端到B，未画B返回A；第二行R0时无槽底附加X让刀。','small')]
    story += [PageBreak(), p('用津上原例理解断屑退刀','title'), p('津上 §7.9.2(1)，纸面7-67（原PDF335）；T15正面钻孔，完整工件图及其余工序见本册第7页。下列保持原程序拼写。','small')]
    code=['N1 M03 S2000 G0 Z-1.0 T1515','X0','M12','G99 G1 Z2.0 F0.02','W-0.2','Z6.0 F0.04','W-0.2','Z10.0','G04 U0.1','G00 Z-1.0 T0']
    for line in code:
        story.append(p(line,'code'))
    story += [Spacer(1,10),table([
        ['原程序动作','与G74对应的概念'],
        ['Z2 → 1.8 → 6 → 5.8 → 10','深入、退0.2、继续深入；W-0.2帮助理解首行R'],
        ['从起点Z-1计，新增深入3、4、4 mm','首段与后段不同，不能直接当固定Q原例'],
        ['F0.02 → F0.04','原例改变进给，单一固定F的G74不能原样表达'],
        ['G04 U0.1','原例有孔底延时；本G74格式未提供对应延时地址'],
        ['W-0.2继承G1及当前F','原例为工进小退刀；G74原图的小回退标为快速运动'],
    ],[230,255])]
    story += [p('另两种“槽”要区分','h'), p('§7.9.3(4)用T铣刀、主轴定位和G98 G01完成端面铣槽；§7.9.5用T23切槽刀配合Z1/Z2同步。二者均非G74端面啄切原例。')]
    story += [p('深孔原例的边界','h'), p('§7.9.4采用双通道、T91与专用安装补正，手写进退程序。原页确写“Z-30.0 F0.05”，与此前Z23.5的关系需核实；本册原样保留负号，不改成Z30.0，不据此生成G74生产程序。','small')]
    story += [p('以上原例数值仅在其原图和刀具条件下解读。主笔记中的φ10-φ16环槽、P1000/Q1000等为自拟教学条件。','small')]
    intro=WORK/'intro.pdf'
    def footer(c,doc):
        c.saveState();c.setFont('CJK',8);c.setFillColor(colors.HexColor('#5b6872'))
        c.drawString(55,27,'G74 原图与实例对照 · 2026-10-27')
        c.drawRightString(A4[0]-55,27,str(doc.page));c.restoreState()
    SimpleDocTemplate(str(intro), pagesize=A4,rightMargin=55,leftMargin=55,topMargin=43,bottomMargin=43).build(story,onFirstPage=footer,onLaterPages=footer)
    intro_reader=PdfReader(intro)
    if len(intro_reader.pages)!=3:
        raise RuntimeError('Intro must be exactly 3 pages, got '+str(len(intro_reader.pages)))
    writer=PdfWriter()
    writer.append(intro_reader,import_outline=False)
    writer.add_outline_item('核查结论与阅读顺序',0)
    writer.add_outline_item('G74原图中文对照',1)
    writer.add_outline_item('津上断屑钻孔逐行对照',2)
    readers={}
    for name,source,page,label in SOURCES:
        if source not in readers:readers[source]=PdfReader(source)
        writer.add_page(readers[source].pages[page-1])
        writer.add_outline_item(label,len(writer.pages)-1)
    writer.add_metadata({'/Title':'G74 手册原图与实例对照','/Author':'学习资料整理','/Subject':'津上3281-LTQ0C-05与FANUC B-64604EN-1/01原图对照'})
    with OUT.open('wb') as f:writer.write(f)
    check=PdfReader(OUT)
    assert len(check.pages)==10
    print(str(OUT)+' | 10 pages')

if __name__=='__main__':
    prepare() if sys.argv[1]=='prepare' else build()
