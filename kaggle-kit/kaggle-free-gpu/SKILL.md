---
name: kaggle-free-gpu
description: Set up and use the user's Windows Kaggle kit for free-GPU generation with ACE-Step or YuE2 songs, Krea images, and LTX videos. Use when a user asks to connect Kaggle, prepare a PC, or create media through the provided builders.
metadata:
  short-description: Kaggle 무료 GPU 연결 및 제작
---

# Kaggle 무료 GPU 작업

이 스킬은 Codex, Claude Code, Google Antigravity에서 공통으로 쓸 수 있는 `SKILL.md` 형식이다. 각 도구에 스킬 폴더를 따로 등록해야 하며, 한 도구에 등록했다고 다른 도구에도 자동 등록되지는 않는다. 초보자에게는 쉬운 말로 한 단계씩 안내하고, 계정 인증처럼 사람이 직접 해야 하는 단계만 요청한다.

## 먼저 확인할 것

- Windows의 기본 키트 폴더는 `%USERPROFILE%\kaggle`이다. 이미 준비된 PC에서는 작업 전 `README.md`와 `CODEX.md`를 읽는다. 새 PC의 준비 절차는 배포 묶음의 `START_HERE_KO.md`를 따른다.
- 제공된 키트와 그 안의 최신 `README.md`를 기준으로 한다. 참고 페이지: [Kaggle GPU setup](https://tall-red-1ed.notion.site/Kaggle-GPU-Claude-Code-Codex-2026-10-3f8564bf1d2381c3bcdceb7391b6f7fb).
- Kaggle API 토큰은 OpenAI API 키가 아니다. ACE-Step, YuE2, Krea를 PC에 설치하지 않고, 제공된 빌더가 지원하면 새 노트북을 직접 만들지 않는다. 생성은 Kaggle 노트북에서 한다.
- 토큰 파일은 존재 여부만 확인한다. 내용을 읽거나 출력하거나 복사하지 말고, 채팅으로 보내 달라고 하지 않는다. 인증은 계정의 `kg.py list` 명령으로 확인한다.
- 토큰은 채팅, Notion, 작업 JSON, 로그, 스크린샷, ZIP, 버전 관리에 넣지 않는다. 사용자가 Kaggle 가입, 휴대폰 인증, 토큰 발급을 직접 한다. Kaggle 사용자명을 알 수 없을 때만 사용자명을 물어본다. 사용자명은 비밀이 아니다.
- 새 PC의 첫 설치는 풀패키지 ZIP을 풀고 **`INSTALL.cmd`를 더블클릭**하는 것이 시작점이다. `INSTALL.cmd`가 Python 확인(없으면 winget으로 3.12 자동 설치, 실패하면 다운로드 페이지 안내) → 토큰 저장 안내 → 키트의 `setup.ps1` 실행 → 스킬 등록까지 한다. `setup.ps1`을 직접 실행하는 것은 키트만 따로 받은 경우의 수동 절차다. 사용자는 Kaggle 가입·휴대폰 인증·토큰 발급을 직접 해야 하고, winget이 없는 PC에서는 Python도 직접 설치해야 하므로 완전 자동 설치라고 말하지 않는다. 새 PC에서 시험하지 않았다면 설치가 검증됐다고 말하지 않는다.

## AI 도구에 스킬 등록하기

스킬 파일은 `kaggle-free-gpu\SKILL.md`이다. 폴더 이름을 `kaggle-free-gpu`로 유지해 각 도구의 스킬 위치에 폴더째 복사한다. 아래 경로의 `<사용자>`는 Windows 계정 폴더다.

- Codex: `%USERPROFILE%\.codex\skills\kaggle-free-gpu\SKILL.md`
- Claude Code: `%USERPROFILE%\.claude\skills\kaggle-free-gpu\SKILL.md`
- Google Antigravity 앱/IDE 전역: `%USERPROFILE%\.gemini\config\skills\kaggle-free-gpu\SKILL.md`
- Google Antigravity 프로젝트 전용: `<프로젝트폴더>\.agents\skills\kaggle-free-gpu\SKILL.md`

Codex는 스킬 메뉴에서 등록하거나 위 사용자 스킬 폴더에 복사한다. Claude Code와 Antigravity는 새 대화/세션을 열면 스킬을 찾는다. Claude Code와 Antigravity에서는 `/kaggle-free-gpu`로 직접 호출할 수 있고, Codex에서는 `$kaggle-free-gpu`로 호출하거나 관련 요청에서 자동 사용하게 한다. Antigravity에서는 에이전트 설정의 Customizations에서 발견 여부를 확인할 수 있다.

## 첫 연결

1. 필요하면 사용자가 브라우저에서 Kaggle 가입과 휴대폰 인증을 완료하도록 안내한다.
2. 유효한 토큰 파일이 없으면 Kaggle **Settings → API → Create New Token**으로 발급하라고 안내한다. 새 토큰을 만들면 다른 PC의 기존 토큰이 무효가 될 수 있다. 사용자가 자신의 PC에 저장하고, 토큰은 대화로 전달하지 않는다.
3. 기본 토큰 위치는 `%USERPROFILE%\.kaggle\access_token`이다. 두 번째 계정은 `%USERPROFILE%\.kaggle-<username>\access_token`을 쓰고, 각 명령에 계정별 환경 변수를 지정한다.
4. 풀패키지가 있으면 `INSTALL.cmd`를 실행하게 한다. 키트 ZIP만 있는 경우에만 압축을 푼 키트 폴더에서 `setup.ps1 -User <username>`을 실행한다. 다른 설치 절차를 만들지 않는다. 설치가 실패해도 `INSTALL.cmd`를 다시 실행하면 처음부터 다시 확인한다(`%USERPROFILE%\kaggle\.install-complete`가 생겨야 완료).
5. 새 PowerShell 창에서 계정 설정과 `PYTHONUTF8=1`을 지정한다. 두 번째 계정은 다음과 같이 실행한다.

   ```powershell
   $env:PYTHONUTF8 = '1'
   $env:KAGGLE_USER = '<username>'
   $env:KAGGLE_CONFIG_DIR = Join-Path $env:USERPROFILE '.kaggle-<username>'
   ```

6. `python kg.py list`와 키트의 쿼터 명령으로 확인한다. 새 PC에서는 GPU 쿼터를 쓰는 점을 먼저 설명한 뒤 `gpu-check`와 짧은 생성 시험을 한다. 토큰 파일 내용을 열어 인증 문제를 해결하려 하지 않는다.

## 작업 만들고 실행하기

키트에 있는 작업 JSON 형식과 빌더만 쓴다.

- 이미지(Krea): `python build_krea_batch.py <job.json> --slug <unique-name>`
- 곡(ACE-Step): `python build_song_batch.py ace <job.json> --slug <unique-name>`
- 곡(YuE2): `python build_song_batch.py yue2 <job.json> --slug <unique-name>`
- 영상(LTX): `python build_ltx_batch.py <shots.json> --slug <unique-name>`

그다음 `python kg.py run <unique-name> --to <destination>`을 백그라운드로 실행한다. Windows에서는 `PYTHONUTF8=1`을 설정한다. 기본 계정이 아니면 그 프로세스에 `KAGGLE_USER`와 `KAGGLE_CONFIG_DIR`도 설정한다. 매 요청마다 고유한 slug를 쓰고 예상 대기 시간을 알려준다. 실행 중 Kaggle이 상태만 보여 줄 수 있다. 완료될 때까지 기다리고 같은 작업을 중복 제출하지 않는다.

곡은 요청에 맞춰 가사, 언어, 길이, BPM, 조성, seeds, styles를 작업 JSON에 작성한다. ACE-Step 또는 YuE2 중 사용자가 고른 모델을 사용한다. 빠진 음악 정보는 무리 없이 정하거나 곡에 큰 영향을 주는 항목만 질문한다. 아티스트를 참고할 때는 일반적인 음악적 특성을 설명해 독창적인 곡을 만든다. 생존 아티스트의 고유한 창법이나 특정 곡을 그대로 복제하지 않는다. 생성된 오디오 파일을 제공해 사용자가 직접 듣고 고르게 하며 STT로 순위를 매기지 않는다.

## 기존 작업 보호

- 다른 사용자의 노트북, 결과 폴더, 토큰을 삭제하거나 덮어쓰지 않는다. 고유 slug를 쓰고 빌더 실행 전 같은 이름이 있는지 확인한다.
- 계정은 GPU 배치 작업을 동시에 최대 2개까지 실행할 수 있다. 한도에 도달하면 기존 작업을 확인하고 끝날 때까지 기다린다. 중복 작업을 만들지 않는다.
- 실패하면 해당 실행의 출력 로그를 읽고 입력이나 해당 빌더를 고친다. 무관한 모델 설치 방법으로 처음부터 다시 시작하지 않는다.
