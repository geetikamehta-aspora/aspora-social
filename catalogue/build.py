"""Builds catalogue.html from the product data below.

To add products: add an entry to a category's "products" list (or add a new category dict), drop the
photos into images/, then run `python3 build.py && node render.mjs`.

Product layouts:
  "top"  - one big photo + text (for single photos)
  "grid" - six model shots + four detail shots; give "prefix" and "details" (see MODELS)
"""
from html import escape

HANDLE = "@furry.pooch"
PHONE = "+91 99407 27027"
EMAIL = "furrypooch2@gmail.com"
CONTACT_NAME = "Darpan"

MODELS = ["golden-retriever", "pomeranian", "dachshund", "ragdoll-cat", "shih-tzu", "tabby-cat"]

PAW_PATH = ('<ellipse cx="4.6" cy="11" rx="2.3" ry="3"/><ellipse cx="9.4" cy="6" rx="2.3" ry="3"/>'
            '<ellipse cx="14.6" cy="6" rx="2.3" ry="3"/><ellipse cx="19.4" cy="11" rx="2.3" ry="3"/>'
            '<ellipse cx="12" cy="17.4" rx="5.8" ry="4.6"/>')
PAW = f'<svg viewBox="0 0 24 24">{PAW_PATH}</svg>'

COLORS = {"purple": "#5B4FD6", "brown": "#4A2410", "sun": "#FFD95A", "cream": "#FFF6DF",
          "soft": "#F8CD66", "lilac": "#D9D3FB", "deep": "#EBB03C"}

ICONS = {
    "leaf": '<svg viewBox="0 0 24 24"><path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19l8-8"/></svg>',
    "paw": f'<svg class="fill" viewBox="0 0 24 24">{PAW_PATH}</svg>',
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "insta": '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17" cy="7" r=".6"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/></svg>',
}

PERKS = [("leaf", "Lightweight<br>&amp; Comfortable"), ("paw", "Festive<br>Look"), ("heart", "Easy to Wear<br>&amp; Pet Friendly")]

