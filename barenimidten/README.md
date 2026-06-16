# Baren i Midten – Snapsting 2026 (barenimidten.dk)

Statisk website for **Baren i Midten (BIM)** under **Snapsting 2026** i Viborg
(19.–28. juni 2026). Bygget i ren HTML/CSS/JS uden afhængigheder, så det kan
hostes hvor som helst.

> Dette site ligger i mappen `barenimidten/` og er adskilt fra den finansielle
> ledelsesrapport i repo-roden, som er urørt.

## Sider

| Fil | Menupunkt | Indhold |
|---|---|---|
| `index.html` | Forside | Intro til Snapsting + Baren i Midten, de tre pladser, genveje |
| `musikprogram.html` | Musikprogram | Filtrerbart program for Nytorv, Hjultorvet og Paradepladsen |
| `menukort.html` | Menukort | Klargjort med pladsholdere – menukort lægges ind senere |
| `pladstegninger.html` | Pladstegninger | Tegneserie-agtige SVG-kort over Nytorv og Hjultorvet |
| `pant-regler.html` | Pant & regler | Pant, husregler, sikkerhed og praktisk håndtering |
| `ambassadorer.html` | Viborg Ambassadørerne | Om Ambassadørerne og koncerterne på Nytorv |

`assets/`: `styles.css` (tema), `program.js` (programdata + renderer), `nav.js` (mobilmenu).

## Pladser

Baren i Midten står for tre pladser: **Nytorv**, **Hjultorvet** og **Paradepladsen**.

## Programdata

`assets/program.js` indeholder programmet som `window.SNAPSTING_PROGRAM`
({ plads → dag → liste af { time, act, kind } }). Det er udtrukket fra
afviklingsskemaet *Program for Snapsting 2026 (v5)* og renset til publikumsinfo
(akt + showtid; interne kolonner som load-in/curfew/load-out er udeladt).
Opdatér programmet ved at rette `window.SNAPSTING_PROGRAM` i `program.js`.

## Classic Race / øvrige arrangementer

Classic Race er flyttet væk fra hovedindholdet og optræder som et lille punkt
under **"Øvrige arrangementer"** i footeren på alle sider.
Linket peger pt. på `https://www.classicrace.dk` – ret det, hvis den korrekte
adresse er en anden.

## Pladstegninger

Tegningerne er håndtegnede SVG'er i en let tegneserie-stil, baseret på de
officielle pladstegninger (Nytorv rev. 10.03.2026, Hjultorv indretning V16).
Paradepladsen mangler tegning og har pt. en pladsholder.

## Kør lokalt

Åbn `index.html` direkte i en browser, eller server mappen:

```
cd barenimidten
python3 -m http.server 8000
# → http://localhost:8000
```
