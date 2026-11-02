# Kaggle 일괄 실행 준비 — 이 폴더에서:  powershell -ExecutionPolicy Bypass -File setup.ps1 -User <Kaggle 아이디>
param([string]$User = "")
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$env:PYTHONUTF8 = "1"

Write-Host "[1/4] kaggle CLI"
python -m pip install --quiet "kaggle==2.2.4"   # 검증한 버전으로 고정
python -m kaggle --version

Write-Host "[2/4] 계정 이름"
if ($User) {
    [Environment]::SetEnvironmentVariable("KAGGLE_USER", $User, "User")
    $env:KAGGLE_USER = $User
    Write-Host "  KAGGLE_USER=$User (사용자 환경변수로 저장, 새 창부터 적용)"
} elseif (-not $env:KAGGLE_USER) {
    Write-Host "  -User <아이디> 로 다시 실행하세요 (빌더가 노트북 주인 이름으로 씁니다)" -ForegroundColor Yellow
    exit 1
}

Write-Host "[3/4] 토큰 · 인증 확인"
if (-not (Test-Path "$HOME\.kaggle\access_token")) {
    Write-Host "  토큰 없음: kaggle.com > Settings > API > Create New Token 후 $HOME\.kaggle\access_token 에 저장하고 다시 실행" -ForegroundColor Yellow
    exit 1
}
python -m kaggle kernels list --mine --page-size 3

Write-Host "[4/4] 원본 노트북 받기"
python fetch_sources.py
Write-Host "완료. 휴대폰 인증이 안 된 계정이면 GPU 가 붙지 않습니다 (kaggle.com Settings)." -ForegroundColor Green
Write-Host "AI 에게는 'batch/CODEX.md 를 읽고 그대로만 해' 라고 요청하세요."
