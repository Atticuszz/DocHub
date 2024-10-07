---
first-title-word: "ABGICP:"
title-rest: "Photo-realistic Dense SLAM with Gaussian Splatting"
bibliography: C:/Users/18317/DevSpace/DocHub/essay/zotero/bibliography.bib
csl: C:/Users/18317/DevSpace/DocHub/essay/zotero/ieee.csl
resource-path: C:/Users/18317/DevSpace/DocHub/essay;C:/Users/18317/DevSpace/DocHub/assets;C:\Users\18317\DevSpace\DocHub\essay\template\arxiv
author:
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Elias D. Striatum
    orcid: https://orcid.org/0000-0000-0000-0000
abstract: We present a dense simultaneous localization and mapping (SLAM) method that uses 3D Gaussians as a scene representation. Our approach enables interactive-time reconstruction and photo-realistic rendering from real-world single-camera RGBD videos. To this end, we propose a novel effective strategy for seeding new Gaussians for newly explored areas and their effective online optimization that is independent of the scene size and thus scalable to larger scenes. This is achieved by organizing the scene into sub-maps which are independently optimized and do not need to be kept in memory. We further accomplish frame-tomodel camera tracking by minimizing photometric and geometric losses between the input and rendered frames. The Gaussian representation allows for high-quality photo-realistic real-time rendering of real-world scenes. Evaluation on synthetic and real-world datasets demonstrates competitive or superior performance in mapping, tracking, and rendering compared to existing neural dense SLAM methods.
url: https://spla-tam.github.io
---

# Introduction

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

# Related Work

in the image,[@caiIkdTreeIncrementalKD2021] typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**[@keethaSplaTAMSplatTrack2024]
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

# Method

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

## Gaussian Splatting

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by[@koideVoxelizedGicpFast2021] the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

$$\mathrm{RMSE}_{eT}=\sqrt{\frac1N\sum_{i=1}^N\left(\|t_i-t_i^{\prime}\|\right)^2}$$
in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

# Experiments

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

# Conclusion

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units [@haRGBDGSICPSLAM2024]used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.

in the image, typically given in pixels.$f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.$d$: Depth value at the pixel $(u, v)$ [@kornColorSupportedGeneralizedICP2014a]after scaling, given in meters.$I_d(u, v)$: Depth value from the _original depth image_ at pixel $(u, v)$, typically given in the units used by the depth sensor.$s$: Scale factor to convert the depth values from the depth image units to meters.$\mathbf{p}$ : 3D point in _camera coordinates_, represented as a vector.Keetha and colleagues mention something important .
**Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
The final array, points, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.
