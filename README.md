# Kaggle에서 ACE-Step 1.5 편집 화면(Gradio) 자동 설치

Kaggle 노트북 셀 하나로 [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) 편집 화면을 설치하고, 공개 주소(`https://xxxx.gradio.live`)를 띄운다. 편곡(Remix · cover) 작업용이다.

## 쓰는 방법

1. Kaggle → New Notebook → File → Import Notebook → GitHub 탭에서 이 저장소의 `ace-ui.ipynb` 선택(또는 파일을 받아 올리기)
2. 오른쪽 설정에서 **Internet 켜기**, **GPU T4** 선택
3. 셀 실행 → 설치 · 모델 받기가 끝나면 출력 끝에 `Running on public URL: https://xxxx.gradio.live` 가 나온다
4. 그 주소를 브라우저나 Claude 에게 넘긴다. 주소는 72시간 뒤 끊긴다. 작업이 끝나면 노트북 세션을 끈다(GPU 시간이 계속 줄어든다).

모델은 맨 위 `MODEL` 값으로 바꾼다.

| 값 | 용도 |
|---|---|
| `acestep-v15-xl-base` (기본) | 편곡 — 원곡 선율을 유지하는 것은 XL base 뿐이었다 |
| `acestep-v15-turbo` | 가벼운 시험 · 새 곡 생성 |

## 미리 막아 둔 함정

| 증상 | 원인 · 처리 |
|---|---|
| 편곡 · 악기 추가 결과가 무음이나 잡음 | T4 는 bf16 이 없어 float16 을 쓰는데 cover · lego 에서 NaN → 코드를 float32 로 바꾼다 |
| 하위 프로세스가 바로 죽음 | 노트북의 `MPLBACKEND` 값이 넘어감 → `Agg` 로 지정 |
| 화면을 열어도 모델이 없음 | `--init_service true --config_path …` 로 시작할 때 올려 둔다 |
| 메모리 부족 | float32 로 커진 만큼 `int8_weight_only` + CPU offload 로 줄인다 |

## 알려진 한계

- XL base 를 T4(16GB)에서 float32 + int8 로 돌리는 조합은 아직 끝까지 확인하지 못했다. 메모리 부족으로 멈추면 48GB GPU(예: Runpod A40)에서 돌린다.
- 원곡을 편곡한 결과는 원곡 권리 확인 전에는 공개하지 않는다.
