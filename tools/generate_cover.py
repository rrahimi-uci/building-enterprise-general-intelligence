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
    return _save(rendered,out,root,W,H)

def _save(rendered,out:Path,root:Path,W:int,H:int)->Path:
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

def back_alt(root:Path)->str:
    """Alternative text for the back cover: its own words, in reading order."""
    cfg=json.loads((root/'config/book.json').read_text())['book']; b=cfg['cover']['back']
    return ' '.join([f"Back cover: {cfg['title']}.",b['headline'],*b['paragraphs'],' '.join(b['principle']),b['learn_heading'].capitalize()+': '+'; '.join(b['learn'])+'.',b['case'],b['audience'],b['author_line']])

def generate_back(root:Path)->Path:
    """Back cover: the same cover art, darker, carrying the book description.

    Every word comes from config/book.json (cover.back), so the description is
    one edit away. Text is laid out to the column width, never hand-broken.
    """
    book=json.loads((root/'config/book.json').read_text())['book']; cfg=book['cover']; b=cfg['back']
    out=root/f"assets/cover/back-cover-v{book['version']}.png"
    art=Image.open(root/'assets/cover/cover-art.png').convert('RGB'); W,H=2550,3300
    scale=max(W/art.width,H/art.height)
    art=art.resize((int(art.width*scale),int(art.height*scale)),Image.Resampling.LANCZOS)
    art=art.crop(((art.width-W)//2,(art.height-H)//2,(art.width+W)//2,(art.height+H)//2)).convert('RGBA')
    overlay=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay)
    for y in range(H): od.line((0,y,W,y),fill=(3,17,38,246))
    im=Image.alpha_composite(art,overlay); d=ImageDraw.Draw(im)
    reg,bold=font_path(False,root),font_path(True,root)
    F=lambda n,bd=False: ImageFont.truetype(bold if bd else reg,n)
    left,right=200,W-200; width=right-left
    def wrap(text,font,limit=width):
        lines=[]
        for word in text.split():
            trial=(lines[-1]+' '+word) if lines else word
            if lines and d.textlength(trial,font=font)<=limit: lines[-1]=trial
            else: lines.append(word)
        return lines
    def balanced(text,font):
        # Narrowest column that keeps the greedy line count, so a headline never
        # ends on a one-word last line.
        n=len(wrap(text,font)); lo,hi=width//3,width
        while hi-lo>4:
            mid=(lo+hi)//2
            if len(wrap(text,font,mid))<=n: hi=mid
            else: lo=mid
        return wrap(text,font,hi)
    def block(text,font,y,fill,lead,limit=width,x=left):
        for line in wrap(text,font,limit): d.text((x,y),line,font=font,fill=fill); y+=lead
        return y
    d.rounded_rectangle((165,145,1215,245),radius=22,fill=(24,104,210,225))
    d.text((215,175),cfg.get('eyebrow',''),font=F(45,True),fill='white')
    y=370
    for line in balanced(b['headline'],F(104,True)):
        d.text((left,y),line,font=F(104,True),fill='white',stroke_width=2,stroke_fill=(8,31,58)); y+=132
    y+=40; d.line((left,y,left+560,y),fill=(224,154,50),width=10); y+=84
    for text in b['paragraphs']: y=block(text,F(51),y,(224,238,249),76)+34
    # The principle: three short sentences in a framed panel, set apart because
    # it is the one line a reader should leave with.
    y+=34; lines=b['principle']; panel_h=76+len(lines)*104
    d.rounded_rectangle((left-20,y,right+20,y+panel_h),radius=26,fill=(5,25,52,235),outline=(81,220,234,255),width=4)
    py=y+34
    for line in lines: d.text((left+44,py),line,font=F(80,True),fill=(81,220,234) if line is lines[-1] else 'white'); py+=104
    y+=panel_h+100
    d.text((left,y),b['learn_heading'],font=F(42,True),fill=(224,154,50)); y+=90
    for item in b['learn']:
        d.ellipse((left+4,y+22,left+30,y+48),fill=(81,220,234))
        y=block(item,F(50),y,(224,238,249),70,limit=width-70,x=left+66)+20
    y+=40; y=block(b['case'],F(50,True),y,'white',72)+26
    block(b['audience'],F(50),y,(205,225,241),72)
    d.line((left,2900,right,2900),fill=(81,220,234),width=3)
    d.text((left,2940),book['author'].upper(),font=F(58,True),fill='white')
    block(b['author_line'],F(38),3028,(205,225,241),54)
    d.text((left,3170),cfg.get('strapline',''),font=F(34),fill=(160,190,215))
    return _save(im.convert('RGB'),out,root,W,H)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); a=ap.parse_args(); generate(a.root.resolve()); generate_back(a.root.resolve())
