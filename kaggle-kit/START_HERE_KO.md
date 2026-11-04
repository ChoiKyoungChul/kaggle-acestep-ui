# Kaggle 무료 GPU 풀패키지 설치 안내

## 이 ZIP으로 설치할 수 있는 것

- Kaggle 작업 도구와 ACE-Step·YuE2·Krea·LTX용 빌더
- Kaggle CLI와 계정 연결 확인
- Codex·Claude Code·Google Antigravity에서 함께 쓸 `kaggle-free-gpu` 스킬

이 파일은 `.exe`가 아닙니다. ZIP 안의 `INSTALL.cmd`를 더블클릭하면 PowerShell 설치 스크립트가 실행됩니다. 모델을 PC에 설치하지 않으며, 생성은 Kaggle에서 합니다.

## 설치 순서

1. ZIP 파일을 내려받아 마우스 오른쪽 버튼을 누르고 **모두 압축 풀기**를 선택합니다.
2. 압축을 푼 폴더를 열고 **`INSTALL.cmd`를 더블클릭**합니다.
3. Kaggle 프로필의 사용자명을 입력합니다. 이메일 주소가 아닙니다.
4. Kaggle 휴대폰 인증이 안 되어 있으면 먼저 인증합니다.
5. 토큰 파일이 없는 PC에서는 브라우저와 메모장이 열립니다. Kaggle **Settings → API → Create New Token**에서 발급한 토큰을 메모장에 붙여 넣고 저장(Ctrl+S)한 뒤 설치 창으로 돌아와 Enter 를 누릅니다. 토큰을 Codex·Claude·Antigravity 채팅에 붙이지 마세요.
6. 설치가 끝나면 사용하는 AI 앱을 닫았다가 다시 엽니다.

Python 3.10 이상이 없으면 설치기가 Windows 기본 앱 설치 관리자(winget)로 Python 3.12를 자동 설치합니다(관리자 권한 불필요). winget이 없거나 자동 설치가 실패하면 공식 Python 다운로드 페이지를 열고 멈춥니다. 그때는 설치 화면에서 **Add python.exe to PATH**를 선택해 설치한 뒤 `INSTALL.cmd`를 다시 실행하세요.

설치가 끝나면 창에 **[성공]** 또는 **[실패]**가 크게 표시됩니다. 실패하면 원인 문구를 확인하고 고친 뒤 다시 실행하면 됩니다. 아무 키나 누르면 창이 닫힙니다.

## 설치 후 사용

AI 앱에서 `%USERPROFILE%\kaggle` 폴더를 열고 다음처럼 요청합니다.

> Kaggle README를 읽고 계정 연결과 쿼터를 확인해 줘. 토큰 내용은 열거나 출력하지 마.

스킬 직접 호출은 Codex에서 `$kaggle-free-gpu`, Claude Code와 Antigravity에서 `/kaggle-free-gpu`입니다. 설치기는 세 도구의 사용자 전역 스킬 위치에 파일을 복사합니다.

설치기는 토큰과 Kaggle CLI 연결만 확인합니다. 첫 GPU 확인이나 시험곡 생성은 Kaggle 무료 GPU 시간을 쓰므로 자동으로 실행하지 않습니다.

## 주의 사항

- 기존 `%USERPROFILE%\kaggle` 폴더가 있어도 그 안의 파일은 덮어쓰지 않습니다. 같은 이름의 파일은 건너뛰고 없는 파일만 채우며, 건너뛴 파일 목록을 화면에 보여 줍니다. 이미 작업 중인 키트(`kg.py` 있음)면 파일은 아예 복사하지 않고 Kaggle CLI 설치와 계정 연결만 확인합니다.
- 설치가 중간에 실패해도 `INSTALL.cmd`를 다시 실행하면 처음부터 다시 확인합니다. 끝까지 마치면 `%USERPROFILE%\kaggle\.install-complete` 파일이 생기고, 그다음부터는 AI 스킬만 다시 등록합니다.
- Kaggle 사용자명과 토큰은 같은 계정이어야 합니다.
- 토큰은 `%USERPROFILE%\.kaggle\access_token`에만 저장합니다. 배포 ZIP에는 토큰이 없습니다.
- PowerShell 실행 정책은 설치를 실행하는 프로세스에만 우회 옵션을 적용합니다. Windows 전체 설정은 바꾸지 않습니다.
- 연결 오류가 나면 휴대폰 인증, Kaggle 아이디, 토큰 파일을 확인하고 설치기를 다시 실행하세요. 새 토큰은 다른 PC의 기존 토큰을 무효화할 수 있으니 필요할 때만 발급하세요.
