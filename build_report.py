#!/usr/bin/env python3
"""Bygger BG2 ApS ledelsesrapport: afstemmer kildedata og genererer data.json + index.html.

Brug:
    pip install pandas openpyxl pdfplumber
    python3 build_report.py --src /sti/til/kildefiler

Forventede kildefiler i --src (genkendes på navnemønster):
    *Salgsdata*.xlsx                 OnlinePOS salgslinjer
    *Posteringer*01.07.24*.xlsx      e-conomic posteringer 2024/25
    *Posteringer*01.07.25*.xlsx      e-conomic posteringer 2025/26
    *Danloen*.csv                    Danløn løneksport
    *PDF*.pdf                        Danløn lønspecifikation (tidsregistrering)
"""
import argparse, glob, json, os, re
import pandas as pd

def find(src, *pats):
    for p in pats:
        m = glob.glob(os.path.join(src, p))
        if m:
            return m[0]
    raise FileNotFoundError(f"Fandt ingen fil for {pats} i {src}")

# ---------- e-conomic posteringer ----------
def load_post(path):
    df = pd.read_excel(path, header=5).dropna(subset=['Konto'])
    df['Konto'] = df['Konto'].astype(int)
    df['Beløb'] = pd.to_numeric(df['Beløb'], errors='coerce').fillna(0)
    df['ym'] = pd.to_datetime(df['Dato']).dt.to_period('M').astype(str)
    return df

def gs(df, lo, hi):
    return float(df[(df['Konto'] >= lo) & (df['Konto'] <= hi)]['Beløb'].sum())

def acct(df, k):
    return float(df[df['Konto'] == k]['Beløb'].sum())

def build_pnl(df):
    d = dict(
        rev=-gs(df, 1010, 1099),
        cogs=gs(df, 1300, 1399),
        cogs_carlsberg=acct(df, 1302), cogs_drinx=acct(df, 1301),
        cogs_rabat=acct(df, 1303) + gs(df, 1304, 1304) + gs(df, 1350, 1351),
        staff=gs(df, 2200, 2299), wages_cash=acct(df, 2210),
        premises=gs(df, 3400, 3499), forpagt=acct(df, 3410),
        salg=gs(df, 2800, 2899), koda=acct(df, 3625),
        admin=gs(df, 3600, 3799), deprec=gs(df, 3900, 3949), fin=gs(df, 4000, 4999),
    )
    d['db'] = d['rev'] - d['cogs']
    d['otherext'] = d['premises'] + d['salg'] + d['admin']
    d['ebitda'] = d['db'] - d['staff'] - d['otherext']
    d['ebit'] = d['ebitda'] - d['deprec']
    d['result'] = d['ebit'] - d['fin']
    return d

# ---------- OnlinePOS salgsdata ----------
DOWS = ['Man', 'Tir', 'Ons', 'Tor', 'Fre', 'Lør', 'Søn']

def build_sales(path):
    s = pd.read_excel(path, header=None)
    s[0] = pd.to_datetime(s[0], errors='coerce')
    s = s.dropna(subset=[0])
    s.columns = ['date', 'time', 'product', 'cat', 'qty', 'line', 'pay', 'tbl', 'reg', 'receipt']
    s['ex'] = s['line'] / 1.25            # linjebeløb inkl. moms -> ekskl. moms
    s['ym'] = s['date'].dt.to_period('M').astype(str)
    s['dow'] = s['date'].dt.dayofweek
    s['hour'] = s['time'].apply(lambda t: int(str(t).split(':')[0]) if ':' in str(t) else None)
    s['catg'] = s['cat'].apply(lambda c: 'Flaskeøl' if 'Flaskeøl' in str(c) else c)
    return s

