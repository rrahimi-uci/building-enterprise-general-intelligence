from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, textwrap

OUT=Path('/data/v3_diagrams'); OUT.mkdir(exist_ok=True)
W,H=1800,1000
BG='#F5F8FC'; NAVY='#102A4C'; NAVY2='#173E68'; BLUE='#1769D2'; CYAN='#20B8D8'; TEAL='#118A84'; AMBER='#E09A32'; RED='#C94A4A'; GRAY='#60758D'; LIGHT='#E7EFF8'; WHITE='#FFFFFF'; INK='#12233F'
font_path='/usr/share/fonts/msttcorefonts/Arial.ttf'
bold_path='/usr/share/fonts/msttcorefonts/Arial_Bold.ttf'
if not Path(font_path).exists():
    font_path='/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf'; bold_path='/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf'

def F(size,bold=False): return ImageFont.truetype(bold_path if bold else font_path,size)

def new(title, subtitle=''):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,35,W-40,H-35),radius=34,fill=WHITE,outline='#C9D7E6',width=3)
    d.rounded_rectangle((40,35,W-40,170),radius=34,fill=NAVY)
    d.rectangle((40,110,W-40,170),fill=NAVY)
    d.text((85,68),title,font=F(48,True),fill=WHITE)
    if subtitle: d.text((88,128),subtitle,font=F(23),fill='#B9D6F2')
    return im,d

def wrap(text,width): return textwrap.wrap(text,width=width,break_long_words=False)

