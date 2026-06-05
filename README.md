# BG2 ApS — Ledelsesrapportering 2025/26

Dynamisk HTML-rapport med de væsentlige nøgletal for **BG2 ApS** (Borgergade 2, Aalborg) —
en bar- og aktivitetscafé. Rapporten er afstemt mod tre datakilder og dækker regnskabsåret
**2025/26** (status pr. 5. juni 2026) med benchmark mod det fulde år **2024/25**.

## Åbn rapporten

Åbn `index.html` i en browser. Siden er selvstændig (data er indlejret); Chart.js hentes fra CDN,
så internetadgang anbefales for at vise graferne.

## Indhold

- **Overblik** – hovednøgletal som KPI-kort
- **Resultatopgørelse** – 2024/25 (helår) vs. 2025/26 (jul–dec) vs. normaliseret helårsestimat
- **Omsætning** – månedsudvikling, produktmix, ugedags- og klokkeslætsmønster, største produkter
- **Vareforbrug** – vareforbrugsprocent og sammensætning
- **Løn & bemanding** – lønprocent, omsætning pr. bemandet time, månedlig udvikling
- **Benchmark & baggrund** – sammenligning med branchenormer
- **Observationer & anbefalinger**

## Væsentlige nøgletal (hovedtal)

| Nøgletal | Værdi | Bemærkning |
|---|---|---|
| Omsætning (helårstakt 25/26) | ~2,27 mio. kr | +7,8 % vs. 2024/25 |
| Vareforbrugsprocent (strukturel) | ~23 % | Dækningsgrad ~77 % |
| Lønprocent (kontant løn) | ~14 % | Faldet fra 19,2 % året før |
| Omsætning pr. bemandet time | ~887 kr | ekskl. moms |
| Forpagtningsafgift | ~21 % af oms. | Største faste post |
| Driftsresultat 2024/25 | ~425 t.kr | 20 % driftsmargin |

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
- **Periodisering i bogføringen:** e-conomic-posteringerne for 2025/26 er kun ført til og med
  december 2025, og næsten et helt års vareindkøb (bl.a. Carlsberg) samt hele forpagtningen er
  bogført i halvåret. Derfor viser halvårsregnskabet et kunstigt højt vareforbrug (42 %) og et
  midlertidigt underskud. Dette er en **timing-effekt**, ikke en reel forværring.
- **Normaliseret helårsestimat:** omsætning fremskrevet fra faktisk salg år-til-dato; vareforbrug
  sat til det strukturelle niveau (22,7 %, som 2024/25); løn til aktuel takt fra tidsregistreringen;
  forpagtning/øvrige faste omkostninger som 2024/25.
- **Tidsregistrering** dækker 2.536 bemandede timer for året inkl. planlagte vagter frem til 27.
  juni 2026. Operationelle lønnøgletal er beregnet på de afsluttede måneder (jul 2025 – maj 2026).

## Reproduktion

`build_report.py` indlæser kildefilerne, afstemmer tallene og genererer `data.json` + `index.html`.

```
pip install pandas openpyxl pdfplumber
python3 build_report.py
```

*Branchenormer er vejledende (HORESTA, OnlinePOS, Danmarks Statistik). Drikkevaredrevne barer
ligger typisk lavere på vareforbrug og kan ligge lavere på lønprocent end fuld-service restauranter.*
