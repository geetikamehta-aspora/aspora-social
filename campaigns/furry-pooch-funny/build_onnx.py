# Rebuild Real-ESRGAN "realesr-general-x4v3" (SRVGGNetCompact) as an ONNX model without torch.
import zipfile, pickle, io, numpy as np, onnx, sys
from onnx import helper, TensorProto, numpy_helper

W = sys.argv[1]; OUT = sys.argv[2]
z = zipfile.ZipFile(W)
names = z.namelist()
prefix = names[0].split("/")[0]
class Storage:
    def __init__(self, dtype): self.dtype = dtype; self.key=None
DT = {"FloatStorage": np.float32, "HalfStorage": np.float16, "DoubleStorage": np.float64}
def rebuild(storage, offset, size, stride, *a):
    arr = np.frombuffer(z.read(f"{prefix}/data/{storage.key}"), dtype=storage.dtype)
    n = int(np.prod(size)) if len(size) else 1
    return arr[offset:offset+n].reshape(size).copy()
class U(pickle.Unpickler):
    def find_class(self, mod, name):
        if name == "_rebuild_tensor_v2": return rebuild
        if name in DT: return lambda *a, n=name: Storage(DT[n])
        if name == "OrderedDict": 
            import collections; return collections.OrderedDict
        return super().find_class(mod, name)
    def persistent_load(self, pid):
        # ('storage', storage_type, key, location, numel)
        st = pid[1]; s = st() if callable(st) else st
        s.key = pid[2]; return s
sd = U(io.BytesIO(z.read(f"{prefix}/data.pkl"))).load()
if "params" in sd: sd = sd["params"]
ks = list(sd.keys()); print(len(ks), ks[:4], ks[-3:])

nconv = max(int(k.split(".")[1]) for k in ks if k.startswith("body.") ) 
# body layout: [conv, prelu, (conv, prelu)*num_conv, conv_last]
idx = sorted({int(k.split(".")[1]) for k in ks})
last = idx[-1]
nodes, inits = [], []
cur = "input"
def add_init(name, arr): inits.append(numpy_helper.from_array(arr.astype(np.float32), name)); return name
for i in idx:
    if f"body.{i}.weight" in sd and sd[f"body.{i}.weight"].ndim == 4:
        w = add_init(f"w{i}", sd[f"body.{i}.weight"]); b = add_init(f"b{i}", sd[f"body.{i}.bias"])
        out = f"c{i}"; nodes.append(helper.make_node("Conv", [cur, w, b], [out], kernel_shape=[3,3], pads=[1,1,1,1])); cur = out
    else:
        s = sd[f"body.{i}.weight"].reshape(1, -1, 1, 1)
        sl = add_init(f"s{i}", s); out = f"p{i}"; nodes.append(helper.make_node("PRelu", [cur, sl], [out])); cur = out
# pixel shuffle x4
nodes.append(helper.make_node("DepthToSpace", [cur], ["ps"], blocksize=4, mode="CRD"))
# nearest upsample of input x4 and add
scales = add_init("scales", np.array([1,1,4,4], dtype=np.float32))
inits.append(numpy_helper.from_array(np.array([], dtype=np.float32), "roi"))
nodes.append(helper.make_node("Resize", ["input", "roi", "scales"], ["base"], mode="nearest"))
nodes.append(helper.make_node("Add", ["ps", "base"], ["output"]))
g = helper.make_graph(nodes, "srvgg",
    [helper.make_tensor_value_info("input", TensorProto.FLOAT, [1,3,"h","w"])],
    [helper.make_tensor_value_info("output", TensorProto.FLOAT, [1,3,"H","W"])], inits)
m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 13)]); m.ir_version = 8
onnx.checker.check_model(m); onnx.save(m, OUT); print("saved", OUT)
