# Søhøjlandets Dødsbo — website

En komplet, selvstændig hjemmeside for **Søhøjlandets Dødsbo** — en dødsbo-tjeneste
(vurdering, opkøb, rydning, rengøring og klargøring til salg) under
**Søhøjlandets Begravelser**.

Sitet er bygget med ren HTML, CSS og JavaScript (ingen build-værktøjer), så det kan
hostes hvor som helst — fx GitHub Pages, Netlify, Simply.com eller et almindeligt webhotel.
Funktionaliteten svarer til edoedsbo.dk: præsentation af ydelser, proces, priser, FAQ,
samt en interaktiv flertrins-formular til gratis vurdering og en kontaktformular.

## Indhold

| Fil | Side |
|---|---|
| `index.html` | Forside (hero, ydelser, proces, anmeldelser, dækningsområde, CTA) |
| `ydelser.html` | Detaljerede ydelser |
| `saadan-foregaar-det.html` | Processen i 4 trin |
| `vurdering.html` | **Flertrins vurderingsformular** (med validering + indsendelse) |
| `priser.html` | Priser og prismodel |
| `om-os.html` | Om virksomheden og værdier |
| `faq.html` | Ofte stillede spørgsmål (accordion) |
| `kontakt.html` | Kontaktinfo + kontaktformular |
| `privatlivspolitik.html` | GDPR-privatlivspolitik |
| `404.html` | Fejlside |
| `assets/css/styles.css` | Designsystem |
| `assets/js/main.js` | Menu, accordion, formularlogik |
| `assets/img/*.svg` | Logo og illustrationer (originale) |
| `robots.txt`, `sitemap.xml` | SEO |

## Sådan ses sitet lokalt

Åbn `index.html` direkte i en browser, eller kør en lokal server:

```bash
cd soehoejlandets-doedsbo
python3 -m http.server 8080
# åbn http://localhost:8080
```

## Formularer — sådan virker indsendelse

Begge formularer (vurdering + kontakt) validerer i browseren og indsender derefter.
Indsendelse styres i toppen af `assets/js/main.js`:

```js
var FORM_ENDPOINT = "";              // sæt til fx Formspree-URL for direkte afsendelse
var CONTACT_EMAIL = "kontakt@shlb.dk";
```

- **Med endpoint:** Udfyld `FORM_ENDPOINT` med et endpoint fra fx
  [Formspree](https://formspree.io), Make/Zapier-webhook eller egen backend.
  Data sendes som JSON via `fetch`.
- **Uden endpoint (standard):** Som fallback åbnes brugerens mailprogram med en
  færdigudfyldt e-mail til `CONTACT_EMAIL`, så sitet virker uden server fra dag ét.

## Tilpasning

- **Navn/brand:** Tjenestens navn "Søhøjlandets Dødsbo" og undertitlen står i hver sides
  header/footer — søg og erstat hvis et andet navn ønskes.
- **Kontaktoplysninger:** Telefon (`86 89 12 12` / `tel:+4586891212`), e-mail
  (`kontakt@shlb.dk`), adresser og CVR (`42454974`) går igen i header, footer og
  kontaktsiden. Verificér mod virksomhedens aktuelle oplysninger før publicering.
- **Farver/typografi:** Ændres centralt i `:root` i `assets/css/styles.css`.

> Bemærk: Indhold, tekster, illustrationer og kode er originalt udarbejdet til
> Søhøjlandets Begravelser og er inspireret af konceptet bag edoedsbo.dk — ikke kopieret.