CATEGORIES = [
    {
        "name": "Pet Kurtas",
        "blurb": "Embroidered, mirror-work and multi-print Indian kurtas, tailored for dogs and cats.",
        "short": "Embroidered, mirror-work & multi-print kurtas",
        "products": [
            {
                "code": "FP-K01", "name": "Phool Bagh Floral Kurta", "layout": "top",
                "hero": "teal-floral-kurta.jpg", "pos": "center 25%", "sticker": "Dress<br>me up!",
                "desc": "A garden in bloom: an aqua-teal kurta covered in coral, pink and gold floral embroidery, finished with a stand collar and short sleeves.",
                "features": ["Aqua-teal base with all-over floral embroidery", "Gold thread detailing on collar and sleeves",
                             "Stand collar, short sleeves", "Shown on a Ragdoll cat"],
            },
            {
                "code": "FP-K02", "name": "Aasmani Mirror-Work Kurta", "layout": "grid", "prefix": "sky",
                "details": [("flatlay-front", "Front"), ("flatlay-back", "Back"), ("detail-mirror-border", "Mirror border"), ("detail-sleeve", "Sleeve")],
                "desc": "A sky-blue kurta with a sprinkle of gold stars and hand-finished mirror and sequin borders. Shown here on dogs and cats of different breeds and sizes.",
                "features": ["Mirror, sequin and thread-work borders", "Mandarin collar with centre placket",
                             "Flared sleeves with embroidered cuffs", "Curved hem, easy leg openings"],
            },
            {
                "code": "FP-K03", "name": "Rangeela Multi-Print Jacket Kurta Set", "layout": "grid", "prefix": "rangeela-kurta-set",
                "details": [("front", "Front"), ("back", "Back"), ("collar", "Collar"), ("cuff", "Gold-lace cuff")],
                "sizes": ["XS", "S", "M", "L", "XL"],
                "desc": "Two looks in one: a patchwork multi-print ethnic jacket layered over a hot-pink kurta with gold-lace striped sleeves.",
                "features": ["Multi-print jacket with floral and paisley panels", "Hot-pink kurta, gold-lace striped sleeves",
                             "Mandarin collar, front button placket", "Curved hem"],
            },
            {
                "code": "FP-K04", "name": "Haldi Silver-Lace Kurta", "layout": "grid", "prefix": "haldi-silver-lace-kurta",
                "details": [("front", "Front"), ("back", "Back"), ("collar", "Lace collar"), ("sleeve", "Lace cuff")],
                "desc": "A sunny haldi-yellow kurta trimmed with silver zari lace on the collar, placket and sleeves. Bright, festive and ready for the puja.",
                "features": ["Bright haldi-yellow body", "Silver lace on collar, placket and cuffs",
                             "Stand collar with centre placket", "Curved hem, easy leg openings"],
            },
            {
                "code": "FP-K05", "name": "Phoolwari Pocket Kurta", "layout": "grid", "prefix": "phoolwari-pocket-kurta",
                "details": [("front", "Front"), ("back", "Back"), ("pocket", "Pocket square"), ("fabric", "Print")],
                "desc": "A sky-blue garden of tiny flowers and paisleys, with a chest pocket and a mustard pocket square for the dapper touch.",
                "features": ["Floral and paisley print on sky blue", "Chest pocket with mustard pocket square",
                             "Stand collar, short sleeves", "Soft blue lining, curved hem"],
            },
        ],
    },
    {
        "name": "Pet Sherwanis",
        "blurb": "Dapper sherwanis for the grand entrance.",
        "short": "Sequin-embroidered sherwanis",
        "products": [
            {
                "code": "FP-S01", "name": "Gulaal Sequin Sherwani", "layout": "grid", "prefix": "gulaal-sequin-sherwani",
                "details": [("front", "Front"), ("back", "Back"), ("collar", "Collar & buttons"), ("sleeve", "Sleeve")],
                "desc": "A dusty-rose sherwani sprinkled with gold sequin motifs, finished with a mandarin collar and covered buttons.",
                "features": ["Gold sequin-embroidered motifs all over", "Mandarin collar with covered buttons",
                             "Short sleeves, soft cream inner lining", "Curved hem for easy movement"],
            },
        ],
    },
    {
        "name": "Pet Jackets",
        "blurb": "Statement jackets in rich festive fabrics.",
        "short": "Brocade jackets",
        "products": [
            {
                "code": "FP-J01", "name": "Gulabi Brocade Zip Jacket", "layout": "grid", "prefix": "gulabi-brocade-jacket",
                "details": [("front", "Front & pocket"), ("back", "Back"), ("pocket", "Pocket square"), ("armhole", "Armhole")],
                "desc": "A rich pink-and-gold paisley brocade jacket with a front zip, mandarin collar and a tiny pocket square.",
                "features": ["Pink and gold paisley brocade", "Front zip closure", "Chest pocket with pocket square",
                             "Sleeveless, with soft pink lining"],
            },
        ],
    },
    {
        "name": "Pet Lehengas & Frocks",
        "blurb": "Twirl-ready lehenga dresses and ethnic frocks in rich festive fabrics.",
        "short": "Festive lehenga dresses & frocks",
        "products": [
            {
                "code": "FP-L01", "name": "Ruby Zari Lehenga Dress", "layout": "top",
                "hero": "ruby-lehenga-frock.jpg", "pos": "center 62%", "sticker": "Twirl<br>time!",
                "desc": "Rich ruby-red brocade scattered with gold zari, a full flared skirt and a gold-bordered hem trimmed with tiny pearl beads. Made for weddings and festivals.",
                "features": ["Ruby-red zari brocade fabric", "Gold floral border with pearl-bead lace edge",
                             "Gold waist band, short sleeves", "Gathered, flared skirt for twirling"],
            },
            {
                "code": "FP-L02", "name": "Jamuni Double-Layer Ethnic Frock", "layout": "grid", "prefix": "jamuni-frock",
                "details": [("front", "Front"), ("back", "Back"), ("neckline", "Neckline"), ("hem", "Gold-lace hem")],
                "desc": "A deep-purple twirl dress with two ruffled tiers and chevron gold lace, tied up at the neck.",
                "features": ["Deep purple with gold gota lace", "Chevron-lace bodice, tie-up neck",
                             "Double-layered ruffle skirt", "Gold lace trim on every tier"],
            },
            {
                "code": "FP-L03", "name": "Lal Pari Bow Frock", "layout": "grid", "prefix": "lal-pari-bow-frock",
                "models": ["shih-tzu", "golden-retriever", "persian-cat", "tabby-cat", "pomeranian", "dachshund"],
                "details": [("front", "Front"), ("back", "Back"), ("border", "Gold-lace border"), ("bow", "Bow & tassels")],
                "desc": "A red party frock scattered with tiny gold motifs, with a gold-lace hem and a bow tied at the waist, finished with golden tassels.",
                "features": ["Red fabric with gold dot motifs", "Gold lace along the hem and neckline",
                             "Waist bow with golden tassels", "Full gathered skirt, sleeveless"],
            },
        ],
    },
    {
        "name": "Collars & Harnesses",
        "blurb": "Frilly bell collars and an adventure-ready harness to finish the look.",
        "short": "Ruffle bell collars & harnesses",
        "products": [
            {
                "code": "FP-A01", "name": "Ruffle Bell Collar", "layout": "collar", "cover": "collar-hero.jpg",
                "desc": "Frilly polka-dot ribbon ruffles with a snap buckle and a jingly bell. Shown on a Golden Retriever and a Ragdoll cat.",
                "features": ["Ruffled polka-dot ribbon bows", "Snap-buckle closure", "Jingle-bell charm", "Five colours to pick from"],
                "colours": [("red", "Red"), ("green", "Neon Green"), ("hotpink", "Hot Pink"), ("babypink", "Baby Pink"), ("orange", "Orange")],
            },
            {
                "code": "FP-A02", "name": "Orange Adventure Dog Harness", "layout": "trio", "cover": "harness-front.jpg",
                "desc": "A bright orange harness with a breathable teal mesh panel and adjustable buckle straps, made for walks that turn into adventures.",
                "features": ["Bright orange body with breathable teal mesh panel", "Adjustable buckle straps at chest and sides",
                             "Top D-ring for the leash clip", "Contrast grey piping"],
            },
        ],
    },
]


