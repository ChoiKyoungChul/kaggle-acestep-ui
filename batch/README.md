# Kaggle 무료 GPU 일괄 실행 — AI 코딩 도구용

PC 에서 명령 두 줄로 Kaggle 무료 GPU(T4 ×2, 주 30시간)에 곡 · 이미지 · 영상 작업을 보내고 결과를 받아 온다.
모델 설치 · 다운로드 · 생성은 전부 Kaggle 노트북 **안에서** 된다. PC 에는 Python 과 kaggle CLI 만 있으면 된다(GPU 불필요).

| 모델 | 빌더 | 결과 | 상태 |
|---|---|---|---|
| ACE-Step 1.5 (노래 · 연주곡) | `build_song_batch.py ace` | flac/mp3 | 검증 |
| YuE2 (노래, 비상업) | `build_song_batch.py yue2` | mp3 | 검증 |
| Krea 2 Turbo (이미지) | `build_krea_batch.py` | png | 검증 |
| LTX-2.5 (사진 → 영상 + 소리) | `build_ltx_batch.py` | mp4 | 검증(11/2) |
| Z-Image · Qwen-Image · Wan 2.2 | `build_wgp_batch.py` | png · mp4 | 시험 중 |

## 설치 (Windows PowerShell)

```powershell
git clone https://github.com/ChoiKyoungChul/kaggle-acestep-ui.git
cd kaggle-acestep-ui\batch
powershell -ExecutionPolicy Bypass -File setup.ps1 -User <내 Kaggle 아이디>
```

`setup.ps1` 이 하는 일: kaggle CLI 2.2.4 설치 → `KAGGLE_USER` 저장 → 토큰 · 인증 확인 → 원본 노트북 받기(`fetch_sources.py`).
준비물: kaggle.com 가입 + **휴대폰 인증** + Settings › API › Create New Token → `%USERPROFILE%\.kaggle\access_token` 에 저장.
macOS · Linux 는 `pip install kaggle==2.2.4 && export KAGGLE_USER=<아이디> && python fetch_sources.py`.

## 쓰는 법

```bash
python build_ltx_batch.py jobs/ltx_example.json --slug ltx-test     # 노트북 만들기
python kg.py run ltx-test --to ./result                              # 올리기 → 대기 → 받기 → 삭제
python kg.py usage                                                   # 이번 주 사용 시간
```

자세한 순서 · 작업 파일 형식 · 오류 표는 **[CODEX.md](CODEX.md)** — AI 에게는 "batch/CODEX.md 를 읽고 그대로만 해"라고 시키면 된다.
이 폴더의 `AGENTS.md` · `CLAUDE.md` · `GEMINI.md` 는 이 폴더에서 연 AI 를 CODEX.md 로 안내한다.

## 출처 · 라이선스

- 빌더가 고쳐 쓰는 원본 노트북(설치할 때 Kaggle 에서 받음, 저장소에는 넣지 않음): AIQUEST Academy(`unlockbulk`) LTX-2.5, hangglewriter 한국어판 Krea 2 · ACE-Step · YuE2(원본 AIQUEST).
- 엔진 [Wan2GP](https://github.com/DeepBeepMeep/Wan2GP) · 모델 가중치는 각 저장소 라이선스를 따른다. YuE2 가중치는 CC BY-NC(비상업). LTX · Krea 상업 조건은 원문 확인.
