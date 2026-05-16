# alanrampacek.sk — Financie & Reality

Osobná webstránka Alana Rampaceka spájajúca **finančné poradenstvo** (základ)
a **realitné služby** pod značkou **AccentReal** (`accentreal.sk`).

Postavené v Pythone (Flask) v modernom dizajne inšpirovanom prosight.sk.

## Funkcie

- Hlavná informatívna stránka (hero, služby, prečo ja, sociálny dôkaz)
- Sekcia **Finančné služby** (hypotéky, investovanie, poistenie, ...)
- Sekcia **Reality – AccentReal** s prelinkovaním na `accentreal.sk`
- **Inzeráty** s filtrovaním (predaj / prenájom, typ, mesto) a detailom
- **Prihlásenie na newsletter** (vo footri, viditeľné na každej stránke)
- Kontaktný formulár (ukladá sa do DB)
- JSON API `/api/listings` pre zdieľanie inzerátov

## Stack

- Python 3.11+
- Flask 3, Flask-SQLAlchemy, SQLite (alebo Postgres cez `DATABASE_URL`)
- TailwindCSS (CDN) + Inter font
- Gunicorn na produkciu

## Spustenie lokálne

```bash
cd website
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app.py init-db        # vytvorí DB + 3 demo inzeráty
flask --app app.py run --debug    # http://127.0.0.1:5000
```

## Produkcia

```bash
SECRET_KEY="..." DATABASE_URL="postgresql://..." \
gunicorn -w 3 -b 0.0.0.0:8000 app:app
```

Nasaďte za reverzný proxy (nginx) na doméne `alanrampacek.sk`.

## Štruktúra

```
website/
├── app.py                  # Flask app + modely + routy
├── requirements.txt
├── templates/              # Jinja2 šablóny
│   ├── base.html
│   ├── index.html
│   ├── finance.html
│   ├── reality.html
│   ├── listings.html
│   ├── listing_detail.html
│   ├── about.html
│   ├── contact.html
│   └── _listing_card.html
├── static/
│   ├── css/site.css
│   └── js/site.js
└── data/                   # SQLite DB
```

## Doplnenie inzerátov

Najjednoduchšie cez Python REPL:

```python
from app import app, db, Listing
with app.app_context():
    db.session.add(Listing(
        title="...", kind="predaj", property_type="byt",
        city="Bratislava", price_eur=199000, area_m2=65, rooms="3",
        description="...", image_url="https://...",
    ))
    db.session.commit()
```

V budúcnosti je možné doplniť admin rozhranie alebo synchronizáciu
inzerátov z `accentreal.sk` cez API / RSS / scraper.