# ---------- helpers ----------
def paw(x, y, size, rot=0, color="purple", opacity=1):
    c = COLORS.get(color, color)
    return (f'<span class="paw" style="left:{x}mm;top:{y}mm;width:{size}mm;height:{size}mm;transform:rotate({rot}deg);opacity:{opacity}">'
            f'<svg viewBox="0 0 24 24" fill="{c}">{PAW_PATH}</svg></span>')


def trail(points, size, color="purple", rot=90, opacity=1):
    return "".join(paw(x, y, size * (0.85 if i % 2 else 1), rot + (-8 if i % 2 else 8), color, opacity) for i, (x, y) in enumerate(points))


def foot(n, dark=False):
    logo = "assets/logo-yellow.png" if dark else "assets/logo-brown.png"
    return f'<div class="foot"><img src="{logo}" alt="Furry Pooch"><span>{HANDLE}</span><span class="num">{n}</span></div>'


def features_html(items):
    return '<ul class="features">' + "".join(f"<li>{PAW}<span>{escape(i)}</span></li>" for i in items) + "</ul>"


def blobs(spec):
    return "".join(f'<div class="blob {c}" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm"></div>' for c, x, y, d in spec)


def perks_html(top=None):
    st = f' style="top:{top}mm"' if top is not None else ""
    return f'<div class="perks"{st}>' + "".join(f'<div class="perk"><i>{ICONS[i]}</i><span>{t}</span></div>' for i, t in PERKS) + "</div>"


def sticker(text, x, y, size, rot, cls="round", extra=""):
    return (f'<div class="sticker {cls}" style="left:{x}mm;top:{y}mm;width:{size}mm;height:{size}mm;transform:rotate({rot}deg);'
            f'font-size:{size * 0.42:.1f}pt;{extra}">{text}</div>')


