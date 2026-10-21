import sys, time, numpy as np, onnxruntime as ort
from PIL import Image
sess = ort.InferenceSession("/tmp/claude-0/-home-user-aspora-social/5ebbe127-3feb-5bd9-9aae-9f591acd8c0c/scratchpad/sr/sr_x4.onnx", providers=["CPUExecutionProvider"])
def sr(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)/255.0
    x = a.transpose(2,0,1)[None]
    y = sess.run(None, {"input": x})[0][0].transpose(1,2,0)
    return Image.fromarray((np.clip(y,0,1)*255+.5).astype(np.uint8))
if __name__ == "__main__":
    for src, dst in zip(sys.argv[1::2], sys.argv[2::2]):
        t=time.time(); im=Image.open(src); out=sr(im); out.save(dst); print(src.split('/')[-1], im.size, "->", out.size, round(time.time()-t,1),"s")
