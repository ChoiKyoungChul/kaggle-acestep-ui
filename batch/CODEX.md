# AI 용 Kaggle 일괄 작업 지침 — ACE-Step · Krea 2 · YuE2 · LTX-2.5 · Z-Image · Qwen · Wan 2.2

Codex · Claude Code · Gemini 등 AI 코딩 도구가 Kaggle 무료 GPU(T4 ×2, 주 30시간)로 곡 · 이미지 · 영상을 만들 때 **이 문서만 따른다.**
설치 · 노트북 작성 · 다른 방법 찾기를 하지 않는 것이 핵심이다. AI 가 헤매는 원인은 거의 다 "모델을 직접 설치하려다 막힌 것"이다.

## 0. 절대 하지 않는 것

- ACE-Step · Krea · YuE2 · LTX · Wan · Qwen · Z-Image 를 **PC 에 pip 로 설치하지 않는다.** 모델 GitHub 저장소를 clone 하지 않는다.
- **Kaggle 노트북을 새로 짜지 않는다.** 빌더(`build_*_batch.py`)가 만든 노트북이 Kaggle 안에서 설치 · 모델 받기 · 생성을 다 한다. PC 에 GPU 가 없어도 된다.
- 실행 중 로그가 안 보인다고 **다시 올리거나 다른 방법으로 넘어가지 않는다.** Kaggle 일괄 실행은 끝나야 로그를 준다. 상태가 `running` 이면 기다린다.
- 토큰 파일 내용을 출력하거나 채팅 · 문서 · 커밋에 적지 않는다.
- 사용자가 직접 만든 노트북 · 다른 창이 만든 노트북 · 결과 폴더는 지우지 않는다.

## 1. 시작 전 점검 (한 번)

```powershell
$env:PYTHONUTF8=1                     # 한국어 Windows cp949 오류 방지 — 모든 명령에 필요 (bash: export PYTHONUTF8=1)
python -m kaggle --version            # 없으면 pip install kaggle==2.2.4
Test-Path $HOME\.kaggle\access_token  # True 여야 한다 (내용은 보지 않는다)
python -m kaggle kernels list --mine  # 오류 없이 목록이 나오면 인증 OK
python fetch_sources.py               # 빌더가 읽는 원본 노트북 받기(처음 한 번)
```

- **계정 이름**: `$env:KAGGLE_USER="<Kaggle 아이디>"` 를 설정하거나 빌더에 `--user <아이디>` 를 붙인다. 토큰 계정과 다르면 push 가 `403` 으로 실패한다.
- 계정은 kaggle.com Settings 에서 **휴대폰 인증**이 되어 있어야 GPU · 인터넷이 붙는다.
- 이 작업은 인터넷(`kaggle` CLI)과 작업 폴더 쓰기가 필요하다. 샌드박스가 막으면 사용자에게 권한 허용을 요청하고, 우회 방법을 찾지 않는다.

## 2. 곡 (ACE-Step · YuE2)

1. 작업 파일 — 예시 `jobs/ace_example.json`
   ```json
   {"lyrics": "[Verse 1]\n...", "language": "ko", "seconds": 180, "bpm": 92, "key": "C major",
    "seeds": [7, 42], "styles": {"ballad": "영어 스타일 태그"}}
   ```
   반주만: lyrics 에 `[Instrumental]`, 스타일에 `no vocals`.
2. `python build_song_batch.py ace <작업.json> --slug ace-<이름>` (YuE2 는 `yue2`, 가중치 비상업)
3. `python kg.py run ace-<이름> --to <결과 폴더>` — 백그라운드로. 준비 약 9분 + 곡당 약 11분.
4. 결과 `<이름>-out/outputs/*` → **사용자가 직접 듣고 고른다.** STT 로 순위를 매기지 않는다.

## 3. 이미지 (Krea 2 Turbo)

`python build_krea_batch.py <job_img.json> --slug krea-<이름>` → `python kg.py run krea-<이름> --to <폴더>`
작업 파일 예시 `jobs/img_example.json` — 비율 `16:9hd`(1920×1088) · `9:16hd` · `16:9` · `9:16` · `4:3` · `3:4` · `1:1`. 1920×1088 장당 약 155초.

## 4. 영상 (LTX-2.5, 사진 → 5초 영상 + 소리) — HF 토큰 필요 없음

