# Kaggle 무료 GPU 자동 연동 설치 프로그램 (v3)

Windows PC 에서 **`INSTALL.cmd` 더블클릭 한 번**으로 Kaggle 무료 GPU 작업 도구를 설치하고, Codex · Claude Code · Google Antigravity 에 `kaggle-free-gpu` 스킬을 등록한다.
AI 채팅에서 "노래 만들어 줘", "이미지 뽑아 줘" 라고 하면 Kaggle 무료 T4 에서 ACE-Step · YuE2(곡) · Krea 2(이미지) · LTX-2.5(영상)를 돌린다. 모델은 PC 에 설치하지 않는다.

## ⬇️ 내려받기

**[kaggle-free-gpu-full-package-v3.zip 내려받기](https://github.com/ChoiKyoungChul/kaggle-acestep-ui/releases/download/kaggle-kit-v3/kaggle-free-gpu-full-package-v3.zip)** (약 190KB)

## 설치 요약

1. ZIP 을 내려받아 **모두 압축 풀기** → `INSTALL.cmd` 더블클릭
2. Kaggle 프로필 **사용자명** 입력(이메일 아님) · 휴대폰 인증이 안 됐으면 먼저 인증
3. 토큰이 없으면 브라우저와 메모장이 열린다 → Kaggle **Settings → API → Create New Token** 값을 메모장에 붙여 저장 → 설치 창에서 Enter
4. **[성공]** 이 뜨면 AI 앱을 닫았다가 다시 연다

자세한 안내 · 주의 사항: [START_HERE_KO.md](START_HERE_KO.md) · 스킬 내용: [kaggle-free-gpu/SKILL.md](kaggle-free-gpu/SKILL.md)

## 들어 있는 것

| 파일 | 내용 |
|---|---|
| `INSTALL.cmd` | 설치 시작(더블클릭) |
| `Install-FullPackage.ps1` | 실제 설치 스크립트 — Python 3.12 자동 설치(winget), Kaggle CLI, 계정 연결 확인, 스킬 등록 |
| `kaggle_kit_v3_ltx.zip` | Kaggle 작업 도구(`%USERPROFILE%\kaggle`) — 빌더 · 노트북 원본 · `kg.py` |
| `kaggle-free-gpu/SKILL.md` | AI 도구용 스킬 |
| `START_HERE_KO.md` | 처음 쓰는 사람용 안내 |

## 주의

- **토큰은 절대 AI 채팅에 붙이지 않는다.** 토큰은 `%USERPROFILE%\.kaggle\access_token` 에만 저장되고 이 ZIP 에는 들어 있지 않다.
- 기존 `%USERPROFILE%\kaggle` 폴더의 파일은 덮어쓰지 않는다.
- Kaggle 무료 GPU 는 계정당 주 30시간 · 동시 2개까지다. 첫 GPU 확인 · 시험 생성은 시간을 쓰므로 자동으로 하지 않는다.
- 빌더의 기본 계정 이름(motionchoi)은 설치할 때 입력한 사용자명으로 바뀐다.
