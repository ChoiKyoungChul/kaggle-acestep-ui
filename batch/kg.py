# -*- coding: utf-8 -*-
r"""Kaggle 일괄 노트북을 올리고 · 기다리고 · 내려받고 · 지운다. 어떤 AI 도구(Claude Code · Codex 등)에서도 같은 명령을 쓴다.
사용: python kg.py run <노트북 폴더> [--to <결과를 복사할 폴더>] [--keep]
      python kg.py list            내 노트북과 상태
      python kg.py usage           이번 주 GPU 사용 시간 · 남은 시간(주 30시간, usage.csv 기록 기준)
인증: ~/.kaggle/access_token (내용을 화면 · 문서에 적지 않는다)
"""
import argparse, glob, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, PYTHONUTF8="1")
_TOK = os.path.join(os.environ.get("KAGGLE_CONFIG_DIR", ""), "access_token")   # CLI 2.2 는 CONFIG_DIR 의 access_token 을 안 읽음 → 환경변수로 넘긴다
if os.environ.get("KAGGLE_CONFIG_DIR") and os.path.exists(_TOK):
    ENV["KAGGLE_API_TOKEN"] = open(_TOK, encoding="utf-8").read().strip()


_CLI = ["kaggle"] if shutil.which("kaggle") else [sys.executable, "-m", "kaggle"]   # 새 PC 에서 pip Scripts 가 PATH 에 없을 때(11/2)


def kaggle(*args):
    r = subprocess.run([*_CLI, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    return (r.stdout or "") + (r.stderr or "")


_ACC = os.path.basename(os.environ.get("KAGGLE_CONFIG_DIR", "").rstrip("/\\"))   # 다른 계정은 KAGGLE_CONFIG_DIR=~/.kaggle-<계정>
USAGE = os.path.join(HERE, f"usage-{_ACC}.csv" if _ACC and _ACC != ".kaggle" else "usage.csv")   # 시작(UTC 초),끝,분,노트북 — 계정마다 따로
QUOTA_H = 30.0                               # 주 30시간, 토요일 00:00 UTC(= 토 09:00 KST)에 다시 채워진다


def log_usage(ref, t0, t1):
    with open(USAGE, "a", encoding="utf-8") as f:
        f.write(f"{int(t0)},{int(t1)},{(t1 - t0) / 60:.1f},{ref}\n")


def usage_text():
    now = time.time()
    g = time.gmtime(now)
    week0 = now - (((g.tm_wday - 5) % 7) * 86400 + g.tm_hour * 3600 + g.tm_min * 60 + g.tm_sec)   # 지난 토요일 00:00 UTC
    rows = []
    if os.path.exists(USAGE):
        for line in open(USAGE, encoding="utf-8"):
            p = line.strip().split(",")
            if len(p) >= 4 and float(p[0]) >= week0:
                rows.append((float(p[2]), p[3]))
    used = sum(m for m, _ in rows) / 60
    nxt = time.strftime("%m/%d %H:%M", time.localtime(week0 + 7 * 86400))
    return (f"[Kaggle GPU] 이번 주 기록된 사용 {used:.1f}시간 ({len(rows)}세션) · 남은 시간 약 {QUOTA_H - used:.1f}시간 / {QUOTA_H:.0f}시간 · 다시 채워지는 때 {nxt}\n"
            "  ※ kg.py 로 돌린 세션만 센다(끝날 때까지 기다린 시간 기준 · 약간 많게 잡힌다). 정확한 값은 kaggle.com/settings 의 GPU 사용량.")


def run(folder, to, keep):
    folder = folder if os.path.isabs(folder) else os.path.join(HERE, folder)
    ref = json.load(open(os.path.join(folder, "kernel-metadata.json"), encoding="utf-8"))["id"]
    # GPU 일괄 세션은 동시에 2개까지라 자리가 날 때까지 다시 올린다
    while True:
        out = kaggle("kernels", "push", "-p", folder, "--accelerator", "NvidiaTeslaT4")
        if "successfully pushed" in out:
            break
        print(time.strftime("%H:%M"), "대기:", out.strip().splitlines()[-1][:120], flush=True)
        time.sleep(90)
    print(time.strftime("%H:%M"), "올림", ref, flush=True)
    t0 = time.time()
    while True:
        st = kaggle("kernels", "status", ref).upper()
        if any(k in st for k in ("COMPLETE", "ERROR", "CANCEL")):
            break
        time.sleep(90)
    print(time.strftime("%H:%M"), st.strip().splitlines()[-1], flush=True)
    log_usage(ref, t0, time.time())
    print(usage_text(), flush=True)
    dst = folder + "-out"
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
    kaggle("kernels", "output", ref, "-p", dst)
    files = [f for f in glob.glob(os.path.join(dst, "outputs", "*")) if not f.endswith("log.json")]
    print("결과", len(files), "개 ->", os.path.join(dst, "outputs"), flush=True)
    if to:
        os.makedirs(to, exist_ok=True)
        for f in files:
            shutil.copy(f, to)
    if not keep and "COMPLETE" in st:
        print(kaggle("kernels", "delete", ref, "-y").strip().splitlines()[-1])
    return 0 if files else 1


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
r = sub.add_parser("run"); r.add_argument("folder"); r.add_argument("--to", default=""); r.add_argument("--keep", action="store_true")
sub.add_parser("list")
sub.add_parser("usage")
a = ap.parse_args()
if a.cmd == "list":
    print(kaggle("kernels", "list", "--mine"))
elif a.cmd == "usage":
    print(usage_text())
else:
    sys.exit(run(a.folder, a.to, a.keep))
