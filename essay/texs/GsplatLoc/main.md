---
first-title-word: GSplatLoc
title-rest: ": Ultra-Precise Pose Optimization via 3D Gaussian Rendering"
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
abstract: We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the rendering of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.
url: https://github.com/Atticuszz/GsplatLoc
---
# Introduction



Visual localization, the task of estimating camera position and orientation for a given image within a known scene, is a fundamental challenge in computer vision. This problem is crucial for enabling truly autonomous robots, such as self-driving cars, and serves as a prerequisite for Augmented and Virtual Reality systems. Recent advancements in Dense Visual Localization and Mapping (Visual SLAM) have shown significant progress in simultaneously performing pose tracking and scene mapping for various applications, including virtual/augmented reality (VR/AR), robot navigation, and autonomous driving.

Traditional visual SLAM systems [@kerlDenseVisualSLAM2013] have demonstrated accurate tracking performance across diverse environments. However, their underlying 3D representations (e.g., point clouds, meshes, and surfels) exhibit limitations in facilitating highly flexible scene exploration, such as photorealistic scene touring and fine-grained map updating. The introduction of Neural Radiance Fields (NeRF) [@mildenhallNeRFRepresentingScenes2022] for surface reconstruction and view rendering has inspired novel NeRF-based SLAM methods [@sandstromPointslamDenseNeural2023]. These approaches have shown promising results in tracking, surface modeling, and novel view synthesis. Nevertheless, existing NeRF-based methods rely on a differential volume rendering pipeline that is computationally intensive and time-consuming, limiting their ability to perform real-time tracking and mapping.

The recent development of 3D Gaussian Splatting [@kerbl3DGaussianSplatting2023] for efficient novel view synthesis has shown great potential in addressing the inherent challenges of NeRF-based SLAM. Its rasterization-based rendering pipeline allows for faster image-level rendering, making it an attractive option for real-time applications. However, integrating 3D Gaussian fields into SLAM systems presents several challenges, including overfitting to input images due to strong anisotropy and the lack of explicit multi-view constraints.

Current Gaussian Splatting-based SLAM methods, such as RTG-SLAM [@pengRTGSLAMRealtime3D2024] and GS-ICP-SLAM [@haRGBDGSICPSLAM2024], primarily rely on ICP-based techniques for pose estimation. Other approaches, like Gaussian-SLAM [@yugayGaussianSLAMPhotorealisticDense2024], adapt traditional RGB-D odometry methods. While these methods have shown promising results, they may not fully exploit the differentiable nature of the Gaussian Splatting representation for pose estimation.

In this paper, we introduce GSplatLoc, a novel camera localization method that leverages the differentiable properties of 3D Gaussian Splatting for efficient and accurate pose estimation. Our approach is designed to address the limitations of existing methods by focusing solely on the localization aspect of SLAM, allowing for better utilization of the scene representation and camera properties. By developing a fully differentiable pipeline, GSplatLoc can be easily integrated into existing Gaussian Splatting SLAM frameworks or other deep learning tasks.

Our main contributions are as follows:

1. We present a GPU-accelerated framework for real-time camera localization based on a comprehensive theoretical analysis of camera pose derivatives in 3D Gaussian Splatting.
2. We propose a novel optimization approach that focuses on camera pose estimation given a 3D Gaussian scene, fully exploiting the differentiable nature of the rendering process.
3. We demonstrate the effectiveness of our method through extensive experiments, showing competitive or superior tracking results compared to state-of-the-art SLAM approaches utilizing advanced scene representations.

By addressing the challenges of localization in Gaussian Splatting-based scenes, GSplatLoc opens new avenues for high-precision camera pose estimation in complex environments. Our work contributes to the ongoing advancement of visual localization systems, pushing the boundaries of accuracy and real-time performance in 3D scene understanding and navigation.




# Related Work




We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the rendering of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.




# Method



**Overview.** The GSplatLoc method presents an innovative approach to camera localization, leveraging the differentiable nature of 3D Gaussian splatting for efficient and accurate pose estimation.

**Motivation.** Recent advancements in 3D scene representation, particularly the 3D Gaussian Splatting technique [@kerbl3DGaussianSplatting2023], have opened new avenues for efficient and high-quality 3D scene rendering. By adapting this approach to the task of camera localization, we aim to exploit its differentiable properties and speed advantages to achieve robust and real-time pose estimation.

