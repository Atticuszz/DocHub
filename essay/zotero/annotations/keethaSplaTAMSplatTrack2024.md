---
Title: "SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM"
Authors: Nikhil Keetha, Jay Karhade, Krishna Murthy Jatavallabhula, Gengshan Yang, Sebastian Scherer, Deva Ramanan, Jonathon Luiten

Date: 2024-04-16
citekey: keethaSplaTAMSplatTrack2024
tags: #Computer-Science---Artificial-Intelligence, #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics
---

## SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM

**Bibliographie :** [1]

N. Keetha _et al._, ‘SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM’, Apr. 16, 2024, _arXiv_: arXiv:2312.02126. Accessed: Jun. 09, 2024. [Online]. Available: [http://arxiv.org/abs/2312.02126](http://arxiv.org/abs/2312.02126)

**Lien de la publication :** http://arxiv.org/abs/2312.02126

**Lien Zotero :** [Keetha et al. - 2024 - SplaTAM Splat, Track & Map 3D Gaussians for Dense.pdf](zotero://select/library/items/WUQKHF5Y)

**Tags :** #Computer-Science---Artificial-Intelligence, #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics

> [!abstract]+
> _« Dense simultaneous localization and mapping (SLAM) is crucial for robotics and augmented reality applications. However, current methods are often hampered by the non-volumetric or implicit way they represent a scene. This work introduces SplaTAM, an approach that, for the first time, leverages explicit volumetric representations, i.e., 3D Gaussians, to enable high-fidelity reconstruction from a single unposed RGB-D camera, surpassing the capabilities of existing methods. SplaTAM employs a simple online tracking and mapping system tailored to the underlying Gaussian representation. It utilizes a silhouette mask to elegantly capture the presence of scene density. This combination enables several benefits over prior representations, including fast rendering and dense optimization, quickly determining if areas have been previously mapped, and structured map expansion by adding more Gaussians. Extensive experiments show that SplaTAM achieves up to 2x superior performance in camera pose estimation, map construction, and novel-view synthesis over existing methods, paving the way for more immersive high-fidelity SLAM applications. »_

> [!Annotation|#f19837]+
> _« spla-tam.github.io »_([1](zotero://open-pdf/library/items/WUQKHF5Y?page=1&annotation=PAWJN6QZ))

> [!Annotation|#2ea8e5]+
> _« Gaussian Splatting [14] renders an RGB image as follows: Given a collection of 3D Gaussians and camera pose, first sort all Gaussians from front-to-back. RGB images can then be efficiently rendered by alpha-compositing the splatted 2D projection of each Gaussian in order in pixel space. The rendered color of pixel p = (u, v) can be written as: »_([7](zotero://open-pdf/library/items/WUQKHF5Y?page=7&annotation=N5U7KQ5N))

> [!Annotation|#5fb236]+
> _« The camera pose is initialized for a new timestep by a constant velocity forward projection of the pose parameters in the camera center + quaternion space. E.g. the camera parameters are initialized using the following: Et+1 = Et + (Et − Et-1) (7) The camera pose is then updated iteratively by gradientbased optimization through differentiably rendering RGB, depth, and silhouette maps, and updating the camera parameters to minimize the following loss while keeping the Gaussian parameters fixed: »_([7](zotero://open-pdf/library/items/WUQKHF5Y?page=7&annotation=H7Z8DGNZ))
>
> ### 定位方式解析

#### 定位方法简介

SplaTAM (Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM) 方法通过3D高斯点（3D Gaussian Splats）进行实时SLAM。该方法结合了微分渲染和梯度优化，实现了高保真度的相机跟踪和场景重建。

#### 详细解析

1. **相机跟踪**

相机跟踪通过最小化当前RGB-D帧和渲染图像之间的误差来估计相机姿态。具体步骤如下：

- **初始相机姿态**：使用恒速前向投影初始化相机姿态：
    $$
  E_{t+1} = E_t + (E_t - E_{t-1})
  $$

- **误差计算**：通过微分渲染计算RGB、深度和剪影图像，并使用梯度优化更新相机参数，最小化以下损失：
    $$
  L_t = \sum_p \left[ \mathbb{1}(S(p) > 0.99) \cdot L1(D(p)) + 0.5 \cdot L1(C(p)) \right]
  $$
    其中，$S(p)$ 是剪影图像，$D(p)$ 和 $C(p)$ 分别是深度和颜色渲染，$L1$ 表示L1损失函数【24†source】。

2. **高斯致密化**

在每个输入帧中，基于当前帧的深度图和渲染剪影图像，系统通过以下步骤添加新的高斯点：

- **致密化掩码**：生成一个致密化掩码来确定需要增加高斯点的像素：
    $$
  M(p) = \mathbb{1}\left(S(p) < 0.5 + \left|D_{GT}(p) - D(p)\right| \cdot \frac{L1(D(p))}{\lambda \cdot MDE}\right)
  $$
    其中，$D_{GT}(p)$ 是地面真实深度，$MDE$ 是中位深度误差，$\lambda$ 是经验选定的阈值【24†source】。

3. **地图更新**

通过微分渲染和梯度优化更新3D高斯地图的参数：

- **选择关键帧**：选择与当前帧重叠度最高的前几个关键帧，并优化这些帧的高斯参数。
- **损失函数**：与跟踪过程类似，但不使用剪影掩码，优化所有像素的RGB和深度误差，同时添加SSIM损失，剔除不透明度接近0或过大的无用高斯点【24†source】。

### 定位部分的评估标准及实验数据展示

#### 评估标准

1. **平均绝对轨迹误差 (ATE) 的根均方误差 (RMSE)**：
      - 评估相机轨迹的精度。
      - 计算方法：比较估计轨迹与真实轨迹的差异。

2. **图像质量指标**：
      - **峰值信噪比 (PSNR)**：用于评估重建地图的质量，值越高表示质量越好。
      - **结构相似性指数 (SSIM)**：用于评估重建图像与参考图像的相似度，值越高表示相似度越高。
      - **感知图像对比性损失 (LPIPS)**：用于评估图像感知质量，值越低表示质量越好【24†source】。

> [!Annotation|#ff6666]+
> _« 4. Experimental Setup »_([9](zotero://open-pdf/library/items/WUQKHF5Y?page=9&annotation=ECX6QXBH))
>
> ## 定位部分评估标准与实验数据展示

### 评估标准

论文中使用了以下评估标准来评估定位部分的性能：

1. **平均绝对轨迹误差 (ATE RMSE)**:
      $$\text{ATE RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N} \| \mathbf{p}_i - \mathbf{\hat{p}}_i \|^2}$$
      其中，$\mathbf{p}_i$ 是真实轨迹点，$\mathbf{\hat{p}}_i$ 是估计轨迹点，$N$ 是总轨迹点数。

2. **RGB渲染性能**:
      - PSNR (峰值信噪比):
        $$\text{PSNR} = 10 \cdot \log_{10}\left(\frac{\text{MAX}^2}{\text{MSE}}\right)$$
        其中，$\text{MAX}$ 是像素值的最大可能值，$\text{MSE}$ 是均方误差。
      - SSIM (结构相似性指数):
        $$\text{SSIM}(\mathbf{x}, \mathbf{y}) = \frac{(2\mu_x \mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$$
      - LPIPS (感知损失):
        $$\text{LPIPS} = \|\mathbf{f}(\mathbf{x}) - \mathbf{f}(\mathbf{y})\|_2$$
        其中，$\mathbf{f}$ 是特征提取函数，$\mathbf{x}$ 和 $\mathbf{y}$ 是输入图像。

3. **深度渲染性能**:
      - 深度 L1 损失:
        $$\text{Depth L1} = \frac{1}{N}\sum_{i=1}^{N} |\mathbf{d}_i - \mathbf{\hat{d}}_i|$$
        其中，$\mathbf{d}_i$ 是真实深度值，$\mathbf{\hat{d}}_i$ 是估计深度值。

### 实验数据

论文中包含了多个数据集的实验数据，具体如下：

#### ScanNet++ 数据集

| Methods      | Avg   | S1    | S2    |
| ------------ | ----- | ----- | ----- |
| Point-SLAM   | 343.8 | 296.7 | 390.8 |
| ORB-SLAM3    | 158.2 | 156.8 | 159.7 |
| SplaTAM      | 1.2   | 0.6   | 1.9   |

#### Replica 数据集

| Methods       | Avg  | R0   | R1   | R2   | Of0  | Of1  | Of2  | Of3  | Of4  |
| ------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| DROID-SLAM    | 0.38 | 0.53 | 0.38 | 0.45 | 0.35 | 0.24 | 0.36 | 0.33 | 0.43 |
| Vox-Fusion    | 3.09 | 1.37 | 4.70 | 1.47 | 8.48 | 2.04 | 2.58 | 1.11 | 2.94 |
| NICE-SLAM     | 1.06 | 0.97 | 1.31 | 1.07 | 0.88 | 1.00 | 1.06 | 1.10 | 1.13 |
| ESLAM         | 0.63 | 0.71 | 0.70 | 0.52 | 0.57 | 0.55 | 0.58 | 0.72 | 0.63 |
| Point-SLAM    | 0.52 | 0.61 | 0.41 | 0.37 | 0.38 | 0.48 | 0.54 | 0.69 | 0.72 |
| SplaTAM       | 0.36 | 0.31 | 0.40 | 0.29 | 0.47 | 0.27 | 0.29 | 0.32 | 0.55 |

#### TUM-RGBD 数据集

| Methods       | Avg   | 0000  | 0059  | 0106  | 0169  | 0181  | 0207  |
| ------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Vox-Fusion    | 26.90 | 68.84 | 24.18 | 8.41  | 27.28 | 23.30 | 9.41  |
| NICE-SLAM     | 10.70 | 12.00 | 14.00 | 7.90  | 10.90 | 13.40 | 6.20  |
| Point-SLAM    | 12.19 | 10.24 | 7.81  | 8.65  | 22.16 | 14.77 | 9.54  |
| SplaTAM       | 11.88 | 12.83 | 10.10 | 17.72 | 12.08 | 11.10 | 7.46  |
