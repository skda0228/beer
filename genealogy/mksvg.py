import re, sys

CSS = """
<style>
  :root{
    --panel:#FFFFFF; --panel-2:#F7F9FB; --ink:#12161D; --ink-2:#48515F; --ink-3:#798393;
    --rule-2:#E6EAEF;
    --kirin:#1B7A4B; --sapporo:#A0721A; --asahi:#1F5FA8; --yebisu:#932F48;
    --suntory:#57429E; --orion:#0A716E; --trunk:#454B57;
    --hite:#12736A; --ob:#AE3244; --jinro:#A0721A; --lotte:#57429E; --craft:#1F5FA8; --jp:#798393;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --panel:#161A21; --panel-2:#1B2028; --ink:#E7EAF0; --ink-2:#A7AFBD; --ink-3:#767F8E;
      --rule-2:#232932;
      --kirin:#4FC183; --sapporo:#DFA845; --asahi:#63A3E8; --yebisu:#E17E96;
      --suntory:#9E8AE0; --orion:#3EC0BA; --trunk:#AEB6C4;
      --hite:#3FBDAF; --ob:#E8798C; --jinro:#DFA845; --lotte:#9E8AE0; --craft:#63A3E8; --jp:#7C8695;
    }
  }
  .bg{fill:var(--panel)}
  text{font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,sans-serif}
  .lane{fill:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round}
  .lane.thin{stroke-width:3}
  .lane.trunk{stroke-width:8.5;stroke:var(--trunk)}
  .lane.ghost{stroke-width:2.5;stroke-dasharray:2 7;opacity:.62}
  .k{stroke:var(--kirin)} .s{stroke:var(--sapporo)} .a{stroke:var(--asahi)}
  .y{stroke:var(--yebisu)} .u{stroke:var(--suntory)} .o{stroke:var(--orion)}
  .fk{fill:var(--kirin)} .fs{fill:var(--sapporo)} .fa{fill:var(--asahi)}
  .fy{fill:var(--yebisu)} .fu{fill:var(--suntory)} .fo{fill:var(--orion)}
  .h{stroke:var(--hite)} .b{stroke:var(--ob)} .j{stroke:var(--jinro)}
  .t{stroke:var(--lotte)} .g{stroke:var(--jp)}
  .fh{fill:var(--hite)} .fb{fill:var(--ob)} .fj{fill:var(--jinro)}
  .ft{fill:var(--lotte)} .fg{fill:var(--jp)} .fc{fill:var(--craft)}
  .dot{stroke:var(--panel);stroke-width:2.5}
  .yr{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;font-weight:700;fill:var(--ink-3)}
  .yr.big{font-size:17px;fill:var(--ink)}
  .lbl{font-size:12.5px;font-weight:600;fill:var(--ink)}
  .lbl.sub{font-size:11px;font-weight:500;fill:var(--ink-3)}
  .lbl.big{font-size:14px;font-weight:750}
  .foot{font-size:13.5px;font-weight:750;fill:var(--ink)}
  .gridline{stroke:var(--rule-2);stroke-width:1}
  .band{fill:var(--trunk);opacity:.055}
  .axnote{font-size:10.5px;fill:var(--ink-3);font-family:ui-monospace,Menlo,monospace}
  .bar{fill:var(--craft)}
  .barlab{font-size:12px;font-weight:700;fill:var(--ink);font-family:ui-monospace,Menlo,monospace}
</style>
"""

def extract(html, idx):
    blocks = re.findall(r'<svg\b.*?</svg>', html, re.S)
    return blocks[idx]

src, idx, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
html = open(src, encoding='utf-8').read()
svg = extract(html, idx)
vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
w, h = vb.group(1), vb.group(2)
# strip the trailing '>' of the opening tag to inject attrs + style + bg
open_tag_end = svg.index('>')
head = svg[:open_tag_end]
body = svg[open_tag_end+1:]
head = head.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s"' % (w, h), 1)
doc = head + '>' + CSS + '<rect class="bg" x="0" y="0" width="%s" height="%s"/>' % (w, h) + body
open(out, 'w', encoding='utf-8').write(doc)
print(out, len(doc), 'bytes')