def box(d,xy,text,fill=LIGHT,outline=BLUE,title=None,small=False):
    x1,y1,x2,y2=xy
    d.rounded_rectangle(xy,radius=18,fill=fill,outline=outline,width=3)
    if title:
        d.rounded_rectangle((x1,y1,x2,y1+44),radius=16,fill=outline)
        d.rectangle((x1,y1+24,x2,y1+44),fill=outline)
        d.text((x1+18,y1+10),title,font=F(24,True),fill=WHITE)
        y=y1+58
    else: y=y1+18
    size=21 if small else 25
    lines=wrap(text, max(10,int((x2-x1)/(size*0.56))))
    total=len(lines)*(size+6)
    if not title: y=max(y,(y1+y2-total)//2)
    for line in lines:
        bbox=d.textbbox((0,0),line,font=F(size,False)); tw=bbox[2]
        d.text(((x1+x2-tw)//2,y),line,font=F(size,False),fill=INK)
        y+=size+6

def arrow(d,p1,p2,color=GRAY,width=5):
    d.line([p1,p2],fill=color,width=width)
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0]); al=18
    for a in (ang+2.6,ang-2.6):
        d.line([p2,(p2[0]+al*math.cos(a),p2[1]+al*math.sin(a))],fill=color,width=width)

def save(im,key): im.save(OUT/f'{key}.png',quality=95)

def grid_flow(key,title,nodes,cols=4,subtitle='Responsibility and evidence flow'):
    im,d=new(title,subtitle); rows=math.ceil(len(nodes)/cols)
    gapx,gapy=28,36; left,right,top,bottom=90,W-90,220,H-75
    bw=(right-left-gapx*(cols-1))/cols; bh=(bottom-top-gapy*(rows-1))/rows
    centers=[]
    for i,(label,color) in enumerate(nodes):
        r,c=divmod(i,cols); x=left+c*(bw+gapx); y=top+r*(bh+gapy)
        box(d,(x,y,x+bw,y+bh),label,fill='#F3F7FB',outline=color,small=True); centers.append((x+bw/2,y+bh/2))
    for i in range(len(centers)-1):
        if (i+1)%cols:
            arrow(d,(centers[i][0]+bw/2,centers[i][1]),(centers[i+1][0]-bw/2,centers[i+1][1]),CYAN,4)
        elif i+1<len(centers):
            arrow(d,(centers[i][0],centers[i][1]+bh/2),(centers[i+1][0],centers[i+1][1]-bh/2),AMBER,4)
    save(im,key)

def layers(key,title,items,subtitle='Layered enterprise control model'):
    im,d=new(title,subtitle); y=215; gap=16; bh=(H-285-gap*(len(items)-1))/len(items)
    for i,(name,desc,color) in enumerate(items):
        x1=110+i*18; x2=W-110-i*18
        d.rounded_rectangle((x1,y,x2,y+bh),radius=16,fill='#F4F8FC',outline=color,width=3)
        d.rounded_rectangle((x1,y,x1+330,y+bh),radius=16,fill=color)
        d.rectangle((x1+300,y,x1+330,y+bh),fill=color)
        d.text((x1+24,y+bh/2-16),name,font=F(28,True),fill=WHITE)
        lines=wrap(desc,80)
        yy=y+bh/2-(len(lines)*27)/2
        for line in lines:
            d.text((x1+360,yy),line,font=F(24),fill=INK); yy+=28
        y+=bh+gap
    save(im,key)

def two_col(key,title,left_title,left_items,right_title,right_items):
    im,d=new(title,'Before / after architecture and control responsibilities')
    d.rounded_rectangle((85,210,850,925),radius=25,fill='#FFF5F5',outline=RED,width=4)
    d.rounded_rectangle((950,210,1715,925),radius=25,fill='#F0FBF8',outline=TEAL,width=4)
    d.text((120,235),left_title,font=F(34,True),fill=RED); d.text((985,235),right_title,font=F(34,True),fill=TEAL)
    y=310
    for it in left_items:
        box(d,(130,y,805,y+105),it,fill=WHITE,outline=RED,small=True); y+=125
    y=310
    for it in right_items:
        box(d,(995,y,1670,y+105),it,fill=WHITE,outline=TEAL,small=True); y+=125
    arrow(d,(850,565),(950,565),AMBER,8)
    save(im,key)

def cycle(key,title,nodes,subtitle='Closed loop with governed promotion'):
    im,d=new(title,subtitle); cx,cy=W/2,585; rx,ry=650,300; n=len(nodes); centers=[]
    for i,(label,color) in enumerate(nodes):
        a=-math.pi/2+2*math.pi*i/n; centers.append((cx+rx*math.cos(a),cy+ry*math.sin(a)))
    for i in range(n): arrow(d,centers[i],centers[(i+1)%n],GRAY,4)
    for (x,y),(label,color) in zip(centers,nodes): box(d,(x-120,y-45,x+120,y+45),label,fill=WHITE,outline=color,small=True)
    d.rounded_rectangle((650,485,1150,685),radius=30,fill=NAVY)
    d.text((745,525),'Versioned evidence',font=F(32,True),fill=WHITE)
    d.text((730,575),'ChangeBundle · ReleaseManifest',font=F(24),fill='#B9D6F2')
    d.text((790,615),'Rollback · LearningRecord',font=F(24),fill='#B9D6F2')
    save(im,key)

# 0 guide map
grid_flow('book-map','Enterprise Agentic AI Architecture Guide',[(x,c) for x,c in [
('I Foundations',NAVY),('II Reference Architecture',NAVY),('III Developer Platform & SDK',BLUE),('IV Patterns',CYAN),
('V Anti-Patterns',RED),('VI Multi-Agent & Integration',BLUE),('VII LLM Gateway',AMBER),('VIII Security & Guardrails',RED),
('IX Observability & Evaluation',TEAL),('X Continuous Learning',TEAL),('XI Governance',AMBER),('XII Production Operations',NAVY2)]],4,'Twelve-part narrative from first principles to governed operation')

layers('reference-architecture','Enterprise Agentic AI Reference Architecture',[
('Experience & Channels','User intent, review, accessibility, recourse',BLUE),
('Agent Applications','Domain behavior, topology, accepted outcomes',CYAN),
('Runtime & Orchestration','Durable state, budgets, retries, joins, cancellation',NAVY2),
('Context · Memory · Skills','Authorized evidence, snapshots, provenance, reusable capabilities',TEAL),
('Gateways & Integrations','LLM, tools, MCP, A2A, APIs and events',AMBER),
('Security & Governance','Identity, policy, guardrails, approvals, audit',RED),
('Evaluation & Operations','Tracing, evaluation, release, SLOs, learning',NAVY)])

grid_flow('request-sequence','Request to Verified Outcome',[(x,c) for x,c in [
('1 Authenticate subject + workload',NAVY),('2 Admit run + pin versions',NAVY),('3 Build ContextManifest',TEAL),('4 Model proposes typed decision',CYAN),
('5 Policy + optional approval',RED),('6 Tool façade commits effect',AMBER),('7 Acceptance engine verifies',NAVY),('8 Trace + evaluate + learn',TEAL)]],4)

# Developer platform 16-capability grid
grid_flow('developer-platform','Agentic Developer Platform & SDK',[(x,[NAVY,BLUE,TEAL,AMBER][i%4]) for i,x in enumerate([
'Agent Runtime','Workflow / Orchestration','Tool SDK','MCP Integration','Agent-to-Agent','Context / RAG','Memory','Skills','Identity & Permissions','Guardrails','LLM Gateway','Evaluation','Observability / Tracing','Durable Execution','Human-in-the-Loop','Deployment & Versioning'])],4,'Reusable paved-road capabilities surrounding application-specific behavior')

im,d=new('Portable Contracts, Replaceable Adapters','Applications depend on enterprise contracts—not provider-native objects')
box(d,(90,310,420,720),'Application\nAgentSpec · TaskEnvelope',fill='#F3F7FB',outline=BLUE)
box(d,(540,240,840,430),'Framework adapter A',fill=WHITE,outline=CYAN)
box(d,(540,500,840,690),'Framework adapter B',fill=WHITE,outline=CYAN)
box(d,(960,220,1300,440),'Shared platform services\nPolicy · Tools · Context · Tracing',fill=WHITE,outline=NAVY)
box(d,(960,500,1300,720),'Provider adapters\nModels · MCP · A2A · APIs',fill=WHITE,outline=AMBER)
box(d,(1420,310,1710,720),'Providers and enterprise systems',fill='#F3F7FB',outline=TEAL)
for a,b in [((420,515),(540,335)),((420,515),(540,595)),((840,335),(960,330)),((840,595),(960,610)),((1300,330),(1420,430)),((1300,610),(1420,600))]: arrow(d,a,b)
save(im,'portability')

cycle('developer-lifecycle','Local-to-Production Agent Lifecycle',[(x,c) for x,c in [('Create',BLUE),('Attach',TEAL),('Configure',AMBER),('Test',NAVY),('Evaluate',TEAL),('Package',NAVY2),('Promote',AMBER),('Observe',BLUE),('Improve',TEAL)]])
grid_flow('dx-golden-path','Developer Golden Path',[(x,c) for x,c in [('Scaffold',BLUE),('Develop',CYAN),('Debug',TEAL),('Evaluate',TEAL),('Package',NAVY),('Promote',AMBER),('Operate',NAVY2),('Improve',TEAL)]],4,'Fast local iteration with explicit evidence and governed promotion')

# test pyramid
im,d=new('Agentic Testing and Simulation Pyramid','Higher layers are fewer, slower, and more production-realistic')
levels=[('Canary + shadow evaluation',AMBER,420),('End-to-end staging',NAVY,560),('Trajectory simulation',TEAL,720),('Component evaluation',CYAN,900),('Tool + adapter contracts',BLUE,1080),('Deterministic unit tests',NAVY2,1280)]
y=240
for label,color,width in levels:
    x=(W-width)/2; d.rounded_rectangle((x,y,x+width,y+92),radius=15,fill=color)
    bbox=d.textbbox((0,0),label,font=F(28,True)); d.text(((W-(bbox[2]-bbox[0]))/2,y+29),label,font=F(28,True),fill=WHITE); y+=108
save(im,'test-pyramid')

grid_flow('pattern-decision-tree','Pattern Selection Decision Tree',[(x,c) for x,c in [
('Known path?\nDeterministic workflow',NAVY),('Adaptive observation?\nBounded ReAct',CYAN),('Long-running/waits?\nDurable execution',NAVY),('Specialists?\nTyped tasks + join',BLUE),
('Protected effect?\nProposal + approval',RED),('Ambiguous outcome?\nEffect reconciliation',AMBER),('Cross boundary?\nIdentity + gateway',RED),('Improve after release?\nGoverned learning',TEAL)]],4,'Choose by hidden obligation, uncertainty, and risk')

two_col('anti-before-after','Anti-Pattern to Governed Architecture','AUTONOMOUS MONOLITH',['Transcript = state','Broad credentials + full tool catalog','Local retries + model says done','Unlinked logs + in-place edits'],'GOVERNED SYSTEM',['Durable workflow + bounded agent','Least privilege + eligible tools','Effect ledger + acceptance','Causal trace + versioned release'])

# gateways
im,d=new('Gateway Responsibilities','Each gateway owns one boundary; orchestration owns execution state')
box(d,(690,360,1110,690),'LLM Gateway\nModel policy · routing · data · budgets',fill='#EAF7FB',outline=CYAN)
positions=[(90,230,480,420,'API Gateway\nClient perimeter',BLUE),(90,620,480,810,'Agent Gateway\nWorkload/task boundary',NAVY),(1320,230,1710,420,'MCP Gateway\nServer/tool boundary',AMBER),(1320,620,1710,810,'Orchestration\nState/retries/joins',TEAL)]
for x1,y1,x2,y2,t,c in positions:
    box(d,(x1,y1,x2,y2),t,fill=WHITE,outline=c); arrow(d,((x1+x2)/2,(y1+y2)/2),(900,525),GRAY,4)
save(im,'gateway-position')
grid_flow('model-routing','Policy-First Model Routing',[(x,c) for x,c in [('Identity + purpose',NAVY),('Data class + region',RED),('Risk + capabilities',AMBER),('Approved versions',NAVY),('Quality/latency/cost',TEAL),('Health + quota',BLUE),('Selected route',CYAN),('Recorded evidence',TEAL)]],4,'Eligibility first; optimization second; fallback obeys the same invariants')

layers('security-depth','Defense-in-Depth Guardrails',[
('Input & Channel','Authentication, abuse, injection and jailbreak detection',RED),
('Context & Memory','ACL, source trust, provenance, poisoning and lifecycle',TEAL),
('Model & Output','Approved route, structured output, claim checks and DLP',CYAN),
('Agent & Workflow','Budgets, topology, durable state and safe terminals',NAVY2),
('Identity & Effects','Least privilege, policy, approval, idempotency, reconciliation',AMBER),
('Execution & Supply Chain','Sandbox, egress, secrets, signing and provenance',RED),
('Detection & Response','Monitoring, audit, containment, revocation and recovery',NAVY)])

grid_flow('security-boundaries','Security Trust Boundaries',[(x,c) for x,c in [('User / Channel',BLUE),('Agent Runtime',CYAN),('Context + Memory',TEAL),('LLM Gateway + Model',AMBER),('Tool / MCP / A2A Gateways',RED),('Enterprise + External Systems',NAVY)]],3,'Trust is re-established at every crossing—never inherited through the chain')
grid_flow('guardrail-sequence','Protected-Effect Guardrail Sequence',[(x,c) for x,c in [('1 Authenticate',NAVY),('2 Classify input',RED),('3 Build trusted context',TEAL),('4 Route model',CYAN),('5 Validate output',BLUE),('6 Authorize tool',RED),('7 Approve exact proposal',AMBER),('8 Execute in boundary',NAVY),('9 Reconcile + accept',TEAL),('10 Monitor + recover',NAVY2)]],5)

cycle('learning-loop','Continuous Learning and Improvement',[(x,c) for x,c in [('Observe',BLUE),('Measure',TEAL),('Detect',RED),('Diagnose',AMBER),('Recommend',CYAN),('Validate',NAVY),('Approve',RED),('Deploy',AMBER),('Monitor',BLUE),('Learn',TEAL)]])
two_col('runtime-offline','Runtime Adaptation vs Offline Improvement','RUNTIME · FIXED ENVELOPE',['Select approved route/fallback','Reduce optional context or shed load','Stop, ask, escalate, roll back','Never expand authority or policy'],'OFFLINE · NEW RELEASE',['Edit prompt/context/memory/tool/Skill','Change model route/topology/workflow/code','Evaluate + approve proportional to risk','Canary, monitor, rollback, learn'])

im,d=new('Federated Governance Operating Model','Centralized control services with accountable domain ownership')
box(d,(630,330,1170,700),'Enterprise control services\nPolicy · Identity · Gateways\nEvidence · Release · Incident',fill='#ECF3FA',outline=NAVY)
for xy,title,color in [((100,250,500,450),'Domain product teams\nOutcome · tools · evaluation truth',BLUE),((100,600,500,800),'Platform product\nSDK · runtime · paved road',TEAL),((1300,250,1700,450),'Security · privacy · risk\nThreats · controls · exceptions',RED),((1300,600,1700,800),'Operations · finance\nSLO · recovery · capacity · cost',AMBER)]:
    box(d,xy,title,fill=WHITE,outline=color); arrow(d,((xy[0]+xy[2])/2,(xy[1]+xy[3])/2),(900,515),GRAY,4)
save(im,'governance-model')

print(f'generated {len(list(OUT.glob("*.png")))} diagrams in {OUT}')
