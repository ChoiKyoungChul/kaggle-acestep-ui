# -*- coding: utf-8 -*-
"""Wan2GP(WanGP) 일괄 API 로 Z-Image · Qwen-Image · Wan 2.2 를 Kaggle T4 ×2 에서 돌리는 노트북을 만든다(11/2).
Wan2GP 는 Krea · LTX Kaggle 노트북이 쓰는 엔진이다. 모델은 DeepBeepMeep 저장소에서 엔진이 직접 받는다(HF 토큰 필요 없음).
사용:
  이미지  python build_wgp_batch.py zimage <job_img.json> --slug zimg-이름 [--ids c01,c02] [--seeds 1,2] [--steps 8]
          python build_wgp_batch.py qwen   <job_img.json> --slug qwen-이름 [--steps 30]
  영상    python build_wgp_batch.py wan    <ltx_shots.json> --slug wan-이름 [--only c01] [--res 1280x720] [--steps 4]
  → python kg.py run <slug> --to <결과 폴더>   (결과: outputs/<id>_s<seed>.png 또는 outputs/<컷>.mp4 + log.json)
job_img.json 은 Krea 와 같은 형식, ltx_shots.json 은 LTX(Runpod · Kaggle)와 같은 형식이다.
"""
import argparse, base64, io, json, os
from pathlib import Path
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WAN2GP_COMMIT = "f02a38275fa43057ea75814e8ef4368e5530dcf2"   # LTX-2.5 Kaggle 노트북이 검증한 커밋(2026-10-06)
MODELS = {   # 모델 종류: (Wan2GP model_type, 기본 스텝, guidance, 메모리 프로필)
    "zimage": ("z_image", 8, 0.0, "4"),
    "qwen": ("qwen_image_2512_20B", 30, 4.0, "4"),
    "wan": ("i2v_2_2_Enhanced_Lightning_v2", 4, 1.0, "4"),
}
SIZES = {"16:9hd": (1920, 1088), "9:16hd": (1088, 1920), "16:9": (1664, 928), "9:16": (928, 1664),
         "4:3": (1472, 1104), "3:4": (1104, 1472), "1:1": (1328, 1328)}

ap = argparse.ArgumentParser()
ap.add_argument("model", choices=list(MODELS))
ap.add_argument("job")
ap.add_argument("--slug", default="")
ap.add_argument("--ids", default="")
ap.add_argument("--only", default="")
ap.add_argument("--seeds", default="")
ap.add_argument("--steps", type=int, default=0)
ap.add_argument("--res", default="1280x720")       # 영상 해상도(가로 기준, 세로 이미지는 자동으로 뒤집음)
ap.add_argument("--profile", default="")
ap.add_argument("--user", default=os.environ.get("KAGGLE_USER", ""))   # 다른 계정: --user <이름> + KAGGLE_CONFIG_DIR
a = ap.parse_args()
if not a.user:
    raise SystemExit("Kaggle 아이디가 없습니다: --user <아이디> 를 붙이거나 환경변수 KAGGLE_USER 를 설정하세요")
model_type, def_steps, guide, profile = MODELS[a.model]
steps = a.steps or def_steps
profile = a.profile or profile
slug = a.slug or f"{a.model}-batch"
OUT = os.path.join(HERE, slug)

job_path = Path(a.job).resolve()
J = json.loads(job_path.read_text(encoding="utf-8"))
tasks = []
if a.model in ("zimage", "qwen"):
    ids = [x for x in a.ids.split(",") if x] or list(J["images"].keys())
    seeds = [int(x) for x in a.seeds.split(",") if x] or J.get("seeds", [1])
    for i in ids:
        im = J["images"][i]
        w, h = SIZES[im.get("ratio", "16:9hd")]
        for s in seeds:
            tasks.append({"name": f"{i}_s{s}", "ext": "png", "seed": s, "settings": {
                "prompt": im["prompt"], "negative_prompt": im.get("negative", ""), "resolution": f"{w}x{h}"}})
else:
    src = (job_path.parent / J["src"]).resolve() if J.get("src") else job_path.parent
    only = [x for x in a.only.split(",") if x]
    W, H = [int(v) for v in a.res.lower().split("x")]
    for i, s in enumerate(J["shots"]):
        if only and s["name"] not in only:
            continue
        p = next((src / (s["name"] + e) for e in (".png", ".jpg", ".jpeg", ".webp") if (src / (s["name"] + e)).exists()), None)
        if p is None:
            raise SystemExit(f"이미지 없음: {src / s['name']}.png — Wan 은 이미지 → 영상만 지원")
        im = Image.open(p).convert("RGB")
        im.thumbnail((1536, 1536), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=93)
        w, h = (W, H) if im.width >= im.height else (H, W)
        frames = int(round(float(s.get("secs", 5)) * 16 / 4)) * 4 + 1   # Wan 16fps, 4k+1 프레임(5초=81)
        tasks.append({"name": s["name"], "ext": "mp4", "seed": int(J.get("seed", 42)) + i * 10 + int(s.get("seed_offset", 0)),
                      "image": base64.b64encode(buf.getvalue()).decode(), "settings": {
                          "prompt": (s["prompt"] + " " + J.get("style", "")).strip(), "negative_prompt": J.get("negative", ""),
                          "resolution": f"{w}x{h}", "video_length": frames}})
if not tasks:
    raise SystemExit("만들 항목이 없음")

