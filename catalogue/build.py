"""Compact catalogue: two products per page, one or two photos each, codes FP01, FP02, ...

Add a product: append a P(...) line to the right category in CATEGORIES, drop its photos in images/,
then run `python3 build.py && node render.mjs`. Codes are assigned automatically in order.
The long 49-page version lives in build_detailed.py (`python3 build_detailed.py && node render.mjs --detailed`).
"""
import os
from html import escape
from build_detailed import (HANDLE, CONTACT_NAME, PAW, paw, foot, blobs, sticker, perks_html, trail,
                            page_cover, page_closing)


def P(name, desc, pts, *imgs):
    """imgs: file name, or (file name, css object-position)."""
    return {"name": name, "desc": desc, "pts": pts, "imgs": [i if isinstance(i, tuple) else (i, "center 25%") for i in imgs]}


def tile_size(img):
    """(width, height) in mm of the main photo tile; 4th/3rd tuple items override the 110 x 128 default."""
    return (img[2], img[3]) if len(img) > 3 else (110, 128)


CATEGORIES = [
    ("Pet Kurtas", "Embroidered, mirror-work & multi-print kurtas", [
        P("Phool Bagh Floral Kurta", "Aqua-teal kurta with coral, pink and gold floral embroidery.",
          ["Floral embroidery all over", "Gold thread on collar and sleeves", "Stand collar, short sleeves"], ("teal-floral-kurta.jpg", "center 22%"), "teal-kurta-detail.jpg"),
        P("Aasmani Mirror-Work Kurta", "Sky-blue kurta with gold stars and hand-finished mirror borders.",
          ["Mirror, sequin and thread borders", "Mandarin collar, centre placket", "Flared sleeves, embroidered cuffs"], "sky-golden-retriever.jpg", "sky-flatlay-front.jpg"),
        P("Rangeela Jacket Kurta Set", "A multi-print ethnic jacket layered over a hot-pink kurta.",
          ["Patchwork floral and paisley jacket", "Gold-lace striped sleeves", "Sizes XS to XL"], "rangeela-kurta-set-golden-retriever.jpg", "rangeela-kurta-set-front.jpg"),
        P("Haldi Silver-Lace Kurta", "Sunny haldi-yellow kurta trimmed with silver zari lace.",
          ["Silver lace on collar and cuffs", "Stand collar, centre placket", "Curved hem"], "haldi-silver-lace-kurta-golden-retriever.jpg", "haldi-silver-lace-kurta-front.jpg"),
        P("Phoolwari Pocket Kurta", "Sky-blue floral and paisley kurta with a mustard pocket square.",
          ["Floral and paisley print", "Chest pocket and pocket square", "Soft blue lining"], "phoolwari-pocket-kurta-golden-retriever.jpg", "phoolwari-pocket-kurta-front.jpg"),
        P("Gulabi Patta Gota Kurta", "Bright pink kurta with a red leaf print and gold gota lace.",
          ["Red leaf print on pink", "Gold gota lace trim", "Stand collar, centre placket"], "gulabi-patta-kurta-poodle.jpg", "gulabi-patta-kurta-front.jpg"),
        P("Sindoori Zari Jaal Kurta", "Red sleeveless kurta with all-over gold jaal embroidery and sequin lace trim.",
          ["Gold jaal embroidery", "Beaded lace on collar and armholes", "Sleeveless, curved hem"], ("rz-hero.jpg", "center", 110, 97), "rz-flat.jpg"),
        P("Sarson Block-Print Kurta", "Mustard-yellow short-sleeve kurta with a cream paisley block print.",
          ["Cream block print", "Short sleeves", "Stand collar, easy fit"], ("mk-hero.jpg", "center", 110, 102), "mk-flat.jpg"),
    ]),
    ("Sherwanis & Suits", "Sherwanis & tuxedo suits", [
        P("Gulaal Sequin Sherwani", "Dusty-rose sherwani sprinkled with gold sequin motifs.",
          ["Gold sequin motifs all over", "Mandarin collar, covered buttons", "Soft cream lining"], "gulaal-sequin-sherwani-golden-retriever.jpg", "gulaal-sequin-sherwani-front.jpg"),
        P("Pet Tuxedo Suit", "Tuxedo jacket with a white shirt front and bow tie, for dogs and cats.",
          ["Black, gray or navy", "Red or pink bow tie", "Easy Velcro closure"], "tuxedo-suit-m1.jpg", "tuxedo-suit-f1.jpg"),
    ]),
    ("Pet Jackets", "Brocade jackets", [
        P("Gulabi Brocade Zip Jacket", "Pink and gold paisley brocade jacket with a front zip.",
          ["Front zip closure", "Chest pocket with pocket square", "Soft pink lining"], "gulabi-brocade-jacket-golden-retriever.jpg", "gulabi-brocade-jacket-front.jpg"),
    ]),
    ("Pet Lehengas & Frocks", "Festive lehenga dresses & frocks", [
        P("Lal Pari Bow Frock", "Red party frock with gold motifs, a waist bow and golden tassels.",
          ["Gold-lace hem", "Waist bow with golden tassels", "Sleeveless, gathered skirt"], "lal-pari-bow-frock-golden-retriever.jpg", "lal-pari-bow-frock-front.jpg"),
        P("Jamuni Double-Layer Frock", "Deep-purple twirl dress with two ruffled tiers and gold lace.",
          ["Gold gota lace trim", "Chevron bodice, tie-up neck", "Double-layer ruffle skirt"], "jamuni-frock-golden-retriever.jpg", "jamuni-frock-front.jpg"),
        P("Indradhanush Tutu Dress", "Rainbow tulle tiers with a silver satin bib, rose and bow.",
          ["Layered tulle skirt", "Silver satin bib, glitter rose", "Big satin bow at the back"], "rainbow-tutu-dress-golden.jpg", "rainbow-tutu-dress-rose.jpg"),
        P("Lal Polka Bow Frock", "Red polka-dot twirl dress with a cream satin bow.",
          ["Cream satin waist bow", "Ruffled, gathered skirt", "Sleeveless, easy to wear"], "lal-polka-bow-frock-poodle.jpg", "lal-polka-bow-frock-ragdoll.jpg"),
        P("Sherbet Stripe Bow Dress", "Pastel-striped dress with a big orange satin bow.",
          ["Pink, peach and lemon stripes", "Tiered ruffle skirt", "Buttons down the back"], "sherbet-stripe-bow-dress-m2.jpg", "sherbet-stripe-bow-dress-m3.jpg"),
        P("Gulabi Phool Bow Dress", "Pink blossoms on white with a satin bow and crystal centre.",
          ["Pink satin bow", "Gathered, swishy skirt", "Buttons down the back"], "gulabi-phool-bow-dress-m2.jpg", "gulabi-phool-bow-dress-m3.jpg"),
        P("Pista Phool Bow Dress", "Mint and peach flowers with a sunny yellow satin bow.",
          ["Yellow bow with crystal centre", "Gathered skirt, sleeveless", "Buttons down the back"], "pista-phool-bow-dress-m2.jpg", "pista-phool-bow-dress-m3.jpg"),
    ]),
    ("Bows & Bandanas", "Lace collars, bows, ties & bandanas", [
        P("Sailor Plaid Lace Collar", "Plaid collar with scalloped white lace and a gold anchor button.",
          ["Sky blue or rose pink", "Scalloped lace edge", "Soft white ribbon tie"], ("plaid-lace-collar-hero.jpg", "center 30%"), "plaid-lace-collar-flat-pink.jpg"),
        P("Pearl Satin Rose Bandana", "Glossy pearl-silver satin bandana with a fabric rose.",
          ["Pearl-silver satin", "Fabric rose at the corner", "Classic triangle shape"], "pearl-satin-bandana-golden.jpg", "pearl-satin-bandana-ragdoll.jpg"),
        P("Midnight Butterfly Bandana", "Deep midnight bandana with a colourful butterfly charm.",
          ["Midnight-green fabric", "Colourful butterfly charm", "Classic triangle shape"], "velvet-butterfly-bandana-poodle.jpg", "velvet-butterfly-bandana-cat.jpg"),
        P("Red Satin Bow Tie", "Shiny red satin bow tie with a black centre knot.",
          ["Shiny red satin", "Black centre knot", "For dogs and cats"], "satin-bow-tie-red-golden.jpg", "satin-bow-tie-red-cat.jpg"),
        P("Polka-Dot Bow Tie", "Black bow tie with crisp white polka dots.",
          ["Black with white dots", "Neat, structured bow", "For dogs and cats"], "satin-bow-tie-polka-poodle.jpg", "satin-bow-tie-polka-cat.jpg"),
        P("Tuxedo Bow Tie", "Glossy black satin bow tie with a red centre knot.",
          ["Black satin bow", "Red satin centre knot", "Made for weddings and photo shoots"], ("tuxedo-bow-tie-hero.jpg", "center 40%"), "tuxedo-bow-detail.jpg"),
        P("Pawty Neckties", "Fun neckties in paw, stripe and corgi prints.",
          ["Three prints to pick from", "Neat collar band", "For dogs and cats"], "pawty-necktie-paw-poodle.jpg", "pawty-necktie-stripe-golden.jpg"),
        P("Tropical Bloom Bandana & Bow Tie Set", "Pink and black floral bandana with a red or black bow tie.",
          ["Red or black bow tie", "Adjustable bow-tie strap", "Printed on both sides"], "bloom-bandana-set-m2.jpg", "bloom-bandana-set-flat.jpg"),
        P("Tuxedo Bandana, Midnight Black", "Black bandana with a white shirt front and black bow tie.",
          ["Two button details", "Black bow tie", "Grey adjustable strap"], "tux-black-m2.jpg", "tux-black-flat.jpg"),
        P("Tuxedo Bandana, Black & Red", "A tuxedo bandana in black with a red bow, or red with a black bow.",
          ["Soft and comfortable", "Adjustable neck strap", "Party and photo ready"], "tux-redblack-m1.jpg", "tux-redblack-m2.jpg"),
        P("Tuxedo Bandana, Sky Blue & Plaid", "Notched-lapel tuxedo bandanas in sky blue, red and grey plaid.",
          ["Sky blue with pink gingham bow", "Grey plaid with red bow", "Adjustable neck strap"], "tux-blueplaid-m1.jpg", "tux-blueplaid-m2.jpg"),
        P("Classic Bow Tie Collar", "White shirt collar with a black bow tie and soft Velcro.",
          ["Soft Velcro closure", "Adjustable neck strap", "For dogs and cats"], "bowtie-collar-m1.jpg", "bowtie-collar-d1.jpg"),
        P("Lal Jaali Bow Bandana", "Crimson quilted-look bandana with tiny gold flowers and a big matching bow.",
          ["Elegant festive design", "Gold flower motifs", "Big bow at the corner"], ("bdn-crimson-cat.jpg", "center", 110, 121), "bdn-crimson-swatch.jpg"),
        P("Gulabi Sheesha Bow Bandana", "Pink embroidered bandana with mirror work and a gold-edged bow.",
          ["Intricate embroidered look", "Mirror and sequin lines", "Matching embroidered bow"], ("bdn-pink-cat.jpg", "center", 110, 121), "bdn-pink-swatch.jpg"),
        P("Haldi Sitara Bow Bandana", "Sunny yellow bandana with sequin flowers, silver lace edge and a bow.",
          ["Sequin flower detailing", "Silver lace border", "Matching bow"], ("bdn-haldi-hero.jpg", "center", 90, 128), "bdn-haldi-flat.jpg"),
        P("Zamrud Gota Bow Bandana", "Deep emerald bandana trimmed with gold gota lace and a lace-edged bow.",
          ["Gold gota lace edge", "Matching emerald bow", "Rich festive green"], ("bdn-green-hero.jpg", "center", 92, 128), "bdn-green-flat.jpg"),
        P("Kaali Phool Bow Bandana", "Black bandana with a tiny floral print, gold lace edge and a jewelled bow.",
          ["Small floral and diamond print", "Gold lace border", "Jewelled centre on the bow"], ("bdn-black-cat.jpg", "center", 108, 128), "bdn-black-flat.jpg"),
        P("Sunehri Frill Bandana", "Gold brocade bandana with a ruffled edge and two pearl buttons.",
          ["Gold brocade fabric", "Ruffled edge", "Two pearl-button details"], ("bdn-gold-cat.jpg", "center", 108, 128), "bdn-gold-flat.jpg"),
        P("Kesari Stripe Bow Bandana", "Saffron-orange bandana with gold-lace stripes and a big satin bow.",
          ["Gold-lace stripes", "Big orange bow", "Bright festive colour"], ("bdn-orange-cat.jpg", "center", 108, 128), "bdn-orange-flat.jpg"),
        P("Neela Paisley Bow Bandana", "Navy paisley bandana with gold lace trim and a jewelled bow.",
          ["Multicolour paisley print", "Gold lace trim", "Jewelled centre on the bow"], ("bdn-navy-cat.jpg", "center", 108, 128), "bdn-navy-flat.jpg"),
    ]),
    ("Collars & Harnesses", "Collars, harnesses & leash", [
        P("Ruffle Bell Collar", "Frilly polka-dot ribbon ruffles with a snap buckle and jingle bell.",
          ["Five colours", "Snap-buckle closure", "Jingle-bell charm"], ("collar-full.jpg", "center", 110, 84), "collar-swatch-hotpink.jpg"),
        P("Orange Adventure Dog Harness", "Bright orange harness with a breathable teal mesh panel.",
          ["Adjustable buckle straps", "Top D-ring for the leash", "Grey contrast piping"], "harness-front.jpg", "harness-side.jpg"),
        P("Kitty Face Bell Collar", "Slim printed collar with a cat-face buckle and a shiny bell.",
          ["Grey-black, blue or lime green", "Cat-face buckle", "Jingle bell"], ("kitty-collar-composite.jpg", "center", 110, 128), "kitty-collar-white-green.jpg"),
        P("Lime Mesh Comfort Harness", "Lightweight lime-green mesh vest harness for cats and small dogs.",
          ["Breathable mesh fabric", "Secure, adjustable straps", "Strong D-ring and buckle"], "mesh-harness-cat.jpg", "mesh-harness-3d.jpg"),
        P("Premium Rope Leash", "Braided rope leash with a foam handle and reflective threads.",
          ["Reflective for night walks", "360-degree rotating hook", "Ten colours"], "rope-leash-hero.jpg", "rope-leash-rolls.jpg"),
        P("Tactical Control-Handle Dog Collar", "Black nylon training collar with a padded inner and control handle.",
          ["Secure buckle lock and D-ring", "Soft, breathable padding", "Adjustable fit"], "tactical-collar-dog.jpg", "tactical-collar-product.jpg"),
        P("Teddy Bear Tweed Harness", "Grey tweed vest harness with cream trim and a cute teddy-bear patch.",
          ["Teddy-bear patch with D-ring", "Soft tweed with cream piping", "Adjustable buckle straps"], ("th-hero.jpg", "center", 110, 104), "th-flat.jpg"),
        P("Reflective Mesh Harness with Leash", "Black mesh harness with orange panels, reflective strips and a matching leash.",
          ["Reflective strips", "Breathable black mesh", "Leash comes with its own pouch"], ("bo-hero.jpg", "center", 90, 128), "bo-flat.jpg"),
    ]),
    ("Shades & Headbands", "Sunglasses & festive headbands", [
        P("Retro Round Sunglasses", "Gold-rimmed round shades in yellow, purple, black and red.",
          ["Four lens colours", "Gold-tone metal frame", "For dogs and cats"], "retro-sunglasses-yellow-golden.jpg", "retro-sunglasses-red-cat.jpg"),
        P("Santa Headband", "Red headband with two springy Santa toppers, for Christmas.",
          ["Two bobbing Santa faces", "Soft red band", "Christmas parties and photos"], ("hb-corgi.jpg", "center", 110, 114), "hb-santa-flat.jpg"),
        P("Reindeer Headband", "Red headband with glittery red antlers, gold ears and holly berries.",
          ["Glitter antlers", "Shimmery gold ears", "Holly and berry detail"], ("hb-cat.jpg", "center", 110, 86), "hb-reindeer-flat.jpg"),
    ]),
    ("Care & Grooming", "Nail clipper set", [
        P("Pet Nail Clipper Set", "Stainless steel clipper with a safety lock and a nail file.",
          ["Non-slip ergonomic handle", "Strong spring for smooth use", "Dogs, cats and small animals"], ("nail-clipper-product.jpg", "center", 92, 128), "nail-clipper-pets.jpg"),
    ]),
    ("Pet Tees", "Printed tees", [
        P("Dungaree-Print Pet Tee", "White sleeveless tee with a printed dungaree design.",
          ["Gold buckle prints", "Front pocket graphic", "Easy to slip on"], "overalls-tee-cat.jpg", "tee-print-detail.jpg"),
        P("Elephant Pet T-Shirt", "Soft white tee with a hand-painted elephant wearing a purple bow.",
          ["Soft, breathable fabric", "Easy to wash and durable", "Comfortable neck, stretchy fit"], ("tshirt-elephant-pets.jpg", "center", 110, 106), "tshirt-elephant-front.jpg"),
    ]),
]


