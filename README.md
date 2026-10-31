# Kaggle · Colab 에서 ACE-Step 1.5 편집 화면(Gradio) 한 번에 설치

[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/ChoiKyoungChul/kaggle-acestep-ui/blob/main/ace-ui.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChoiKyoungChul/kaggle-acestep-ui/blob/main/ace-ui.ipynb)
[![Deploy on Runpod](https://img.shields.io/badge/Deploy%20on-Runpod%20(XL%20base%20%ED%8E%B8%EA%B3%A1)-673ab7?logo=data:image/svg%2bxml;base64,PHN2Zz48L3N2Zz4=)](https://console.runpod.io/deploy?template=7y2vpgweau)

| 버튼 | 무엇이 되나 |
|---|---|
| **Open In Kaggle / Colab** | 무료 T4 — 노트북이 열린다 → GPU · 인터넷 켜고 **Run All** 한 번이면 설치 → 모델 → 공개 주소까지 자동. 새 곡 생성 · 가벼운 시험용(turbo) |
| **Deploy on Runpod** | 유료 48GB GPU — GPU(A40 권장)만 고르고 Deploy 하면 Pod 가 뜨면서 설치 · 모델까지 자동, 5~8분 뒤 `https://<Pod ID>-7860.proxy.runpod.net`. 원곡 선율을 지키는 **편곡(XL base)** 용. 끝나면 Pod 삭제 |

Runpod 템플릿은 지금 **비공개**(만든 계정에서만 버튼이 열린다). 다른 계정은 아래 「Runpod 에서」 설정으로 템플릿을 하나 만들면 같다.
[ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) 공식 코드를 받아 쓰며, 편곡(Remix · cover) · 새 곡 생성용이다.

## 쓰는 방법

1. 위 **Open In Kaggle** 또는 **Open In Colab** 버튼
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
