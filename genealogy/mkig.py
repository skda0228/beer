import re, sys
src, out = sys.argv[1], sys.argv[2]
html = open(src, encoding='utf-8').read()
style = re.search(r'<style>.*?</style>', html, re.S).group(0)
svg = re.search(r'<svg\b.*?</svg>', html, re.S).group(0)
i = svg.index('>')
head = svg[:i]
# viewBox on the <svg> element itself — not on any nested <marker>
x, y, w, h = re.search(r'viewBox="(-?[\d.]+) (-?[\d.]+) ([\d.]+) ([\d.]+)"', head).groups()
head = head.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s"' % (w, h), 1)
bg = '<rect x="%s" y="%s" width="%s" height="%s" fill="var(--panel)"/>' % (x, y, w, h)
open(out, 'w', encoding='utf-8').write(head + '>' + style + bg + svg[i+1:])
print(out, w, h)