# ---------- Danløn PDF tidsregistrering ----------
def build_shifts(path):
    import pdfplumber
    pat = re.compile(r'^(0?1|02|T4)\s+(\d{2}\.\d{2}\.\d{4})\s+[\d:]+\s*-\s*[\d:]+\s+BG2\s+(\w+)\s+'
                     r'([\d.,]+)\s+kr\.\s*([\d.,]+)\s+kr\.\s*([\d.,]+)')
    num = lambda x: float(x.replace('.', '').replace(',', '.'))
    rows = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            for line in (pg.extract_text() or '').split('\n'):
                m = pat.match(line.strip())
                if m:
                    _, date, grp, antal, _, belob = m.groups()
                    rows.append((date, grp, num(antal), num(belob)))
    df = pd.DataFrame(rows, columns=['date', 'grp', 'hours', 'belob'])
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df['ym'] = df['date'].dt.to_period('M').astype(str)
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='.', help='mappe med kildefiler')
    ap.add_argument('--out', default='.', help='output-mappe')
    a = ap.parse_args()

    post25 = load_post(find(a.src, '*Posteringer*01.07.25*xlsx', '*25.26*xlsx'))
    post24 = load_post(find(a.src, '*Posteringer*01.07.24*xlsx', '*24.25*xlsx'))
    p24 = build_pnl(post24)
    p25 = build_pnl(post25)
    s = build_sales(find(a.src, '*Salgsdata*xlsx'))
    sh = build_shifts(find(a.src, '*PDF*pdf', '*Lonspec*pdf'))

    # operationelle nøgletal
    msales = s.groupby('ym')['ex'].sum()
    mlab = sh.groupby('ym').agg(hours=('hours', 'sum'), wage=('belob', 'sum'))
    mon = pd.DataFrame({'sales_ex': msales}).join(mlab).fillna(0)
    mon['lonpct'] = (mon['wage'] / mon['sales_ex'] * 100).round(1)
    mon['rev_per_hour'] = (mon['sales_ex'] / mon['hours']).round(0)
    monthly = [dict(ym=i, **{k: float(r[k]) for k in ['sales_ex', 'hours', 'wage', 'lonpct', 'rev_per_hour']})
               for i, r in mon.iterrows()]

    act = mon.loc['2025-07':'2026-05']          # afsluttede måneder
    ytd_sales, ytd_wage, ytd_hours = act['sales_ex'].sum(), act['wage'].sum(), act['hours'].sum()
    # månedlig vareforbrugsprocent (e-conomic 1300-1399 ÷ POS-omsætning)
    post25['m'] = post25['ym']
    cogs_m = post25[(post25['Konto'] >= 1300) & (post25['Konto'] <= 1399)].groupby('ym')['Beløb'].sum()
    for r in monthly:
        c = float(cogs_m.get(r['ym'], 0.0))
        r['cogs'] = round(c)
        r['cogs_pct'] = round(c / r['sales_ex'] * 100, 1) if r['sales_ex'] else None

    rec = s.groupby('receipt')['ex'].sum()
    catmix = {k: round(float(v)) for k, v in s.groupby('catg')['ex'].sum().items() if v > 1}
    pay = {k: round(float(v)) for k, v in s.groupby('pay')['ex'].sum().items()}
    top = s.groupby('product').agg(qty=('qty', 'sum'), ex=('ex', 'sum')).sort_values('ex', ascending=False).head(15)
    days_open = s.groupby('dow')['date'].apply(lambda x: x.dt.date.nunique())
    wd = s.groupby('dow')['ex'].sum()
    hr = s.groupby('hour')['ex'].sum()
    n_months = len(act)
    ann_sales = ytd_sales / n_months * 12

    ops = dict(
        monthly=monthly, catmix=catmix, pay=pay,
        top=[{'product': i, 'qty': int(r['qty']), 'ex': round(float(r['ex']))} for i, r in top.iterrows()],
        weekday=[{'d': DOWS[i], 'total': round(float(wd[i])), 'days': int(days_open[i]),
                  'avg': round(float(wd[i] / days_open[i]))} for i in range(7) if i in days_open.index],
        hourly={int(k): round(float(v)) for k, v in hr.items() if k is not None},
        basket=round(float(rec.mean()), 1), receipts=int(rec.shape[0]),
        ann_sales=round(float(ann_sales)),
        ytd=dict(sales=round(float(ytd_sales)), wage=round(float(ytd_wage)), hours=round(float(ytd_hours)),
                 lonpct=round(ytd_wage / ytd_sales * 100, 1), rev_per_hour=round(ytd_sales / ytd_hours),
                 eff_wage=round(ytd_wage / ytd_hours)),
    )

    # ---- periodeopdelt resultatopgørelse (Maj + ÅTD + sammenligning) ----
    m_atd26 = [f'2025-{m:02d}' for m in range(7, 13)] + [f'2026-{m:02d}' for m in range(1, 6)]
    m_atd25 = [f'2024-{m:02d}' for m in range(7, 13)] + [f'2025-{m:02d}' for m in range(1, 6)]
    pos_rev = lambda ms: sum(mon.loc[m, 'sales_ex'] for m in ms if m in mon.index)
    dl_wage = lambda ms: sum(mon.loc[m, 'wage'] for m in ms if m in mon.index)
    dl_hours = lambda ms: sum(mon.loc[m, 'hours'] for m in ms if m in mon.index)

    def rsum(df, lo, hi, ms):
        d = df[(df['Konto'] >= lo) & (df['Konto'] <= hi)]
        return float(d[d['ym'].isin(ms)]['Beløb'].sum())

    def period(df, ms, op):  # op=True -> brug POS/Danløn for omsætning+løn
        rev = pos_rev(ms) if op else -rsum(df, 1010, 1099, ms)
        wages = dl_wage(ms) if op else float(df[(df['Konto'] == 2210) & (df['ym'].isin(ms))]['Beløb'].sum())
        d = dict(rev=rev, cogs=rsum(df, 1300, 1399, ms), wages=wages,
                 hours=(dl_hours(ms) if op else None),
                 premises=rsum(df, 3400, 3499, ms), forpagt=float(df[(df['Konto'] == 3410) & (df['ym'].isin(ms))]['Beløb'].sum()),
                 salgadm=rsum(df, 2800, 2899, ms) + rsum(df, 3600, 3799, ms),
                 deprec=rsum(df, 3900, 3949, ms), fin=rsum(df, 4000, 4999, ms))
        d['db'] = d['rev'] - d['cogs']
        d['otherext'] = d['premises'] + d['salgadm']
        d['ebitda'] = d['db'] - d['wages'] - d['otherext']
        return d

    all24 = sorted(post24['ym'].unique())
    periods = dict(
        may26=period(post25, ['2026-05'], True), atd26=period(post25, m_atd26, True),
        may25=period(post24, ['2025-05'], False), atd25=period(post24, m_atd25, False),
        fy25=period(post24, all24, False),
    )
    ops['growth_atd'] = round((periods['atd26']['rev'] / periods['atd25']['rev'] - 1) * 100, 1)
    ops['ann_sales'] = round(periods['atd26']['rev'] / len(m_atd26) * 12)

    # normaliseret helårsestimat
    norm = dict(rev=ops['ann_sales'], cogs=round(ops['ann_sales'] * 0.227),
                wages_cash=round(ytd_wage / n_months * 12))
    norm['staff'] = round(norm['wages_cash'] * 1.06)
    norm['premises'] = round(p24['premises']); norm['forpagt'] = p24['forpagt']
    norm['salg'] = round(p24['salg']); norm['admin'] = round(p24['admin'])
    norm['db'] = norm['rev'] - norm['cogs']
    norm['otherext'] = norm['premises'] + norm['salg'] + norm['admin']
    norm['ebitda'] = norm['db'] - norm['staff'] - norm['otherext']

    master = dict(A=p24, B=p25, norm=norm, ops=ops, periods=periods)
    json.dump(master, open(os.path.join(a.out, 'data.json'), 'w'), ensure_ascii=False)
    print('Skrev data.json. Kør build_html-trinnet for at indlejre i index.html.')
    print(f"  Omsætning helårstakt 25/26: {ops['ann_sales']:,.0f} kr  | Lønprocent: {ops['ytd']['lonpct']}%")

if __name__ == '__main__':
    main()
