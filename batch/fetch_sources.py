# -*- coding: utf-8 -*-
"""빌더가 읽는 원본 노트북을 Kaggle 에서 받아 온다(처음 한 번). 저장소에는 남의 노트북을 복사해 두지 않는다.
사용: python fetch_sources.py        (kaggle CLI 인증이 되어 있어야 한다)
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = ["kaggle"] if shutil.which("kaggle") else [sys.executable, "-m", "kaggle"]
SOURCES = {   # 폴더: (Kaggle 공개 노트북, 빌더가 찾는 파일 이름)
    "krea-src": ("hangglewriter/krea-2-turbo", "krea-2-turbo.ipynb"),                     # Krea 2 Turbo 한국어판(원본 AIQUEST)
    "src-ace-step": ("hangglewriter/ace-step", "ace-step.ipynb"),                         # ACE-Step 1.5
    "src-yue2-music": ("hangglewriter/yue2-music", "yue2-music.ipynb"),                   # YuE2 (비상업)
    "src-ltx25": ("unlockbulk/ltx-2-5-22b-distilled-video-generator",
                  "ltx-2-5-22b-distilled-video-generator.ipynb"),                         # LTX-2.5 (AIQUEST)
}
ok = True
for folder, (ref, name) in SOURCES.items():
    dest = os.path.join(HERE, folder)
    if os.path.exists(os.path.join(dest, name)):
        print("있음", folder); continue
    os.makedirs(dest, exist_ok=True)
    r = subprocess.run([*CLI, "kernels", "pull", ref, "-p", dest, "-m"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONUTF8="1"))
    if os.path.exists(os.path.join(dest, name)):
        print("받음", folder, "<-", ref)
    else:
        ok = False
        print("실패", folder, "<-", ref, (r.stdout + r.stderr).strip()[-300:])
print("완료" if ok else "일부 실패 — 위 메시지 확인(인증 · 인터넷)")
sys.exit(0 if ok else 1)
