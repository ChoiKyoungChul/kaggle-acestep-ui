# 오픈소스 AI 원클릭 실행 모음 — Kaggle · Colab · Runpod

> 🆕 **Kaggle 무료 GPU 자동 연동 설치 프로그램 v3** — Windows 에서 `INSTALL.cmd` 더블클릭으로 Kaggle 작업 도구 + Codex · Claude Code · Antigravity 스킬 설치. **[ZIP 내려받기](https://github.com/ChoiKyoungChul/kaggle-acestep-ui/releases/download/kaggle-kit-v3/kaggle-free-gpu-full-package-v3.zip)** · [설명](kaggle-kit/)

버튼 하나로 설치 → 모델 받기 → 화면(Gradio · ComfyUI)까지 자동으로 뜬다. 무료 T4(Kaggle · Colab)와 유료 48GB GPU(Runpod) 두 길을 함께 둔다.

- **Kaggle**: 노트북이 열리면 *Copy & Edit* → 오른쪽 Settings 에서 Internet on · GPU T4 → **Run All**
- **Colab**: 런타임 유형 T4 GPU → **모두 실행**
- **Runpod**: GPU 고르고 **Deploy** → 5~15분 뒤 Pod 의 *Connect* 에서 화면 열기. 끝나면 Pod **삭제**(켜 둔 시간만큼 과금)

★ = 이 저장소에서 만들고 실제로 써 본 것. 나머지 무료 노트북은 [TeamAIQ/Colab-notebooks](https://github.com/TeamAIQ/Colab-notebooks)(AIQUEST Academy)가 관리하는 검증된 노트북으로 연결한다.
**상업 이용**은 모델마다 다르다 — 표의 라이선스를 먼저 본다(2026-10 기준, 쓰기 전에 원문 확인).

## 🎵 음악

| 모델 | 용도 · 메모 | 라이선스 | 무료 (T4) | Runpod (48GB) |
|---|---|---|---|---|
| ★ **ACE-Step 1.5** | 노래 · 연주곡 생성, 편곡(cover). 원곡 선율을 지키는 편곡은 XL base(48GB)만 됐다 | MIT — 상업 가능 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/elrohm0119/ace-step-1-5-one-click-gradio) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChoiKyoungChul/kaggle-acestep-ui/blob/main/ace-ui.ipynb) | [![Runpod](https://img.shields.io/badge/Deploy-Runpod-673ab7)](https://console.runpod.io/deploy?template=7y2vpgweau) |
| ACE-Step 1.5 + LoRA 학습 | 내 곡 모음으로 창법 · 편곡 학습 | MIT | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/ACE_Step_1_5_Music_Generator_LoRA_Training_by_AIQUEST.ipynb) | |
| **YuE2-3B** | 가사 → 전곡(보컬 포함). 한국어 발음 · 감정이 자연스러웠다 | 가중치 CC BY-NC — **비상업** | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/yue2-3b-frontier-full-song-music-generation) | |
| HeartMuLa 3B | 음악 생성 | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/HeartMuLa_by_AIQUEST.ipynb) | |

## 🖼️ 이미지

