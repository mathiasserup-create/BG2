# BG2 ApS — Ledelsesrapportering 2025/26

Dynamisk HTML-rapport med de væsentlige nøgletal for **BG2 ApS** (Borgergade 2, Aalborg, CVR
39579847) — en bar- og aktivitetscafé. Rapporten er afstemt mod tre datakilder og viser
**maj 2026** og **år-til-dato 01.07.2025 – 31.05.2026** sammenlignet med tilsvarende perioder
året før samt det fulde regnskabsår **2024/25**.

## Åbn rapporten

Åbn `index.html` i en browser. Siden er selvstændig (data er indlejret); Chart.js hentes fra CDN,
så internetadgang anbefales for at vise graferne.

## Indhold

- **Overblik** – hovednøgletal som KPI-kort (ÅTD vs. samme periode året før)
- **Resultatopgørelse** – Maj 2026 · Maj 2025 · ÅTD 25/26 · ÅTD 24/25 · Helår 24/25
- **Omsætning** – månedsudvikling, produktmix, ugedags- og klokkeslætsmønster, største produkter
- **Vareforbrug** – vareforbrugsprocent og sammensætning
- **Løn & bemanding** – lønprocent, omsætning pr. bemandet time, månedlig udvikling
- **Benchmark & baggrund** – sammenligning med branchenormer
- **Observationer & anbefalinger**

## Væsentlige nøgletal — ÅTD 01.07.2025–31.05.2026 (mod samme periode 24/25)

| Nøgletal | ÅTD 25/26 | ÅTD 24/25 | Bemærkning |
|---|---|---|---|
| Omsætning (ekskl. moms) | 2.083 t.kr | 1.944 t.kr | +7,2 % |
| Vareforbrugsprocent | 21,7 % | 24,3 % | forbedret · dækningsgrad 78,3 % |
| Lønprocent (kontant løn) | 14,0 % | 19,2 % | årets største forbedring |
| EBITDA-margin | 29,3 % | 24,1 % | |
| Omsætning pr. bemandet time | ~887 kr | — | effektiv timeløn ~124 kr |
| Forpagtning & lokaler | 25,3 % af oms. | 24,4 % | tungeste faste post |

Helårstakt 25/26 ca. **2,27 mio. kr**. Helåret 2024/25 gav driftsresultat ~425 t.kr (20 % margin)
og resultat efter renter ~352 t.kr.

## Datakilder

| Fil | Indhold | Periode |
|---|---|---|
| `Salgsdata_BG.xlsx` (OnlinePOS) | Salgslinjer pr. bon | 03.07.2025 – 05.06.2026 |
| `Posteringer ...24.25.xlsx` (e-conomic) | Finansposteringer | 01.07.2024 – 30.06.2025 |
| `Posteringer ...25.26.xlsx` (e-conomic) | Finansposteringer | 01.07.2025 – dec. 2025 |
| `Danloen ...csv` + `PDF ...pdf` (Danløn) | Løn & tidsregistrering | 01.07.2025 – (planlagt) 30.06.2026 |

## Metode & forbehold

- **Omsætning afstemt:** Salgsdataens linjebeløb inkl. moms ÷ 1,25 = bogført omsætning
  (jul–dec 2025: 1.068.064 kr i begge kilder — eksakt match).
- **Omsætning & løn for jan–maj 2026** er endnu ikke bogført i e-conomic (kun omkostninger er
  ført). Disse linjer hentes derfor fra OnlinePOS (omsætning) og Danløn-tidsregistreringen (løn) —
  begge afstemt 1:1 mod bogføringen for jul–dec 2025.
- **Vareforbrug** tages som bogført; lageret reguleres løbende. Den månedlige vareforbrugsprocent
  svinger pga. partivis fakturering af indkøb — ÅTD-tallet (21,7 %) er det retvisende niveau.
  (En tidligere udgave viste 42 % alene fordi december-udtrækket ikke var ajourført; med
  posteringer til og med maj er billedet nu rent.)
- **Afskrivninger og renter** bogføres ved årsafslutning og indgår derfor kun i helårskolonnen
  (2024/25), ikke i maj-/ÅTD-kolonnerne.
- **Tidsregistrering** dækker ~2.348 bemandede timer ÅTD (afsluttede måneder jul 2025 – maj 2026).

## Reproduktion

`build_report.py` indlæser kildefilerne, afstemmer tallene og genererer `data.json` + `index.html`.

```
pip install pandas openpyxl pdfplumber
python3 build_report.py
```

*Branchenormer er vejledende (HORESTA, OnlinePOS, Danmarks Statistik). Drikkevaredrevne barer
ligger typisk lavere på vareforbrug og kan ligge lavere på lønprocent end fuld-service restauranter.*
