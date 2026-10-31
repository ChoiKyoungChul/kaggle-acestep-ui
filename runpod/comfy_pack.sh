#!/bin/bash
# Runpod 공식 ComfyUI 이미지(runpod/comfyui, CUDA 12.8) 위에 모델 묶음을 자동으로 받는다.
# 템플릿 시작 명령: bash -c "curl -fsSL https://raw.githubusercontent.com/ChoiKyoungChul/kaggle-acestep-ui/main/runpod/comfy_pack.sh | bash & exec /start.sh"
# 환경변수 COMFY_PACKS = "krea zimage qwen wan s2v ltx" 중 원하는 것(띄어쓰기로 여럿)
#   ltx 는 잠긴 저장소 → Pod 환경변수 HF_TOKEN 필요(Hugging Face 에서 Lightricks/LTX-2.5 접근 동의 후 토큰)
# 진행 로그: /workspace/comfy_pack.log · 끝나면 ComfyUI(포트 8188) 의 Templates 에서 해당 모델 워크플로를 열면 된다
exec > >(tee -a /workspace/comfy_pack.log) 2>&1
PACKS="${COMFY_PACKS:-krea zimage}"
C=/workspace/runpod-slim/ComfyUI; M=$C/models
L=/models_local; mkdir -p $L   # /workspace(네트워크 디스크)에 큰 파일을 동시에 쓰면 멈춘다 → 컨테이너 디스크 + 링크
echo "[$(date -u +%T)] 모델 묶음: $PACKS — ComfyUI 준비를 기다린다"
for i in $(seq 1 120); do [ -d $M ] && break; sleep 5; done
[ -d $M ] || { echo "ComfyUI 폴더가 10분 안에 안 생김 — 중단"; exit 1; }

Z=https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files
K=https://huggingface.co/Comfy-Org/Krea-2/resolve/main
Q=https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files
W=https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files
X=https://huggingface.co/Lightricks/LTX-2.5/resolve/main
g(){ mkdir -p $M/$1; [ -f $L/$2 ] && { ln -sf $L/$2 $M/$1/$2; echo "있음 $2"; return; }
  curl -sfL --retry 5 ${4:+-H "Authorization: Bearer $4"} -o $L/$2.part "$3" && mv $L/$2.part $L/$2 && ln -sf $L/$2 $M/$1/$2 && echo "받음 $2" || echo "실패 $2"; }
NEED_MASTER=0
for m in $PACKS; do case $m in
  zimage)  # ~20GB, Apache 2.0
    g diffusion_models z_image_turbo_bf16.safetensors $Z/diffusion_models/z_image_turbo_bf16.safetensors &
    g text_encoders qwen_3_4b.safetensors $Z/text_encoders/qwen_3_4b.safetensors &
    g vae ae.safetensors $Z/vae/ae.safetensors & ;;
  krea)    # ~19GB, Krea-2 Community License(연 매출 100만 달러 미만 상업 무료)
    g diffusion_models krea2_turbo_fp8_scaled.safetensors $K/diffusion_models/krea2_turbo_fp8_scaled.safetensors &
    g text_encoders qwen3vl_4b_fp8_scaled.safetensors $K/text_encoders/qwen3vl_4b_fp8_scaled.safetensors &
    g vae qwen_image_vae.safetensors $K/vae/qwen_image_vae.safetensors & ;;
  qwen)    # ~30GB, Apache 2.0
    g diffusion_models qwen_image_2512_fp8_e4m3fn.safetensors $Q/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors &
    g text_encoders qwen_2.5_vl_7b_fp8_scaled.safetensors $Q/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors &
    g vae qwen_image_vae.safetensors $Q/vae/qwen_image_vae.safetensors & ;;
  wan)     # ~37GB, Apache 2.0 — Wan 2.2 I2V 14B + 4스텝 LoRA
    g diffusion_models wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors $W/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors &
    g diffusion_models wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors $W/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors &
    g text_encoders umt5_xxl_fp8_e4m3fn_scaled.safetensors $W/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors &
    g vae wan_2.1_vae.safetensors $W/vae/wan_2.1_vae.safetensors &
    g loras wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors $W/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors &
    g loras wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors $W/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors & ;;
  s2v)     # ~18GB 추가 — Wan 2.2 S2V 립싱크(wan 과 함께)
    g diffusion_models wan2.2_s2v_14B_fp8_scaled.safetensors $W/diffusion_models/wan2.2_s2v_14B_fp8_scaled.safetensors &
    g audio_encoders wav2vec2_large_english_fp16.safetensors $W/audio_encoders/wav2vec2_large_english_fp16.safetensors &
    g loras wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors $W/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors & ;;
  ltx)     # ~40GB, 48GB GPU — 잠긴 저장소(HF_TOKEN), ComfyUI master 필요
    [ -n "$HF_TOKEN" ] || { echo "ltx: HF_TOKEN 환경변수가 없어 건너뜀"; continue; }
    NEED_MASTER=1
    g diffusion_models ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors $X/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors "$HF_TOKEN" &
    g text_encoders gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors $X/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors "$HF_TOKEN" &
    g vae ltx-2.5-video-vae-bf16.safetensors $X/vae/ltx-2.5-video-vae-bf16.safetensors "$HF_TOKEN" &
    g vae ltx-2.5-audio-vae-bf16.safetensors $X/vae/ltx-2.5-audio-vae-bf16.safetensors "$HF_TOKEN" &
    g latent_upscale_models ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors $X/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors "$HF_TOKEN" & ;;
  *) echo "모르는 묶음: $m" ;;
esac; done
wait
if [ $NEED_MASTER = 1 ]; then   # LTX-2.5 노드는 태그 버전에 없고 master 에만 있다(2026-10)
  echo "ComfyUI 를 master 로 올리고 다시 시작"
  for i in $(seq 1 60); do [ -x $C/.venv-cu128/bin/python ] && break; sleep 5; done
  cd $C && git fetch -q origin master && git checkout -q -f origin/master
  $C/.venv-cu128/bin/pip install -q -r requirements.txt
  pkill -f "main.py --listen"; sleep 3
  setsid nohup $C/.venv-cu128/bin/python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header > /workspace/comfy.log 2>&1 < /dev/null &
fi
du -sh $L; echo "[$(date -u +%T)] 모델 준비 끝 — ComfyUI 화면에서 Templates 를 열어 쓰면 된다"
