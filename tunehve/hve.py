from typing import Sequence
from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def visualize_hve(
        data_path: Path,
        output_path: Path,
        domain_min: float,
        domain_max: float,
        kappa_candidates: Sequence[float] = np.linspace(1e-2, 1.0, 5),
        sigma_candidates: Sequence[float] = np.linspace(1e-2, 1.0, 5)):
    """データの HVE を視覚化します。

    Args:
        data_path (Path): データのパス
        output_path (Path): 出力先のパス
        domain_min (float): ドメインの最小値
        domain_max (float): ドメインの最大値
        kappa_candidates (Sequence[float], optional): kappa の候補. Defaults to np.linspace(1e-2, 1.0, 5).
        sigma_candidates (Sequence[float], optional): sigma の候補. Defaults to np.linspace(1e-2, 1.0, 5).
    """
    N_GRID = 10000

    # データを読み込みます。
    df = pd.read_csv(data_path)
    y_list = df.iloc[:, 0].values

    # データの件数を確認します。
    n = len(y_list)

    # y^r の経験分布を生成します。
    y_grid = np.linspace(domain_min, domain_max, N_GRID)
    f_grid = np.zeros_like(y_grid)
    for i_sample, y in enumerate(y_list):
        # y に最も近いグリッド点を検索します。
        i_grid = np.argmin(np.abs(y_grid - y))
        # 質量を追加します。
        f_grid[i_grid] += 1 / n

    # Plot the data
    fig, ax = plt.subplots()
    # ax.scatter(y_list, np.zeros(n), s=1)
    ax.plot(y_grid, f_grid, label="empirical density")
    ax.plot(y_grid, np.convolve(f_grid), label="empirical density")
    ax.set_xlabel('HVE')
    ax.set_ylabel('Count')
    ax.set_title('HVE distribution')
    ax.legend()
    plt.show()
    fig.savefig(output_path)
    plt.close()


if __name__ == '__main__':

    # コマンドライン引数を分析するためのパーサーを生成します。
    parser = ArgumentParser(prog="tunehve", description="Tune HVE")
    parser.add_argument("data", help="data file")
    parser.add_argument("output", help="output file")
    
    # ターゲット ドメインの最大値と最小値を指定します。
    parser.add_argument("--max", type=float, default=3.0, help="max value")
    parser.add_argument("--min", type=float, default=-3.0, help="min value")

    # コマンドライン引数をパースします。
    args = parser.parse_args()
    
    # 入力パラメーターの妥当性を確認します。
    if args.max <= args.min:
        raise ValueError("max must be greater than min")
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError("data file not found")
    output_path = Path(args.output)

    # データの HVE を視覚化します。
    visualize_hve(data_path, output_path, args.max, args.min)
