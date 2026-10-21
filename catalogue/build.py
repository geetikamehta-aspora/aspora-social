"""Builds catalogue.html from the product data below.

To add products: append to CATEGORIES (new category = new dict, new product = new entry
in its "products" list), drop the photos into images/, then run `python3 build.py && node render.mjs`.
"""
from html import escape

HANDLE = "@furry.pooch"

PAW = ('<svg viewBox="0 0 24 24"><ellipse cx="4.6" cy="11" rx="2.3" ry="3"/><ellipse cx="9.4" cy="6" rx="2.3" ry="3"/>'
       '<ellipse cx="14.6" cy="6" rx="2.3" ry="3"/><ellipse cx="19.4" cy="11" rx="2.3" ry="3"/>'
       '<ellipse cx="12" cy="17.4" rx="5.8" ry="4.6"/></svg>')

CATEGORIES = [
    {
        "name": "Pet Kurtas",
        "blurb": "Embroidered and mirror-work Indian kurtas, tailored for dogs and cats.",
        "short": "Embroidered & mirror-work kurtas",
        "products": [
            {
                "code": "FP-K01",
                "name": "Phool Bagh Floral Kurta",
                "layout": "top",
                "hero": "teal-floral-kurta.jpg",
                "pos": "center 25%",
                "desc": "A garden in bloom: an aqua-teal kurta covered in coral, pink and gold floral embroidery, finished with a stand collar and short sleeves.",
                "features": [
                    "Aqua-teal base with all-over floral embroidery",
                    "Gold thread detailing on collar and sleeves",
                    "Stand collar, short sleeves",
                    "Shown on a Ragdoll cat",
                ],
            },
            {
                "code": "FP-K02",
                "name": "Aasmani Mirror-Work Kurta",
                "layout": "grid",
                "models": ["sky-golden-retriever.jpg", "sky-pomeranian.jpg", "sky-dachshund.jpg",
                           "sky-ragdoll-cat.jpg", "sky-shih-tzu.jpg", "sky-tabby-cat.jpg"],
                "details": [("sky-flatlay-front.jpg", "Front"), ("sky-flatlay-back.jpg", "Back"),
                            ("sky-detail-mirror-border.jpg", "Mirror border"), ("sky-detail-sleeve.jpg", "Sleeve")],
                "cover": "sky-ragdoll-cat.jpg",
                "desc": "A sky-blue kurta with a sprinkle of gold stars and hand-finished mirror and sequin borders. Shown here on dogs and cats of different breeds and sizes.",
                "features": [
                    "Mirror, sequin and thread-work borders",
                    "Mandarin collar with centre placket",
                    "Flared sleeves with embroidered cuffs",
                    "Curved hem, easy leg openings",
                ],
            },
        ],
    },
    {
        "name": "Pet Lehengas",
        "blurb": "Twirl-ready lehenga dresses in rich festive fabrics for your little princess.",
        "short": "Festive lehenga dresses",
        "products": [
            {
                "code": "FP-L01",
                "name": "Ruby Zari Lehenga Dress",
                "layout": "top",
                "hero": "ruby-lehenga-frock.jpg",
                "pos": "center 62%",
                "desc": "Rich ruby-red brocade scattered with gold zari, a full flared skirt and a gold-bordered hem trimmed with tiny pearl beads. Made for weddings and festivals.",
                "features": [
                    "Ruby-red zari brocade fabric",
                    "Gold floral border with pearl-bead lace edge",
                    "Gold waist band, short sleeves",
                    "Gathered, flared skirt for twirling",
                ],
            },
        ],
    },
]


def foot(n, logo="assets/logo-brown.png"):
    return f'<div class="foot"><img src="{logo}" alt="Furry Pooch"><span>{HANDLE}</span><span class="num">{n}</span></div>'


def features_html(items):
    return '<ul class="features">' + "".join(f"<li>{PAW}<span>{escape(i)}</span></li>" for i in items) + "</ul>"


def blobs(spec):
    return "".join(f'<div class="blob {c}" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm"></div>' for c, x, y, d in spec)


def cover_img(p):
    return p.get("cover") or p.get("hero") or p["models"][0]


