$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$kitZip = Join-Path $packageRoot 'kaggle_kit_v3_ltx.zip'
$skillSource = Join-Path $packageRoot 'kaggle-free-gpu\SKILL.md'
$kaggleFolder = Join-Path $env:USERPROFILE 'kaggle'
$doneMarker = Join-Path $kaggleFolder '.install-complete'

function Get-PythonInfo {
    try {
        $output = (& python --version 2>&1 | Out-String).Trim()
        $match = [regex]::Match($output, 'Python\s+(\d+)\.(\d+)\.(\d+)')
        if ($match.Success) {
            return [pscustomobject]@{
                Version = [version]::new([int]$match.Groups[1].Value, [int]$match.Groups[2].Value, [int]$match.Groups[3].Value)
                Output = $output
            }
        }
    } catch { }
    return $null
}

function Test-TokenFile([string]$path) {
    return (Test-Path -LiteralPath $path) -and ((Get-Item -LiteralPath $path).Length -gt 0)
}

function Add-PythonToPath {
    # 방금 설치한 Python 을 이 설치 창(과 하위 setup.ps1)에서 바로 쓰도록 PATH 앞에 붙인다.
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$user;$machine"
    $candidates = @(Get-ChildItem -Path (Join-Path $env:LOCALAPPDATA 'Programs\Python') -Directory -Filter 'Python3*' -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending | Where-Object { Test-Path (Join-Path $_.FullName 'python.exe') })
    if ($candidates.Count -gt 0) {
        $dir = $candidates[0].FullName
        $env:Path = "$dir;$dir\Scripts;$env:Path"
    }
}

function Install-PythonAuto {
    # winget 으로 사용자 계정에만(관리자 권한 없이) Python 3.12 를 설치한다. 실패하면 $false.
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if (-not $winget) { Write-Host '  winget(앱 설치 관리자)이 없어 자동 설치를 할 수 없습니다.' -ForegroundColor Yellow; return $false }
    Write-Host 'Python 3.12 를 자동으로 설치합니다. 몇 분 걸릴 수 있습니다…' -ForegroundColor Cyan
    & $winget.Source install --id Python.Python.3.12 -e --source winget --scope user --silent `
        --accept-package-agreements --accept-source-agreements `
        --override '/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 InstallLauncherAllUsers=0'
    if ($LASTEXITCODE -ne 0) { Write-Host "  winget 설치 실패 (코드 $LASTEXITCODE)" -ForegroundColor Yellow }
    Add-PythonToPath
    return [bool](Get-PythonInfo)
}

function Show-Result([bool]$ok, [string]$detail) {
    $line = '=' * 56
    Write-Host ''
    if ($ok) {
        Write-Host $line -ForegroundColor Green
        Write-Host '  [성공] 설치가 완료되었습니다.' -ForegroundColor Green
        Write-Host $line -ForegroundColor Green
    } else {
        Write-Host $line -ForegroundColor Red
        Write-Host '  [실패] 설치가 끝나지 않았습니다.' -ForegroundColor Red
        Write-Host $line -ForegroundColor Red
    }
    if ($detail) { Write-Host $detail }
    Write-Host ''
    Write-Host '아무 키나 누르면 이 창이 닫힙니다.'
}

