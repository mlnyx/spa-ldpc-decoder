# evaluator.py
import numpy as np
from decoder import spa_decode
from plotter import plot_llr_distribution

def evaluate_snr(H, G, snr_db, num_trials=100):
    n = G.shape[1]
    k = G.shape[0]
    ber_total = 0
    fer_total = 0
    total_iterations = 0
    total_time = 0.0

    sigma = np.sqrt(1 / (2 * 10 ** (snr_db / 10)))

    for trial in range(num_trials):
        msg = np.random.randint(0, 2, k)
        codeword = msg @ G % 2
        tx = 1 - 2 * codeword
        rx = tx + np.random.normal(0, sigma, size=n)
        llr = 2 * rx / (sigma ** 2)
        decoded, iters, decode_time, L = spa_decode(H, llr)

        # 대표 SNR에서 첫 trial만 LLR 시각화 및 저장
        if snr_db in [0, 4, 8] and trial == 0:
            filename = f"results/llr_dist_snr{snr_db}_trial{trial}.png"
            plot_llr_distribution(L, title=f"LLR 분포 (SNR={snr_db}dB)", save_path=filename)

        errors = np.sum(decoded != codeword)
        ber_total += errors
        fer_total += 1 if errors > 0 else 0
        total_iterations += iters
        total_time += decode_time

    return {
        "ber": ber_total / (num_trials * n),
        "fer": fer_total / num_trials,
        "avg_iter": total_iterations / num_trials,
        "avg_time": total_time / num_trials
    }