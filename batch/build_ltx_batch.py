# -*- coding: utf-8 -*-
"""ltx_shots.json(Runpod ltx_gen.py 와 같은 형식)을 Kaggle 일괄 실행 노트북으로 만든다 — 이미지 → 영상(소리 포함).
원본: AIQUEST LTX-2.5 22B distilled Kaggle 노트북(src-ltx25, T4 ×2 · INT8 · Wan2GP 고정판). 화면(Gradio) 부분만 빼고
generate_video 를 컷마다 부른다. 모델은 DeepBeepMeep/LTX-2 (HF 토큰 필요 없음, 약 40GB, 세션마다 받는다).
사용: python build_ltx_batch.py <ltx_shots.json> --slug ltx-이름 [--only c01,c02] [--res 480|704|1088] [--steps 8]
  - 이미지는 shots.json 의 src 폴더에서 <name>.png(.jpg) 를 찾아 노트북 안에 넣는다(긴 변 1536 JPEG).
  - 결과: outputs/<name>.mp4 + log.json
"""
import argparse, base64, io, json, os
from pathlib import Path
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src-ltx25", "ltx-2-5-22b-distilled-video-generator.ipynb")

ap = argparse.ArgumentParser()
ap.add_argument("shots")
ap.add_argument("--slug", default="ltx-batch")
ap.add_argument("--only", default="")
ap.add_argument("--res", type=int, default=704)   # 짧은 변 기준. T4 권장 480, 우리 기준 704(1280×704)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--user", default=os.environ.get("KAGGLE_USER", ""))   # 다른 계정: --user <이름> + KAGGLE_CONFIG_DIR
a = ap.parse_args()
if not a.user:
    raise SystemExit("Kaggle 아이디가 없습니다: --user <아이디> 를 붙이거나 환경변수 KAGGLE_USER 를 설정하세요")
OUT = os.path.join(HERE, a.slug)

shots_path = Path(a.shots).resolve()
J = json.loads(shots_path.read_text(encoding="utf-8"))
src = (shots_path.parent / J["src"]).resolve() if J.get("src") else shots_path.parent
only = [x for x in a.only.split(",") if x]
tasks = []
for i, s in enumerate(J["shots"]):
    if only and s["name"] not in only:
        continue
    img_b64 = ""
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = src / (s["name"] + ext)
        if p.exists():
            im = Image.open(p).convert("RGB")
            im.thumbnail((1536, 1536), Image.LANCZOS)
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=93)
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            break
    if not img_b64:
        print("이미지 없음 → 텍스트만으로 생성:", s["name"])
    secs = float(s.get("secs", 5))
    frames = int(round(secs * 24 / 8)) * 8 + 1   # LTX 는 8k+1 프레임
    tasks.append({"name": s["name"], "prompt": (s["prompt"] + " " + J.get("style", "")).strip(), "frames": frames,
                  "seed": int(J.get("seed", 42)) + i * 10 + int(s.get("seed_offset", 0)), "image": img_b64})
if not tasks:
    raise SystemExit("만들 컷이 없음")

nb = json.load(io.open(SRC, encoding="utf-8"))
code = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
setup_cell, launch_cell = code[0], code[1]

# 엔진 스크립트(RUN_SCRIPT_CODE)에서 화면 부분을 잘라 내고 일괄 루프를 붙인다
pre, rest = launch_cell.split("RUN_SCRIPT_CODE = r'''", 1)
engine, post = rest.split("\n'''\n", 1)
engine = engine.split("# ==== Generation as a background job ====")[0]
loop = r'''
# ============================================================
#  일괄 생성 (애드플랜) — tasks.json 의 컷을 차례로 만든다
# ============================================================
import base64, io, json, shutil
from PIL import Image as _PILImage
TASKS = json.load(open(os.path.join(WORK_DIR, "tasks.json"), encoding="utf-8"))
RESOLUTIONS["batch"] = BATCH_RES
_log, _t_all = [], time.time()
for _n, _t in enumerate(TASKS, 1):
    _key = f"{_t['frames']}f"
    DURATIONS[_key] = _t["frames"]
    _img = _PILImage.open(io.BytesIO(base64.b64decode(_t["image"]))) if _t["image"] else None
    _aspect = "16:9 Landscape"
    if _img is not None and _img.width < _img.height:
        _aspect = "9:16 Portrait"
    _t0 = time.time()
    _path, _status = generate_video(_t["prompt"], _img, None, _key, "batch", _aspect, BATCH_STEPS, _t["seed"])
    _ok = bool(_path) and os.path.exists(_path)
    if _ok:
        _dest = os.path.join(OUTPUT_DIR, _t["name"] + ".mp4")
        shutil.move(_path, _dest)
    _log.append({"name": _t["name"], "ok": _ok, "sec": round(time.time() - _t0, 1), "frames": _t["frames"],
                 "seed": _t["seed"], "status": _status})
    print(f"[{_n}/{len(TASKS)}] {_t['name']} {'OK' if _ok else 'FAIL'} {round(time.time() - _t0)}s", flush=True)
    json.dump({"res": BATCH_RES, "steps": BATCH_STEPS, "total_sec": round(time.time() - _t_all, 1), "items": _log},
              open(os.path.join(OUTPUT_DIR, "log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE", round(time.time() - _t_all, 1), "s", flush=True)
'''
engine = engine + f"\nBATCH_RES = {a.res}\nBATCH_STEPS = {a.steps}\n" + loop
launch = pre + "RUN_SCRIPT_CODE = r'''" + engine + "\n'''\n" + post

tasks_cell = ("import json\njson.dump(" + json.dumps(tasks, ensure_ascii=False) +
              ", open('/kaggle/working/tasks.json','w',encoding='utf-8'), ensure_ascii=False)\nprint(len(json.load(open('/kaggle/working/tasks.json',encoding='utf-8'))), 'tasks')")
# 배치 실행은 /kaggle/working 전체가 결과물로 남으므로 프로그램 · 입력은 지우고 영상만 남긴다(모델은 /kaggle/tmp)
clean_cell = ("import shutil, os\nfor p in ['Wan2GP','run_ltx25.py','tasks.json','ltx25_settings.json']:\n"
              "    p=os.path.join('/kaggle/working',p)\n"
              "    shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))\n"
              "print(os.listdir('/kaggle/working'), os.listdir('/kaggle/working/outputs') if os.path.isdir('/kaggle/working/outputs') else None)")


def cell(src_):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src_}


out = {"cells": [cell(c) for c in [setup_cell, tasks_cell, launch, clean_cell]],
       "metadata": nb["metadata"], "nbformat": nb["nbformat"], "nbformat_minor": nb["nbformat_minor"]}
os.makedirs(OUT, exist_ok=True)
json.dump(out, io.open(os.path.join(OUT, a.slug + ".ipynb"), "w", encoding="utf-8"), ensure_ascii=False)
meta = {"id": a.user + "/" + a.slug, "title": a.slug, "code_file": a.slug + ".ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False, "enable_internet": True,
        "keywords": [], "dataset_sources": [], "kernel_sources": [], "competition_sources": [], "model_sources": [],
        "machine_shape": "NvidiaTeslaT4"}
json.dump(meta, io.open(os.path.join(OUT, "kernel-metadata.json"), "w", encoding="utf-8"), indent=1)
print(len(tasks), "컷 ->", OUT, f"(해상도 {a.res}p · {a.steps}스텝)")
