---
first-title-word: GSplatLoc
title-rest: ": Ultra-Precise Pose Optimization via 3D Gaussian Reprojection"
bibliography: C:/Users/18317/DevSpace/DocHub/essay/zotero/bibliography.bib
csl: C:/Users/18317/DevSpace/DocHub/essay/zotero/ieee.csl
resource-path: C:/Users/18317/DevSpace/DocHub/essay;C:/Users/18317/DevSpace/DocHub/assets;
author:
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
abstract: We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.
url: https://spla-tam.github.io
---
# Introduction



We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.


# Related Work


We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.

# Method


## Depth Reprojection 


Depth at a pixel $i$ is represented by combining contributions from multiple Gaussian elements, each associated with a certain depth and confidence. Depth $D_i$ can be expressed as[@kerbl3dGaussianSplatting2023]:
$$ 
D_i = \frac{\sum_{n \leq N} d_n \cdot c_n \cdot \alpha_n \cdot T_n}{\sum_{n \leq N} c_n \cdot \alpha_n \cdot T_n} 
$$
$d_n$ is the depth value from the $n$-th Gaussian, $c_n$ is the confidence or weight of the $n$-th Gaussian,$\alpha_n$ is the opacity calculated from Gaussian parameters, $T_n$ is the product of transparencies from all Gaussians in front of the $n$-th Gaussian.

The reprojection method utilizes the alignment of 2D Gaussian projections with observed depth data from an RGB-D camera. This involves adjusting the parameters of the Gaussians to minimize the discrepancy between the projected depth and the observed depth. The offset $\Delta_n$ and the covariance matrix $\Sigma'$ are crucial for calculating the Gaussian weights $\alpha_n$ and their impact on reprojection accuracy.

## Camera Tracking

## loss



The loss function is designed to ensure accurate depth estimations and edge alignment, incorporating both depth magnitude and contour accuracy. It can be defined as:
$$ 
L = \lambda_1 \cdot L_{\text{depth}} + \lambda_2 \cdot L_{\text{contour}} 
$$
where: $L_{\text{depth}} = \sum_i |D_i^{\text{predicted}} - D_i^{\text{observed}}|$ represents the L1 loss for depth accuracy, $L_{\text{contour}} = \sum_j |\nabla D_j^{\text{predicted}} - \nabla D_j^{\text{observed}}|$ focuses on the alignment of depth contours or edges, $\lambda_1$ and $\lambda_2$ are weights that balance the two parts of the loss function, tailored to the specific requirements of the application.


# Experiments


We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.

# Conclusion


We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.