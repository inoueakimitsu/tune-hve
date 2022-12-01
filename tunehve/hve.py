from typing import Sequence

from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 可視化時のグリッド数を指定します。
GRID_SIZE = 10000

def gaussian_kernel(x, sigma):
    """ガウシアン カーネルを生成します。

    Args:
        x: 入力値です。
        sigma: 標準偏差(バンド幅)です。
    """
    return np.exp(
        -x ** 2 / (2 * sigma ** 2)) / np.sqrt(2 * np.pi) / sigma

def visualize_hve(
        data_file_path: Path,
        output_image_path: Path,
        domain_min: float,
        domain_max: float,
        kappa_candidates: Sequence[float] = np.linspace(1e-2, 1.0, 5),
        sigma_candidates: Sequence[float] = np.linspace(1e-2, 1.0, 5)):
    """HVE (Hard Vicinity Estimates) により、
    実データの回帰ラベルの近傍として考慮される値域を可視化します。

    Args:
        data_file_path (Path): データのパス
        output_image_path (Path): 出力先のパス
        domain_min (float): ドメインの最小値
        domain_max (float): ドメインの最大値
        kappa_candidates (Sequence[float], optional): kappa の候補です。
        sigma_candidates (Sequence[float], optional): sigma の候補です。
    """

    # データを読み込みます。
    df = pd.read_csv(data_file_path)
    
    # 最初の列を使用します。
    y_list = df.iloc[:, 0].values

    # データの件数を確認します。
    n = len(y_list)

    # y^r の経験分布を生成します。
    y_grid = np.linspace(domain_min, domain_max, GRID_SIZE)
    f_grid = np.zeros_like(y_grid)

    # 経験分布のグリッドの刻み幅を求めます。
    delta_y_grid = y_grid[1] - y_grid[0]

    for y in y_list:

        # y に最も近いグリッド点を検索します。
        i_grid = np.argmin(np.abs(y_grid - y))

        # デルタ関数の近似値を追加します。
        f_grid[i_grid] += 1 / n / delta_y_grid

    # ガウシアン カーネルを畳み込みます。
    sigma = sigma_candidates[0]
    f_gaussian_applied_grid = np.convolve(
        f_grid, gaussian_kernel(y_grid - y_grid[GRID_SIZE // 2], sigma) * delta_y_grid, mode="same")

    # ボックス カーネルを畳み込みます。
    kappa = kappa_candidates[0]
    box_kernel_size = int(2 * kappa / delta_y_grid)
    f_box_gaussian_applied_grid = np.convolve(
        f_gaussian_applied_grid, np.ones(box_kernel_size) / box_kernel_size, mode="same")

    # 結果を可視化します。
    fig, axes = plt.subplots(
            nrows=3, ncols=1, sharex=True, figsize=(6, 6),
            gridspec_kw=dict(height_ratios=[2,4,4]))

    axes[0].hist(y_list, bins=50, density=False, color="red", edgecolor = "black")
    axes[0].set_ylabel('count')
    axes[0].set_xlabel('y')
    axes[0].set_title('empirical label distribution')
    axes[0].scatter(y_list, np.zeros(n), s=1, label="data", color="red")

    axes[1].fill_between(y_grid, f_gaussian_applied_grid,
                        label="f_gaussian_applied density",
                        color="skyblue", alpha=0.4)
    axes[1].plot(y_grid, f_gaussian_applied_grid,
                color="Slateblue", alpha=0.6, linewidth=2)
    axes[1].set_xlabel('y')
    axes[1].set_ylabel('density')
    axes[1].set_title('theoretical label density added gaussian noise')
    axes[1].grid(which="both")
    axes[1].scatter(y_list, np.zeros(n), s=1, label="data", color="red")
    

    axes[2].fill_between(y_grid, f_box_gaussian_applied_grid,
                        label="f_box_gaussian_applied density",
                        color="skyblue", alpha=0.4)
    axes[2].plot(y_grid, f_box_gaussian_applied_grid,
                color="Slateblue", alpha=0.6, linewidth=2)
    axes[2].set_xlabel('y')
    axes[2].set_ylabel('density')
    axes[2].set_title('theoretical label coverage')
    axes[2].grid(which="both")
    axes[2].scatter(y_list, np.zeros(n), s=1, label="data", color="red")

    fig.suptitle(rf"$\kappa$ = {kappa}, $\sigma$ = {sigma}")

    fig.tight_layout()
    plt.show()
    fig.savefig(output_image_path)
    plt.close()


if __name__ == '__main__':

    # コマンドライン引数を分析するためのパーサーを生成します。
    parser = ArgumentParser(prog="tunehve", description="Tune HVE")
    parser.add_argument("data", help="data file")
    parser.add_argument("output", help="output file")

    # ターゲット ドメインの最大値と最小値を指定します。
    parser.add_argument("--max", type=float, default=4.0, help="max value")
    parser.add_argument("--min", type=float, default=-4.0, help="min value")

    # kappa を指定します。
    parser.add_argument("--kappa", type=float, default=0.5, help="kappa")

    # sigma を指定します。
    parser.add_argument("--sigma", type=float, default=0.5, help="sigma")

    # コマンドライン引数をパースします。
    args = parser.parse_args()

    # 入力パラメーターの妥当性を確認します。
    if args.max <= args.min:
        raise ValueError("max must be greater than min")
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError("data file not found")
    output_path = Path(args.output)

    # HVE (Hard Vicinity Estimates) により、
    # 実データの回帰ラベルの近傍として考慮される値域を可視化します。
    visualize_hve(data_path, output_path,
                  domain_min=args.min, domain_max=args.max,
                  kappa_candidates=[args.kappa],
                  sigma_candidates=[args.sigma])
