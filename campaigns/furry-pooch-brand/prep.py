import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-aspora-social/5ebbe127-3feb-5bd9-9aae-9f591acd8c0c/scratchpad/sr")
from upscale import sr
from PIL import Image, ImageOps
SRC="/tmp/claude-0/-home-user-aspora-social/5ebbe127-3feb-5bd9-9aae-9f591acd8c0c/scratchpad/cat/im-%s.jpg"
OUT="/home/user/aspora-social/campaigns/furry-pooch-brand/assets/photos/"
rng = np.random.default_rng(11)
def grain(im, sigma=3.0):
    a = np.asarray(im).astype(np.float32); n = rng.normal(0, sigma, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
def make(sid, size, centering, crop=None, blend=0.35):
    im = Image.open(SRC % sid).convert("RGB")
    if crop: im = im.crop(crop)
    base = im.resize((im.width*4, im.height*4), Image.LANCZOS)
    im = Image.blend(base, sr(im), blend)
    return grain(ImageOps.fit(im, size, Image.LANCZOS, centering=centering))
jobs = {
  "a-hero-tutu":     ("013", (2160, 2100), (0.5, 0.0)),   # golden in rainbow tutu dress
  "b-cat-lace":      ("014", (2160, 2700), (0.5, 0.4)),    # ragdoll in sailor lace collar
  "c-poodle-tux":    ("029", (1040, 1688), (0.5, 0.25)),   # poodle, midnight tuxedo bandana
  "c-golden-plaid":  ("112", (1000, 828),  (0.5, 0.2)),    # golden, plaid tuxedo bandana
  "c-cat-red-tux":   ("109", (1000, 828),  (0.5, 0.35)),   # cat, red tuxedo bandana
}
for name, (sid, size, cen) in jobs.items():
    out = make(sid, size, cen); out.save(OUT + name + ".jpg", quality=93); print(name, size)