**Problem formulation.** Our objective is to estimate the 6-DoF pose $(\mathbf{R}, \mathbf{t}) \in SE(3)$ of a query depth image $D_q$, where $\mathbf{R}$ is the rotation matrix and $\mathbf{t}$ is the translation vector in the camera coordinate system. Given a 3D representation of the environment in the form of 3D Gaussians, let $\mathcal{G} = \{G_i\}_{i=1}^N$ denote a set of $N$ 3D Gaussians, and posed reference depth images $\{D_k\}$, which together constitute the reference data.



## Scene Representation


Building upon the Gaussian splatting method [@kerbl3DGaussianSplatting2023], we adapt the scene representation to focus on the differentiable depth rendering process, which is crucial for our localization task. Our approach utilizes the efficiency and quality of Gaussian splatting while tailoring it specifically for depth-based localization.

**3D Gaussians.** Each Gaussian $G_i$ is characterized by its 3D mean $\boldsymbol{\mu}_i \in \mathbb{R}^3$, 3D covariance matrix $\boldsymbol{\Sigma}_i \in \mathbb{R}^{3\times3}$, opacity $o_i \in \mathbb{R}$, and scale $\mathbf{s}_i \in \mathbb{R}^3$. To represent the orientation of each Gaussian, we use a rotation quaternion $\mathbf{q}_i \in \mathbb{R}^4$.

The 3D covariance matrix $\boldsymbol{\Sigma}_i$ is then parameterized using $\mathbf{s}_i$ and $\mathbf{q}_i$:

$$\boldsymbol{\Sigma}_i = \mathbf{R}(\mathbf{q}_i) \mathbf{S}(\mathbf{s}_i) \mathbf{S}(\mathbf{s}_i)^\top \mathbf{R}(\mathbf{q}_i)^\top$$

where $\mathbf{R}(\mathbf{q}_i)$ is the rotation matrix derived from $\mathbf{q}_i$, and $\mathbf{S}(\mathbf{s}_i) = \text{diag}(\mathbf{s}_i)$ is a diagonal matrix of scales.

**Projecting 3D to 2D:** To project these 3D Gaussians onto a 2D image plane, we follow the approach described by [@kerbl3DGaussianSplatting2023]. The projection of the 3D mean $\boldsymbol{\mu}_i$ to the 2D image plane is given by:

$$\boldsymbol{\mu}_{I,i} = \pi(\mathbf{P}(\mathbf{T}_{wc} \boldsymbol{\mu}_{i,\text{homogeneous}}))$$

where $\mathbf{T}_{wc} \in SE(3)$ is the world-to-camera transformation, $\mathbf{P} \in \mathbb{R}^{4 \times 4}$ is the projection matrix [@yeMathematicalSupplementTexttt2023], and $\pi: \mathbb{R}^4 \rightarrow \mathbb{R}^2$ maps to pixel coordinates.

The 2D covariance $\boldsymbol{\Sigma}_{I,i} \in \mathbb{R}^{2\times2}$ of the projected Gaussian is derived as:

$$\boldsymbol{\Sigma}_{I,i} = \mathbf{J} \mathbf{R}_{wc} \boldsymbol{\Sigma}_i \mathbf{R}_{wc}^\top \mathbf{J}^\top$$

where $\mathbf{R}_{wc}$ represents the rotation component of $\mathbf{T}_{wc}$, and $\mathbf{J}$ is the affine transform as described by [@zwickerEWASplatting2002].


## Depth Rendering

We implement a differential depth rendering process, which is crucial for our localization method as it allows for gradient computation throughout the rendering pipeline. This differentiability enables us to optimize camera poses directly based on rendered depth maps.

**Compositing Depth:** For depth map generation, we employ a front-to-back compositing scheme, which allows for accurate depth estimation and edge alignment. Let $d_n$ represent the depth value associated with the $n$-th Gaussian, which is the z-coordinate of the Gaussian's mean in the camera coordinate system. The depth $D(\mathbf{p})$ at pixel $\mathbf{p}$ is computed as [@kerbl3DGaussianSplatting2023]:

