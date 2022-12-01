# tune-hve

Hard Vicinal Estimates Hyperparameter Tuning Tool


<img src=https://raw.githubusercontent.com/inoueakimitsu/tune-hve/main/images/demo.png width=50.0% />

## Summary

The $\hat{p}_{g}^{\mathrm{HVE}} (\bold{x}, y)$ in CcGAN is
influenced by the settings of $\kappa$ and $\sigma$.
If $\kappa$ or $\sigma$ are too small, the vicinity is not taken into account.

Given $y^r$, $\kappa$, and $\sigma$,
this tool visualize the range covered by the the second term of
$\hat{p}_{g}^{\mathrm{HVE}} (\bold{x}, y)$.

This gives the setting guidelines for $\kappa$ and $\sigma$.

## Approach

For the empirical distribution of labels on real data, we do the following:
- First, convolve a Gaussian kernel with bandwidth $\sigma$.
- Next, we convolve a box kernel with bandwidth $\kappa$.
- This visualizes the range covered by the labels in the real data.

## Usage

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

The following commands can be run to check the behavior for unbalanced age data.

```bash
python tunehve/hve.py testdata/y1.csv out.png --min 0 --max 90 --kappa 2 --sigma 0.3
```

## License

tune-hve is available under the MIT License.

## Reference

1. Ding, Xin, et al. "CcGAN: continuous conditional generative adversarial networks for image generation." International Conference on Learning Representations. 2020.
