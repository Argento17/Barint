# -*- coding: utf-8 -*-
"""
Generate branded visuals for the Bari nutrition-partnership deck.
Real-data charts use the live frontend corpus; diagrams use the Bari palette.
All chart text is English (deck speaker notes carry the Hebrew nuance) to avoid
RTL/font rendering issues in matplotlib. Outputs PNGs into assets/.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
from matplotlib.lines import Line2D

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(A, exist_ok=True)

# brand palette
INK="#0E1A2B"; NAVY="#142A45"; TEAL="#1F8F6A"; TEAL2="#2BB28F"; TEALDK="#156B5E"; GOLD="#C99A3F"
PAPER="#F6F4EF"; SLATE="#3A4A5E"; MIST="#8A98A8"; LINE="#D8DDE3"; WHITE="#FFFFFF"
LTEAL="#EAF4F1"; LGOLD="#FBF3E3"
GRADE = {"A":"#1F8F6A","B":"#6FB39A","C":"#C9A23F","D":"#D98A4E","E":"#B5564E"}

plt.rcParams.update({
    "font.family":"DejaVu Sans", "font.size":12,
    "axes.edgecolor":LINE, "text.color":INK, "axes.labelcolor":INK,
    "xtick.color":SLATE, "ytick.color":SLATE,
})

def _save(fig, name, transparent=True):
    fig.savefig(os.path.join(A,name), dpi=200, transparent=transparent,
                bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("  ", name)

def _panel(w=4.6, h=4.7):
    fig = plt.figure(figsize=(w,h)); ax = fig.add_axes([0,0,1,1]); ax.axis("off")
    ax.set_xlim(0,10); ax.set_ylim(0,10)
    return fig, ax

def _band(w=12.4, h=2.05):
    fig = plt.figure(figsize=(w,h)); ax = fig.add_axes([0,0,1,1]); ax.axis("off")
    ax.set_xlim(0,100); ax.set_ylim(0,20)
    return fig, ax

def rbox(ax, x, y, w, h, fc, ec="none", lw=0, rad=0.12, z=2, alpha=1):
    p = FancyBboxPatch((x,y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
                       fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha)
    ax.add_patch(p); return p

def arrow(ax, x1,y1,x2,y2, color=TEAL, lw=2.4, z=3, ms=12):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle="-|>,head_width=2.6,head_length=4.2",
                 mutation_scale=ms, color=color, lw=lw, zorder=z))

# --------------------------------------------------------------- 1 missing layer
def v_missing_layer():
    fig, ax = _panel()
    rbox(ax, 0.4, 5.6, 3.6, 3.6, INK)                      # label
    for i,yy in enumerate([6.3,7.0,7.7,8.4]):
        ax.add_line(Line2D([0.9,3.5],[yy,yy], color="#7FA8C9", lw=2, alpha=.7))
    ax.text(2.2,5.0,"DENSE LABEL", ha="center", color=SLATE, fontsize=11, weight="bold")
    c = Circle((8.0,7.4),1.5, fc=PAPER, ec=MIST, lw=2); ax.add_patch(c)
    ax.add_patch(Circle((8.0,7.7),0.5, fc=SLATE))
    ax.add_patch(FancyBboxPatch((7.1,5.6),1.8,1.1, boxstyle="round,pad=0,rounding_size=0.4", fc=SLATE))
    ax.text(8.0,5.0,"CONFUSED SHOPPER", ha="center", color=SLATE, fontsize=11, weight="bold")
    rbox(ax, 2.3, 2.2, 5.4, 1.7, TEAL)
    ax.text(5.0,3.05,"MISSING\nINTERPRETATION LAYER", ha="center", va="center",
            color=WHITE, fontsize=12.5, weight="bold")
    arrow(ax, 4.0,7.4, 6.4,7.4, color=GOLD, lw=2.6)
    arrow(ax, 2.2,5.6, 3.4,3.9, color=TEAL); arrow(ax, 7.8,5.6, 6.6,3.9, color=TEAL)
    _save(fig,"problem_missing_layer.png")

# --------------------------------------------------------------- 2 trust decline
def v_trust():
    fig = plt.figure(figsize=(4.8,4.5)); ax = fig.add_axes([0.10,0.12,0.86,0.80])
    ax.set_xlim(0,10); ax.set_ylim(0,10)
    for s in ax.spines.values(): s.set_visible(False)
    # axes
    ax.add_line(Line2D([0.5,0.5],[0.5,9.5], color=LINE, lw=1.4))
    ax.add_line(Line2D([0.5,9.7],[0.5,0.5], color=LINE, lw=1.4))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("time  →", color=SLATE, fontsize=10.5)
    ax.set_ylabel("consumer trust  →", color=SLATE, fontsize=10.5)
    # declining line for brands/influencers
    ax.plot([1.0,9.3],[8.6,2.0], color=MIST, lw=3.2, zorder=2)
    ax.text(2.0,8.0,"brands / influencers", color=MIST, fontsize=10.5, weight="bold",
            rotation=-25, rotation_mode="anchor", ha="left", va="bottom")
    # Bari target zone (high trust, upper-right)
    ax.add_patch(Rectangle((6.05,6.2),3.5,2.7, fc=LTEAL, ec=TEAL, lw=1.8, ls=(0,(4,2)), zorder=1))
    ax.text(7.8,7.55,"where Bari aims:\ntrusted + usable", color=TEALDK, fontsize=9.5,
            ha="center", va="center", weight="bold", zorder=4)
    # small 'the gap' indicator between line and zone
    ax.annotate("", xy=(8.0,6.1), xytext=(8.0,3.6),
                arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.6))
    ax.text(8.25,4.85,"the gap =\nthe opening", color=GOLD, fontsize=8.5, weight="bold",
            ha="left", va="center")
    _save(fig,"problem_trust.png", transparent=True)

# --------------------------------------------------------------- 3 one engine / three surfaces
def v_engine_surface():
    fig, ax = _panel(4.9,4.7)
    rbox(ax, 0.3, 3.1, 2.7, 3.8, INK)
    ax.text(1.65,5.7,"BSIP\nengine", ha="center", va="center", color=WHITE, weight="bold", fontsize=12)
    ax.text(1.65,4.1,"evidence +\nconfidence", ha="center", va="center", color=TEAL2, fontsize=8.5)
    labels=[("Consumer", TEAL, "live"),("Professional", "#2E7DA6", "next"),
            ("Industry / Data", SLATE, "future"),("Commerce / Marketplace", GOLD, "cross-cutting")]
    for i,(t,c,tag) in enumerate(labels):
        yy = 7.55-1.95*i
        rbox(ax, 4.4, yy, 5.4, 1.5, c)
        ax.text(4.75, yy+0.9, t, color=WHITE, weight="bold", fontsize=11.5, va="center")
        ax.text(4.75, yy+0.38, tag, color=WHITE, fontsize=8.5, va="center", alpha=.85)
        arrow(ax, 3.0, 5.0, 4.3, yy+0.75, color=TEAL, lw=1.8, ms=11)
    _save(fig,"engine_surface.png")

# --------------------------------------------------------------- 4 rigor stack
def v_rigor():
    fig, ax = _panel(4.8,4.7)
    quad=[("Evidence","registry · EV-ids", TEAL, 0.4,5.3),
          ("Confidence","verified/partial/null", "#2E7DA6", 5.1,5.3),
          ("Validation","golden corpus · QA", GOLD, 0.4,0.4),
          ("Governance","constitution · exceptions", SLATE, 5.1,0.4)]
    for t,s,c,x,y in quad:
        rbox(ax, x, y, 4.5, 4.3, c)
        ax.text(x+0.35,y+3.4,t, color=WHITE, weight="bold", fontsize=14)
        ax.text(x+0.35,y+2.5,s, color=WHITE, fontsize=10, alpha=.92)
    ax.add_patch(Circle((5.0,5.0),0.95, fc=WHITE, ec=INK, lw=1.5, zorder=5))
    ax.text(5.0,5.0,"BSIP", ha="center", va="center", color=INK, weight="bold", fontsize=10.5, zorder=6)
    _save(fig,"rigor_stack.png")

# --------------------------------------------------------------- 5 moat flywheel
def v_flywheel():
    import math
    fig, ax = _panel(4.8,4.7)
    cx,cy,R=5,5.1,2.75
    nodes=["Audience","Data","Calibration","Trust"]
    cols=[TEAL,SLATE,GOLD,"#2E7DA6"]
    ang=[90,0,-90,180]
    # ring
    ax.add_patch(Circle((cx,cy),R, fill=False, ec=TEAL2, lw=2.6, zorder=1))
    # small clockwise direction triangles at the 45deg midpoints
    for a in [45,-45,-135,135]:
        ar=math.radians(a)
        px,py=cx+R*math.cos(ar), cy+R*math.sin(ar)
        tx,ty=math.sin(ar),-math.cos(ar)      # clockwise tangent
        nx,ny=-ty,tx
        s=0.40
        p1=(px+tx*s, py+ty*s)
        p2=(px-tx*s*0.5+nx*s*0.75, py-ty*s*0.5+ny*s*0.75)
        p3=(px-tx*s*0.5-nx*s*0.75, py-ty*s*0.5-ny*s*0.75)
        ax.add_patch(Polygon([p1,p2,p3], closed=True, fc=TEAL2, ec="none", zorder=2))
    for i,a in enumerate(ang):
        ar=math.radians(a); x,y=cx+R*math.cos(ar), cy+R*math.sin(ar)
        rbox(ax, x-1.2,y-0.5,2.4,1.0, cols[i], z=3)
        ax.text(x,y,nodes[i], ha="center", va="center", color=WHITE, weight="bold", fontsize=11, zorder=4)
    ax.text(cx,cy,"content\nflywheel", ha="center", va="center", color=SLATE, fontsize=10, weight="bold", zorder=2)
    _save(fig,"moat_flywheel.png")

# --------------------------------------------------------------- 6 grade distributions (REAL)
LIVE = [   # category, n, dict of grades  (live datasets)
 ("Bread",24,{"A":3,"B":18,"C":3}),
 ("Cheese",51,{"B":20,"C":24,"D":6,"E":1}),
 ("Hummus",64,{"A":5,"B":14,"C":38,"D":7}),
 ("Dairy desserts",84,{"B":3,"C":26,"D":40,"E":15}),
 ("Bars",18,{"B":1,"C":5,"D":8,"E":4}),
 ("Yogurt",11,{"B":8,"C":1,"D":1,"E":1}),
]
def v_grades():
    fig = plt.figure(figsize=(4.9,4.7)); ax = fig.add_axes([0.30,0.10,0.66,0.84])
    cats=[c[0] for c in LIVE][::-1]; ns=[c[1] for c in LIVE][::-1]; data=[c[2] for c in LIVE][::-1]
    y=range(len(cats))
    for i,gd in enumerate(data):
        left=0; tot=sum(gd.values())
        for g in ["A","B","C","D","E"]:
            v=gd.get(g,0)
            if not v: continue
            w=v/tot*100
            ax.barh(i,w,left=left,color=GRADE[g],edgecolor="white",lw=.8,height=.62)
            if w>9: ax.text(left+w/2,i,g,ha="center",va="center",color="white",fontsize=9,weight="bold")
            left+=w
    ax.set_yticks(list(y)); ax.set_yticklabels([f"{c}\n(n={n})" for c,n in zip(cats,ns)], fontsize=9.5)
    ax.set_xlim(0,100); ax.set_xticks([0,50,100]); ax.set_xticklabels(["0%","50%","100%"], fontsize=9)
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    hands=[Rectangle((0,0),1,1,color=GRADE[g]) for g in "ABCDE"]
    ax.legend(hands,list("ABCDE"),ncol=5,loc="lower center",bbox_to_anchor=(0.5,1.01),
              frameon=False,fontsize=9,handlelength=1,columnspacing=1)
    _save(fig,"progress_grades.png", transparent=True)

# --------------------------------------------------------------- 7 yogurt ruling
def v_yogurt():
    fig = plt.figure(figsize=(4.7,4.5)); ax = fig.add_axes([0.12,0.14,0.84,0.74])
    gd={"B":8,"C":1,"D":1,"E":1}
    xs=list("ABCDE"); ys=[0,8,1,1,1]
    bars=ax.bar(xs,ys,color=[GRADE[g] for g in xs],edgecolor="white",lw=1, width=.66)
    ax.bar("A",0.0,color=GRADE["A"])
    ax.annotate("A = 0\nby design", xy=(0,0.4), xytext=(0.2,5.2), fontsize=10, color=INK, weight="bold",
                ha="center", arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6))
    ax.axhline(0, color=LINE)
    ax.text(1,8.3,"+12 moved C→B\nafter EV-024 fix", fontsize=9.5, color=TEAL, weight="bold", ha="center")
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.set_yticks([]); ax.tick_params(length=0, labelsize=12)
    ax.set_title("Yogurt — B/78.7 is the truthful ceiling", fontsize=11, color=INK, weight="bold", pad=10)
    _save(fig,"yogurt_grades.png", transparent=True)

# --------------------------------------------------------------- 8 cereals fortification
def v_cereals():
    fig = plt.figure(figsize=(4.7,4.5)); ax = fig.add_axes([0.14,0.14,0.82,0.74])
    ax.bar(["Assumed\n(endemic)"],[80],color=LINE,edgecolor="none",width=.5)
    ax.text(0,82,"discount applied?\n✗ NO",ha="center",fontsize=10,color=SLATE, weight="bold")
    ax.bar(["Measured"],[27.2],color=TEAL,edgecolor="none",width=.5)
    ax.text(1,30,"27.2%",ha="center",fontsize=13,color=TEAL,weight="bold")
    ax.set_ylim(0,100); ax.set_ylabel("% of products fortified", fontsize=10)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    ax.tick_params(length=0, labelsize=10)
    ax.set_title("Cereals — the prior was wrong, so we dropped the rule",
                 fontsize=10.5, color=INK, weight="bold", pad=10)
    _save(fig,"cereals_fortification.png", transparent=True)

# --------------------------------------------------------------- 9 hummus boundary (schematic)
def v_hummus():
    fig = plt.figure(figsize=(4.9,4.7)); ax = fig.add_axes([0.13,0.13,0.83,0.70])
    ax.set_xlim(0,10); ax.set_ylim(0,10)
    # two decision regions split by a diagonal rule
    ax.add_patch(Polygon([(0,10),(10,10),(10,0)], closed=True, fc=LTEAL, zorder=0))
    ax.add_patch(Polygon([(0,0),(10,0),(0,10)], closed=True, fc=LGOLD, zorder=0))
    ax.plot([0,10],[10,0], color=SLATE, lw=2.2, ls=(0,(5,3)), zorder=2)
    ax.text(5.0,5.2,"the engine's split", color=SLATE, fontsize=9, weight="bold",
            rotation=-45, rotation_mode="anchor", ha="center", va="bottom")
    # region labels
    ax.text(7.4,7.9,"PREPARED SPREAD", color=TEALDK, fontsize=12, weight="bold", ha="center")
    ax.text(7.4,7.0,"scored as a spread", color=SLATE, fontsize=9.5, ha="center")
    ax.text(2.8,2.9,"RAW / BASE", color="#9A7416", fontsize=12, weight="bold", ha="center")
    ax.text(2.8,2.0,"scored as raw", color=SLATE, fontsize=9.5, ha="center")
    # a few representative products in each region
    for x,y in [(7.7,8.7),(8.6,7.3),(6.7,8.2),(8.2,6.5),(7.2,6.7)]:
        ax.add_patch(Circle((x,y),0.17,fc=TEAL,ec="white",lw=.7,zorder=3))
    for x,y in [(2.0,3.5),(3.5,1.9),(1.6,1.7),(3.1,3.7),(2.5,2.5)]:
        ax.add_patch(Circle((x,y),0.17,fc=GOLD,ec="white",lw=.7,zorder=3))
    ax.set_xlabel("more tahini  →", fontsize=10.5)
    ax.set_ylabel("more sodium / energy  →", fontsize=10.5)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(LINE)
    ax.set_title("How the engine decides what a hummus is",
                 fontsize=11.5, color=INK, weight="bold", pad=30)
    fig.text(0.545,0.88,"by tahini + sodium + energy — not protein, not the label word",
             fontsize=8.8, color=SLATE, ha="center", style="italic")
    _save(fig,"hummus_boundary.png", transparent=True)

# --------------------------------------------------------------- 10 dairy + EV-029 (band)
def v_dairy():
    fig, ax = _band(12.4,2.4); ax.set_ylim(0,24)
    # left: frozen milk chip
    rbox(ax,2,3,26,18, INK, rad=1.2)
    ax.text(4,17.5,"milk · run_004", color=WHITE, weight="bold", fontsize=13)
    ax.text(4,13.5,"FROZEN INVARIANT", color=TEAL2, fontsize=9.5, weight="bold")
    rbox(ax,19,5.5,7,9, TEAL, rad=0.8)
    ax.text(22.5,10,"85 / A", color=WHITE, weight="bold", fontsize=15, ha="center", va="center")
    ax.text(4,8.0,"whole / 4% / goat", color="white", fontsize=9)
    ax.text(4,5.0,"ceiling does not drift", color="#9FB4C4", fontsize=8.5, style="italic")
    # right: EV-029 timeline
    steps=[("bug","fat zeroed", "#B5564E"),
           ("fix","central parser", GOLD),
           ("guard","COV-006", TEAL),
           ("re-score","re-run", SLATE)]
    x0=36; step=15
    for i,(t,s,c) in enumerate(steps):
        x=x0+i*step
        ax.add_patch(Circle((x+3.5,15),3.0, fc=c)); ax.text(x+3.5,15,str(i+1),ha="center",va="center",color="white",weight="bold",fontsize=12)
        ax.text(x+3.5,8.5,t,ha="center",color=INK,weight="bold",fontsize=9.5)
        ax.text(x+3.5,5.0,s,ha="center",color=SLATE,fontsize=8.5)
        if i<3: arrow(ax,x+6.8,15,x+step,15,color=MIST,lw=1.8,ms=11)
    ax.text(58,1.0,"EV-029 — found, fixed once, guarded permanently", ha="center", color=SLATE, fontsize=9, style="italic")
    _save(fig,"dairy_fermentation.png", transparent=True)

# --------------------------------------------------------------- 10b 5-year roadmap band
def v_roadmap():
    fig, ax = _band(12.4,2.0); ax.set_ylim(0,20)
    yrs=[("Year 1","Israeli comparison\nplatform"),("Year 2","Category\nintelligence"),
         ("Year 3","Professional\ntools"),("Year 4","Retail +\nmarketplace"),
         ("Year 5","US expansion +\necosystem")]
    cols=[INK,"#274B66","#2E7DA6",TEAL,TEAL2]
    ax.add_patch(Polygon([(1,8),(99,4),(99,16),(1,12)], closed=True, fc=PAPER, ec=LINE, zorder=0))
    w=17; x0=2
    for i,(y,t) in enumerate(yrs):
        x=x0+i*19.3; h=8+i*2.4; yb=2
        rbox(ax,x,yb,w,h,cols[i], rad=0.7, z=2)
        ax.text(x+w/2,yb+h-1.8,y,ha="center",color="white",weight="bold",fontsize=11, zorder=3)
        ax.text(x+w/2,yb+1.6,t,ha="center",va="bottom",color="white",fontsize=8.3, zorder=3)
    _save(fig,"roadmap_band.png", transparent=True)

# --------------------------------------------------------------- logo (two bg variants)
def v_logo(dark):
    name = "logo_dark.png" if dark else "logo_light.png"
    wc = WHITE if dark else INK
    fig=plt.figure(figsize=(2.7,0.82)); ax=fig.add_axes([0,0,1,1]); ax.axis("off")
    ax.set_xlim(0,13.5); ax.set_ylim(0,4)
    ax.text(0.1,2.0,"Bari", fontsize=31, weight="bold", color=wc, va="center", ha="left")
    cx,cy,s=11.0,2.0,0.44
    struct=[(0,-4),(-2,-2),(2,-2),(-3,0),(3,0),(-2,2),(2,2),(0,4)]
    teal=[(0,-2),(0,0),(0,2)]
    ax.add_line(Line2D([cx,cx],[cy-2*s,cy+2*s],color=TEAL,lw=2.4,zorder=1))
    for dx,dy in struct:
        ax.add_patch(Circle((cx+dx*s,cy+dy*s),0.17, fc=wc, zorder=2))
    for dx,dy in teal:
        ax.add_patch(Circle((cx+dx*s,cy+dy*s),0.19, fc=TEAL, zorder=3))
    _save(fig,name, transparent=True)

# --------------------------------------------------------------- 11 closing pyramid
def v_pyramid():
    fig, ax = _panel(4.9,4.7)
    layers=[("International expansion", TEAL, 9.0, 2.0),
            ("Retailer-intelligence layer", "#2E7DA6", 7.1, 3.4),
            ("Professional decision-support", SLATE, 5.2, 4.8),
            ("Nutrition-intelligence engine", GOLD, 3.3, 6.2),
            ("Trusted consumer platform", INK, 1.4, 7.6)]
    for t,c,y,w in layers:
        x=(10-w)/2
        ax.add_patch(Polygon([(x,y),(x+w,y),(x+w-0.0,y+1.7),(x+0.0,y+1.7)], closed=True, fc=c))
        ax.text(5,y+0.85,t,ha="center",va="center",color="white",weight="bold",fontsize=10.5)
    _save(fig,"closing_pyramid.png")

# --------------------------------------------------------------- 12 why now (cement)
def v_whynow():
    fig = plt.figure(figsize=(4.7,4.4)); ax=fig.add_axes([0.04,0.08,0.92,0.86]); ax.axis("off")
    ax.set_xlim(0,10); ax.set_ylim(0,10)
    ax.add_patch(Rectangle((0.5,3.0),9,2.6, fc=PAPER, ec=LINE))
    import numpy as np
    xs=np.linspace(0.6,9.4,80)
    ax.fill_between(xs, 3.0, 5.6, where=(xs<5.2), color=SLATE, alpha=.30)
    ax.fill_between(xs, 3.0, 5.6, where=(xs>=5.2), color=TEAL, alpha=.16)
    ax.text(2.7,6.2,"hardening", ha="center", color=SLATE, fontsize=11, weight="bold")
    ax.text(7.4,6.2,"still wet", ha="center", color=TEAL, fontsize=11, weight="bold")
    ax.annotate("YOU\nARE HERE", xy=(7.4,5.6), xytext=(7.4,8.2), ha="center", fontsize=11, weight="bold",
                color=INK, arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
    for x,t in [(1.6,"SIE"),(2.9,"dairy\ninvariants"),(4.3,"evidence\ngrading")]:
        ax.text(x,4.3,t,ha="center",va="center",color="white",fontsize=8.5,weight="bold")
    for x,t in [(6.4,"SIE\nspine"),(7.8,"calibration\nauthorship"),(9.0,"public\nco-sign")]:
        ax.text(x,4.3,t,ha="center",va="center",color=TEAL,fontsize=8.5,weight="bold")
    ax.text(5,1.8,"foundational scientific decisions set over the next two quarters",
            ha="center", color=SLATE, fontsize=10, style="italic")
    _save(fig,"why_now_cement.png", transparent=True)

# =============================================================== BANDS
def v_pipeline_band():
    fig, ax = _band()
    stages=[("BSIP0","acquisition · label parsing\nraw-source replay", INK),
            ("BSIP1","consolidation · trust layer\n10-field enrichment  (not scoring)", "#2E7DA6"),
            ("BSIP2","scoring engine · 4 layers\nrouter · confidence/null  v0.4.0", TEAL)]
    x0=2; w=25; gap=9
    for i,(t,s,c) in enumerate(stages):
        x=x0+i*(w+gap)
        rbox(ax,x,3,w,14,c, rad=1.0)
        ax.text(x+1.4,13.0,t,color="white",weight="bold",fontsize=15)
        ax.text(x+1.4,6.6,s,color="white",fontsize=9.5)
        if i<2: arrow(ax,x+w+1.2,10,x+w+gap-1.2,10,color=GOLD,lw=2.8,ms=15)
    _save(fig,"pipeline_band.png")

def v_three_layers_band():
    fig, ax = _band(12.4, 1.7)
    L=[("Consumer","comparison pages", TEAL,"live"),
       ("Professional","dossiers & tools", "#2E7DA6","next"),
       ("Industry / Data","shelf intelligence", SLATE,"future"),
       ("Commerce / Marketplace","discover → buy", GOLD,"cross-cutting")]
    w=22.3; gap=2.2; x0=2.5
    for i,(t,s,c,tag) in enumerate(L):
        x=x0+i*(w+gap)
        rbox(ax,x,3,w,14,c, rad=1.0)
        ax.text(x+1.3,12.6,t,color="white",weight="bold",fontsize=11.5)
        ax.text(x+1.3,7.4,s,color="white",fontsize=9, alpha=.93)
        ax.text(x+1.3,3.9,tag,color="white",fontsize=8.5,alpha=.8)
    _save(fig,"three_layers_band.png")

def v_staircase():
    fig, ax = _band(13.6,1.95); ax.set_ylim(0,27)
    steps=[("1","Audience\n+ trust"),("2","Content\n+ influence"),("3","Professional\nsubscriptions"),
           ("4","Commerce /\nmarketplace"),("5","Industry\nintelligence"),("6","Retail /\necosystem")]
    cols=[INK,"#27506B","#2E7DA6",GOLD,TEAL,TEAL2]
    w=13.5; x0=2.5; step=16; base=2
    tops=[]
    for i,(num,t) in enumerate(steps):
        x=x0+i*step; h=6.0+i*2.8
        rbox(ax,x,base,w,h,cols[i], rad=0.5)
        ax.add_patch(Circle((x+w/2, base+h-2.1),1.25, fc="white", ec=cols[i], lw=1.6, zorder=4))
        ax.text(x+w/2, base+h-2.1, num, ha="center", va="center", color=cols[i], weight="bold", fontsize=11, zorder=5)
        ax.text(x+w/2, base+1.4, t, ha="center", va="bottom", color="white", fontsize=8.0, weight="bold")
        tops.append((x+w/2, base+h+1.1))
    # clean upward trend line above the bars (does not cross any label)
    ax.plot([p[0] for p in tops],[p[1] for p in tops], color=GOLD, lw=1.8, alpha=.55, zorder=1)
    ax.annotate("", xy=(tops[-1][0]+3, tops[-1][1]+0.4), xytext=tops[-1],
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.8, alpha=.7))
    ax.text(1.5,25.2,"revenue / defensibility  →", color=SLATE, fontsize=9.5, style="italic", weight="bold")
    _save(fig,"monetization_staircase.png", transparent=True)

def v_loop_band():
    fig, ax = _band(12.4,2.1); ax.set_ylim(0,20)
    nodes=[("Delegate","agents tasked", SLATE),
           ("Evidence","packets assembled", "#2E7DA6"),
           ("Review","EXPERT adjudicates", TEAL),
           ("Govern / Close","versioned · gated", INK)]
    w=18; x0=2; step=24
    for i,(t,s,c) in enumerate(nodes):
        x=x0+i*step
        hl = (i==2)
        rbox(ax,x,3,w,13,c if not hl else TEAL, rad=0.8, lw=0)
        if hl:
            ax.add_patch(FancyBboxPatch((x-0.6,2.4),w+1.2,14.2, boxstyle="round,pad=0,rounding_size=1.0",
                         fc="none", ec=GOLD, lw=2.4))
        ax.text(x+w/2,11.5,t,ha="center",color="white",weight="bold",fontsize=12)
        ax.text(x+w/2,6.2,s,ha="center",color="white",fontsize=9, alpha=.93)
        if i<3: arrow(ax,x+w+1.2,9.5,x+step-1.2,9.5,color=GOLD,lw=2.6,ms=13)
    _save(fig,"expert_loop.png", transparent=True)

def v_swimlane():
    fig, ax = _band(12.4,2.6); ax.set_ylim(0,30)
    lanes=[("Supplement Engine (SIE)", TEAL),("Dairy calibration","#2E7DA6"),
           ("Evidence registry", GOLD),("Category reviews", SLATE),("Methodology validation", INK)]
    for i,(t,c) in enumerate(lanes[::-1]):
        y=1+i*5.6
        rbox(ax,2,y,22,4.8,c, rad=0.6)
        ax.text(3,y+2.4,t,color="white",va="center",fontsize=9.5,weight="bold")
        for j,lab in enumerate(["wk 1","day 30","day 90"]):
            x=30+j*22
            ax.add_patch(Circle((x,y+2.4),1.0, fc=c, ec="white", lw=1.2))
            ax.text(x,y+2.4,"•",ha="center",va="center",color="white")
    for j,lab in enumerate(["week 1","day 30","day 90"]):
        ax.text(30+j*22,29,lab,ha="center",color=SLATE,fontsize=9,weight="bold")
    _save(fig,"swimlane_90day.png", transparent=True)

if __name__=="__main__":
    print("generating visuals ->", A)
    for fn in [v_missing_layer,v_trust,v_engine_surface,v_rigor,v_flywheel,v_grades,
               v_yogurt,v_cereals,v_hummus,v_dairy,v_roadmap,v_pyramid,v_whynow,
               v_pipeline_band,v_three_layers_band,v_staircase,v_loop_band,v_swimlane]:
        fn()
    v_logo(True); v_logo(False)
    print("done.")