def page_pets(n):
    """Intro page: six different designs (no repeats), clothes and accessories, dogs and cats."""
    pics = [("rangeela-kurta-set-golden-retriever", 12, 76, "center 20%"), ("gulabi-brocade-jacket-ragdoll-cat", 77, 88, "center 20%"),
            ("gulaal-sequin-sherwani-pomeranian", 142, 76, "center 20%"), ("tux-black-m2", 12, 148, "center 20%"),
            ("mesh-harness-cat", 77, 160, "center 20%"), ("retro-sunglasses-yellow-golden", 142, 148, "center 25%")]
    circles = "".join(f'<div class="circle" style="left:{x}mm;top:{y}mm;width:56mm;height:56mm"><img src="images/{f}.jpg" style="object-position:{pos}"></div>'
                      for f, x, y, pos in pics)
    return (f'<section class="page purple pets">{blobs([("psoft", 120, -50, 150), ("pdeep", -50, 180, 130)])}'
            f'{paw(10, 12, 12, -14, "sun")}{paw(192, 56, 9, 20, "sun")}'
            f'<h1>Dogs. Cats.<br>Everyone&rsquo;s invited!</h1>'
            f'<p class="lead">Kurtas, sherwanis, jackets, tuxedo bandanas, harnesses and shades &mdash; something stylish for every furry family member.</p>'
            f'{circles}{sticker("Woof!", 2, 70, 26, -14, "round sun")}{sticker("Meow!", 118, 136, 26, 12, "round sun")}'
            f'{perks_html(228)}{trail([(22 + i * 22, 252) for i in range(8)], 8, "sun", 90, .9)}{foot(n, True)}</section>')


