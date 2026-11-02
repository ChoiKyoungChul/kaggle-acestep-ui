# -*- coding: utf-8 -*-
"""job_song.json(Runpod 곡 작업과 같은 형식)을 Kaggle 일괄 실행 노트북으로 만든다.
사용: python build_song_batch.py ace|yue2 <job_song.json> [--styles a,b] [--seeds 5,23] [--seconds 240]
"""
import argparse, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("engine", choices=["ace", "yue2"])
ap.add_argument("job")
ap.add_argument("--styles", default="")
ap.add_argument("--seeds", default="")
ap.add_argument("--seconds", type=int, default=0)
ap.add_argument("--slug", default="")
ap.add_argument("--user", default=os.environ.get("KAGGLE_USER", ""))   # 다른 계정: --user <이름> + KAGGLE_CONFIG_DIR
a = ap.parse_args()
if not a.user:
    raise SystemExit("Kaggle 아이디가 없습니다: --user <아이디> 를 붙이거나 환경변수 KAGGLE_USER 를 설정하세요")

job = json.load(io.open(a.job, encoding="utf-8"))
styles = [x for x in a.styles.split(",") if x] or list(job["styles"].keys())
seeds = [int(x) for x in a.seeds.split(",") if x] or job.get("seeds", [1])
# styles 값은 문구 하나, 또는 {"style", "bpm", "key", "seconds", "lyrics"} — 큐마다 템포 · 조 · 길이가 다른 BGM 묶음용
def _st(st, k, dflt):
    v = job["styles"][st]
    return v.get(k, dflt) if isinstance(v, dict) else dflt
tasks = [{"id": f"{st}_s{s}", "style": _st(st, "style", job["styles"][st]), "lyrics": _st(st, "lyrics", job.get("lyrics", "[Instrumental]")), "seed": s,
          "seconds": a.seconds or _st(st, "seconds", job.get("seconds", 180)), "language": job.get("language", "unknown"),
          "bpm": _st(st, "bpm", job.get("bpm", 0)), "key": _st(st, "key", job.get("key", ""))} for st in styles for s in seeds]

SRC = {"ace": ("src-ace-step", "ace-step.ipynb"), "yue2": ("src-yue2-music", "yue2-music.ipynb")}[a.engine]
nb = json.load(io.open(os.path.join(HERE, *SRC), encoding="utf-8"))
code = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]

if a.engine == "ace":
    # 원본 화면 스크립트에서 모델 불러오기 · 메모리 분배 부분만 가져온다
    head = code[3].split("\n", 1)[1].split("LANG_CHOICES = [")[0].replace("import gradio as gr\n", "")
    loop = r'''
import json
tasks = json.load(open("/kaggle/working/tasks.json", encoding="utf-8"))
OUT = "/kaggle/working/outputs"; os.makedirs(OUT, exist_ok=True)
log = []; t_all = time.time()
with torch.inference_mode():
    for n, t in enumerate(tasks, 1):
        gc.collect(); torch.cuda.empty_cache()
        custom = {}
        if t.get("bpm"): custom["bpm"] = int(t["bpm"])
        if t.get("key"): custom["keyscale"] = t["key"]
        t0 = time.time()
        try:
            result = pipeline.generate(
                input_prompt=t["lyrics"], model_mode=0, audio_guide=None, alt_prompt=t["style"].strip(),
                audio_guide2=None, audio_prompt_type="", duration_seconds=float(t["seconds"]),
                sampling_steps=8, guidance_scale=1.0, alt_guide_scale=2.5, temperature=0.85, top_p=0.9,
                seed=int(t["seed"]), language=t["language"], custom_settings=custom or None,
                callback=lambda *a, **k: None, set_header_text=lambda s: (print("  [진행]", s), sys.stdout.flush()),
            )
            audio = result.get("x"); sr = int(result.get("audio_sampling_rate", 48000))
            if torch.is_tensor(audio): audio = audio.detach().cpu().float().numpy()
            audio = np.asarray(audio, dtype=np.float32)
            while audio.ndim > 2: audio = audio[0]
            if audio.ndim == 2 and audio.shape[0] <= 2: audio = audio.T
            name = t["id"] + ".flac"
            sf.write(os.path.join(OUT, name), np.clip(audio, -1.0, 1.0), sr)
            sec = round(time.time() - t0, 1)
            log.append({"file": name, "sec": sec, "audio_sec": round(len(audio) / sr, 1), "ok": True})
            print(f"[{n}/{len(tasks)}] {name} {sec}s"); sys.stdout.flush()
        except Exception as e:
            traceback.print_exc(); log.append({"file": t["id"], "ok": False, "error": str(e)[:300]})
        json.dump({"engine": "ace_step_v1_5_xl", "total_sec": round(time.time() - t_all, 1), "items": log},
                  open(os.path.join(OUT, "log.json"), "w"), indent=1)
print("DONE", round(time.time() - t_all, 1), "s")
'''
    script = "%%writefile run_batch.py\n" + head + loop
    run = "!cd /kaggle/working && python -u run_batch.py 2>&1"
    clean = ["Wan2GP", "run_batch.py", "tasks.json"]
