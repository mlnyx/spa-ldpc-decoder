# plotter.py
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import networkx as nx

# 폰트 설정 (macOS 기준)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

def plot_ber_vs_snr(snr_range, ber_list):
    plt.semilogy(snr_range, ber_list, marker='o')
    plt.xlabel("SNR (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.title("SPA LDPC Performance (BER vs SNR)")
    plt.grid(True, which="both")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/ber_vs_snr.png")
    plt.show()

def plot_tanner_graph(H):
    import seaborn as sns
    sns.heatmap(H, cmap="Greys", cbar=False, square=True)
    plt.title("Parity-Check Matrix H")
    plt.xlabel("Bit Nodes")
    plt.ylabel("Check Nodes")
    plt.show()

def plot_llr_distribution(L, title="LLR Distribution", save_path=None):
    plt.hist(L, bins=30, color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel("LLR value")
    plt.ylabel("Bit count")
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    plt.show(block=False)
    plt.pause(1.5)
    plt.close()

def plot_tanner_graph(H):
    m, n = H.shape
    G = nx.Graph()

    bit_nodes = [f'b{i}' for i in range(n)]
    check_nodes = [f'c{j}' for j in range(m)]
    G.add_nodes_from(bit_nodes, bipartite=0)
    G.add_nodes_from(check_nodes, bipartite=1)

    for j in range(m):
        for i in range(n):
            if H[j, i] == 1:
                G.add_edge(f'b{i}', f'c{j}')

    pos = {}
    for i, b in enumerate(bit_nodes):
        pos[b] = (i, 0)
    for j, c in enumerate(check_nodes):
        pos[c] = (j, -1)

    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightgreen', font_size=9)
    plt.title("Tanner Graph")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/tanner_graph.png")
    plt.show()

def save_results_to_csv(filepath, snr_range, ber_list):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SNR (dB)", "BER"])
        for snr, ber in zip(snr_range, ber_list):
            writer.writerow([snr, ber])