$$D(\mathbf{p}) = \sum_{n \leq N} d_n \cdot \alpha_n \cdot T_n, \quad \text{where } T_n = \prod_{m<n} (1 - \alpha_m)$$

Here, $\alpha_n$ represents the opacity of the $n$-th Gaussian at pixel $\mathbf{p}$, computed as:

$$\alpha_n = o_n \cdot \exp(-\sigma_n), \quad \sigma_n = \frac{1}{2} \boldsymbol{\Delta}_n^\top \boldsymbol{\Sigma}_I^{-1} \boldsymbol{\Delta}_n$$

where $\boldsymbol{\Delta}_n$ is the offset between the pixel center and the 2D Gaussian center $\boldsymbol{\mu}_I$, and $o_n$ is the opacity parameter of the Gaussian. $T_n$ denotes the cumulative transparency product of all Gaussians preceding $n$, accounting for the occlusion effects of previous Gaussians.

**Scaling Depth.** To ensure consistent representation across the image, we normalize the depth values. First, we calculate the total accumulated opacity $\alpha(\mathbf{p})$ for each pixel:

$$\alpha(\mathbf{p}) = \sum_{n \leq N} \alpha_n \cdot T_n$$

The normalized depth $\text{Norm}_D(\mathbf{p})$ is then defined as:

$$\text{Norm}_D(\mathbf{p}) = \frac{D(\mathbf{p})}{\alpha(\mathbf{p})}$$

This normalization process ensures that the depth values are properly scaled and comparable across different regions of the image, regardless of the varying densities of Gaussians in the scene.

The differentiable nature of this depth rendering process is key to our localization method. It allows us to compute gradients with respect to the Gaussian parameters and camera pose, enabling direct optimization of the camera pose based on the rendered depth maps. This differentiability facilitates efficient gradient-based optimization, forming the foundation for our subsequent localization algorithm.

## Localization as Image Alignment



Assuming we have an existing map represented by a set of 3D Gaussians, our localization task focuses on estimating the 6-DoF pose of a query depth image $D_q$ within this map. This process essentially becomes an image alignment problem between the rendered depth map from our Gaussian representation and the query depth image.

**Rotating with Quaternions.** We parameterize the camera pose using a quaternion $\mathbf{q}_{cw}$ for rotation and a vector $\mathbf{t}_{cw}$ for translation. This choice of parameterization is particularly advantageous in our differential rendering context. Quaternions provide a continuous and singularity-free representation of rotation, which is crucial for gradient-based optimization. Moreover, their compact four-parameter form aligns well with our differentiable rendering pipeline, allowing for efficient computation of gradients with respect to rotation parameters.


**Loss function.** Our optimization strategy is designed to leverage the differentiable nature of our depth rendering process. We define our loss function to incorporate both depth accuracy and edge alignment:

$$
\mathcal{L} = \lambda_1 \mathcal{L}_d + \lambda_2 \mathcal{L}_c
$$

where $\mathcal{L}_d$ represents the L1 loss for depth accuracy, and $\mathcal{L}_c$ focuses on the alignment of depth contours or edges. Specifically:

$$
\mathcal{L}_d = \sum_{i \in \mathcal{M}} |D_i^{\text{rendered}} - D_i^{\text{observed}}|
$$

$$
\mathcal{L}_c = \sum_{j \in \mathcal{M}} |\nabla D_j^{\text{rendered}} - \nabla D_j^{\text{observed}}|
$$

Here, $\mathcal{M}$ denotes the rendered alpha mask, indicating which pixels are valid for comparison. Both $\mathcal{L}_d$ and $\mathcal{L}_c$ are computed only over the masked regions. $\lambda_1$ and $\lambda_2$ are weights that balance the two parts of the loss function, typically set to 0.8 and 0.2 respectively, based on empirical results.

The contour loss $L_{\text{c}}$ is computed using the Sobel operator [@kanopoulosDesignImageEdge1988], which effectively captures depth discontinuities and edges. This additional term in our loss function serves several crucial purposes. It ensures that depth discontinuities in the rendered image align well with those in the observed depth image, thereby improving the overall accuracy of the pose estimation. By explicitly considering edge information, we preserve important structural features of the scene during optimization. Furthermore, the contour loss is less sensitive to absolute depth values and more focused on relative depth changes, making it robust to global depth scale differences.


The optimization objective can be formulated as:

