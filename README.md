# 🧠 LDPC SPA 디코더 시뮬레이션

이 프로젝트는 **LDPC (Low-Density Parity-Check)** 부호를 사용하여 통신 채널에서 전송된 데이터를 **오류 없이 복원하는 알고리즘**, 특히 **SPA (Sum-Product Algorithm)** 디코더의 성능을 실험하고 분석하는 데 목적이 있습니다.

## 프로젝트 목표

- LDPC 부호의 핵심 디코딩 알고리즘인 **SPA**를 직접 구현
- 다양한 SNR(Signal-to-Noise Ratio) 환경에서 **BER/FER 성능 평가**
- 향후 Min-Sum, Neural Min-Sum 알고리즘과의 비교를 위한 **baseline 확보**
- 성능 결과를 시각적으로 표현하고, 연구 또는 교육 목적에 활용 가능

---

## 구조 및 구성 파일 설명

```
ldpc_spa_project/
├── test.py                # 전체 실험 실행 스크립트
├── decoder.py             # SPA 디코더 함수 (LLR 기반 메시지 전달)
├── ldpc_generator.py      # H, G 행렬 생성 및 변환 함수
├── evaluator.py           # SNR 루프 기반 성능 측정 (BER, FER, 반복수, 시간)
├── plotter.py             # 성능 그래프 및 H 행렬 시각화
└── README.md              # 프로젝트 설명 파일 (바로 이 파일)
```

test.py가 중심이 되어,
ldpc_generator.py로 랜덤 H/G를 만들고,
decoder.py로 디코딩을 수행하며,
evaluator.py로 성능을 평가하고,
plotter.py로 결과를 시각화

---

## 실행 환경 및 설치 방법

### 설치

pip install numpy matplotlib seaborn

### ▶실행

python test.py

### 실행 결과

1. H 행렬 시각화(화면 출력)
2. SNR 0~8dB 실험 반복 (BER, FER, 반복 수 출력)
3. 결과 그래프 출력 (BER vs SNR 그래프 출력)
4. LLR 분포 시각화 (조건부로 여러 창 생성됨)
5. CSV 저장 성공 (자동) results/ber_result.csv 파일 확인 가능

---

## 핵심 용어 설명

| 용어     | 설명                                                       |
| -------- | ---------------------------------------------------------- |
| **LDPC** | 통신 시 발생하는 오류를 자동으로 수정해주는 수학적 부호    |
| **SPA**  | 오류를 수정하기 위해 메시지를 반복적으로 교환하는 알고리즘 |
| **SNR**  | 신호 세기 대비 잡음 세기. 높을수록 통신이 정확함           |
| **BER**  | 전송된 비트 중 잘못된 비트 비율                            |
| **FER**  | 프레임(한 묶음) 중 오류가 발생한 프레임의 비율             |

---

## 예시 출력 결과

```
[INFO] H, G 생성 중...
[실험] SNR 0dB...
BER: 0.21083, FER: 0.980, 평균 반복: 49.8, 시간: 0.0021s
[실험] SNR 1dB...
BER: 0.15192, FER: 0.850, 평균 반복: 43.2, 시간: 0.0018s
...
(SNR vs BER 그래프 출력)
```

---

## 확장 가능성

- SPA 외에 Min-Sum, Neural Min-Sum 알고리즘 비교 실험으로 확장 가능
- GPGPU 연산 또는 하드웨어 구현 시뮬레이션으로 발전 가능
- 연구 논문 기반 성능 검증 실험 도구로 활용 가능

## 참고

- SPA 알고리즘은 **MAP 디코딩에 가장 근접한 확률 기반 메시지 전달 방식**입니다.
- 본 프로젝트는 실제 통신 환경을 단순화한 **AWGN + BPSK** 조건에서 동작합니다.