setup_cell = f'''import os, subprocess
subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
if not os.path.isdir("Wan2GP/.git"):
    subprocess.run(["git", "init", "-q", "Wan2GP"], check=True)
    subprocess.run(["git", "-C", "Wan2GP", "remote", "add", "origin", "https://github.com/DeepBeepMeep/Wan2GP.git"], check=True)
subprocess.run(["git", "-C", "Wan2GP", "fetch", "-q", "--depth", "1", "origin", "{WAN2GP_COMMIT}"], check=True)
subprocess.run(["git", "-C", "Wan2GP", "reset", "-q", "--hard", "FETCH_HEAD"], check=True)
# 모델은 용량이 큰 /kaggle/tmp 에 받는다(/kaggle/working 은 결과물 한도 20GB)
os.makedirs("/kaggle/tmp/ckpts", exist_ok=True)
if not os.path.islink("Wan2GP/ckpts"):
    subprocess.run(["rm", "-rf", "Wan2GP/ckpts"]); os.symlink("/kaggle/tmp/ckpts", "Wan2GP/ckpts")
print("Wan2GP ready")
'''
# Kaggle 에 깔린 torch 3종을 고정한 채 설치(requirements 가 torch 를 올려 torchaudio 와 어긋나는 사고, 10/16)
install_cell = ("!pip list --format=freeze | grep -iE '^(torch|torchvision|torchaudio)==' > /tmp/torch_pin.txt; cat /tmp/torch_pin.txt\n"
                "!pip install --timeout 120 --retries 5 -q -r Wan2GP/requirements.txt -c /tmp/torch_pin.txt\n"
                "!pip install --timeout 120 --retries 5 -q mmgp -c /tmp/torch_pin.txt")
tasks_cell = ("import json\njson.dump(" + json.dumps(tasks, ensure_ascii=False) +
              ", open('/kaggle/working/tasks.json','w',encoding='utf-8'), ensure_ascii=False)\nprint(len(json.load(open('/kaggle/working/tasks.json',encoding='utf-8'))), 'tasks')")
run_script = f'''%%writefile /kaggle/working/run_wgp.py
# -*- coding: utf-8 -*-
import base64, json, os, shutil, sys, time, traceback
from pathlib import Path
WAN2GP = Path("/kaggle/working/Wan2GP")
OUT = Path("/kaggle/working/outputs"); OUT.mkdir(exist_ok=True)
TMP_OUT = Path("/kaggle/tmp/wgp_out"); TMP_OUT.mkdir(parents=True, exist_ok=True)
INP = Path("/kaggle/tmp/inputs"); INP.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
sys.path.insert(0, str(WAN2GP)); os.chdir(WAN2GP)
from shared.api import init
tasks = json.load(open("/kaggle/working/tasks.json", encoding="utf-8"))
t_all = time.time()
session = init(root=WAN2GP, output_dir=TMP_OUT, cli_args=["--attention", "sdpa", "--profile", "{profile}", "--fp16"])
print("session ready", round(time.time() - t_all), "s", flush=True)
log = []
for n, t in enumerate(tasks, 1):
    s = dict(t["settings"]); s.update({{"model_type": "{model_type}", "num_inference_steps": {steps}, "seed": t["seed"],
                                        "guidance_scale": {guide}, "batch_size": 1}})
    if t.get("image"):
        p = INP / (t["name"] + ".jpg"); p.write_bytes(base64.b64decode(t["image"])); s["image_start"] = str(p); s["image_prompt_type"] = "S"
    t0 = time.time(); ok, err = False, ""
    try:
        res = session.submit_task(s).result()
        files = [f for f in res.generated_files if os.path.exists(f)]
        if res.success and files:
            shutil.move(files[0], OUT / (t["name"] + os.path.splitext(files[0])[1])); ok = True
        else:
            err = "; ".join(e.message for e in res.errors)[:500] or "no file"
    except Exception as e:
        traceback.print_exc(); err = str(e)[:500]
    log.append({{"name": t["name"], "ok": ok, "sec": round(time.time() - t0, 1), "error": err}})
    print(f"[{{n}}/{{len(tasks)}}] {{t['name']}} {{'OK' if ok else 'FAIL ' + err}} {{round(time.time() - t0)}}s", flush=True)
    json.dump({{"model": "{model_type}", "steps": {steps}, "total_sec": round(time.time() - t_all, 1), "items": log}},
              open(OUT / "log.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE", round(time.time() - t_all, 1), "s", flush=True)
'''
run_cell = "import time\n_t=time.time()\n!cd /kaggle/working && python -u run_wgp.py 2>&1 | grep -v -E 'it/s\\]|s/it\\]' \nprint('run cell', round(time.time()-_t,1), 's')"
clean_cell = ("import shutil, os\nfor p in ['Wan2GP','run_wgp.py','tasks.json']:\n"
              "    p=os.path.join('/kaggle/working',p)\n"
              "    shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) and not os.path.islink(p) else (os.path.exists(p) and os.remove(p))\n"
              "print(os.listdir('/kaggle/working'), os.listdir('/kaggle/working/outputs') if os.path.isdir('/kaggle/working/outputs') else None)")


def cell(src_):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src_}


nb = {"cells": [cell(c) for c in [setup_cell, install_cell, tasks_cell, run_script, run_cell, clean_cell]],
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 4}
os.makedirs(OUT, exist_ok=True)
json.dump(nb, io.open(os.path.join(OUT, slug + ".ipynb"), "w", encoding="utf-8"), ensure_ascii=False)
meta = {"id": a.user + "/" + slug, "title": slug, "code_file": slug + ".ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False, "enable_internet": True,
        "keywords": [], "dataset_sources": [], "kernel_sources": [], "competition_sources": [], "model_sources": [],
        "machine_shape": "NvidiaTeslaT4"}
json.dump(meta, io.open(os.path.join(OUT, "kernel-metadata.json"), "w", encoding="utf-8"), indent=1)
print(len(tasks), "개 ->", OUT, f"({model_type} · {steps}스텝 · profile {profile})")
