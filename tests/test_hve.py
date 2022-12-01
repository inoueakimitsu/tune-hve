from tempfile import TemporaryDirectory
from pathlib import Path

from pytest import approx

from tunehve.hve import visualize_hve, gaussian_kernel

def test_visualize_hve():
    temp_dir = TemporaryDirectory()
    visualize_hve(
        data_file_path="testdata/y1.csv",
        output_image_path=Path(temp_dir.name) / "y1_out.png",
        domain_min=0, domain_max=90,
        kappa_candidates=[2.0],
        sigma_candidates=[0.3])
    temp_dir.cleanup()

def test_gaussian_kernel():
    assert gaussian_kernel(0, 1) == approx(0.3989423)
