import sys, time
from rembg import remove, new_session
from PIL import Image
model = sys.argv[1]
s = new_session(model)
P="/home/user/aspora-social/campaigns/pets-day-out/assets/photos/"
for n in ["golden-rangeela-kurta.jpg","shihtzu-red-lehenga.png","golden-blue-sherwani.png","cat-red-lehenga.png"]:
    t=time.time()
    im=Image.open(P+n).convert("RGB")
    out=remove(im, session=s, alpha_matting=False)
    out.save(sys.argv[2]+"/"+n.rsplit(".",1)[0]+"-"+model+".png")
    print(n, out.size, round(time.time()-t,1),"s")