$extractRoot = $null
try {
    Write-Host 'Kaggle 무료 GPU 풀패키지 설치를 시작합니다.' -ForegroundColor Cyan
    Write-Host 'Kaggle 사용자명과 토큰 발급은 본인이 직접 처리합니다. 토큰을 AI 채팅에 붙여 넣지 마세요.'

    if (-not (Test-Path -LiteralPath $kitZip)) { throw 'kaggle_kit_v3_ltx.zip 파일을 찾을 수 없습니다.' }
    if (-not (Test-Path -LiteralPath $skillSource)) { throw 'kaggle-free-gpu\SKILL.md 파일을 찾을 수 없습니다.' }

    # 설치를 끝까지 마친 PC만 건너뛴다. 폴더만 있고 표시 파일이 없으면(중간 실패 · 예전 설치) 연결 확인을 다시 한다.
    $installDone = Test-Path -LiteralPath $doneMarker
    # 이미 작업 중인 kaggle 폴더(kg.py 있음)는 파일을 덮어쓰지 않는다.
    $keepExistingFiles = Test-Path -LiteralPath (Join-Path $kaggleFolder 'kg.py')

    if ($installDone) {
        Write-Host '이 PC는 Kaggle 키트 설치와 연결 확인을 이미 마쳤습니다. AI 스킬만 다시 등록합니다.' -ForegroundColor Yellow
    } else {
        if ($keepExistingFiles) {
            Write-Host '기존 kaggle 폴더를 발견했습니다. 파일은 덮어쓰지 않고 Kaggle CLI 설치와 계정 연결만 확인합니다.' -ForegroundColor Yellow
        }
        $python = Get-PythonInfo
        if (-not $python -or $python.Version -lt [version]'3.10') {
            Write-Host 'Python 3.10 이상이 없습니다.' -ForegroundColor Yellow
            if (Install-PythonAuto) { $python = Get-PythonInfo }
        }
        if (-not $python -or $python.Version -lt [version]'3.10') {
            Write-Host 'Python 자동 설치에 실패했습니다. Python 설치 페이지를 열겠습니다.' -ForegroundColor Yellow
            Start-Process 'https://www.python.org/downloads/windows/'
            throw 'Python 3.10 이상을 설치하고 설치 화면에서 "Add python.exe to PATH"를 선택한 뒤 INSTALL.cmd를 다시 실행해 주세요.'
        }
        Write-Host "Python 확인: $($python.Output)"

        $defaultUser = [Environment]::GetEnvironmentVariable('KAGGLE_USER', 'User')
        if ($defaultUser) {
            $kaggleUser = Read-Host "Kaggle 사용자명을 입력하세요 (이메일 주소가 아닌 프로필 아이디, Enter = $defaultUser)"
            if ([string]::IsNullOrWhiteSpace($kaggleUser)) { $kaggleUser = $defaultUser }
        } else {
            $kaggleUser = Read-Host 'Kaggle 사용자명을 입력하세요 (이메일 주소가 아닌 프로필 아이디)'
        }
        if ([string]::IsNullOrWhiteSpace($kaggleUser)) { throw 'Kaggle 사용자명이 필요합니다.' }
        $kaggleUser = $kaggleUser.Trim()
        if ($kaggleUser -match '@') { throw '이메일 주소가 아니라 Kaggle 프로필 아이디(kaggle.com/<아이디>)를 입력해 주세요.' }

        $tokenDir = Join-Path $env:USERPROFILE '.kaggle'
        $tokenPath = Join-Path $tokenDir 'access_token'
        if (-not (Test-TokenFile $tokenPath)) {
            New-Item -ItemType Directory -Force -Path $tokenDir | Out-Null
            if (-not (Test-Path -LiteralPath $tokenPath)) { New-Item -ItemType File -Path $tokenPath | Out-Null }
            Write-Host ''
            Write-Host '브라우저의 Kaggle 설정과 메모장이 열립니다.' -ForegroundColor Yellow
            Write-Host '  1) Kaggle Settings > API > Create New Token 으로 토큰을 발급합니다.'
            Write-Host '  2) 메모장에 토큰을 붙여 넣고 저장(Ctrl+S)합니다. 토큰은 이 파일에만 넣으세요.'
            Write-Host '  3) 이 창으로 돌아와 Enter 를 누릅니다.'
            Start-Process 'https://www.kaggle.com/settings'
            # Windows 11 메모장은 탭으로 열리면 바로 끝나므로 기다리지 않고 Enter 로 확인한다.
            Start-Process -FilePath 'notepad.exe' -ArgumentList ('"{0}"' -f $tokenPath)
            $tries = 0
            while (-not (Test-TokenFile $tokenPath)) {
                $tries++
                if ($tries -gt 1) { Write-Host '토큰 파일이 아직 비어 있습니다. 메모장에서 저장(Ctrl+S)했는지 확인해 주세요.' -ForegroundColor Yellow }
                if ($tries -gt 5) { throw '토큰 파일이 비어 있습니다. Kaggle Settings > API에서 토큰을 저장한 뒤 다시 실행해 주세요.' }
                [void](Read-Host '토큰을 저장했으면 Enter 를 누르세요')
            }
            Write-Host '토큰 파일 저장을 확인했습니다. 토큰 내용은 읽지 않았습니다.'
        } else {
            Write-Host '기존 Kaggle 토큰 파일을 확인했습니다. 토큰 내용은 읽지 않았습니다.'
        }

        # 실행마다 새 임시 폴더를 만들고, 이 실행이 만든 폴더만 마지막에 지운다.
        $extractRoot = Join-Path $env:TEMP ('kaggle-free-gpu-kit-' + [guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $extractRoot | Out-Null
        Expand-Archive -LiteralPath $kitZip -DestinationPath $extractRoot -Force
        $setupScript = Join-Path $extractRoot 'kaggle_kit\setup.ps1'
        if (-not (Test-Path -LiteralPath $setupScript)) { throw '설치 묶음 안에서 setup.ps1을 찾지 못했습니다.' }

        Write-Host 'Kaggle 작업 도구와 명령줄 프로그램을 설치하고 계정 연결을 확인합니다.' -ForegroundColor Cyan
        if ($keepExistingFiles) {
            & $setupScript -User $kaggleUser -SkipCopy
        } else {
            & $setupScript -User $kaggleUser
        }
        if ($LASTEXITCODE -ne 0) { throw 'Kaggle 연결 확인에 실패했습니다. 휴대폰 인증과 사용자명/토큰 계정을 확인한 뒤 INSTALL.cmd를 다시 실행해 주세요.' }

        New-Item -ItemType Directory -Force -Path (Join-Path $kaggleFolder 'jobs') | Out-Null
        Set-Content -LiteralPath $doneMarker -Value ("installed {0} user={1}" -f (Get-Date -Format s), $kaggleUser) -Encoding ASCII
    }

    $skillTargets = @(
        (Join-Path $env:USERPROFILE '.codex\skills\kaggle-free-gpu'),
        (Join-Path $env:USERPROFILE '.claude\skills\kaggle-free-gpu'),
        (Join-Path $env:USERPROFILE '.gemini\config\skills\kaggle-free-gpu')
    )
    foreach ($target in $skillTargets) {
        New-Item -ItemType Directory -Force -Path $target | Out-Null
        Copy-Item -LiteralPath $skillSource -Destination (Join-Path $target 'SKILL.md') -Force
    }

    $exitCode = 0
    Show-Result $true ("다음 순서:`n  1) Codex, Claude Code, Antigravity 중 사용하는 앱을 닫았다가 다시 여세요.`n" +
        "  2) kaggle 폴더($kaggleFolder)를 열고 `"Kaggle 연결 상태를 확인해 줘`"라고 요청하세요.`n" +
        "  ※ GPU 시험 생성은 Kaggle 사용 시간을 쓰므로 원할 때 따로 실행합니다.")
} catch {
    $exitCode = 1
    Show-Result $false ("원인: $($_.Exception.Message)`n안내대로 고친 뒤 INSTALL.cmd 를 다시 실행하면 이어서 확인합니다.")
} finally {
    if ($extractRoot -and (Test-Path -LiteralPath $extractRoot)) {
        Remove-Item -LiteralPath $extractRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
exit $exitCode