| 모델 | 용도 · 메모 | 라이선스 | 무료 (T4) | Runpod (48GB) |
|---|---|---|---|---|
| ★ **Krea 2 Turbo** | 사진 · 인물 · 음식 · 인테리어 1순위. 8스텝, 장당 약 15초(A40). 한글 글자는 틀린다 | Krea-2 Community — 연 매출 100만 달러 미만 상업 무료 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/krea-2-turbo-fast-text-to-image-generator) | [![Runpod](https://img.shields.io/badge/Deploy-Runpod-673ab7)](https://console.runpod.io/deploy?template=ce6vhvq3x3) |
| ★ **Z-Image Turbo** | 감정 클로즈업 · 컷 일괄 | Apache 2.0 | | [![Runpod](https://img.shields.io/badge/Deploy-Runpod-673ab7)](https://console.runpod.io/deploy?template=ce6vhvq3x3) |
| ★ **Qwen-Image 2512** | 구도 · 소품 지시를 잘 따름, Krea 다음 2순위 | Apache 2.0 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/Qwen_Image_2_1_Uncensored_INT8_Colab_by_AIQUEST.ipynb) (2.1) | [![Runpod](https://img.shields.io/badge/Deploy-Runpod-673ab7)](https://console.runpod.io/deploy?template=ce6vhvq3x3) |
| HYPIR | 4K 업스케일 · 복원 | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/HYPIR_4K_image_upscale_by_AIQUEST.ipynb) | |

Runpod 이미지 묶음은 ComfyUI 에 Krea 2 · Z-Image · Qwen-Image 를 함께 받는다(약 70GB). ComfyUI 화면의 **Templates** 에서 모델 워크플로를 열어 쓴다.

## 🎬 영상

| 모델 | 용도 · 메모 | 라이선스 | 무료 (T4) | Runpod (48GB) |
|---|---|---|---|---|
| ★ **LTX-2.5 22B** | 사진 → 5~8초 영상 + 주변음, 감정 연기에 강함. 1280×704 5초 약 130초(A40) | LTX 라이선스 — 상업 조건 원문 확인 · **HF 접근 동의 필요** | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/ltx-2-5-22b-distilled-video-generator) | [![Runpod](https://img.shields.io/badge/Deploy-Runpod-673ab7)](https://console.runpod.io/deploy?template=7x4p0svb1h) |
| LTX-2.3 Q4 · A2V · MSR Ref | 텍스트/이미지 → 영상, 음성 → 립싱크, 다중 참조 | 원문 확인 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/ltx-2-3-22b-distilled-1-1-q4-t2v-kaggle) [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/ltx-2-3-a2v-q4-kaggle) [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/ltx-2-3-22b-msr-ref-distilled-1-1-kaggle) | |
| ★ **Wan 2.2 I2V · S2V** | 사진 → 5초 영상(4스텝 LoRA), 음성 → 립싱크. 카메라 이동 + 군중은 무너진다 | Apache 2.0 | | [![Runpod](https://img.shields.io/badge/Deploy-Runpod-673ab7)](https://console.runpod.io/deploy?template=stb32bbvmy) |
| MiniMax H3 Turbo | 영상 + 32kHz 소리 동시 생성 | 원문 확인 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/minimax-h3-turbo-int8-video-audio) | |
| FlashVSR+ | 영상 업스케일 720p~1440p | 원문 확인 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/flashvsr-video-upscaler) | |
| SoulX FlashHead | 음성 → 말하는 얼굴 | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/SoulX_FlashHead_by_AIQUEST.ipynb) | |

LTX 템플릿은 Deploy 화면의 환경변수 `HF_TOKEN` 에 본인 Hugging Face 토큰을 넣어야 모델을 받는다(Lightricks/LTX-2.5 페이지에서 접근 동의 먼저). 토큰은 Pod 정보에 보이므로 쓰고 나면 Pod 를 지우고 필요하면 토큰을 새로 만든다.

## 🗣️ 음성 · 받아쓰기

| 모델 | 용도 | 라이선스 | 무료 |
|---|---|---|---|
| MOSS-TTS v1.5 | 48kHz TTS · 목소리 복제 | 원문 확인 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/moss-tts-v1-5-standalone-foundation-model) |
| VoxCPM2 | 30개 언어 TTS · 목소리 디자인 | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/VoxCPM2_Gradio_Colab_AIQUEST.ipynb) |
| OmniVoice | 600개 언어 제로샷 TTS | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/OmniVoice_TTS_By_AIQUEST.ipynb) |
| Qwen3-TTS 1.7B | TTS | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/Qwen_3_TTS_1_7B_by_AIQUEST.ipynb) |
| DramaBox | 감정 · 웃음 · 속삭임 대사 | 원문 확인 | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/unlockbulk/dramabox-expressive-tts) |
| SeedVC | 목소리 바꾸기 · 노래 커버 | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/SeedVC_Voice_Changer_by_AIQUEST.ipynb) |
| Cohere Transcribe | 14개 언어 받아쓰기 | 원문 확인 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TeamAIQ/Colab-notebooks/blob/main/notebooks/cohere_transcribe_by_AIQUEST.ipynb) |

---

# ACE-Step 1.5 노트북 · 템플릿 자세히

## 🤖 AI 코딩 도구로 일괄 실행 (Codex · Claude Code)

