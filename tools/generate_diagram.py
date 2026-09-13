#!/usr/bin/env python3
"""Generate a deterministic architecture diagram from a simple JSON spec."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
COLORS={'external':'EEF4FA','control':'FFF4DF','runtime':'E8F7F7','data':'EAF3FB'}
def font(size,bold=False):
    # Prefer the Liberation Sans bundled in latex/fonts/ so diagram rendering is
    # identical on every host; fall back to system Arial only if it is missing.
    name='LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf'
    paths=[str(Path(__file__).resolve().parents[1]/'latex/fonts'/name),
           '/usr/share/fonts/msttcorefonts/Arial_Bold.ttf' if bold else '/usr/share/fonts/msttcorefonts/Arial.ttf',
           '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf' if bold else '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf']
    for p in paths:
        try:return ImageFont.truetype(p,size)
        except:pass
    return ImageFont.load_default()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--output'); args=ap.parse_args(); spec=json.loads(Path(args.spec).read_text()); out=Path(args.output or f"{spec['id']}.png")
    im=Image.new('RGB',(spec.get('width',1800),spec.get('height',1000)),'FFFFFF'); d=ImageDraw.Draw(im); nodes={n['id']:n for n in spec['nodes']}
    d.text((60,35),spec['title'],font=font(42,True),fill='#102A4C')
    for e in spec.get('edges',[]):
        a,b=nodes[e['from']],nodes[e['to']]; x1,y1=a['x']+a['w'],a['y']+a['h']/2; x2,y2=b['x'],b['y']+b['h']/2; d.line((x1,y1,x2,y2),fill='#1769D2',width=8); d.polygon([(x2,y2),(x2-22,y2-13),(x2-22,y2+13)],fill='#1769D2'); d.text(((x1+x2)/2-40,(y1+y2)/2-30),e.get('label',''),font=font(22),fill='#173E68')
    for n in spec['nodes']:
        fill='#'+COLORS.get(n.get('kind'),'EEF4FA'); box=(n['x'],n['y'],n['x']+n['w'],n['y']+n['h']); d.rounded_rectangle(box,24,fill=fill,outline='#102A4C',width=5); label=n['label']; bb=d.multiline_textbbox((0,0),label,font=font(30,True),align='center'); d.multiline_text((n['x']+(n['w']-(bb[2]-bb[0]))/2,n['y']+(n['h']-(bb[3]-bb[1]))/2),label,font=font(30,True),fill='#12233F',align='center')
    im.save(out,optimize=True); print(out)
if __name__=='__main__': main()
