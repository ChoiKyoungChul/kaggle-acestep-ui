#!/bin/bash
# Runpod Pod 에서 ACE-Step 1.5 편집 화면(Gradio)을 자동 설치 · 실행한다.
# 템플릿 시작 명령: bash -c "curl -fsSL https://raw.githubusercontent.com/ChoiKyoungChul/kaggle-acestep-ui/main/runpod/start.sh | bash & exec /start.sh"
#   (/start.sh = runpod/pytorch 이미지 기본 시작 — SSH · Jupyter 유지)
# 접속: https://<Pod ID>-7860.proxy.runpod.net   진행 로그: /workspace/acestep.log
# 모델: 환경변수 ACE_MODEL (기본 acestep-v15-xl-base — 원곡 선율을 지키는 편곡용, 48GB GPU 권장)
exec > >(tee -a /workspace/acestep.log) 2>&1
set -e
MODEL="${ACE_MODEL:-acestep-v15-xl-base}"
echo "[$(date -u +%T)] ACE-Step 설치 시작 — 모델 $MODEL"
# 큰 파일은 컨테이너 디스크(/root)에 — /workspace 는 작게 둔다
export HF_HOME=/root/hf_cache UV_CACHE_DIR=/root/uv_cache UV_HTTP_TIMEOUT=300 UV_LINK_MODE=copy HF_HUB_ENABLE_HF_TRANSFER=1 MPLBACKEND=Agg
command -v uv > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
cd /root
[ -d ACE-Step-1.5 ] || git clone -q --depth 1 https://github.com/ace-step/ACE-Step-1.5.git
cd ACE-Step-1.5
hf() { uvx --with hf_transfer --from huggingface_hub hf download "$@"; }
# 모델 받기와 패키지 설치를 동시에
[ -f "checkpoints/$MODEL/config.json" ] || hf "ACE-Step/$MODEL" --local-dir "checkpoints/$MODEL" > /root/dl_model.log 2>&1 &
[ -d checkpoints/vae ] || hf ACE-Step/Ace-Step1.5 --local-dir checkpoints > /root/dl_main.log 2>&1 &
uv sync 2>&1 | tail -2
wait
echo "[$(date -u +%T)] 설치 끝 — 화면 시작 (모델을 GPU 에 올리는 데 1~2분)"
exec uv run acestep --server-name 0.0.0.0 --port 7860 --init_service true --config_path "$MODEL" --init_llm false
