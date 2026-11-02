# -*- coding: utf-8 -*-
"""job_img.json(Runpod krea_run.py 와 같은 형식)을 Kaggle 일괄 실행 노트북으로 만든다.
사용: python build_krea_batch.py <job_img.json> [--ids f01,f02] [--seeds 1] [--steps 8] [--slug 이름]
"""
import argparse, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "krea-src", "krea-2-turbo.ipynb")
OUT = os.path.join(HERE, "krea-batch")
SIZES = {"16:9hd": (1920, 1088), "9:16hd": (1088, 1920), "16:9": (1664, 928), "9:16": (928, 1664),
         "4:3": (1472, 1104), "3:4": (1104, 1472), "1:1": (1328, 1328)}

ap = argparse.ArgumentParser()
ap.add_argument("job")
ap.add_argument("--ids", default="")
ap.add_argument("--seeds", default="")
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--slug", default="krea-batch")
ap.add_argument("--user", default=os.environ.get("KAGGLE_USER", ""))   # 다른 계정: --user <이름> + KAGGLE_CONFIG_DIR
a = ap.parse_args()
if not a.user:
    raise SystemExit("Kaggle 아이디가 없습니다: --user <아이디> 를 붙이거나 환경변수 KAGGLE_USER 를 설정하세요")
OUT = os.path.join(HERE, a.slug)

job = json.load(io.open(a.job, encoding="utf-8"))
ids = [x for x in a.ids.split(",") if x] or list(job["images"].keys())
seeds = [int(x) for x in a.seeds.split(",") if x] or job.get("seeds", [1])
tasks = []
for i in ids:
    im = job["images"][i]
    w, h = SIZES[im.get("ratio", "16:9hd")]
    for s in seeds:
        tasks.append({"id": i, "seed": s, "w": w, "h": h, "prompt": im["prompt"], "neg": im.get("negative", "")})

nb = json.load(io.open(SRC, encoding="utf-8"))
code = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
env_cell, install_cell, dl_cell, app_cell = code[0], code[1], code[2], code[3]

# 원본 화면(gradio) 스크립트에서 모델 불러오기 · 메모리 분배 부분만 가져온다
head = app_cell.split("\n", 1)[1].split("#  3) 프롬프트 자동 보강 기능")[0].rsplit("# ====", 1)[0]
head = head.replace("import gradio as gr\n", "")
loop = r'''
# ============================================================
#  일괄 생성 (애드플랜) — tasks.json 을 차례로 만든다
# ============================================================
import json
tasks = json.load(open("/kaggle/working/tasks.json", encoding="utf-8"))
os.makedirs(OUTPUT_DIR, exist_ok=True)
log = []
t_all = time.time()
with torch.inference_mode():
    for n, t in enumerate(tasks, 1):
        gc.collect(); torch.cuda.empty_cache()
        t0 = time.time()
        name = f"{t['id']}_s{t['seed']}.png"
        try:
            result = krea_model.generate(
                seed=int(t["seed"]), input_prompt=t["prompt"],
                n_prompt=t["neg"] if t["neg"].strip() else None,
                sampling_steps=STEPS, width=t["w"], height=t["h"],
                guide_scale=0.0, batch_size=1, callback=None,
                loras_slists={"phase1": []},
            )
            if result is None:
                raise RuntimeError("generate returned None")
            Image.fromarray(result[:, 0].permute(1, 2, 0).numpy()).save(os.path.join(OUTPUT_DIR, name))
            sec = round(time.time() - t0, 1)
            log.append({"file": name, "sec": sec, "w": t["w"], "h": t["h"], "ok": True})
            print(f"[{n}/{len(tasks)}] {name} {t['w']}x{t['h']} {sec}s"); sys.stdout.flush()
        except Exception as e:
            traceback.print_exc()
            log.append({"file": name, "ok": False, "error": str(e)[:300]})
        json.dump({"steps": STEPS, "total_sec": round(time.time() - t_all, 1), "items": log},
                  open(os.path.join(OUTPUT_DIR, "log.json"), "w"), indent=1)
print("DONE", round(time.time() - t_all, 1), "s")
'''
script = "%%writefile run_batch.py\n# -*- coding: utf-8 -*-\nOUTPUT_DIR = \"/kaggle/working/outputs\"\nSTEPS = " + str(a.steps) + "\n" + head + loop

tasks_cell = "import json\njson.dump(" + repr(tasks) + ", open('/kaggle/working/tasks.json','w',encoding='utf-8'), ensure_ascii=False)\nprint(len(json.load(open('/kaggle/working/tasks.json',encoding='utf-8'))), 'tasks')"
run_cell = "import time\n_t=time.time()\n!python -u run_batch.py 2>&1\nprint('run cell', round(time.time()-_t,1), 's')"
# 배치 실행은 /kaggle/working 전체가 결과물로 남으므로 모델 · 프로그램은 지우고 그림만 남긴다
clean_cell = "import shutil, os\nfor p in ['Wan2GP','run_batch.py','tasks.json']:\n    p=os.path.join('/kaggle/working',p)\n    shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))\nprint(os.listdir('/kaggle/working'), os.listdir('/kaggle/working/outputs') if os.path.isdir('/kaggle/working/outputs') else None)"

def cell(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}

out = {"cells": [cell(c) for c in [env_cell, install_cell, dl_cell, tasks_cell, script, run_cell, clean_cell]],
       "metadata": nb["metadata"], "nbformat": nb["nbformat"], "nbformat_minor": nb["nbformat_minor"]}
os.makedirs(OUT, exist_ok=True)
json.dump(out, io.open(os.path.join(OUT, a.slug + ".ipynb"), "w", encoding="utf-8"), ensure_ascii=False)
meta = {"id": a.user + "/" + a.slug, "title": a.slug, "code_file": a.slug + ".ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False, "enable_internet": True,
        "keywords": [], "dataset_sources": [], "kernel_sources": [], "competition_sources": [], "model_sources": [],
        "machine_shape": "NvidiaTeslaT4"}
json.dump(meta, io.open(os.path.join(OUT, "kernel-metadata.json"), "w", encoding="utf-8"), indent=1)
print(len(tasks), "tasks ->", OUT)
