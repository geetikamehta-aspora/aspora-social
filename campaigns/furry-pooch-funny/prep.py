import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-aspora-social/5ebbe127-3feb-5bd9-9aae-9f591acd8c0c/scratchpad/sr")
from upscale import sr
from PIL import Image, ImageOps
SRC="/tmp/claude-0/-home-user-aspora-social/5ebbe127-3feb-5bd9-9aae-9f591acd8c0c/scratchpad/cat/im-%s.jpg"
OUT="/home/user/aspora-social/campaigns/furry-pooch-funny/assets/photos/"
rng = np.random.default_rng(11)
def grain(im, sigma=3.0):
    a = np.asarray(im).astype(np.float32); n = rng.normal(0, sigma, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
CROPS = {"018": (6, 4, 739, 1092)}
def make(sid, size, centering, crop=None, blend=0.35):
    crop = crop or CROPS.get(sid)
    im = Image.open(SRC % sid).convert("RGB")
    if crop: im = im.crop(crop)
    base = im.resize((im.width*4, im.height*4), Image.LANCZOS)
    im = Image.blend(base, sr(im), blend)
    return grain(ImageOps.fit(im, size, Image.LANCZOS, centering=centering))
jobs = {
  "f1-golden-sherwani": ("008", (2160, 1860), (0.5, 0.5)),    # golden in Gulaal Sequin Sherwani
  "f2-cat-dungaree":    ("022", (1244, 1860), (0.5, 0.5)),    # grey cat in dungaree-print tee
  "f3-golden-harness":  ("018", (1252, 1860), (0.5, 0.5)),    # golden sitting in orange harness (full pose)
}
for name, (sid, size, cen) in jobs.items():
    out = make(sid, size, cen); out.save(OUT + name + ".jpg", quality=93); print(name, size)