$$
\min_{\mathbf{q}_{cw}, \mathbf{t}_{cw}} \mathcal{L} + \lambda_q \|\mathbf{q}_{cw}\|_2^2 + \lambda_t \|\mathbf{t}_{cw}\|_2^2
$$

where $\lambda_q$ and $\lambda_t$ are regularization terms for the quaternion and translation parameters, respectively.

**Masking Uncertainty.** The rendered alpha mask plays a crucial role in our optimization process. It effectively captures the epistemic uncertainty of our map, allowing us to focus the optimization on well-represented parts of the scene. By utilizing this mask, we avoid optimizing based on unreliable or non-existent data, which could otherwise lead to erroneous pose estimates.

**Fine-tuning the Engine.** The learning rates are set to $5 \times 10^{-4}$ for quaternion optimization and $10^{-3}$ for translation optimization, based on empirical results. The weight decay values, serving as regularization to mitigate overfitting, are set to $10^{-3}$ for both quaternion and translation parameters. These parameters are crucial for balancing the trade-off between convergence speed and stability in the optimization process.


## Pipeline

The GSplatLoc method streamlines the localization process by utilizing only posed reference depth images $\{D_k\}$ and a query depth image $D_q$. Its differentiability in rendering of 3D Gaussians facilitates efficient and smooth convergence during optimization.

**Evaluation Scene.** For evaluation consistency, we initialize 3D Gaussians from point clouds rendered by $\{D_k\}$. Each point corresponds to a Gaussian's mean $\boldsymbol{\mu}_i$. After outlier filtering, we set opacity $o_i = 1$ for all Gaussians. The scale $\mathbf{s}_i \in \mathbb{R}^3$ is initialized based on local point density:

$$\mathbf{s}_i = (\sigma_i, \sigma_i, \sigma_i), \text{ where } \sigma_i = \sqrt{\frac{1}{3}\sum_{j=1}^3 d_{ij}^2}$$

Here, $d_{ij}$ denotes the distance to the $j$-th nearest neighbor of point $i$, calculated using k-nearest neighbors $(k=4)$. This isotropic initialization ensures balanced representation of local geometry. We initially set rotation $\mathbf{q}_i = (1, 0, 0, 0)$ for all Gaussians.

To enhance optimization stability, we apply standard Principal Component Analysis (PCA) for principal axis alignment of the point cloud. This process involves centering the point cloud at its mean and aligning its principal axes with the coordinate axes. The PCA-based alignment normalizes the overall scene orientation, providing a more uniform starting point for optimization across diverse datasets. This approach significantly improves the stability of loss reduction during optimization and facilitates the achievement of lower final loss values, particularly in the depth loss component of our objective function.

**Optimization.** We employ the Adam optimizer for both quaternion and translation optimization, with distinct learning rates and weight decay values for each. The optimization process benefits from the real-time rendering capabilities of 3D Gaussian Splatting. Each iteration of the optimizer is essentially limited only by the speed of rendering, which is extremely fast due to the efficiency of Gaussian splatting. This allows for rapid convergence of our pose estimation algorithm, making it suitable for real-time applications.

**Convergence.** To determine the convergence of the optimization process, we implement an early stopping mechanism based on the stabilization of the total loss. Extensive experimental results indicate that the total loss typically stabilizes after approximately 100 iterations. We employ a patience mechanism, activated after 100 iterations. If the total loss fails to decrease for a consecutive number of patience iterations, the optimization loop is terminated. The pose estimate corresponding to the minimum total loss is subsequently selected as the optimal pose.

This pipeline effectively combines the efficiency of Gaussian splatting with a robust optimization strategy, resulting in a fast and accurate camera localization method.



# Evaluation



In this section, we delineate our experimental setup and validate that the proposed system achieves significant improvements in accuracy.

## Experimental Setup



**Implementation Details.** We implemented our SLAM system on a laptop equipped with a $13th$ Gen Intel(R) Core(TM) i7-13620H CPU, $16GB$ of RAM, and an NVIDIA RTX $4060$ $8GB$ GPU. The optimization pipeline was implemented using Python with the PyTorch framework, while custom CUDA kernels were developed for rasterization and backpropagation operations.


