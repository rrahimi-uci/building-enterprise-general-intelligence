#!/usr/bin/env python3
"""Generate the deterministic publication cover from source art and book.json."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,json,hashlib

def font_path(bold=False,root:Path|None=None):
    """Resolve an Arial-metric font, preferring the copy bundled in this repo.

    latex/fonts/ ships Liberation Sans under the SIL OFL for exactly this reason:
    it makes cover generation deterministic and host-independent. Falling back to
    whatever the operating system happens to have installed is a determinism
    hazard, and the fixed Linux paths below do not exist on macOS at all.
    """
    name='LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf'
    bundled=(root or Path(__file__).resolve().parents[1])/'latex/fonts'/name
    if bundled.exists(): return str(bundled)
    candidates=(['/usr/share/fonts/msttcorefonts/Arial_Bold.ttf','/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf','/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf'] if bold else ['/usr/share/fonts/msttcorefonts/Arial.ttf','/usr/share/fonts/truetype/msttcorefonts/Arial.ttf','/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf'])
    for p in candidates:
        if Path(p).exists(): return p
    raise FileNotFoundError(f'No Arial-metric font found. Expected the bundled {bundled}')

def generate(root:Path)->Path:
    cfg=json.loads((root/'config/book.json').read_text())['book']
    # Artwork drawn from code by tools/render_cover_art.py (make cover-art): the
    # book's thesis as one picture. Committed, so this step needs only Pillow.
    src=root/'assets/cover/cover-art.png'
    out=root/'assets/cover/cover-v1.0.0.png'
    art=Image.open(src).convert('RGB'); W,H=2550,3300
    scale=max(W/art.width,H/art.height)
    art=art.resize((int(art.width*scale),int(art.height*scale)),Image.Resampling.LANCZOS)
    art=art.crop(((art.width-W)//2,(art.height-H)//2,(art.width+W)//2,(art.height+H)//2)).convert('RGBA')
    overlay=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay)
    for y in range(H):
        top=max(0,1-y/1480); bottom=max(0,(y-2180)/1120)
        alpha=int(min(225,178*top+165*bottom)); od.line((0,y,W,y),fill=(3,17,38,alpha))
    im=Image.alpha_composite(art,overlay); d=ImageDraw.Draw(im)
    reg,bold=font_path(False,root),font_path(True,root)
    F=lambda n,b=False: ImageFont.truetype(bold if b else reg,n)
    # Cover wording comes from config/book.json so a retitle is one edit rather
    # than a hunt through the generator.
    art=cfg.get('cover',{})
    eyebrow=art.get('eyebrow','ENTERPRISE ARCHITECTURE REFERENCE')
    # The title is set horizontally and wrapped to the cover's text column:
    # words are filled greedily onto each line until the next word would cross
    # the right margin, so a retitle reflows without hand-made line breaks.
    title_font=F(150,True)
    left,right=165,W-165
    def wrap(text):
        lines=[]
        for word in text.split():
            trial=(lines[-1]+' '+word) if lines else word
            if lines and d.textlength(trial,font=title_font)<=right-left: lines[-1]=trial
            else: lines.append(word)
        return lines
    title_lines=wrap(art.get('title',cfg['title']).upper())
    subtitle=art.get('subtitle','ARCHITECTING GOVERNED AGENTIC SYSTEMS')
    d.rounded_rectangle((165,145,1215,245),radius=22,fill=(24,104,210,225))
    d.text((215,175),eyebrow,font=F(45,True),fill='white')
    y=360
    for line in title_lines:
        d.text((left,y),line,font=title_font,fill='white',stroke_width=2,stroke_fill=(8,31,58)); y+=170
    title_width=max(d.textlength(line,font=title_font) for line in title_lines)
    subtitle_y=y+20
    d.text((170,subtitle_y),subtitle,font=F(44,True),fill=(81,220,234))
    divider_y=subtitle_y+110
    # The rule under the subtitle spans the widest title line, so the block reads as one unit.
    d.line((170,divider_y,int(left+title_width),divider_y),fill=(224,154,50),width=10)
    for i,line in enumerate(art.get('themes',[])):
        d.text((175,divider_y+60+i*68),line,font=F(41),fill=(224,238,249))
    d.rounded_rectangle((155,2740,1325,2920),radius=26,fill=(5,25,52,225),outline=(81,220,234,255),width=4)
    d.text((205,2780),cfg['author'].upper(),font=F(70,True),fill='white')
    d.text((165,3020),art.get('strapline',''),font=F(34),fill=(205,225,241))
    rendered=im.convert('RGB')
    # PNG bytes are only reproducible for a fixed zlib build: the same pixels
    # compress differently under a different zlib/libdeflate version, even with
    # compress_level pinned. Rewriting the file would then change the released
    # cover hash on nothing but a host difference. So compare pixels, not bytes,
    # and leave an already-correct file untouched.
    unchanged=False
    if out.exists():
        with Image.open(out) as existing:
            unchanged=existing.convert('RGB').tobytes()==rendered.tobytes()
    if not unchanged:
        rendered.save(out,format='PNG',compress_level=9,optimize=False)
    print(json.dumps({'cover':str(out.relative_to(root)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'width':W,'height':H,'rewritten':not unchanged},indent=2))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); a=ap.parse_args(); generate(a.root.resolve())
