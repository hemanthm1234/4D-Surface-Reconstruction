#!/bin/bash
# Download script for 4D Surface Reconstruction papers

DOWNLOAD_DIR="/data1/hemanth/4D_surface/papers"
mkdir -p "$DOWNLOAD_DIR"

echo "Downloading 4D Surface Reconstruction Papers in parallel..."

# Function to download a paper only if it hasn't been downloaded yet
download_paper() {
    local title="$1"
    local url="$2"
    local filename="$3"
    
    if [ -f "$DOWNLOAD_DIR/$filename" ]; then
        echo "Skipping (Already downloaded): $title"
    else
        echo "Downloading: $title"
        # Download in silent mode, follow redirects
        curl -sL -o "$DOWNLOAD_DIR/$filename" "$url"
        if [ $? -eq 0 ]; then
            echo "Successfully downloaded: $title"
        else
            echo "Failed to download: $title"
        fi
    fi
}

# === Original Papers ===
download_paper "DySurface" "https://arxiv.org/pdf/2605.10360.pdf" "DySurface.pdf" &
download_paper "4D Gaussian Splatting (4D-GS)" "https://arxiv.org/pdf/2310.08528.pdf" "4D_Gaussian_Splatting_Real_Time.pdf" &
download_paper "Sparse4DGS" "https://arxiv.org/pdf/2511.07122.pdf" "Sparse4DGS.pdf" &
download_paper "4D Gaussian Splatting SLAM" "https://arxiv.org/pdf/2503.16710.pdf" "4D_GS_SLAM.pdf" &
download_paper "ReconDrive" "https://arxiv.org/pdf/2603.07552.pdf" "ReconDrive.pdf" &
download_paper "4C4D" "https://arxiv.org/pdf/2604.04063.pdf" "4C4D.pdf" &

# === New Papers (Focus on Quality, Geometry & Reconstruction) ===
download_paper "4DTAM" "https://arxiv.org/pdf/2505.15286.pdf" "4DTAM.pdf" &
download_paper "TextMesh4D" "https://arxiv.org/pdf/2506.24121.pdf" "TextMesh4D.pdf" &
download_paper "DeSiRe-GS" "https://arxiv.org/pdf/2411.11921.pdf" "DeSiRe-GS.pdf" &
download_paper "DynaSurfGS" "https://arxiv.org/pdf/2408.13972.pdf" "DynaSurfGS.pdf" &
download_paper "Motion2VecSets" "https://arxiv.org/pdf/2401.06614.pdf" "Motion2VecSets.pdf" &
download_paper "Unbiased 4D" "https://arxiv.org/pdf/2206.08368.pdf" "Unbiased_4D.pdf" &

# === Fast & Deformable 3D Gaussians (4DSurf, SpeeDe3DGS, etc.) ===
download_paper "4DSurf" "https://arxiv.org/pdf/2603.28064.pdf" "4DSurf.pdf" &
download_paper "SpeeDe3DGS" "https://arxiv.org/pdf/2506.07917.pdf" "SpeeDe3DGS.pdf" &
download_paper "Fast and Robust Deformable 3DGS" "https://arxiv.org/pdf/2603.20857.pdf" "Fast_Robust_Deformable_3DGS.pdf" &
download_paper "MAPo" "https://arxiv.org/pdf/2508.19786.pdf" "MAPo.pdf" &
download_paper "H3D-DGS" "https://arxiv.org/pdf/2408.13036.pdf" "H3D-DGS.pdf" &

# Wait for all background download jobs to finish
wait

echo "Done! All papers are available in $DOWNLOAD_DIR"
