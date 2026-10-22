# Furry Pooch website

A static, zero-dependency site (HTML, CSS, vanilla JS) built around the Furry Pooch "Festive Edit" catalogue. Open `index.html` in a browser, or serve the folder:

```
npx http-server furry-pooch
```

## What's inside
- `index.html` — hero, collections index, shop grid (FP01–FP60), lookbook, how to order, about (business card), boop-the-dog, order helper, footer
- `products.js` — all catalogue data: names, descriptions, highlights, collections, lookbook. Edit or add products here.
- `styles.css` — brand tokens at the top (`--sun`, `--choc`, `--indigo` …) taken from the logo and business card
- `main.js` — paw cursor and trail, click effects, scroll reveals, marquee, filters and search, product quick view, My picks drawer, lookbook, order helper
- `assets/products/FPxx.webp` (main photo) and `FPxx-b.webp` (flat-lay or detail), `assets/lookbook/` collages (10 looks)

## How ordering works
There is no checkout and no prices, matching the catalogue. Visitors save styles to **My picks**, then the order helper writes a message listing the codes. They copy it into an Instagram DM to @furry.pooch (Instagram cannot pre-fill a message), or send it on WhatsApp to +91 99407 27027.

## Editing
- Phone, email and Instagram are in the contact section of `index.html`; `PHONE` is at the top of `main.js`.
- To add a product, add a line to `FP_PRODUCTS` in `products.js` and drop `FPxx.webp` and `FPxx-b.webp` into `assets/products/`.
- Fonts (Bagel Fat One, Outfit, Gaegu) load from Google Fonts.
- Touch devices get tap effects but no custom cursor. `prefers-reduced-motion` tones the effects down.
