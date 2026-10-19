# Furry Pooch website

A static, zero-dependency site (HTML, CSS, vanilla JS). Open `index.html` in a browser, or serve the folder:

```
npx http-server furry-pooch
```

## What's inside
- `index.html` — all sections: hero, marquee, about (business card), services, how it works, boop-the-dog, booking form, footer
- `styles.css` — brand tokens at the top (`--sun`, `--choc`, `--indigo` …) taken from the logo and business card
- `main.js` — paw cursor and walking trail, click effects (paw stamp, flying bits, word pops, "zoomies" paw rain every 10th click), scroll reveals, marquee, magnetic buttons, 3D tilt, eye-tracking dog, booking form
- `assets/` — transparent logo, business card, illustration

## Editing
- Phone, email and Instagram live in the contact section of `index.html`, and `PHONE` / `EMAIL` at the top of `main.js`.
- The booking form opens WhatsApp (or email) with the message pre-filled, so no backend is needed.
- Service names and descriptions are placeholder copy. Edit them in the `#services` section.
- Fonts (Bagel Fat One, Outfit, Gaegu) load from Google Fonts.
- Touch devices get tap effects but no custom cursor. `prefers-reduced-motion` tones the effects down.
