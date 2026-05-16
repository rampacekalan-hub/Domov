import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{DATA_DIR / 'site.db'}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    source = db.Column(db.String(64), default="web")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(50), nullable=False)        # predaj / prenajom
    property_type = db.Column(db.String(50), nullable=False)  # byt / dom / pozemok / komercia
    city = db.Column(db.String(120), nullable=False)
    area_m2 = db.Column(db.Integer)
    rooms = db.Column(db.String(20))
    price_eur = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    external_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    topic = db.Column(db.String(80))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.context_processor
def inject_globals():
    return {
        "now": datetime.utcnow(),
        "brand": {
            "name": "Alan Rampacek",
            "tagline": "Financie & Reality pod jednou strechou",
            "phone": "+421 900 000 000",
            "email": "info@alanrampacek.sk",
            "domain": "alanrampacek.sk",
            "realitka": "AccentReal",
            "realitka_url": "https://accentreal.sk",
        },
    }


@app.route("/")
def index():
    featured = (
        Listing.query.filter_by(is_active=True)
        .order_by(Listing.created_at.desc())
        .limit(3)
        .all()
    )
    return render_template("index.html", featured=featured)


@app.route("/financne-sluzby")
def finance():
    return render_template("finance.html")


@app.route("/reality")
def reality():
    return render_template("reality.html")


@app.route("/inzeraty")
def listings():
    q_kind = request.args.get("kind")
    q_type = request.args.get("type")
    q_city = request.args.get("city", "").strip()
    query = Listing.query.filter_by(is_active=True)
    if q_kind:
        query = query.filter_by(kind=q_kind)
    if q_type:
        query = query.filter_by(property_type=q_type)
    if q_city:
        query = query.filter(Listing.city.ilike(f"%{q_city}%"))
    items = query.order_by(Listing.created_at.desc()).all()
    return render_template("listings.html", items=items, filters={
        "kind": q_kind or "", "type": q_type or "", "city": q_city,
    })


@app.route("/inzeraty/<int:listing_id>")
def listing_detail(listing_id):
    item = Listing.query.get_or_404(listing_id)
    if not item.is_active:
        abort(404)
    return render_template("listing_detail.html", item=item)


@app.route("/o-mne")
def about():
    return render_template("about.html")


@app.route("/kontakt", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        topic = request.form.get("topic", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Vyplňte prosím meno, e-mail a správu.", "error")
            return redirect(url_for("contact"))
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            flash("Neplatný e-mail.", "error")
            return redirect(url_for("contact"))

        msg = ContactMessage(
            name=name, email=email, phone=phone, topic=topic, message=message
        )
        db.session.add(msg)
        db.session.commit()
        flash("Ďakujem, ozvem sa Vám čo najskôr.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/newsletter", methods=["POST"])
def newsletter_subscribe():
    email = request.form.get("email", "").strip()
    name = request.form.get("name", "").strip()
    source = request.form.get("source", "web")
    next_url = request.form.get("next") or url_for("index")

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        flash("Neplatný e-mail.", "error")
        return redirect(next_url)

    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        flash("Tento e-mail už je prihlásený. Ďakujem!", "success")
        return redirect(next_url)

    sub = NewsletterSubscriber(email=email, name=name or None, source=source)
    db.session.add(sub)
    db.session.commit()
    flash("Ďakujem za prihlásenie do newslettera!", "success")
    return redirect(next_url)


@app.route("/api/listings")
def api_listings():
    items = Listing.query.filter_by(is_active=True).order_by(Listing.created_at.desc()).all()
    return jsonify([
        {
            "id": i.id,
            "title": i.title,
            "kind": i.kind,
            "property_type": i.property_type,
            "city": i.city,
            "price_eur": i.price_eur,
            "area_m2": i.area_m2,
            "rooms": i.rooms,
            "image_url": i.image_url,
            "url": url_for("listing_detail", listing_id=i.id, _external=True),
        }
        for i in items
    ])


@app.cli.command("init-db")
def init_db():
    db.create_all()
    if Listing.query.count() == 0:
        demo = [
            Listing(
                title="3-izbový byt v centre, kompletná rekonštrukcia",
                kind="predaj", property_type="byt", city="Bratislava",
                area_m2=78, rooms="3", price_eur=219000,
                description="Slnečný 3-izbový byt po kompletnej rekonštrukcii, balkón, pivnica, výborná lokalita.",
                image_url="https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=1200",
            ),
            Listing(
                title="Rodinný dom s pozemkom 600 m²",
                kind="predaj", property_type="dom", city="Senec",
                area_m2=140, rooms="5", price_eur=389000,
                description="Moderný 5-izbový rodinný dom s krytým státím, záhradou a terasou.",
                image_url="https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=1200",
            ),
            Listing(
                title="Prenájom 2-izbového bytu, novostavba",
                kind="prenajom", property_type="byt", city="Bratislava",
                area_m2=54, rooms="2", price_eur=850,
                description="Zariadený 2-izbový byt v novostavbe, parking, pivnica, klimatizácia.",
                image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=1200",
            ),
        ]
        db.session.add_all(demo)
        db.session.commit()
    print("DB initialized.")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
