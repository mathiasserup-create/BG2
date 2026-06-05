import json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.gridspec import GridSpec

D=json.load(open('data.json')); O=D['ops']; P=D['periods']
a26,a25,m26,m25,fy=P['atd26'],P['atd25'],P['may26'],P['may25'],P['fy25']
BG='#0e1116'; PAN='#161b24'; INK='#e9eef5'; MUT='#9aa7b8'; LINE='#2a3340'
GOLD='#f5b324'; GRN='#3ddc91'; BLUE='#5aa9ff'; PUR='#b58cff'; RED='#ff6b6b'
plt.rcParams.update({'text.color':INK,'axes.labelcolor':MUT,'xtick.color':MUT,'ytick.color':MUT,
  'font.family':'DejaVu Sans','axes.edgecolor':LINE})
def kr(n,d=0): 
    s=f"{n:,.{d}f}".replace(",","§").replace(".",",").replace("§",".")
    return s

fig=plt.figure(figsize=(15.5,17.6),dpi=110); fig.patch.set_facecolor(BG)
gs=GridSpec(6,3,figure=fig,height_ratios=[0.62,0.9,0.32,1.1,1.1,1.15],hspace=0.52,wspace=0.22,
            left=0.045,right=0.965,top=0.955,bottom=0.035)

# ---- Header ----
hd=fig.add_axes([0,0.963,1,0.037]); hd.axis('off')
hd.text(0.045,0.5,"BG2 ApS — Ledelsesrapportering",fontsize=25,fontweight='bold',va='center')
hd.text(0.965,0.62,"ÅR-TIL-DATO 01.07.2025 – 31.05.2026",fontsize=11,color=GOLD,ha='right',va='center',fontweight='bold')
hd.text(0.965,0.30,"Borgergade 2, Aalborg · vs. samme periode 2024/25",fontsize=10,color=MUT,ha='right',va='center')

# ---- KPI tiles ----
def tile(ax,lab,val,sub,col):
    ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.add_patch(FancyBboxPatch((0.02,0.05),0.96,0.9,boxstyle="round,pad=0.02,rounding_size=0.06",
        fc=PAN,ec=LINE,lw=1.2,mutation_aspect=0.5))
    ax.add_patch(plt.Rectangle((0.02,0.05),0.022,0.9,fc=col,ec='none'))
    ax.text(0.10,0.74,lab,fontsize=10.5,color=MUT,va='center',fontweight='bold')
    ax.text(0.10,0.42,val,fontsize=23,color=INK,va='center',fontweight='bold')
    ax.text(0.10,0.16,sub,fontsize=9.5,color=MUT,va='center')
vf26=a26['cogs']/a26['rev']*100; vf25=a25['cogs']/a25['rev']*100
kpis=[("OMSÆTNING ÅTD",kr(a26['rev']/1000)+" t.kr","+7,2 % vs. 24/25",BLUE),
 ("DÆKNINGSGRAD",kr(a26['db']/a26['rev']*100,1)+" %","24/25: "+kr(a25['db']/a25['rev']*100,1)+" %",GRN),
 ("VAREFORBRUG",kr(vf26,1)+" %","24/25: "+kr(vf25,1)+" %  ↓",GRN),
 ("LØNPROCENT",kr(O['ytd']['lonpct'],1)+" %","24/25: 19,2 %  ↓ kraftigt",GRN),
 ("EBITDA-MARGIN",kr(a26['ebitda']/a26['rev']*100,1)+" %","24/25: "+kr(a25['ebitda']/a25['rev']*100,1)+" %",GRN),
 ("OMS./BEMANDET TIME",kr(O['ytd']['rev_per_hour'])+" kr","eff. timeløn "+kr(O['ytd']['eff_wage'])+" kr",BLUE)]