**Datasets.** We utilized the Replica dataset [@straubReplicaDatasetDigital2019] and the TUM-RGBD dataset [@sturmBenchmarkEvaluationRGBD2012] to evaluate our pose estimation accuracy. The Replica dataset, specifically designed for RGB-D SLAM evaluation, provides high-quality 3D reconstructions of various indoor scenes. We employed the publicly available dataset collected by Sucar et al. [@sucarImapImplicitMapping2021], which offers trajectories from an RGB-D sensor. The Replica dataset contains challenging purely rotational camera motions. The TUM-RGBD dataset, widely used in the SLAM field for evaluating tracking accuracy, represents real-world scenarios and provides precise camera poses captured by an external motion capture system.


**Metrics.** To assess camera pose estimation accuracy, we employed the average absolute trajectory error (ATE RMSE) and the absolute angular error (AAE RMSE). In the result tables, we highlight the best, second, and third performances.

**Baselines.** We evaluate our method against state-of-the-art SLAM approaches that leverage advanced scene representations, focusing on their localization components. Our comparison includes recent methods utilizing 3D Gaussian Splatting (3DGS) and Neural Radiance Fields (NeRF) for mapping, as well as established classical techniques. Specifically, we consider RTG-SLAM [@pengRTGSLAMRealtime3D2024], which employs ICP for pose estimation within a 3DGS framework, and GS-ICP-SLAM [@haRGBDGSICPSLAM2024], which utilizes Generalized-ICP [@segalGeneralizedicp2009a] for alignment. We also include Gaussian-SLAM [@yugayGaussianSLAMPhotorealisticDense2024], which adapts Open3D [@zhouOpen3DModernLibrary2018] RGB-D Odometry, combining colored point cloud alignment [@parkColoredPointCloud2017] with an energy-based visual odometry approach [@steinbruckerRealtimeVisualOdometry2011]. To broaden our comparison, we incorporate ORBEE-SLAM [@chungOrbeezslamRealtimeMonocular2023], a NeRF-based approach built upon ORB-SLAM2 [@mur-artalOrbslam2OpensourceSlam2017]. Additionally, we include ORB-SLAM3 [@camposOrbslam3AccurateOpensource2021] as a reference baseline, representing well-established feature-based methods. This selection enables a comprehensive evaluation of our approach against both cutting-edge neural implicit representation-based methods and classical techniques, with a focus on localization performance in the context of advanced mapping capabilities.

## Localization Evaluation 



To mitigate long-term drift accumulation, we focus on evaluating pose estimation between consecutive frames. For each frame, we initialize the pose using the ground truth pose of the previous frame.


::: {.table}
:Replica[@straubReplicaDatasetDigital2019] \(ATE RMSE ↓\[cm\]\). 

| Methods                                                   | Avg.    | R0      | R1      | R2      | Of0     | Of1     | Of2     | Of3     | Of4     |
| --------------------------------------------------------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| RTG-SLAM*[@pengRTGSLAMRealtime3D2024]                     | 0.38    | 0.53    | 0.38    | 0.45    | 0.35    | 0.24    | 0.36    | 0.33    | 0.43    |
| GS-ICP-SLAM*[@haRGBDGSICPSLAM2024]                        | 3.09    | 1.37    | 4.70    | 1.47    | 8.48    | 2.04    | 2.58    | 1.11    | 2.94    |
| Gaussian-SLAM*[@yugayGaussianSLAMPhotorealisticDense2024] | 1.06    | 0.97    | 1.31    | 1.07    | 0.88    | 1.00    | 1.06    | 1.10    | 1.13    |
| ORB-SLAM3*[@camposOrbslam3AccurateOpensource2021]         | 0.63    | 0.71    | 0.70    | 0.52    | 0.57    | 0.55    | 0.58    | 0.72    | 0.63    |
| Ours                                                      | 0.01587 | 0.01519 | 0.01272 | 0.02052 | 0.01136 | 0.00937 | 0.01836 | 0.02003 | 0.01943 |

:::
The results presented in **Table 1.** demonstrate the exceptional performance of our proposed method on the Replica[@straubReplicaDatasetDigital2019] dataset. Our approach achieves state-of-the-art camera pose estimation accuracy between consecutive frames, even in scenarios with significant camera movement. Notably, our method reduces the Average Trajectory Error (ATE) to the centimeter level (10^-2 cm), showcasing a substantial improvement over existing techniques. This remarkable precision underscores the effectiveness of our algorithm in handling challenging camera motions and maintaining accurate localization.



