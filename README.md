# tune-hve
Hard Vicinal Estimates Hyperparameter Tuning Tool

## 概要

CcGAN における $\hat{p}_{g}^{\mathrm{HVE}} (\bm{x}, y)$ は、
$\kappa$ と $\sigma$ の設定値に強く影響を受けます。
$\kappa$ や $\sigma$ が小さすぎると、vicinity が考慮されなくなります。

このツールは、$y^r$ と $\kappa$ と $\sigma$ を所与としたときの、
$\hat{p}_{g}^{\mathrm{HVE}} (\bm{x}, y)$ の第 2 項を可視化します。

これにより、$\kappa$, $\sigma$ の設定指針を得ることができます。

## アプローチ

real データのラベルの経験分布に対して、
バンド幅 $\sigma$ のガウス カーネルを畳み込み、
さらにバンド幅 $\kappa$ のボックス カーネルを畳み込むことで、
real データのラベルのカバーしている範囲を可視化します。

## 使用方法