1. 작업 파일 — 예시 `jobs/ltx_example.json`. `src` 는 컷 이미지 폴더(작업 파일 기준), 이미지 이름 = 컷 `name`
   ```json
   {"src": "ltx_example_img", "seed": 4242, "style": "모든 컷 공통 문구(카메라 · 빛 · 소리)",
    "shots": [{"name": "c01", "secs": 5, "prompt": "이 컷의 움직임 · 소리"}]}
   ```
2. `python build_ltx_batch.py <작업.json> --slug ltx-<이름> [--res 704|480] [--only c01,c02]`
3. `python kg.py run ltx-<이름> --to <폴더>` → `outputs/<컷>.mp4` (1280×704 · 24fps · 소리)

실측(2026-11-02, T4 ×2): 모델 39.6GB 받기 약 3분, 704p 5초 컷 약 6분, 1컷 세션 전체 약 14분. 10컷 ≈ 70분. 빠르게는 `--res 480`.

## 5. Z-Image · Qwen-Image · Wan 2.2 (Wan2GP 엔진, 11/2 실측)

`build_wgp_batch.py` 가 Wan2GP 엔진의 일괄 API 로 돌린다. 모델은 엔진이 DeepBeepMeep 저장소에서 받는다(HF 토큰 필요 없음). 결과 이미지는 jpg.
```
python build_wgp_batch.py zimage <job_img.json> --slug zimg-<이름>          # Krea 와 같은 작업 파일
python build_wgp_batch.py qwen   <job_img.json> --slug qwen-<이름> [--steps 15]
python build_wgp_batch.py wan    <ltx_shots 형식.json> --slug wan-<이름> [--res 832x480]
```

| 모델 | 1개 시간 (T4 ×2) | 세션 전체 | 판단 |
|---|---|---|---|
| Z-Image Turbo | 1920×1088 약 200초(모델 받기 포함) | 약 9분 | 쓸 만함 — Krea 와 함께 이미지 기본 |
| Qwen-Image 2512 (20B, 30스텝) | 1920×1088 약 17분 | 약 22분 | 느림 — 꼭 필요한 컷만, `--steps 15` 로 줄여 쓰기 |
| Wan 2.2 I2V Lightning (14B ×2) | 1280×720 5초 **약 82분** | 약 84분 | 너무 느림(RAM 31GB 부족으로 모델 일부만 고정) — **영상은 LTX 를 쓴다**. 꼭 Wan 이면 `--res 832x480` 또는 Runpod |

## 6. 끝나면

`python kg.py usage` 로 이번 주 사용 시간 · 남은 시간을 사용자에게 알린다(주 30시간, 토요일 09:00 KST 초기화).

## 7. 오류가 나면 — 이 표부터

| 증상 | 원인 | 할 일 |
|---|---|---|
| `UnicodeEncodeError: 'cp949'` | 한국어 Windows 인코딩 | `PYTHONUTF8=1` 후 다시 |
| `Kaggle 아이디가 없습니다` | `KAGGLE_USER` 미설정 | `--user <아이디>` 또는 환경변수 |
| push `403` · `Permission denied` | 빌더 계정 ≠ 토큰 계정 | 계정 이름 확인 |
| `401 Unauthenticated` | 토큰 없음 · 만료 | Settings › API › Create New Token → `~/.kaggle/access_token` |
| 빌더가 `FileNotFoundError` | 원본 노트북 안 받음 | `python fetch_sources.py` |
| `Maximum batch GPU session count of 2 reached` | 계정당 GPU 동시 2개 | kg.py 가 90초마다 재시도 — 기다린다 |
| `running` 이 오래 그대로 | 정상(준비 + 생성 시간) | 기다린다. 재업로드 금지 |
| 상태 `error` | 노트북 안 오류 | `<이름>-out/*.log` 를 읽고 **빌더를 고친다** |
| GPU 가 안 붙음 · `Internet disabled` | 휴대폰 인증 안 됨 | 사용자에게 kaggle.com 휴대폰 인증 요청 |
| 소리가 깨짐 · NaN | T4 에서 int8 · bf16 | 빌더 기본값 유지 |
| `'kaggle' is not recognized` | pip Scripts 가 PATH 에 없음 | `python -m kaggle …` (kg.py 는 자동 대체) |