버튼 화면 대신 PC 의 AI 에게 맡기는 방법: 작업 파일(가사 · 프롬프트 · 컷 목록)을 만들면 명령 두 줄로 Kaggle 무료 GPU 에서 곡 · 이미지 · 영상을 뽑아 온다. ACE-Step · YuE2 · Krea 2 · **LTX-2.5 영상** · Z-Image · Qwen · Wan 2.2 모두 Kaggle 실측 완료(Qwen · Wan 은 느림).

→ **[batch/README.md](batch/README.md)** · AI 에게 줄 지침 **[batch/CODEX.md](batch/CODEX.md)**

## 쓰는 방법 (Kaggle · Colab)

1. 위 **Open In Kaggle**(→ Copy & Edit) 또는 **Open In Colab** 버튼
2. Kaggle: 오른쪽 Settings → *Internet on* · *Accelerator GPU T4* / Colab: 런타임 유형 T4 GPU
3. **Run All** → 5~10분 뒤 출력에 `🌐 접속 주소: https://…` 가 나온다
   - 기본은 gradio 공개 주소(`*.gradio.live`, 72시간). 1분 안에 안 나오면 cloudflared 터널(`*.trycloudflare.com`)로 자동 전환
4. 작업이 끝나면 세션을 끈다(GPU 시간이 계속 줄어든다)

모델은 1) 셀의 `MODEL` 목록에서 고른다.

| 값 | 용도 |
|---|---|
| `acestep-v15-turbo` (기본) | T4 에서 새 곡 생성 · 가벼운 편곡 시험 |
| `acestep-v15-xl-turbo` | 더 좋은 음질의 새 곡 생성(메모리 여유가 적다) |
| `acestep-v15-xl-base` | 편곡 — 원곡 선율을 유지하는 것은 XL base 뿐이었다. float32 로 16GB 를 넘어 **24GB 이상 GPU** 필요 |

## Runpod 에서 (편곡용 XL base — 48GB GPU)

T4 로는 원곡 선율을 지키는 편곡(XL base)이 메모리가 모자란다. Runpod 템플릿 하나로 자동 설치 · 실행한다.

- 이미지 `runpod/pytorch` (CUDA 12.8), 포트 `7860/http` · `22/tcp`, 컨테이너 디스크 80GB
- 시작 명령: `bash -c "curl -fsSL https://raw.githubusercontent.com/ChoiKyoungChul/kaggle-acestep-ui/main/runpod/start.sh | bash & exec /start.sh"`
- 환경변수 `ACE_MODEL` (기본 `acestep-v15-xl-base`)
- Pod 를 만들면 약 5~8분 뒤 `https://<Pod ID>-7860.proxy.runpod.net` 에 편집 화면이 뜬다. 진행 로그는 `/workspace/acestep.log`
- 권장 GPU: A40 · RTX A6000(48GB). 끝나면 Pod 를 **삭제**한다(켜 둔 시간만큼 과금)

## 미리 막아 둔 함정

| 증상 | 원인 · 처리 |
|---|---|
| 편곡 · 악기 추가 결과가 무음이나 잡음 | T4 는 bf16 이 없어 float16 을 쓰는데 cover · lego 에서 NaN → 코드를 float32 로 바꾼다 |
| 하위 프로세스가 바로 죽음 | 노트북의 `MPLBACKEND` 값이 넘어감 → `Agg` 로 지정 |
| Kaggle 에서 localhost 로 못 들어감 | 공개 주소(gradio share)를 띄우고, 안 되면 cloudflared 터널로 대신 연다 |
| Save Version 이 끝나지 않음 | 저장 실행(Batch)에서는 화면을 띄우지 않고 끝낸다 |
| 화면을 열어도 모델이 없음 | `--init_service true --config_path …` 로 시작할 때 올려 둔다 |
| NaN 잠재값(무음 · 잡음) | INT8 양자화가 원인 → `--quantization none`, 대신 CPU offload 로 메모리를 줄인다 |

## 알려진 한계

- 원곡 선율을 지키는 편곡(XL base)은 T4 에서 메모리가 모자란다 → 48GB GPU(예: Runpod A40)에서 돌린다.
- 참고: [TeamAIQ/Colab-notebooks](https://github.com/TeamAIQ/Colab-notebooks) 의 ACE-Step 노트북도 T4 에서 turbo 를 쓰고 INT8 을 끈다.
- 원곡을 편곡한 결과는 원곡 권리 확인 전에는 공개하지 않는다.