else:
    head = code[3].split("\n", 1)[1].split("def _check(style, lyrics):")[0]
    loop = r'''
tasks = json.load(open("/kaggle/working/tasks.json", encoding="utf-8"))
OUT = "/kaggle/working/outputs"; os.makedirs(OUT, exist_ok=True)
items = []; t_all = time.time()
for n, t in enumerate(tasks, 1):
    t0 = time.time()
    try:
        f, score = _wait(_post(build_graph(t["style"], t["lyrics"], min(int(t["seconds"]), MAX_SEC), t["seed"], None, name=t["id"])), timeout=5400)
        src = os.path.join(COMFY, "output", f.get("subfolder", ""), f["filename"])
        name = t["id"] + os.path.splitext(f["filename"])[1]
        shutil.copy(src, os.path.join(OUT, name))
        open(os.path.join(OUT, t["id"] + ".abc.txt"), "w", encoding="utf-8").write(score or "")
        sec = round(time.time() - t0, 1)
        items.append({"file": name, "sec": sec, "ok": True}); print(f"[{n}/{len(tasks)}] {name} {sec}s", flush=True)
    except Exception as e:
        items.append({"file": t["id"], "ok": False, "error": str(e)[:300]}); print("FAIL", t["id"], e, flush=True)
        print(open("/kaggle/working/comfy.log").read()[-3000:])
    json.dump({"engine": "yue2_3b", "total_sec": round(time.time() - t_all, 1), "items": items},
              open(os.path.join(OUT, "log.json"), "w"), indent=1)
proc.terminate()
print("DONE", round(time.time() - t_all, 1), "s")
'''
    script = "%%writefile /kaggle/working/run_batch.py\n" + head + loop
    run = "!cd /kaggle/working && python -u run_batch.py 2>&1"
    clean = ["run_batch.py", "tasks.json"]

tasks_cell = "import json\njson.dump(" + repr(tasks) + ", open('/kaggle/working/tasks.json','w',encoding='utf-8'), ensure_ascii=False)\nprint(len(json.load(open('/kaggle/working/tasks.json',encoding='utf-8'))), 'tasks')"
# 배치 실행은 /kaggle/working 전체가 결과물로 남으므로 모델 · 프로그램은 지우고 음원만 남긴다
clean_cell = "import shutil, os\nfor p in " + repr(clean) + ":\n    p=os.path.join('/kaggle/working',p)\n    shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))\nprint(os.listdir('/kaggle/working/outputs') if os.path.isdir('/kaggle/working/outputs') else os.listdir('/kaggle/working'))"

def cell(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}

slug = a.slug or (a.engine + "-batch")
OUT = os.path.join(HERE, slug); os.makedirs(OUT, exist_ok=True)
# 10/16: Wan2GP requirements 가 torch 를 고정하지 않아 최신 torch(CUDA 13)가 깔리고 Kaggle 기본 torchaudio(cu128)와 어긋나 실패
#  → Kaggle 에 깔린 torch · torchvision · torchaudio 버전을 제약 파일로 묶어 그대로 쓴다
PIN = "!pip list --format=freeze | grep -iE '^(torch|torchvision|torchaudio)==' > /tmp/torch_pin.txt; cat /tmp/torch_pin.txt\n"
for i in (0, 1, 2):
    if "Wan2GP/requirements.txt" in code[i]:
        code[i] = code[i].replace("!pip install --timeout 120 --retries 5 -q -r Wan2GP/requirements.txt",
                                  PIN + "!pip install --timeout 120 --retries 5 -q -r Wan2GP/requirements.txt -c /tmp/torch_pin.txt")
        code[i] = code[i].replace("!pip install --timeout 120 --retries 5 -q mmgp gradio soundfile",
                                  "!pip install --timeout 120 --retries 5 -q mmgp gradio soundfile -c /tmp/torch_pin.txt")
out = {"cells": [cell(c) for c in [code[0], code[1], code[2], tasks_cell, script, run, clean_cell]],
       "metadata": nb["metadata"], "nbformat": nb["nbformat"], "nbformat_minor": nb["nbformat_minor"]}
json.dump(out, io.open(os.path.join(OUT, slug + ".ipynb"), "w", encoding="utf-8"), ensure_ascii=False)
meta = {"id": a.user + "/" + slug, "title": slug, "code_file": slug + ".ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False, "enable_internet": True,
        "keywords": [], "dataset_sources": [], "kernel_sources": [], "competition_sources": [], "model_sources": [],
        "machine_shape": "NvidiaTeslaT4"}
json.dump(meta, io.open(os.path.join(OUT, "kernel-metadata.json"), "w", encoding="utf-8"), indent=1)
print(len(tasks), "tasks ->", OUT)
