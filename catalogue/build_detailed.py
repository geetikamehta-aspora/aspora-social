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
            {
                "code": "FP-K06", "name": "Gulabi Patta Gota Kurta", "layout": "grid", "prefix": "gulabi-patta-kurta", "mosaic": True, "big_pos": "center 15%",
                "models": ["poodle", "pomeranian", "dachshund"],
                "details": [("ragdoll-cat", ""), ("front", "Front"), ("collar", "Gota-lace collar"), ("back", "Back")],
                "desc": "Bright pink with a bold red leaf print, edged in gold zig-zag gota lace along the collar, placket and sleeves.",
                "features": ["Pink base with red leaf print", "Gold gota lace on collar, placket and sleeves",
                             "Stand collar with centre placket", "Curved hem, easy leg openings"],
            },
            {
                "code": "FP-K07", "name": "Firoza Pocket Kurta", "layout": "grid", "prefix": "firoza-pocket-kurta",
                "models": ["shih-tzu", "dachshund", "ragdoll-cat", "tabby-cat", "persian-cat", "pomeranian"],
                "details": [("front", "Front"), ("pocket-flat", "Pocket"), ("back", "Back")],
                "desc": "A turquoise kurta alive with embroidered-print blooms in coral, pink and gold, with a little chest pocket and a red pocket square.",
                "features": ["Turquoise base with floral embroidery print", "Chest pocket with red pocket square",
                             "Stand collar, short sleeves", "Matching turquoise lining, curved hem"],
            },
            {
                "code": "FP-K08", "name": "Firoza Bloom Kurta", "layout": "grid", "prefix": "firoza-bloom-kurta",
                "models": ["shih-tzu", "ragdoll-cat", "golden-puppy", "tabby-cat", "pomeranian", "bengal-cat"],
                "details": [("front", "Front"), ("back", "Back"), ("maltese", "")],
                "desc": "The same turquoise garden in a button-placket cut, with gold-edged collar and sleeves. Shown on small and big pets alike.",
                "features": ["Turquoise base with coral, pink and gold blooms", "Gold-edged stand collar with placket",
                             "Short sleeves, turquoise lining", "Curved hem, easy leg openings"],
            },
        ],
    },
    {
        "name": "Sherwanis & Suits",
        "blurb": "Dapper sherwanis and tuxedo suits for the grand entrance.",
        "short": "Sherwanis & tuxedo suits",
        "products": [
            {
                "code": "FP-S01", "name": "Gulaal Sequin Sherwani", "layout": "grid", "prefix": "gulaal-sequin-sherwani",
                "details": [("front", "Front"), ("back", "Back"), ("collar", "Collar & buttons"), ("sleeve", "Sleeve")],
                "desc": "A dusty-rose sherwani sprinkled with gold sequin motifs, finished with a mandarin collar and covered buttons.",
                "features": ["Gold sequin-embroidered motifs all over", "Mandarin collar with covered buttons",
                             "Short sleeves, soft cream inner lining", "Curved hem for easy movement"],
            },
            {
                "code": "FP-S02", "name": "Pet Tuxedo Suit", "layout": "gallery", "cols": 12, "perks": False,
                "row_h": [88, 42, 46], "cover": "tuxedo-suit-m1.jpg",
                "photos": [("tuxedo-suit-hero", "", 12, 1),
                           ("tuxedo-suit-f1", "Black", 3, 1), ("tuxedo-suit-f2", "Gray", 3, 1), ("tuxedo-suit-f3", "Navy", 3, 1), ("tuxedo-suit-f4", "Back view", 3, 1),
                           ("tuxedo-suit-m1", "", 3, 1), ("tuxedo-suit-m2", "", 3, 1), ("tuxedo-suit-m3", "", 3, 1), ("tuxedo-suit-m4", "", 3, 1)],
                "desc": "A full tuxedo jacket with a white shirt front and a bow tie, in black, gray or navy. It fastens with Velcro, so it goes on in seconds. For dogs and cats.",
                "features": ["Black, gray or navy jacket", "White shirt front with button details", "Red or pink bow tie", "Velcro closure, easy to wear and adjust"],
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
            {
                "code": "FP-L04", "name": "Indradhanush Tutu Dress", "layout": "grid", "prefix": "rainbow-tutu-dress", "mosaic": True, "big_pos": "center 25%",
                "models": ["golden", "ragdoll", "golden-back"],
                "details": [("cat-back", "Back view"), ("rose", "Silver rose"), ("bow", "Satin bow"), ("tulle", "Tulle tiers")],
                "desc": "A rainbow of tulle, ruffled tier upon tier from butter-cream through pink to lilac, topped with a silver satin bib, glitter rose and a big bow.",
                "features": ["Layered tulle skirt in cream, pink and lilac", "Silver satin bib with a glitter rose",
                             "Big satin bow at the back", "Bandana-style neckline"],
            },
            {
                "code": "FP-L05", "name": "Lal Polka Bow Frock", "layout": "gallery", "cols": 3,
                "cover": "lal-polka-bow-frock-poodle.jpg",
                "photos": [("lal-polka-bow-frock-ragdoll", ""), ("lal-polka-bow-frock-poodle", ""), ("lal-polka-bow-frock-kitten", ""),
                           ("lal-polka-bow-frock-ragdoll-back", ""), ("lal-polka-bow-frock-poodle-back", ""), ("lal-polka-bow-frock-kitten-back", "")],
                "desc": "A cheerful red polka-dot twirl dress with a cream satin bow at the waist and a ruffled skirt. Small pets look extra cute in it.",
                "features": ["Red with white polka dots", "Cream satin bow at the waist", "Ruffled, gathered skirt", "Sleeveless, easy to wear"],
            },
            {
                "code": "FP-L06", "name": "Sherbet Stripe Bow Dress", "layout": "gallery", "cols": 3, "perks": False,
                "row_h": [108, 82], "cover": "sherbet-stripe-bow-dress-m2.jpg",
                "photos": [("sherbet-stripe-bow-dress-m1", ""), ("sherbet-stripe-bow-dress-m2", ""), ("sherbet-stripe-bow-dress-m3", ""), ("sherbet-stripe-bow-dress-spec", "", 3, 1)],
                "desc": "A summery pastel-striped seersucker-style dress in pink, peach and lemon, with a big orange satin bow and a tiered ruffle skirt.",
                "features": ["Pink, peach and lemon stripes", "Big orange satin bow", "Tiered ruffle skirt", "Buttons down the back"],
            },
            {
                "code": "FP-L07", "name": "Gulabi Phool Bow Dress", "layout": "gallery", "cols": 3, "perks": False,
                "row_h": [108, 82], "cover": "gulabi-phool-bow-dress-m2.jpg",
                "photos": [("gulabi-phool-bow-dress-m1", ""), ("gulabi-phool-bow-dress-m2", ""), ("gulabi-phool-bow-dress-m3", ""), ("gulabi-phool-bow-dress-spec", "", 3, 1)],
                "desc": "Little pink blossoms on white, with a big pink satin bow and a crystal centre. A sweet, swishy dress for spring days.",
                "features": ["Pink blossom print on white", "Pink satin bow with crystal centre", "Gathered, swishy skirt", "Buttons down the back"],
            },
            {
                "code": "FP-L08", "name": "Pista Phool Bow Dress", "layout": "gallery", "cols": 3, "perks": False,
                "row_h": [108, 82], "cover": "pista-phool-bow-dress-m2.jpg",
                "photos": [("pista-phool-bow-dress-m1", ""), ("pista-phool-bow-dress-m2", ""), ("pista-phool-bow-dress-m3", ""), ("pista-phool-bow-dress-spec", "", 3, 1)],
                "desc": "Soft mint and peach flowers on white, with a sunny yellow satin bow and a crystal centre. Fresh, light and pretty.",
                "features": ["Mint and peach floral print", "Yellow satin bow with crystal centre", "Gathered skirt, sleeveless", "Buttons down the back"],
            },
        ],
    },
    {
        "name": "Bows & Bandanas",
        "blurb": "Frilly, fancy neckwear that turns heads.",
        "short": "Lace collars, bows & bandanas",
        "products": [
            {
                "code": "FP-B01", "name": "Sailor Plaid Lace Collar", "layout": "grid", "prefix": "plaid-lace-collar", "mosaic": True, "big_pos": "center 30%",
                "models": ["hero", "cat-up", "cat-back"],
                "details": [("bow", "Anchor button"), ("flat-blue", "Sky blue"), ("flat-pink", "Rose pink")],
                "desc": "A soft plaid collar with a scalloped white lace edge and a plaid bow fastened with a gold anchor button. Ties at the back with a white ribbon.",
                "features": ["Plaid in sky blue or rose pink", "Scalloped white lace edge",
                             "Plaid bow with gold anchor button", "Soft white ribbon tie"],
            },
            {
                "code": "FP-B02", "name": "Pari Plaid Ruffle Bow Collar", "layout": "gallery", "cols": 2,
                "cover": "pari-plaid-ruffle-collar-blue-shih-tzu.jpg",
                "photos": [("pari-plaid-ruffle-collar-blue-shih-tzu", ""), ("pari-plaid-ruffle-collar-blue-ragdoll", ""),
                           ("pari-plaid-ruffle-collar-pink-shih-tzu", ""), ("pari-plaid-ruffle-collar-pink-ragdoll", "")],
                "desc": "A frilly double-layer lace ruffle in plaid, finished with a big plaid bow and a gold button. Looks sweet on dogs and cats alike.",
                "features": ["Plaid in sky blue or rose pink", "Double-layer white lace ruffle",
                             "Plaid bow with gold button", "Shown on a Shih Tzu and a Ragdoll cat"],
            },
            {
                "code": "FP-B03 / FP-B04", "name": "Satin & Velvet Bandanas", "layout": "twin",
                "cover": "pearl-satin-bandana-golden.jpg",
                "desc": "Two statement bandanas: a glossy pearl-silver one with a fabric rose, and a deep midnight one with a butterfly charm.",
                "variants": [
                    {"code": "FP-B03", "name": "Pearl Satin Rose Bandana", "photos": ["pearl-satin-bandana-golden", "pearl-satin-bandana-ragdoll"],
                     "features": ["Glossy pearl-silver satin", "Fabric rose at the corner", "Classic triangle bandana"]},
                    {"code": "FP-B04", "name": "Midnight Butterfly Bandana", "photos": ["velvet-butterfly-bandana-poodle", "velvet-butterfly-bandana-cat"],
                     "features": ["Deep midnight-green fabric", "Colourful butterfly charm", "Classic triangle bandana"]},
                ],
            },
            {
                "code": "FP-B05 / FP-B06", "name": "Satin Bow Ties", "layout": "twin",
                "cover": "satin-bow-tie-red-golden.jpg",
                "desc": "Sharp little bow ties for your gentleman or lady. Pick a bold red satin or a classic black polka dot.",
                "variants": [
                    {"code": "FP-B05", "name": "Red Satin Bow Tie", "photos": ["satin-bow-tie-red-golden", "satin-bow-tie-red-cat"],
                     "features": ["Shiny red satin", "Black centre knot", "Shown on a Golden Retriever and a cat"]},
                    {"code": "FP-B06", "name": "Polka-Dot Bow Tie", "photos": ["satin-bow-tie-polka-poodle", "satin-bow-tie-polka-cat"],
                     "features": ["Black with white polka dots", "Neat, structured bow", "Shown on a Poodle and a cat"]},
                ],
            },
            {
                "code": "FP-B07", "name": "Tuxedo Bow Tie", "layout": "top",
                "hero": "tuxedo-bow-tie-hero.jpg", "pos": "center 40%", "sticker": "Dapper<br>duo!",
                "desc": "A glossy black satin bow tie with a red centre knot. A tuxedo-style classic for every wedding, birthday and photo shoot.",
                "features": ["Black satin bow", "Red satin centre knot", "Sized for small dogs and cats", "Shown on a Maltese and a Ragdoll cat"],
            },
            {
                "code": "FP-B08", "name": "Pawty Neckties", "layout": "gallery", "cols": 3, "perks": False,
                "cover": "pawty-necktie-paw-poodle.jpg",
                "photos": [("pawty-necktie-paw-poodle", "Paw Party"), ("pawty-necktie-stripe-golden", "Classic Stripes"), ("pawty-necktie-corgi-corgi", "Corgi Cutie"),
                           ("pawty-necktie-paw-ragdoll", "Paw Party"), ("pawty-necktie-stripe-tabby", "Classic Stripes"), ("pawty-necktie-corgi-ginger-cat", "Corgi Cutie")],
                "desc": "Office-ready neckties with a fun twist. Three prints: colourful paws on black, navy and gold stripes, and little corgi faces on sky blue.",
                "features": ["Three prints to choose from", "Fits on a neat collar band", "Works for dogs and cats", "Matching look for the whole pack"],
            },
            {
                "code": "FP-B09", "name": "Tropical Bloom Bandana & Bow Tie Set", "layout": "gallery", "cols": 4, "perks": False,
                "row_h": [88, 52, 52], "cover": "bloom-bandana-set-m2.jpg",
                "photos": [("bloom-bandana-set-m1", ""), ("bloom-bandana-set-m2", ""), ("bloom-bandana-set-m3", ""), ("bloom-bandana-set-m4", ""),
                           ("bloom-bandana-set-flat", "", 3, 2), ("bloom-bandana-set-close1", ""), ("bloom-bandana-set-close2", "")],
                "desc": "A bold pink and black floral bandana with a bow tie on top. Choose a black or a red bow tie to match your pet's mood.",
                "features": ["Pink, black and white floral bandana", "Red or black bow tie included", "Bow tie on an adjustable strap", "Printed on both sides"],
            },
            {
                "code": "FP-B10", "name": "Tuxedo Bandana, Midnight Black", "layout": "gallery", "cols": 4, "perks": False,
                "row_h": [88, 52, 52], "cover": "tux-black-m2.jpg",
                "photos": [("tux-black-m1", ""), ("tux-black-m2", ""), ("tux-black-m3", ""), ("tux-black-m4", ""),
                           ("tux-black-flat", "", 3, 2), ("tux-black-c1", ""), ("tux-black-c2", "")],
                "desc": "Black-tie for pets: a black bandana with a crisp white shirt front, two buttons and a black bow tie, on a grey adjustable collar strap.",
                "features": ["Black bandana with white shirt front", "Two button details", "Black bow tie", "Grey strap with buckle and D-ring"],
            },
            {
                "code": "FP-B11", "name": "Tuxedo Bandana, Black & Red", "layout": "gallery", "cols": 4, "perks": False, "inset": 22,
                "row_h": [109, 50, 34], "cover": "tux-redblack-m1.jpg",
                "photos": [("tux-redblack-hero", "", 4, 1), ("tux-redblack-flats", "", 4, 1),
                           ("tux-redblack-m1", ""), ("tux-redblack-m2", ""), ("tux-redblack-m3", ""), ("tux-redblack-m4", "")],
                "desc": "The tuxedo bandana in two bold colourways: black with a red bow, and red with a black bow. For dogs and cats.",
                "features": ["Black with red bow, or red with black bow", "Soft and comfortable", "Adjustable neck strap", "Perfect for parties and photos"],
            },
            {
                "code": "FP-B12", "name": "Tuxedo Bandana, Sky Blue & Plaid", "layout": "gallery", "cols": 4, "perks": False, "inset": 22,
                "row_h": [116, 50, 36], "cover": "tux-blueplaid-m2.jpg",
                "photos": [("tux-blueplaid-hero", "", 4, 1), ("tux-blueplaid-flats", "", 4, 1),
                           ("tux-blueplaid-m1", ""), ("tux-blueplaid-m2", ""), ("tux-blueplaid-m3", ""), ("tux-blueplaid-m4", "")],
                "desc": "Notched-lapel tuxedo bandanas in sky blue with a pink gingham bow, red with a black bow, and grey plaid with a red bow.",
                "features": ["Sky blue with pink gingham bow", "Grey plaid with red bow", "Red with black bow", "Adjustable neck strap"],
            },
            {
                "code": "FP-B13", "name": "Classic Bow Tie Collar", "layout": "gallery", "cols": 12, "perks": False,
                "row_h": [112, 32, 52], "cover": "bowtie-collar-m1.jpg",
                "photos": [("bowtie-collar-hero", "", 12, 1),
                           ("bowtie-collar-d1", "Front view", 3, 1), ("bowtie-collar-d2", "Velcro fastening", 3, 1), ("bowtie-collar-d3", "Bow tie detail", 3, 1), ("bowtie-collar-d4", "Soft closure", 3, 1),
                           ("bowtie-collar-m1", "", 3, 1), ("bowtie-collar-m2", "", 3, 1), ("bowtie-collar-m3", "", 3, 1), ("bowtie-collar-m4", "", 3, 1)],
                "desc": "A crisp white shirt collar with a black bow tie, fastened with soft Velcro. The classic look for parties, weddings and photos.",
                "features": ["White collar with black bow tie", "Soft Velcro closure", "Adjustable neck strap", "For dogs and cats"],
            },
        ],
    },
    {
        "name": "Collars & Harnesses",
        "blurb": "Frilly bell collars, adventure-ready harnesses and a sturdy leash to finish the look.",
        "short": "Bell collars, harnesses & leash",
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
            {
                "code": "FP-A03", "name": "Orange Trail Harness for Dogs & Cats", "layout": "gallery", "cols": 2, "perks": False,
                "cover": "trail-harness-golden.jpg",
                "photos": [("trail-harness-golden", ""), ("trail-harness-cat", ""), ("trail-harness-flat-top", ""), ("trail-harness-flat-bottom", "")],
                "desc": "A lighter orange harness with a teal mesh chest panel, made to fit both dogs and cats. Easy to put on, hard to slip out of.",
                "features": ["Orange body with teal mesh panel", "Adjustable buckle straps", "Back ring for the leash clip", "Shown on a Golden Retriever and a cat"],
            },
            {
                "code": "FP-A04", "name": "Kitty Face Bell Collar", "layout": "gallery", "cols": 5, "perks": False,
                "row_h": [98, 98], "col_t": "repeat(4,1fr) 38mm", "cover": "kitty-collar-ginger-blue.jpg",
                "photos": [("kitty-collar-ragdoll-black", ""), ("kitty-collar-ginger-blue", ""), ("kitty-collar-tabby-green", ""), ("kitty-collar-calico-blue", ""),
                           ("kitty-collar-strip", "", 1, 2),
                           ("kitty-collar-ginger-black", ""), ("kitty-collar-tabby-blue", ""), ("kitty-collar-white-green", ""), ("kitty-collar-tuxedo-green", "")],
                "desc": "A slim printed collar with a cute cat-face buckle and a shiny bell, in three colours that suit every kind of kitty.",
                "features": ["Cat-face buckle", "Shiny jingle bell", "Three colours: grey-black, blue and lime green", "Printed webbing band"],
            },
            {
                "code": "FP-A05", "name": "Lime Mesh Comfort Harness", "layout": "gallery", "cols": 12, "perks": False, "inset": 22,
                "row_h": [115, 32, 55], "cover": "mesh-harness-hero.jpg",
                "photos": [("mesh-harness-hero", "", 12, 1), ("mesh-harness-strip", "", 12, 1),
                           ("mesh-harness-cat", "", 4, 1), ("mesh-harness-dog", "", 4, 1), ("mesh-harness-3d", "", 4, 1)],
                "desc": "A lightweight vest harness with breathable lime-green mesh, made for cats and small dogs. Easy to adjust, comfy to wear.",
                "features": ["Lightweight and comfortable", "Secure and adjustable straps", "Breathable mesh fabric", "Strong D-ring and secure buckle"],
            },
            {
                "code": "FP-A06", "name": "Premium Rope Leash", "layout": "gallery", "cols": 12, "perks": False, "inset": 22,
                "row_h": [84, 28, 24, 36], "cover": "rope-leash-hero.jpg",
                "photos": [("rope-leash-rolls", "", 4, 1), ("rope-leash-hero", "", 8, 1),
                           ("rope-leash-d1", "Soft foam handle", 3, 1), ("rope-leash-d2", "Reflective rope", 3, 1),
                           ("rope-leash-d3", "Heavy-duty hook", 3, 1), ("rope-leash-d4", "Reinforced joint", 3, 1),
                           ("rope-leash-colours", "", 12, 1), ("rope-leash-cat", "", 6, 1), ("rope-leash-dog", "", 6, 1)],
                "desc": "A strong braided rope leash with a padded foam handle and reflective threads for night walks. For cats and small to medium dogs.",
                "features": ["Strong and durable rope", "Comfortable foam handle", "Reflective design for night visibility", "360-degree rotating, rust-resistant metal hook"],
            },
            {
                "code": "FP-A07", "name": "Tactical Control-Handle Dog Collar", "layout": "gallery", "cols": 30, "perks": False,
                "row_h": [100, 30, 48], "cover": "tactical-collar-dog.jpg",
                "photos": [("tactical-collar-dog", "", 12, 1), ("tactical-collar-product", "", 18, 1),
                           ("tactical-collar-d1", "Buckle lock", 6, 1), ("tactical-collar-d2", "Control handle", 6, 1), ("tactical-collar-d3", "D-ring", 6, 1),
                           ("tactical-collar-d4", "Padding", 6, 1), ("tactical-collar-d5", "Adjustable", 6, 1),
                           ("tactical-collar-use1", "", 10, 1), ("tactical-collar-use2", "", 10, 1), ("tactical-collar-use3", "", 10, 1)],
                "desc": "A tough black nylon training collar with a padded inner layer and a control handle for a better grip. Built for training, walks and outdoor adventures.",
                "features": ["Strong, durable nylon", "Control handle for better grip", "Secure buckle lock and sturdy D-ring", "Soft, breathable padding, adjustable fit"],
            },
        ],
    },
    {
        "name": "Cool Shades",
        "blurb": "Retro round sunglasses in four juicy colours.",
        "short": "Retro round sunglasses",
        "products": [
            {
                "code": "FP-X01", "name": "Retro Round Sunglasses", "layout": "gallery", "cols": 4, "perks": False,
                "cover": "retro-sunglasses-yellow-golden.jpg",
                "photos": [(f"retro-sunglasses-{c}-{k}", (c.title() if k == "flat" else "")) for c in ("yellow", "purple", "black", "red") for k in ("shih-tzu", "cat", "golden", "flat")],
                "desc": "Gold-rimmed round shades with tinted lenses, in four colours. Cool enough for the beach, the festival or the photo shoot.",
                "features": ["Round gold-tone metal frame", "Yellow, purple, black and red lenses", "Shown on a Shih Tzu, a cat and a Golden Retriever"],
            },
        ],
    },
    {
        "name": "Care & Grooming",
        "blurb": "Everyday essentials for tidy paws.",
        "short": "Nail clipper set",
        "products": [
            {
                "code": "FP-C01", "name": "Pet Nail Clipper Set", "layout": "gallery", "cols": 30, "perks": False,
                "row_h": [118, 30, 40], "cover": "nail-clipper-pets.jpg",
                "photos": [("nail-clipper-pets", "", 17, 1), ("nail-clipper-product", "", 13, 1),
                           ("nail-clipper-d1", "Steel blades", 6, 1), ("nail-clipper-d2", "Strong spring", 6, 1), ("nail-clipper-d3", "Non-slip handle", 6, 1),
                           ("nail-clipper-d4", "Safety lock", 6, 1), ("nail-clipper-d5", "Nail file", 6, 1),
                           ("nail-clipper-use1", "For dogs", 10, 1), ("nail-clipper-use2", "For cats", 10, 1), ("nail-clipper-use3", "Smooth finish", 10, 1)],
                "desc": "A nail clipper with sharp stainless steel blades, a safety lock and a non-slip handle, plus a nail file. For dogs, cats and small animals.",
                "features": ["Sharp, durable stainless steel blades", "Strong spring for smooth use", "Non-slip ergonomic handle", "Safety lock and nail file included"],
            },
        ],
    },
    {
        "name": "Pet Tees",
        "blurb": "Easy everyday tops.",
        "short": "Printed tees",
        "products": [
            {
                "code": "FP-T01", "name": "Dungaree-Print Pet Tee", "layout": "gallery", "cols": 1, "perks": False, "inset": 50,
                "row_h": [150], "cover": "overalls-tee-cat.jpg",
                "photos": [("overalls-tee-cat", "")],
                "desc": "A white sleeveless tee with a fun printed dungaree design, gold buckles and a front pocket. Simple, cute and easy for every day.",
                "features": ["White tee with dungaree print", "Gold buckle and pocket graphics", "Sleeveless, easy to slip on"],
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
    return f'{p["prefix"]}-{p.get("models", MODELS)[0]}.jpg'


def nprod(cat):
    return sum(len(p.get("variants", [0])) for p in cat["products"])


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
            f'<div class="pill">Our Collection</div>'
            f'<div class="sub">Clothes &amp; Accessories</div>'
            f'{trail(walk, 8.5, "purple")}<div class="stage"><img src="images/cover-stage.jpg" alt=""></div></section>')


def page_contents(toc, n):
    rows = "".join(
        f'<div class="toc-row"><div class="no">{ci:02d}</div><div class="meta"><h3>{escape(CATEGORIES[ci-1]["name"])}</h3>'
        f'<p>{escape(CATEGORIES[ci-1]["short"])} &middot; {count_label(nprod(CATEGORIES[ci-1]))}</p></div>'
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
            f'<div class="count"><span class="chip ghost">{count_label(nprod(cat))}</span></div></div>'
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
    mosaic = bool(p.get("mosaic"))
    models = "".join(
        f'<div class="tile"><img class="photo" src="images/{pre}-{m}.jpg"'
        + (f' style="object-position:{p.get("big_pos", "center 20%")}"' if mosaic and k == 0 else "") + '></div>'
        for k, m in enumerate(p.get("models", MODELS)))
    details = "".join(f'<figure><div class="tile"><img class="photo" src="images/{pre}-{s}.jpg"></div>' + (f'<figcaption>{escape(c)}</figcaption>' if c else "") + '</figure>'
                      for s, c in p["details"])
    size = ""
    if p.get("sizes"):
        size = '<div class="size-pill">SIZES ' + "".join(f"<b>{s}</b>" for s in p["sizes"]) + "</div>"
    blob = [("soft", 150, -40, 100)] if idx % 2 == 0 else [("soft", -40, -50, 100)]
    return (f'<section class="page grid{" alt" if idx % 2 else ""}">{blobs(blob)}'
            f'{paw(190 if idx % 2 == 0 else 8, 3, 10, 15, "purple")}'
            f'<div class="head"><div class="l">{head_html(cat, p)}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
            f'<div class="r">{features_html(p["features"])}{size}</div></div>'
            f'{perks_html()}<div class="models{" mosaic" if mosaic else ""}">{models}</div>'
            f'<div class="details" style="grid-template-columns:repeat({len(p["details"])},1fr)">{details}</div>{foot(n)}</section>')


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


def page_gallery(cat, p, n, idx):
    cols = p.get("cols", 3)
    top = 62 if not p.get("perks", True) else 74
    row_h = p.get("row_h")
    if row_h:
        tmpl_rows = " ".join(f"{h}mm" for h in row_h)
        tmpl_cols = p.get("col_t", f"repeat({cols},1fr)")
        h_style = ""
    else:
        rows = -(-len(p["photos"]) // cols)
        h = (272 - top - (rows - 1) * 4) / rows
        tmpl_rows = ""
        tmpl_cols = f"repeat({cols},1fr)"
        h_style = f"height:{h:.1f}mm;"
    tiles = ""
    for k, ph in enumerate(p["photos"]):
        f, c = ph[0], ph[1]
        cs, rs = (ph[2], ph[3]) if len(ph) > 2 else (1, 1)
        rot = 0 if (cs > 1 or rs > 1) else (-.5 if k % 2 == 0 else .5) * (1 if cols < 4 else .5)
        span = f"grid-column:span {cs};grid-row:span {rs};" if (cs > 1 or rs > 1) else ""
        tiles += (f'<div class="tile" style="{h_style}{span}transform:rotate({rot}deg)">'
                  f'<img class="photo" src="images/{f}.jpg">' + (f'<span class="cap">{escape(c)}</span>' if c else "") + '</div>')
    perks = perks_html(58) if p.get("perks", True) else ""
    blob = [("soft", 150, -40, 100)] if idx % 2 == 0 else [("soft", -40, -50, 100)]
    rows_css = f"grid-template-rows:{tmpl_rows};" if tmpl_rows else ""
    return (f'<section class="page grid gal">{blobs(blob)}{paw(190 if idx % 2 == 0 else 8, 3, 10, 15, "purple")}'
            f'<div class="head"><div class="l">{head_html(cat, p)}<h1>{escape(p["name"])}</h1><p class="desc">{escape(p["desc"])}</p></div>'
            f'<div class="r">{features_html(p["features"])}</div></div>{perks}'
            f'<div class="gtiles" style="top:{top}mm;left:{p.get("inset", 12)}mm;right:{p.get("inset", 12)}mm;grid-template-columns:{tmpl_cols};{rows_css}">{tiles}</div>{foot(n)}</section>')


def page_twin(cat, p, n):
    cols = ""
    for v in p["variants"]:
        ph = "".join(f'<div class="tile"><img class="photo" src="images/{f}.jpg"></div>' for f in v["photos"])
        cols += (f'<div class="vcol"><div class="vhead"><span class="code">{v["code"]}</span><h2>{escape(v["name"])}</h2></div>'
                 f'<div class="vphotos">{ph}</div>{features_html(v["features"])}</div>')
    return (f'<section class="page grid twin">{blobs([("soft", 150, -40, 100), ("deep", -40, 240, 90)])}{paw(190, 3, 10, 15, "purple")}'
            f'<div class="head"><div class="l"><span class="chip">{escape(cat["name"])}</span><h1>{escape(p["name"])}</h1>'
            f'<p class="desc">{escape(p["desc"])}</p></div></div><div class="vcols">{cols}</div>{foot(n)}</section>')


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
                       else page_gallery(cat, p, n, n) if lay == "gallery" else page_twin(cat, p, n) if lay == "twin"
                       else page_trio(cat, p, n) if lay == "trio" else page_grid(cat, p, n, n))
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Furry Pooch Catalogue</title>'
           '<link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="styles.css"></head><body>'
           + "".join(out) + '</body></html>')
    open("catalogue-detailed.html", "w").write(doc)
    print(f"built catalogue-detailed.html: {len(plan)} pages")


if __name__ == "__main__":
    build()