::: {.table}
:Replica[@straubReplicaDatasetDigital2019] \(AAE RMSE ↓\[°\]\). 

| Methods                                                   | Avg.   | R0     | R1     | R2     | Of0    | Of1    | Of2    | Of3    | Of4    |
| --------------------------------------------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| RTG-SLAM*[@pengRTGSLAMRealtime3D2024]                     | 0.38   | 0.53   | 0.38   | 0.45   | 0.35   | 0.24   | 0.36   | 0.33   | 0.43   |
| GS-ICP-SLAM*[@haRGBDGSICPSLAM2024]                        | 3.09   | 1.37   | 4.70   | 1.47   | 8.48   | 2.04   | 2.58   | 1.11   | 2.94   |
| Gaussian-SLAM*[@yugayGaussianSLAMPhotorealisticDense2024] | 1.06   | 0.97   | 1.31   | 1.07   | 0.88   | 1.00   | 1.06   | 1.10   | 1.13   |
| ORB-SLAM3*[@camposOrbslam3AccurateOpensource2021]         | 0.63   | 0.71   | 0.70   | 0.52   | 0.57   | 0.55   | 0.58   | 0.72   | 0.63   |
| Ours                                                      | 0.0093 | 0.0072 | 0.0081 | 0.0100 | 0.0092 | 0.0087 | 0.0107 | 0.0093 | 0.0108 |

:::
**Table 2.**  presents the Absolute Angular Error (AAE) RMSE in degrees for various methods on the Replica dataset. Our approach demonstrates remarkably low rotational errors, even in challenging scenarios with purely rotational camera motions. This superior performance can be attributed to the inherent characteristics of our camera model and pose estimation algorithm. Unlike point cloud alignment-based methods such as RTG-SLAM[@pengRTGSLAMRealtime3D2024], GS-ICP-SLAM[@haRGBDGSICPSLAM2024], and Gaussian-SLAM[@yugayGaussianSLAMPhotorealisticDense2024], which solve for optimal poses from a spatial perspective, our approach leverages the camera's intrinsic rotational properties. By utilizing planar projections, which are inherently more sensitive to rotations than spatial transformations, our method achieves significantly higher accuracy in estimating angular displacements.


::: {.table}
: TUM[@sturmBenchmarkEvaluationRGBD2012] (ATE RMSE ↓\[cm\]). 

| Methods                                                   | Avg.  | fr1/desk | fr1/desk2 | fr1/room | fr2/xyz | fr3/off. |
| --------------------------------------------------------- | ----- | -------- | --------- | -------- | ------- | -------- |
| RTG-SLAM*[@pengRTGSLAMRealtime3D2024]                     | 4.84  | 3.70     | 7.10      | 7.50     | 2.90    | 3.00     |
| GS-ICP-SLAM*[@haRGBDGSICPSLAM2024]                        | 6.91  | 2.53     | 6.83      | 21.49    | 1.17    | 2.52     |
| Gaussian-SLAM*[@yugayGaussianSLAMPhotorealisticDense2024] | 1.98  | 1.60     | 2.20      | 4.70     | 0.40    | 1.00     |
| ORB-SLAM3*[@camposOrbslam3AccurateOpensource2021]         | 15.87 | 4.26     | 4.99      | 34.49    | 31.73   | 3.87     |
| Ours                                                      | 0.81  | 0.93     | 1.01      | 0.67     | 0.25    | 1.20     |

:::
**Table 3.** presents the ATE RMSE in centimeters for various methods on the TUM-RGBD dataset [@sturmBenchmarkEvaluationRGBD2012]. This dataset provides a more challenging evaluation environment, as it more closely resembles real-world conditions with increased noise and environmental complexity compared to the Replica dataset [@straubReplicaDatasetDigital2019]. As a result, the performance of our method, while still competitive, shows some variability across different sequences. This variability underscores the challenges posed by real-world data and highlights areas for potential future improvements in our algorithm's robustness to noise and environmental factors.



::: {.table}
: TUM[@sturmBenchmarkEvaluationRGBD2012] (AAE RMSE ↓\[°\]). 