def block(cat, p, code, flip, top):
    imgs = p["imgs"]
    w, h = tile_size(imgs[0])
    ins = (f'<div class="insetimg"><img src="images/{imgs[1][0]}" style="object-position:{imgs[1][1]}"></div>' if len(imgs) > 1 else "")
    main = (f'<div class="tilewrap" style="width:{w}mm;height:{h}mm"><div class="mainimg"><img src="images/{imgs[0][0]}" style="object-position:{imgs[0][1]}"></div>'
            f'{ins}<div class="codebadge">{code}</div></div>')
    pts = "".join(f"<li>{PAW}<span>{escape(t)}</span></li>" for t in p["pts"])
    return (f'<div class="blk{" flip" if flip else ""}" style="top:{top}mm"><div class="imgs">{main}</div>'
            f'<div class="txt"><span class="chip">{escape(cat)}</span><h2>{escape(p["name"])}</h2>'
            f'<p class="desc">{escape(p["desc"])}</p><ul class="features">{pts}</ul></div></div>')


def page_products(items, n):
    tops = (11, 149) if len(items) == 2 else (84,)
    b = "".join(block(cat, p, code, i == 1, tops[i]) for i, (cat, p, code) in enumerate(items))
    pos = [[("soft", 150, -40, 100)], [("soft", -40, -50, 100)]][n % 2]
    return f'<section class="page prod">{blobs(pos + [("deep", -40, 250, 80)])}{b}{foot(n)}</section>'


