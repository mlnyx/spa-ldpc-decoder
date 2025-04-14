import numpy as np
from ldpc_generator import H_to_G
from evaluator import evaluate_snr
from plotter import plot_ber_vs_snr, plot_tanner_graph, save_results_to_csv

def main():
    # [1] 고정된 H 행렬 직접 정의
    H = np.array([
        [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    ], dtype=int)

    # [2] H → G 변환
    G, _ = H_to_G(H)

    # [3] Tanner 그래프 시각화
    plot_tanner_graph(H)

    # [4] SNR 실험 범위 설정 (0~8dB)
    snr_range = range(0, 9)
    ber_list = []

    # [5] SNR별로 실험 반복
    for snr_db in snr_range:
        print(f"[실험] SNR {snr_db} dB 진행 중...")
        result = evaluate_snr(H, G, snr_db, num_trials=200000)
        print(f"BER: {result['ber']:.5f}, FER: {result['fer']:.3f}, "
              f"평균 반복: {result['avg_iter']:.1f}, 시간: {result['avg_time']:.4f}s")
        ber_list.append(result['ber'])

    # [6] 결과 시각화 및 저장
    plot_ber_vs_snr(snr_range, ber_list)
    save_results_to_csv("results/ber_result.csv", snr_range, ber_list)

if __name__ == "__main__":
    main()
