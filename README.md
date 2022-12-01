# tune-hve
Hard Vicinal Estimates Hyperparameter Tuning Tool

## 概要

CcGAN における $\hat{p}_{g}^{\mathrm{HVE}} (\bold{x}, y)$ は、
$\kappa$ と $\sigma$ の設定値に強く影響を受けます。
$\kappa$ や $\sigma$ が小さすぎると、vicinity が考慮されなくなります。

このツールは、$y^r$ と $\kappa$ と $\sigma$ を所与としたときの、
$\hat{p}_{g}^{\mathrm{HVE}} (\bold{x}, y)$ の第 2 項がカバーする値域を
以下のように可視化します。

<img src=https://raw.githubusercontent.com/inoueakimitsu/tunehve/main/images/demo.png width=50.0% />

これにより、$\kappa$, $\sigma$ の設定指針を得ることができます。

## アプローチ

real データのラベルの経験分布に対して、
バンド幅 $\sigma$ のガウス カーネルを畳み込み、
さらにバンド幅 $\kappa$ のボックス カーネルを畳み込むことで、
real データのラベルのカバーしている範囲を可視化します。

## 使用方法

```
usage: tunehve [-h] [--max MAX] [--min MIN] [--kappa KAPPA] [--sigma SIGMA] data output

Tune HVE

positional arguments:
  data           data file
  output         output file

optional arguments:
  -h, --help     show this help message and exit
  --max MAX      max value
  --min MIN      min value
  --kappa KAPPA  kappa
  --sigma SIGMA  sigma
```

以下は擬似的な年齢ラベルに対して実行した例です。

```bash
python tunehve/hve.py testdata/y1.csv out.png --min 0 --max 90 --kappa 2 --sigma 0.3
```

## License

tune-hve is available under the MIT License.
