from pathlib import Path
import json, re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path('/Users/wanghu/Documents/ChatGPT/加工工序学习')
OUT=ROOT/'学习总整理'
OUT.mkdir(exist_ok=True)
doc=Document()
for el in doc.styles.element.xpath('.//w:pBdr'):
 el.getparent().remove(el)
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=Inches(.62);sec.bottom_margin=Inches(.60)
sec.left_margin=sec.right_margin=Inches(.72)
sec.footer_distance=Inches(.25)
for name,size in [('Normal',11),('Title',28),('Subtitle',14),('Heading 1',20),('Heading 2',13),('Heading 3',11),('Caption',9)]:
 s=doc.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.color.rgb=RGBColor(0,0,0)
 s.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Arial Unicode MS')
 for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
  s.element.get_or_add_rPr().rFonts.attrib.pop(qn('w:'+key),None)
 s.paragraph_format.space_after=Pt(5)
 s.paragraph_format.line_spacing=1.12
 if name.startswith('Heading'):s.paragraph_format.space_before=Pt(8);s.paragraph_format.keep_with_next=True
normal=doc.styles['Normal'];normal.paragraph_format.widow_control=True
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=footer.add_run('加工工序学习  ·  ');r.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
pages=[]; current=None
def new(title,part=None):
 global current
 nextpage=bool(pages)
 current={'title':title,'text':[]};pages.append(current)
 if part:
  pp=doc.add_paragraph(part);pp.paragraph_format.space_after=Pt(3)
  pp.paragraph_format.page_break_before=nextpage;pp.paragraph_format.keep_with_next=True
  for r in pp.runs:r.font.size=Pt(9);r.font.color.rgb=RGBColor.from_string('555555')
 pp=doc.add_paragraph(title,'Heading 1')
 if not part:pp.paragraph_format.page_break_before=nextpage
 bid=len(pages);start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),str(bid));start.set(qn('w:name'),f'page{bid}')
 end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(bid));pp._p.insert(0,start);pp._p.append(end)
 return pp
def p(text,bold=False,small=False):
 pp=doc.add_paragraph()
 for i,s in enumerate(re.split(r'(\*\*.*?\*\*)',text)):
  rr=pp.add_run(s[2:-2] if s.startswith('**') else s);rr.bold=bold or s.startswith('**')
  if small:rr.font.size=Pt(9)
 if small:pp.paragraph_format.space_after=Pt(4)
 current['text'].append(text)
 return pp
def h(text):doc.add_paragraph(text,'Heading 2');current['text'].append(text)
def table(headers,rows,widths=None):
 t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 widths=widths or [7.06/len(headers)]*len(headers)
 for col,w in zip(t.columns,widths):col.width=Inches(w)
 pr=t._tbl.tblPr;b=OxmlElement('w:tblBorders')
 for edge in ('top','left','bottom','right','insideH','insideV'):
  x=OxmlElement('w:'+edge);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'D9D9D9');b.append(x)
 pr.append(b)
 for ri,rowdata in enumerate([headers]+rows):
  cells=t.rows[0].cells if ri==0 else t.add_row().cells
  trpr=cells[0]._tc.getparent().get_or_add_trPr();nosplit=OxmlElement('w:cantSplit');trpr.append(nosplit)
  if ri==0:
   repeat=OxmlElement('w:tblHeader');trpr.append(repeat)
  for ci,(cell,txt) in enumerate(zip(cells,rowdata)):
   cell.width=Inches(widths[ci]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   tcpr=cell._tc.get_or_add_tcPr();m=OxmlElement('w:tcMar')
   for side in ('top','bottom','left','right'):
    v=OxmlElement('w:'+side);v.set(qn('w:w'),'65' if side in ('top','bottom') else '90');v.set(qn('w:type'),'dxa');m.append(v)
   tcpr.append(m);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DFEAF1' if ri==0 else ('F4F7F9' if ri%2==0 else 'FFFFFF'));tcpr.append(shade)
   pp=cell.paragraphs[0];pp.paragraph_format.space_after=Pt(1);pp.paragraph_format.space_before=Pt(1);pp.paragraph_format.line_spacing=1.12
   if ci==0 and len(str(txt))<14:pp.alignment=WD_ALIGN_PARAGRAPH.CENTER
   rr=pp.add_run(str(txt));rr.font.size=Pt(10);rr.bold=(ri==0)
  current['text'].append(' | '.join(map(str,rowdata)))
 spacer=doc.add_paragraph();spacer.paragraph_format.space_after=Pt(0);spacer.paragraph_format.space_before=Pt(0);spacer.paragraph_format.line_spacing=Pt(4);spacer.add_run().font.size=Pt(1)
 return t
def code(text):
 pp=doc.add_paragraph();pp.paragraph_format.space_after=Pt(7);pp.paragraph_format.line_spacing=1.05
 pp.paragraph_format.keep_together=True
 rr=pp.add_run(text);rr.font.name='Menlo';rr.font.size=Pt(9.5)
 current['text'].append(text)
def img(path,width=6.8,caption=''):
 pp=doc.add_paragraph();pp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pp.paragraph_format.space_after=Pt(2)
 rr=pp.add_run();sh=rr.add_picture(str(ROOT/path),width=Inches(width));sh._inline.docPr.set('descr',caption or Path(path).stem)
 if caption:doc.add_paragraph(caption,'Caption')
def source(text):p('依据  '+text,small=True)
def link(text,target):
 pp=doc.add_paragraph();hyp=OxmlElement('w:hyperlink');hyp.set(qn('w:anchor'),f'page{target}')
 rr=OxmlElement('w:r');rpr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'234D68');rpr.append(c);rr.append(rpr);tt=OxmlElement('w:t');tt.text=text;rr.append(tt);hyp.append(rr);pp._p.append(hyp)
 current['text'].append(text)
def math(text):
 pp=doc.add_paragraph();om=OxmlElement('m:oMath');mr=OxmlElement('m:r');mt=OxmlElement('m:t');mt.text=text;mr.append(mt);om.append(mr);pp._p.append(om)
 current['text'].append(text)

exec((ROOT/'tmp/book/content.py').read_text())
doc.core_properties.title='加工工序与G代码分类对比学习手册'
doc.core_properties.subject='按工序用途分类 同类代码横向比较 知识层级纵向学习'
doc.core_properties.author=''
doc.save(OUT/'加工工序学习综合手册.docx')
(ROOT/'tmp/book/page_content.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
print('Saved',len(pages),'planned pages')