def img_of(p, which="cover"):
    if p.get("cover"):
        return p["cover"]
    if p.get("hero"):
        return p["hero"]
    return f'{p["prefix"]}-{MODELS[0]}.jpg'


def count_label(n):
    return f'{n} design{"s" if n != 1 else ""}'


# ---------- page builders ----------
def page_cover():
    arches = [("ruby-lehenga-frock.jpg", "center 22%", "arch", 84), ("teal-floral-kurta.jpg", "center 20%", "arch tall", 98),
              ("jamuni-frock-golden-retriever.jpg", "center 20%", "arch", 84)]
    a = "".join(f'<div class="{c}" style="height:{h}mm"><img src="images/{img}" style="object-position:{pos}"></div>' for img, pos, c, h in arches)
    walk = [(16 + i * 20.5, 188 + (-4 if i % 2 else 3)) for i in range(9)]
    return (f'<section class="page cover">{blobs([("soft", 118, -60, 160), ("deep", -50, 190, 130), ("deep", 150, 95, 90)])}'
            f'{paw(168, 14, 14, 18, "purple")}{paw(184, 30, 10, -12, "purple")}'
            f'<img class="logo" src="assets/logo-brown.png" alt="Furry Pooch">'
            f'{sticker("Festive<br>Edit", 11, 12, 33, -12, "round")}'
            f'<div class="pill">The Ethnic Wear Collection</div>'
            f'<div class="sub">Festive outfits for dogs &amp; cats</div>'
            f'{trail(walk, 8.5, "purple")}<div class="arches">{a}</div></section>')


def page_contents(toc, n):
    rows = "".join(
        f'<div class="toc-row"><div class="no">{ci:02d}</div><div class="meta"><h3>{escape(CATEGORIES[ci-1]["name"])}</h3>'
        f'<p>{escape(CATEGORIES[ci-1]["short"])} &middot; {count_label(len(CATEGORIES[ci-1]["products"]))}</p></div>'
        f'<div class="thumbs">{"".join(f"<img src=images/{img_of(p)}>" for p in CATEGORIES[ci-1]["products"][:3])}</div>'
        f'<div class="pg">p. {pg}</div></div>'
        for ci, pg in toc)
    return (f'<section class="page contents">{blobs([("soft", 130, -45, 140), ("deep", -40, 215, 110)])}'
            f'{paw(158, 14, 13, 14, "purple")}{paw(176, 30, 10, -10, "purple")}'
            f'<span class="chip">Inside</span><h1>Our Collections</h1>'
            f'<p class="lead">Handpicked Indian festive wear for pets. Pick a collection, find your favourite, and message us to order.</p>'
            f'<div class="toc">{rows}</div>'
            f'<div class="cta"><h3>Found your favourite?</h3><p>Note its design code (like FP-K01) and message {CONTACT_NAME} on Instagram {HANDLE}.</p></div>'
            f'{foot(n)}</section>')


def page_pets(n):
    pics = [("rangeela-kurta-set-golden-retriever", 12, 76), ("gulabi-brocade-jacket-ragdoll-cat", 77, 88), ("jamuni-frock-dachshund", 142, 76),
            ("gulaal-sequin-sherwani-pomeranian", 12, 148), ("rangeela-kurta-set-tabby-cat", 77, 160), ("gulaal-sequin-sherwani-shih-tzu", 142, 148)]
    circles = "".join(f'<div class="circle" style="left:{x}mm;top:{y}mm;width:56mm;height:56mm"><img src="images/{f}.jpg" style="object-position:center 20%"></div>'
                      for f, x, y in pics)
    return (f'<section class="page purple pets">{blobs([("psoft", 120, -50, 150), ("pdeep", -50, 180, 130)])}'
            f'{paw(10, 12, 12, -14, "sun")}{paw(192, 56, 9, 20, "sun")}'
            f'<h1>Dogs. Cats.<br>Everyone&rsquo;s invited!</h1>'
            f'<p class="lead">From Golden Retrievers to Dachshunds, Ragdolls to Shih Tzus &mdash; our outfits look good on every furry family member.</p>'
            f'{circles}{sticker("Woof!", 2, 70, 26, -14, "round sun")}{sticker("Meow!", 118, 136, 26, 12, "round sun")}'
            f'{perks_html(228)}{trail([(22 + i * 22, 252) for i in range(8)], 8, "sun", 90, .9)}{foot(n, True)}</section>')