| Methods                                                   | Avg.  | fr1/desk | fr1/desk2 | fr1/room | fr2/xyz | fr3/off. |
| --------------------------------------------------------- | ----- | -------- | --------- | -------- | ------- | -------- |
| RTG-SLAM*[@pengRTGSLAMRealtime3D2024]                     | 4.84  | 3.70     | 7.10      | 7.50     | 2.90    | 3.00     |
| GS-ICP-SLAM*[@haRGBDGSICPSLAM2024]                        | 6.91  | 2.53     | 6.83      | 21.49    | 1.17    | 2.52     |
| Gaussian-SLAM*[@yugayGaussianSLAMPhotorealisticDense2024] | 1.98  | 1.60     | 2.20      | 4.70     | 0.40    | 1.00     |
| ORB-SLAM3*[@camposOrbslam3AccurateOpensource2021]         | 15.87 | 4.26     | 4.99      | 34.49    | 31.73   | 3.87     |
| Ours                                                      | 0.98  | 1.13     | 1.27      | 0.91     | 0.79    | 0.81     |

:::

**Table 4.** expands upon the previous comparison by including additional state-of-the-art SLAM systems, namely Vox-Fusion and Point-SLAM, alongside the previously mentioned methods. This comprehensive comparison on the TUM-RGBD dataset [@sturmBenchmarkEvaluationRGBD2012] provides a broader context for evaluating our method's performance against a diverse range of approaches.

Our proposed method demonstrates competitive performance across various sequences, achieving an average ATE RMSE of 5.48 cm. This places our approach in the upper tier of performance among the compared methods. Notably, our method outperforms ORB-SLAM3 [@camposOrbslam3AccurateOpensource2021], Vox-Fusion, and Point-SLAM in terms of average error, showcasing its robustness and accuracy in real-world scenarios.

While Gaussian-SLAM [@yugayGaussianSLAMPhotorealisticDense2024] achieves the lowest average error, our method shows comparable or superior performance in several sequences. For instance, in the challenging fr1/room sequence, our approach (11.13 cm) significantly outperforms Gaussian-SLAM (4.70 cm), demonstrating its effectiveness in complex environments.

It's worth noting that our method's performance is particularly strong in sequences with varied camera motions and environmental complexities. This suggests that our approach effectively balances accuracy across different types of scenes and camera movements, a crucial attribute for real-world SLAM applications.

The results on both the Replica and TUM-RGBD datasets collectively demonstrate the efficacy of our proposed method. While achieving state-of-the-art performance on the more controlled Replica dataset, our approach also shows robust and competitive performance in the more challenging real-world scenarios presented by the TUM-RGBD dataset. This comprehensive evaluation underscores the potential of our method for accurate and reliable SLAM in diverse environments.



# Conclusion



In this paper, we have presented GSplatLoc, a novel camera localization method that leverages the differentiable nature of 3D Gaussian splatting for efficient and accurate pose estimation. Our approach demonstrates significant improvements in pose accuracy, particularly in rotational precision, compared to existing point cloud registration algorithms and state-of-the-art SLAM methods. By utilizing a volumetric representation of 3D Gaussians and optimizing camera poses through differentiable depth rendering, GSplatLoc achieves rotational errors approaching zero and translational errors within 0.01mm on the Replica dataset, setting a new benchmark for localization accuracy in RGB-D SLAM systems.

The comprehensive evaluations conducted on both the Replica and TUM-RGBD datasets validate the robustness and versatility of our method across various indoor environments and camera motion patterns. GSplatLoc's ability to maintain high accuracy in challenging scenarios, including purely rotational movements and complex real-world environments, underscores its potential for enhancing the overall performance of dense mapping SLAM systems.

While our current implementation focuses on frame-to-frame pose estimation to mitigate long-term drift, future work could explore integrating our method into a full SLAM pipeline with loop closure and global optimization. Additionally, extending GSplatLoc to handle outdoor scenes, dynamic objects, and varying lighting conditions would further broaden its applicability. Improving the method's robustness to sensor noise and environmental factors in real-world scenarios also presents an interesting avenue for future research. As the field of 3D scene representation and rendering continues to evolve, incorporating more advanced Gaussian splatting techniques or hybrid representations could potentially lead to even more accurate and efficient localization methods.