for i,(l,v,s,c) in enumerate(kpis):
    ax=fig.add_subplot(gs[0+i//3 if i<3 else 1, i%3]) if False else None
# place KPIs in rows 0 and 1 (3 each)
for i,(l,v,s,c) in enumerate(kpis):
    r=0 if i<3 else 1; cc=i%3
    if r==1 and i>=3 and i<3: pass
# row0 has 3 tiles but row0 height small; use a dedicated kpi band
for i,(l,v,s,c) in enumerate(kpis[:3]):
    tile(fig.add_subplot(gs[0,i]),l,v,s,c)
# second KPI row -> top of gs[1]
kp2=fig.add_axes([0.045,0.772,0.92,0.066]); kp2.axis('off')
for i,(l,v,s,c) in enumerate(kpis[3:]):
    sub=fig.add_axes([0.045+i*0.312,0.772,0.30,0.066])
    tile(sub,l,v,s,c)

# ---- P&L table (gs row1 full width, but we used axes above) -> use gs[1,:] lower part won't work; make new axes
tax=fig.add_axes([0.045,0.560,0.92,0.185]); tax.axis('off')
tax.text(0,1.02,"Resultatopgørelse  (t.kr · % af omsætning)",fontsize=13,fontweight='bold',transform=tax.transAxes)
cols=["",("Maj 26",m26),("Maj 25",m25),("ÅTD 25/26",a26),("ÅTD 24/25",a25),("Helår 24/25",fy)]
rows=[("Omsætning","rev",1,False),("Vareforbrug","cogs",-1,True),("Dækningsbidrag","db",1,True),
      ("Lønomkostninger","wages",-1,True),("Forpagtning & lokaler","premises",-1,True),
      ("Salg & administration","salgadm",-1,True),("EBITDA","ebitda",1,True)]
xs=[0.0,0.30,0.435,0.57,0.71,0.85]
ytop=0.90; dy=0.118
for ci,c in enumerate(cols):
    head=c if ci==0 else c[0]
    tax.text(xs[ci]+(0 if ci==0 else 0.11),ytop+0.05,head,fontsize=10.5,color=GOLD if ci in(1,3) else MUT,
             ha='left' if ci==0 else 'right',fontweight='bold',transform=tax.transAxes)
for ri,(lab,key,sign,showp) in enumerate(rows):
    y=ytop-(ri+1)*dy; bold=key in('db','ebitda')
    tax.text(0,y,lab,fontsize=10.5,color=INK,fontweight='bold' if bold else 'normal',transform=tax.transAxes)
    for ci,c in enumerate(cols[1:],1):
        d=c[1]; v=d[key]
        val=sign*v
        txt=kr(val/1000)
        tax.text(xs[ci]+0.11,y,txt,fontsize=10.5,ha='right',color=INK,fontweight='bold' if bold else 'normal',transform=tax.transAxes)
        if showp:
            tax.text(xs[ci]+0.13,y,f"{abs(v)/d['rev']*100:.0f}%",fontsize=7.8,ha='left',color=MUT,transform=tax.transAxes)
    if bold:
        tax.axhline(y+dy*0.42,xmin=0,xmax=1,color=LINE,lw=0.8)

mon=[m for m in O['monthly'] if m['ym']!='2026-06']
mlab=[{'07':'Jul','08':'Aug','09':'Sep','10':'Okt','11':'Nov','12':'Dec','01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'Maj'}[m['ym'][5:]] for m in mon]
def style(ax,title):
    ax.set_facecolor(PAN); ax.set_title(title,color=INK,fontsize=12,fontweight='bold',pad=9,loc='left')
    for s in ax.spines.values(): s.set_color(LINE)
    ax.grid(axis='y',color=LINE,lw=0.6,alpha=0.6); ax.set_axisbelow(True); ax.tick_params(labelsize=9)

# Row3: revenue, category, weekday
ax1=fig.add_subplot(gs[3,0]); style(ax1,"Månedlig omsætning (ekskl. moms)")
ax1.bar(mlab,[m['sales_ex']/1000 for m in mon],color=GOLD); ax1.set_ylabel("t.kr"); ax1.tick_params(axis='x',rotation=45)

ax2=fig.add_subplot(gs[3,1]); ax2.set_facecolor(PAN); ax2.set_title("Produktmix (oms. ekskl. moms)",color=INK,fontsize=12,fontweight='bold',loc='left',pad=9)
cats=sorted([(k,v) for k,v in O['catmix'].items() if v>1000],key=lambda x:-x[1])
top=cats[:6]; other=sum(v for k,v in cats[6:])
labels=[k for k,v in top]+(["Øvrige"] if other>0 else []); vals=[v for k,v in top]+([other] if other>0 else [])
cols6=[GOLD,PUR,BLUE,GRN,'#e8731c','#7a8aa0','#4ec9c9']
w,_,at=ax2.pie(vals,colors=cols6,startangle=90,counterclock=False,autopct=lambda p:f"{p:.0f}%",
       pctdistance=0.78,textprops={'fontsize':8,'color':'#10141b','fontweight':'bold'},wedgeprops={'width':0.42,'edgecolor':PAN})
ax2.legend(labels,loc='center',fontsize=7.6,frameon=False,labelcolor=INK,ncol=1,bbox_to_anchor=(0.5,0.5))

ax3=fig.add_subplot(gs[3,2]); style(ax3,"Oms. pr. åben dag — ugedag")
wd=O['weekday']; ax3.bar([d['d'] for d in wd],[d['avg']/1000 for d in wd],
   color=[GRN if d['avg']>10000 else BLUE for d in wd]); ax3.set_ylabel("t.kr/dag")

# Row4: oms vs løn, lønprocent+timer
ax4=fig.add_subplot(gs[4,0:2]); style(ax4,"Omsætning vs. lønomkostning pr. måned")
x=np.arange(len(mon)); ax4.bar(x-0.2,[m['sales_ex']/1000 for m in mon],0.4,color=BLUE,alpha=0.7,label='Omsætning')
ax4.bar(x+0.2,[m['wage']/1000 for m in mon],0.4,color=GOLD,label='Løn (kontant)')
ax4.set_xticks(x); ax4.set_xticklabels(mlab,rotation=45); ax4.set_ylabel("t.kr"); ax4.legend(fontsize=9,facecolor=PAN,edgecolor=LINE,labelcolor=INK)

ax5=fig.add_subplot(gs[4,2]); style(ax5,"Lønprocent pr. måned")
ax5.plot(mlab,[m['lonpct'] for m in mon],color=GRN,lw=2.2,marker='o',ms=4)
ax5.fill_between(range(len(mon)),[m['lonpct'] for m in mon],color=GRN,alpha=0.12)
ax5.axhline(O['ytd']['lonpct'],color=GOLD,ls='--',lw=1.3); ax5.set_ylabel("%"); ax5.tick_params(axis='x',rotation=45)
ax5.text(0.02,0.93,f"ÅTD-snit {O['ytd']['lonpct']:.0f}%",transform=ax5.transAxes,color=GOLD,fontsize=8.5,fontweight='bold')

# Row5: vareforbrug monthly, vareforbrug periods, hourly
ax6=fig.add_subplot(gs[5,0]); style(ax6,"Vareforbrugsprocent pr. måned")
ax6.bar(mlab,[m['cogs_pct'] for m in mon],color=BLUE); ax6.axhline(vf26,color=GRN,ls='--',lw=1.4)
ax6.set_ylabel("%"); ax6.tick_params(axis='x',rotation=45)
ax6.text(0.02,0.92,f"ÅTD {vf26:.1f}%",transform=ax6.transAxes,color=GRN,fontsize=8.5,fontweight='bold')

ax7=fig.add_subplot(gs[5,1]); style(ax7,"Vareforbrug — perioder")
pl=['ÅTD\n25/26','ÅTD\n24/25','Helår\n24/25','Maj\n26','Branche']
pv=[vf26,vf25,fy['cogs']/fy['rev']*100,m26['cogs']/m26['rev']*100,30]
ax7.bar(pl,pv,color=[GRN,BLUE,BLUE,GRN,MUT]); ax7.set_ylabel("%")
for i,v in enumerate(pv): ax7.text(i,v+0.6,f"{v:.0f}",ha='center',color=INK,fontsize=9)

ax8=fig.add_subplot(gs[5,2]); style(ax8,"Omsætning efter klokkeslæt")
hrs=sorted([(int(h),v) for h,v in O['hourly'].items() if v>500])
ax8.bar([f"{h}" for h,v in hrs],[v/1000 for h,v in hrs],color=PUR); ax8.set_ylabel("t.kr"); ax8.set_xlabel("klokkeslæt",fontsize=8)

fig.text(0.045,0.012,"Kilder: e-conomic · OnlinePOS · Danløn   |   Omsætning/løn for jan–maj fra POS/Danløn (endnu ej bogført)   |   Afskrivninger/renter kun i helårskolonne",
         fontsize=8,color=MUT)
plt.savefig('/tmp/bg2_dashboard.png',facecolor=BG,bbox_inches='tight')
print("saved")