def page_divider(ci, cat, n):
    prods = cat["products"][:3]
    single = len(prods) == 1
    hs = {1: [118], 2: [72, 72], 3: [60, 72, 60]}[len(prods)]
    thumbs = "".join(
        f'<div class="arch{" tall" if len(prods) == 3 and i == 1 else ""}" style="height:{hs[i]}mm;{"width:92mm;border-radius:46mm 46mm 0 0;" if single else ""}">'
        f'<img src="images/{img_of(p)}" style="object-position:{p.get("pos", "center 20%")}"></div>' for i, p in enumerate(prods))
    return (f'<section class="page purple divider">{blobs([("psoft", 120, -50, 150), ("pdeep", -45, 150, 120)])}'
            f'{paw(176, 20, 16, 16, "sun", .9)}{paw(158, 44, 11, -12, "sun", .9)}'
            f'<div class="bignum">{ci:02d}</div>'
            f'<div class="title"><span class="chip">Collection {ci:02d}</span><h1>{escape(cat["name"])}</h1><p>{escape(cat["blurb"])}</p>'
            f'<div class="count"><span class="chip ghost">{count_label(len(cat["products"]))}</span></div></div>'
            f'<div class="arches" style="bottom:22mm;gap:6mm">{thumbs}</div>{foot(n, True)}</section>')


def head_html(cat, p):
    return f'<span class="chip">{escape(cat["name"])}</span> &nbsp;<span class="code">{p["code"]}</span>'


def page_top(cat, p, n):
    st = sticker(p["sticker"], 152, 168, 38, 9, "round", "") if p.get("sticker") else ""
    return (f'<section class="page top">{blobs([("soft", 140, 215, 120), ("deep", -40, 245, 80)])}'
            f'<div class="hero"><img class="photo" src="images/{p["hero"]}" style="object-position:{p.get("pos", "center 25%")}"></div>{st}'
            f'<div class="info"><div class="l">{head_html(cat, p)}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
            f'<div class="r">{features_html(p["features"])}</div></div>{foot(n)}</section>')


def page_grid(cat, p, n, idx):
    pre = p["prefix"]
    models = "".join(f'<div class="tile"><img class="photo" src="images/{pre}-{m}.jpg"></div>' for m in p.get("models", MODELS))
    details = "".join(f'<figure><div class="tile"><img class="photo" src="images/{pre}-{s}.jpg"></div><figcaption>{escape(c)}</figcaption></figure>'
                      for s, c in p["details"])
    size = ""
    if p.get("sizes"):
        size = '<div class="size-pill">SIZES ' + "".join(f"<b>{s}</b>" for s in p["sizes"]) + "</div>"
    blob = [("soft", 150, -40, 100)] if idx % 2 == 0 else [("soft", -40, -50, 100)]
    return (f'<section class="page grid{" alt" if idx % 2 else ""}">{blobs(blob)}'
            f'{paw(190 if idx % 2 == 0 else 8, 3, 10, 15, "purple")}'
            f'<div class="head"><div class="l">{head_html(cat, p)}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
            f'<div class="r">{features_html(p["features"])}{size}</div></div>'
            f'{perks_html()}<div class="models">{models}</div><div class="details">{details}</div>{foot(n)}</section>')


def page_collar(cat, p, n):
    sw = "".join(f'<div class="sw"><div class="c"><img src="images/collar-swatch-{f}.jpg"></div><span>{escape(t)}</span></div>' for f, t in p["colours"])
    return (f'<section class="page collar">{blobs([("soft", 150, -40, 100), ("deep", -40, 230, 90)])}{paw(190, 3, 10, 15, "purple")}'
            f'<div class="head"><div class="l">{head_html(cat, p)}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
            f'<div class="r">{features_html(p["features"])}</div></div>'
            f'<div class="tile hero"><img class="photo" src="images/collar-hero.jpg"></div>'
            f'{sticker("Jingle<br>jingle!", 156, 44, 30, 10, "round")}'
            f'<div class="duo"><div class="tile"><img class="photo" src="images/collar-detail-dog.jpg"></div><div class="tile"><img class="photo" src="images/collar-detail-cat.jpg"></div></div>'
            f'<div class="swatches"><h3>Pick your colour!</h3><div class="swgrid">{sw}</div></div>{foot(n)}</section>')


