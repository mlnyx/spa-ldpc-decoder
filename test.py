# test.py
from ldpc_generator import mackay_neal_ldpc, H_to_G
from evaluator import evaluate_snr
from plotter import plot_ber_vs_snr, plot_tanner_graph, save_results_to_csv


def main():
    n = 12
    r = 0.5
    v_dist = {3: 1.0}
    h_dist = {6: 1.0}

    print("[INFO] H, G 생성 중...")
    for _ in range(10):
        H = mackay_neal_ldpc(n, r, v_dist, h_dist)
        try:
            G, _ = H_to_G(H)
            break
        except:
            continue
    else:
        raise RuntimeError("G 생성 실패")

    plot_tanner_graph(H)

    snr_range = range(0, 9)
    ber_list = []

    for snr_db in snr_range:
        print(f"[실험] SNR {snr_db}dB...")
        result = evaluate_snr(H, G, snr_db, num_trials=50)
        print(f"BER: {result['ber']:.5f}, FER: {result['fer']:.3f}, 평균 반복: {result['avg_iter']:.1f}, 시간: {result['avg_time']:.4f}s")
        ber_list.append(result['ber'])

    plot_ber_vs_snr(snr_range, ber_list)
    save_results_to_csv("results/ber_result.csv", snr_range, ber_list)

if __name__ == "__main__":
    main()