def build():
    pages = []          # (html, label) tuples; page numbers are assigned by order
    toc = []            # (category index, first page number)

    # page 1: cover, page 2: contents (built last since it needs page numbers)
    all_products = [p for c in CATEGORIES for p in c["products"]]
    arch_imgs = [("ruby-lehenga-frock.jpg", "center 22%", "arch"), ("teal-floral-kurta.jpg", "center 20%", "arch tall"),
                 ("sky-golden-retriever.jpg", "center 20%", "arch")]
    arches = "".join(f'<div class="{cls}" style="height:{ {"arch":"84mm","arch tall":"96mm"}[cls] }"><img src="images/{img}" style="object-position:{pos}"></div>'
                     for img, pos, cls in arch_imgs)
    cover = (f'<section class="page cover">{blobs([("soft", 118, -60, 160), ("deep", -50, 190, 130), ("deep", 150, 95, 90)])}'
             f'<img class="logo" src="assets/logo-brown.png" alt="Furry Pooch">'
             f'<div class="pill">The Ethnic Wear Collection</div>'
             f'<div class="sub">Festive outfits for dogs &amp; cats</div>'
             f'<div class="arches">{arches}</div></section>')

    n = 3
    body = []
    for ci, cat in enumerate(CATEGORIES, 1):
        toc.append((ci, n))
        single = len(cat["products"]) == 1
        thumbs = "".join(
            f'<div class="{"arch tall" if (i == 1 or single) else "arch"}" style="height:{"118mm" if single else ("70mm" if i == 1 else "60mm")};{"width:92mm;border-radius:46mm 46mm 0 0;" if single else ""}">'
            f'<img src="images/{cover_img(p)}" style="object-position:{p.get("pos", "center 25%")}"></div>'
            for i, p in enumerate(cat["products"][:3]))
        body.append(f'<section class="page divider">{blobs([("soft", 120, -50, 150), ("deep", -45, 150, 120)])}'
                    f'<div class="bignum">{ci:02d}</div>'
                    f'<div class="title"><span class="chip">Collection {ci:02d}</span><h1>{escape(cat["name"])}</h1>'
                    f'<p>{escape(cat["blurb"])}</p>'
                    f'<div class="count"><span class="chip ghost">{len(cat["products"])} design{"s" if len(cat["products"]) != 1 else ""}</span></div></div>'
                    f'<div class="arches" style="bottom:22mm;gap:6mm">{thumbs}</div>{foot(n)}</section>')
        n += 1
        for p in cat["products"]:
            head = f'<span class="chip">{escape(cat["name"])}</span> &nbsp;<span class="code">{p["code"]}</span>'
            if p["layout"] == "side":
                body.append(f'<section class="page side">{blobs([("soft", 150, 190, 130)])}'
                            f'<div class="hero"><img class="photo" src="images/{p["hero"]}"></div>'
                            f'<div class="info">{head}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p>'
                            f'<h4>Details</h4>{features_html(p["features"])}</div>{foot(n)}</section>')
            elif p["layout"] == "top":
                body.append(f'<section class="page top">{blobs([("soft", 140, 215, 120)])}'
                            f'<div class="hero"><img class="photo" src="images/{p["hero"]}" style="object-position:{p.get("pos", "center 25%")}"></div>'
                            f'<div class="info"><div class="l">{head}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
                            f'<div class="r">{features_html(p["features"])}</div></div>{foot(n)}</section>')
            else:
                models = "".join(f'<div class="tile"><img class="photo" src="images/{m}"></div>' for m in p["models"])
                details = "".join(f'<figure><div class="tile"><img class="photo" src="images/{img}"></div><figcaption>{escape(cap)}</figcaption></figure>'
                                  for img, cap in p["details"])
                body.append(f'<section class="page grid">{blobs([("soft", 150, -40, 100)])}'
                            f'<div class="head"><div class="l">{head}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
                            f'<div class="r">{features_html(p["features"])}</div></div>'
                            f'<div class="models">{models}</div><div class="details">{details}</div>{foot(n)}</section>')
            n += 1

    closing = (f'<section class="page closing">{blobs([("soft", 120, -50, 150), ("deep", -50, 200, 130)])}'
               f'<img class="logo" src="assets/logo-brown.png" alt="Furry Pooch">'
               f'<h1>Dress up your<br>furry family</h1>'
               f'<div class="qr"><img src="assets/instagram-qr.png" alt="Instagram QR for {HANDLE}"></div>'
               f'<div class="handle">Scan to follow &amp; message us on Instagram</div></section>')

    rows = "".join(
        f'<div class="toc-row"><div class="no">{ci:02d}</div><div class="meta"><h3>{escape(CATEGORIES[ci-1]["name"])}</h3>'
        f'<p>{escape(CATEGORIES[ci-1]["short"])} &middot; {len(CATEGORIES[ci-1]["products"])} design{"s" if len(CATEGORIES[ci-1]["products"]) != 1 else ""}</p></div>'
        f'<div class="thumbs">{"".join(f"<img src=images/{cover_img(p)}>" for p in CATEGORIES[ci-1]["products"][:3])}</div>'
        f'<div class="pg">p. {pg}</div></div>'
        for ci, pg in toc)
    contents = (f'<section class="page contents">{blobs([("soft", 130, -45, 140), ("deep", -40, 215, 110)])}'
                f'<span class="chip">Inside</span><h1>Our Collections</h1>'
                f'<p class="lead">Handpicked Indian festive wear for pets. Pick a collection, find your favourite, and message us to order.</p>'
                f'<div class="toc">{rows}</div>'
                f'<div class="cta"><h3>Found your favourite?</h3><p>Note its design code (like FP-K01) and message us on Instagram {HANDLE}.</p></div>{foot(2)}</section>')

    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Furry Pooch Catalogue</title>'
           '<link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="styles.css"></head><body>'
           + cover + contents + "".join(body) + closing + '</body></html>')
    open("catalogue.html", "w").write(doc)
    print(f"built catalogue.html: {n} pages")


if __name__ == "__main__":
    build()