def page_trio(cat, p, n):
    return (f'<section class="page trio">{blobs([("soft", 150, -40, 100), ("deep", -40, 240, 90)])}{paw(8, 3, 10, -15, "purple")}'
            f'<div class="head"><div class="l">{head_html(cat, p)}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div></div>'
            f'<div class="tile big"><img class="photo" src="images/harness-front.jpg"></div>'
            f'<div class="tile s1"><img class="photo" src="images/harness-side.jpg"></div><div class="tile s2"><img class="photo" src="images/harness-back.jpg"></div>'
            f'<div class="fcard"><h3>Built for adventure</h3>{features_html(p["features"])}</div>'
            f'{paw(150, 226, 30, 14, "sun", .35)}{paw(176, 240, 18, -12, "sun", .35)}'
            f'{sticker("Let&rsquo;s<br>go!", 14, 218, 32, -10, "round sun")}{foot(n)}</section>')


def page_closing():
    rows = [("phone", f"Call {CONTACT_NAME}", PHONE), ("insta", "Instagram", HANDLE), ("mail", "Email", EMAIL)]
    r = "".join(f'<div class="crow"><i>{ICONS[i]}</i><div><small>{l}</small><span>{escape(t)}</span></div></div>' for i, l, t in rows)
    return (f'<section class="page purple closing">{blobs([("psoft", 120, -50, 150), ("pdeep", -50, 200, 130)])}'
            f'{paw(14, 20, 13, -16, "sun")}{paw(30, 38, 9, 10, "sun")}{paw(182, 22, 13, 18, "sun")}'
            f'<img class="logo" src="assets/logo-yellow.png" alt="Furry Pooch">'
            f'<h1>Let&rsquo;s dress your<br>furry family!</h1>'
            f'<div class="contact">{r}</div>'
            f'<div class="qr"><img src="assets/instagram-qr.png" alt="Instagram QR for {HANDLE}"></div>'
            f'<div class="qrcap">Scan to follow us</div>'
            f'<div class="walk"><img src="images/illustration-walk.jpg" alt=""></div>'
            f'{sticker("Say<br>hi!", 160, 224, 30, 12, "round sun")}</section>')


def build():
    # page plan: (kind, args...) -> page number is position + 1
    plan = [("cover",), ("contents",), ("pets",)]
    first_page = {}
    for ci, cat in enumerate(CATEGORIES, 1):
        first_page[ci] = len(plan) + 1
        if len(cat["products"]) >= 2:
            plan.append(("divider", ci))
        for pi in range(len(cat["products"])):
            plan.append(("product", ci, pi))
    plan.append(("closing",))
    toc = sorted(first_page.items())

    out = []
    for i, item in enumerate(plan):
        n = i + 1
        kind = item[0]
        if kind == "cover": out.append(page_cover())
        elif kind == "contents": out.append(page_contents(toc, n))
        elif kind == "pets": out.append(page_pets(n))
        elif kind == "divider": out.append(page_divider(item[1], CATEGORIES[item[1] - 1], n))
        elif kind == "closing": out.append(page_closing())
        else:
            cat = CATEGORIES[item[1] - 1]; p = cat["products"][item[2]]
            lay = p["layout"]
            out.append(page_top(cat, p, n) if lay == "top" else page_collar(cat, p, n) if lay == "collar"
                       else page_trio(cat, p, n) if lay == "trio" else page_grid(cat, p, n, n))
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Furry Pooch Catalogue</title>'
           '<link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="styles.css"></head><body>'
           + "".join(out) + '</body></html>')
    open("catalogue.html", "w").write(doc)
    print(f"built catalogue.html: {len(plan)} pages")


if __name__ == "__main__":
    build()