def page_contents(rows, n):
    r = "".join(
        f'<div class="toc-row"><div class="no">{i:02d}</div><div class="meta"><h3>{escape(name)}</h3>'
        f'<p>{escape(short)} &middot; {first}{"-" + last if first != last else ""}</p></div>'
        f'<div class="thumbs">{"".join(f"<img src=images/{im}>" for im in thumbs)}</div><div class="pg">p. {pg}</div></div>'
        for i, (name, short, first, last, pg, thumbs) in enumerate(rows, 1))
    return (f'<section class="page contents">{blobs([("soft", 130, -45, 140), ("deep", -40, 215, 110)])}{paw(158, 14, 13, 14, "purple")}{paw(176, 30, 10, -10, "purple")}'
            f'<span class="chip">Inside</span><h1>Our Collections</h1>'
            f'<p class="lead">Handpicked festive wear and accessories for pets. Find your favourite, note its code (like FP07) and message us to order.</p>'
            f'<div class="toc">{r}</div>'
            f'<div class="cta"><h3>Found your favourite?</h3><p>Send us its code, for example FP07, and message {CONTACT_NAME} on Instagram {HANDLE}.</p></div>{foot(n)}</section>')


def build():
    flat = []          # (category, product, code)
    spans = []         # per category: name, short, first code, last code, indexes
    for name, short, prods in CATEGORIES:
        start = len(flat)
        for p in prods:
            for im, *_ in p["imgs"]:
                assert os.path.exists(f"images/{im}"), im
            flat.append((name, p, f"FP{len(flat) + 1:02d}"))
        spans.append((name, short, start, len(flat) - 1))
    first_page = 4
    pages = []
    for k in range(0, len(flat), 2):
        pages.append(page_products(flat[k:k + 2], first_page + k // 2))
    rows = []
    for name, short, a, z in spans:
        rows.append((name, short, flat[a][2], flat[z][2], first_page + a // 2 if a % 2 == 0 else first_page + a // 2,
                     [flat[j][1]["imgs"][0][0] for j in range(a, min(z + 1, a + 3))]))
    # page range text
    rows = [(n, s, f, l, f"{first_page + a // 2}" + (f"-{first_page + z // 2}" if a // 2 != z // 2 else ""), t)
            for (n, s, f, l, _, t), (_, _, a, z) in zip(rows, spans)]
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Furry Pooch Catalogue</title>'
           '<link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="styles.css"></head><body>'
           + page_cover() + page_contents(rows, 2) + page_pets(3) + "".join(pages) + page_closing() + '</body></html>')
    open("catalogue.html", "w").write(doc)
    print(f"built catalogue.html: {len(flat)} products, {3 + len(pages) + 1} pages")


if __name__ == "__main__":
    build()
