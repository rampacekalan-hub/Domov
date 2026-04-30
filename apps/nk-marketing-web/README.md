# NK Marketing — statický web

Statický klon webu NK Marketing. Žiadny build proces, žiadna závislosť na Squarespace.

## Spustenie lokálne

```bash
# stačí ľubovoľný statický server, napr.:
npx serve .
# alebo
python3 -m http.server 8080
```

Potom otvor `http://localhost:8080`.

## Štruktúra

- `index.html` — všetky sekcie (hero, služby, proces, referencie, kontakt)
- `styles.css` — kompletný štýl (fareby, typografia, responsive)
- `script.js` — mobilné menu, aktívne odkazy, formulár
- `assets/` — obrázky (hero.jpg, about.jpg, service-1..4.jpg)

## Nasadenie

Vhodné pre:
- **Netlify** — drag & drop priečinka
- **Vercel** — `vercel deploy`
- **GitHub Pages** — push do `gh-pages` branch
- **Vlastný server** — len skopírovať priečinok do webroot

## Čo doplniť

1. **Obrázky** do `assets/`:
   - `hero.jpg` (4:5 portrét)
   - `about.jpg` (sekcia "Viete, že reklamu potrebujete")
   - `service-1.jpg` … `service-4.jpg` (3:4 portréty)
2. **Logá značiek** v sekcii "Dôverujú nám" — momentálne textové placeholdery, vymeniť za SVG/PNG.
3. **Kontaktný formulár** — momentálne len JS alert. Pripojiť na backend (Formspree, Netlify Forms, vlastný API endpoint).
4. **Doménu, OG obrázok, favicon** podľa potreby.

## Farby

- Navy: `#1b1f4d`
- Coral (akcent): `#ff7a5c`
- Peach (pozadie): `#fbe2d8`
