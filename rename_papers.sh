#!/bin/bash

cd /data1/hemanth/4D_surface/papers

# Fix venues from the first (incorrect) run to the correct conferences
mv ArXiv2026_4C4D.pdf CVPR2026_4C4D.pdf
mv ArXiv2026_4DSurf.pdf CVPR2026_4DSurf.pdf
mv ArXiv2025_Sparse4DGS.pdf AAAI2026_Sparse4DGS.pdf
mv ArXiv2025_MAPo.pdf CVPR2026_MAPo.pdf
mv ArXiv2026_SpeeDe3DGS.pdf CVPR2026_SpeeDe3DGS.pdf
mv ArXiv2025_4D_GS_SLAM.pdf ICCV2025_4D_GS_SLAM.pdf
mv ArXiv2024_DeSiRe-GS.pdf CVPR2025_DeSiRe-GS.pdf
mv ArXiv2024_Motion2VecSets.pdf CVPR2024_Motion2VecSets.pdf
mv ArXiv2022_Unbiased_4D.pdf CVPR2023_Unbiased_4D.pdf

# These were already correct or unchanged — no action needed:
# ArXiv2026_DySurface.pdf       (still arXiv preprint)
# ArXiv2026_ReconDrive.pdf      (still arXiv preprint)
# ArXiv2024_DynaSurfGS.pdf      (still arXiv preprint)
# ArXiv2025_4DTAM.pdf           (still arXiv preprint)
# CVPR2024_4D_Gaussian_Splatting_Real_Time.pdf  (already correct)
# TVCG2026_Fast_Robust_Deformable_3DGS.pdf      (already correct)
# NeurIPS2025_H3D-DGS.pdf                       (already correct)
# ICML2026_TextMesh4D.pdf                        (already correct)

echo "Successfully renamed all PDF files with corrected conference venues."
