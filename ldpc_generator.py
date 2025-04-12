import numpy as np
import random

# LDPC 패리티 검사 행렬 H를 생성하는 함수 (MacKay–Neal 방식) ,무작위 LDPC H 생성
def mackay_neal_ldpc(n, r, v_dist, h_dist, remove_cycles=True, max_shuffle_attempts=1000):
    m = int(n * (1 - r))  # m: check 노드 수 (n * (1 - rate))
    H = np.zeros((m, n), dtype=int)  # H: m x n 제로 행렬로 초기화

    alpha, beta = [], []

    # Variable node 쪽 연결 정의 (degree 만큼 반복해서 alpha 리스트에 추가)
    for deg, frac in v_dist.items():
        for col in range(int(n * frac)):
            alpha.extend([col] * deg)

    # Check node 쪽 연결 정의 (degree 만큼 반복해서 beta 리스트에 추가)
    for deg, frac in h_dist.items():
        for row in range(int(m * frac)):
            beta.extend([row] * deg)

    # 총 연결 수가 일치해야 LDPC 행렬 구성 가능
    assert len(alpha) == len(beta), "연결 수 일치 필요"

    # 연결을 무작위로 섞음 (랜덤 매칭)
    random.shuffle(alpha)
    random.shuffle(beta)

    # alpha와 beta 쌍을 이용해 H 행렬 구성 (1로 채우기)
    for col, row in zip(alpha, beta):
        H[row, col] = 1

    # 4-cycle 제거 (선택적 옵션)
    if remove_cycles:
        def has_4_cycle(i, j):
            # i, j번 비트 노드가 같은 체크 노드에 2개 이상 연결되어 있으면 4-cycle
            return np.sum(H[:, i] & H[:, j]) > 1

        changed = True
        attempts = 0

        # 최대 max_shuffle_attempts 번까지 4-cycle 제거 시도
        while changed and attempts < max_shuffle_attempts:
            changed = False
            attempts += 1
            for i in range(n - 1):
                for j in range(i + 1, n):
                    if has_4_cycle(i, j):
                        rows = np.where(H[:, j])[0]  # j열에 연결된 행 찾기
                        np.random.shuffle(rows)     # 행 무작위 재배열
                        H[:, j] = 0                  # j열 초기화
                        H[rows[:len(rows)], j] = 1   # 다시 채움
                        changed = True

    return H  # 완성된 H 행렬 반환

# H → G 변환 함수 (Systematic Form으로 변환)
def H_to_G(H):
    m, n = H.shape
    k = n - m  # 메시지 길이 = 전체 비트 - 체크 비트
    H_sys = H.copy().astype(int)  # H 복사본으로 작업

    row = 0
    for col in range(n):
        if row >= m:
            break
        if H_sys[row, col] == 0:
            for i in range(row + 1, m):
                if H_sys[i, col] == 1:
                    H_sys[[row, i]] = H_sys[[i, row]]  # 행 스왑
                    break
            else:
                continue  # 스왑 실패 → 다음 열로
        for i in range(m):
            if i != row and H_sys[i, col] == 1:
                H_sys[i] ^= H_sys[row]  # XOR로 제거 (가우시안 소거)
        row += 1

    pivot_cols = []  # 피벗 열 인덱스 저장용
    for i in range(m):
        pivot = np.where(H_sys[i] == 1)[0]
        if len(pivot) == 0:
            raise ValueError("G를 만들 수 없습니다: H 정규화 실패")
        pivot_cols.append(pivot[0])  # 피벗 열 등록

    free_cols = [i for i in range(n) if i not in pivot_cols]  # 나머지 자유 열

    perm = free_cols + pivot_cols  # 열 재정렬 순서
    H_sys = H_sys[:, perm]         # H 행렬 재배열

    P = H_sys[:, :k]               # 좌측 블록을 P 행렬로 사용
    G = np.concatenate([np.eye(k, dtype=int), P.T % 2], axis=1)  # [I | P^T] 형식으로 G 구성
    return G, perm  # G와 열 재배열 정보 반환
