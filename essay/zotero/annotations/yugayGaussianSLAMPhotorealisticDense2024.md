---
Title: "Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting"
Authors: Vladimir Yugay, Yue Li, Theo Gevers, Martin R. Oswald

Date: 2024-03-22
citekey: yugayGaussianSLAMPhotorealisticDense2024
tags: #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics
---

## Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting

**Bibliographie :** [1]

V. Yugay, Y. Li, T. Gevers, and M. R. Oswald, ‘Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting’, Mar. 22, 2024, _arXiv_: arXiv:2312.10070. Accessed: Jun. 09, 2024. [Online]. Available: [http://arxiv.org/abs/2312.10070](http://arxiv.org/abs/2312.10070)

**Lien de la publication :** http://arxiv.org/abs/2312.10070

**Lien Zotero :** [Yugay et al_2024_Gaussian-SLAM.pdf](zotero://select/library/items/IPBKIVSA)

**Tags :** #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics

> [!abstract]+
> _« We present a dense simultaneous localization and mapping (SLAM) method that uses 3D Gaussians as a scene representation. Our approach enables interactive-time reconstruction and photo-realistic rendering from real-world single-camera RGBD videos. To this end, we propose a novel effective strategy for seeding new Gaussians for newly explored areas and their effective online optimization that is independent of the scene size and thus scalable to larger scenes. This is achieved by organizing the scene into sub-maps which are independently optimized and do not need to be kept in memory. We further accomplish frame-to-model camera tracking by minimizing photometric and geometric losses between the input and rendered frames. The Gaussian representation allows for high-quality photo-realistic real-time rendering of real-world scenes. Evaluation on synthetic and real-world datasets demonstrates competitive or superior performance in mapping, tracking, and rendering compared to existing neural dense SLAM methods. »_

> [!Annotation|#ff6666]+
>_« L tracking »_([17](zotero://open-pdf/library/items/IPBKIVSA?page=17&annotation=ZBQC3YE5))
>
> ### 定位方式的分析与公式

#### 相机姿态估计

相机姿态估计通过最小化输入帧与渲染帧之间的光度和几何误差来实现。其主要步骤如下：

1. **相机姿态初始化**：

$$
T_i = T_{i-1} + (T_{i-1} - T_{i-2})
$$

其中，$T_i$ 表示相机姿态，包括四元数 $q_i$ 和平移向量 $t_i$。

2. **跟踪损失函数**：

相对相机姿态 $T_{i-1,i}$ 在帧 $i-1$ 和 $i$ 之间，通过最小化跟踪损失 $L_{tracking}$ 进行估计：

$$
\arg \min_{T_{i-1,i}} L_{tracking}(Î(T_{i-1,i}), D̂(T_{i-1,i}), I_i, D_i, \alpha)
$$

其中，$Î(T_{i-1,i})$ 和 $D̂(T_{i-1,i})$ 分别是通过相对变换 $T_{i-1,i}$ 渲染的颜色和深度图，$I_i$ 和 $D_i$ 是帧 $i$ 的输入颜色和深度图。

3. **软alpha和误差掩码**：

为了避免跟踪损失受到未观察或重建不良区域的污染，引入软alpha掩码 $M_{alpha}$ 和误差掩码 $M_{inlier}$，其跟踪损失计算如下：

$$
L_{tracking} = \sum M_{inlier} \cdot M_{alpha} \cdot (\lambda_c | Î - I | + (1 - \lambda_c) | D̂ - D |)
$$

其中，$\lambda_c$ 是权重参数，$M_{alpha}$ 是alpha图的多项式，$M_{inlier}$ 是颜色和深度误差大于阈值的像素。

#### 高斯溅射模型

高斯溅射是将场景表示为3D高斯点云，用于新视图合成，其主要公式如下：

1. **3D高斯的均值和协方差**：

3D高斯参数化为均值 $\mu \in \mathbb{R}^3$、协方差 $\Sigma \in \mathbb{R}^{3 \times 3}$、不透明度 $o \in \mathbb{R}$ 和 RGB 颜色 $C \in \mathbb{R}^3$。投影到2D图像平面的均值 $\mu_I$ 计算公式：

$$
\mu_I = \pi P (T_{wc} \mu_{homogeneous})
$$

其中，$T_{wc} \in SE(3)$ 是世界到相机的变换矩阵，$P \in \mathbb{R}^{4 \times 4}$ 是 OpenGL 风格的投影矩阵，$\pi : \mathbb{R}^4 \rightarrow \mathbb{R}^2$ 是像素坐标的投影。

2. **2D协方差**：

投影后的2D协方差 $\Sigma_I$ 计算公式：

$$
\Sigma_I = J R_{wc} \Sigma R_{wc}^T J^T
$$

其中，$J \in \mathbb{R}^{2 \times 3}$ 是仿射变换矩阵，$R_{wc} \in SO(3)$ 是世界到相机变换的旋转部分。

3. **颜色渲染**：

受m个高斯影响的像素$i$处的颜色 $C_{ch,i}$ 计算公式：

$$
C_{ch,i} = \sum_{j \leq m} C_{ch,j} \cdot \alpha_j \cdot T_j, \quad T_j = \prod_{k<j} (1 - \alpha_k)
$$

其中，$\alpha_j$ 计算公式：

$$
\alpha_j = o_j \cdot \exp(-\sigma_j), \quad \sigma_j = \frac{1}{2} \Delta_j^T \Sigma_I^{-1} \Delta_j
$$

其中，$\Delta_j \in \mathbb{R}^2$ 是像素坐标与高斯均值之间的偏移量。

> [!Annotation|#ff6666]+
>_« 4 Experiments »_([17](zotero://open-pdf/library/items/IPBKIVSA?page=17&annotation=P72JCCVY))
>
> ### 定位部分的评估标准

本文中关于定位部分的评估标准主要包括跟踪精度和渲染性能。以下是具体的评估标准和实验数据展示：

#### 跟踪精度评估

1. **绝对轨迹误差（ATE）**：

评估相机轨迹与地面真值轨迹的偏差，计算轨迹点之间的均方根误差（RMSE）。

#### 实验数据表格

##### TUM-RGBD数据集上的跟踪性能

表格展示了不同方法在TUM-RGBD数据集上的跟踪性能比较：

| 方法              | desk (cm)↓ | xyz (cm)↓ | office (cm)↓ | 平均值 (cm)↓ |
|-----------------|-------------|-----------|--------------|--------------|
| NICE-SLAM [89]  | 4.3         | 31.7      | 3.9          | 13.3         |
| Vox-Fusion [78] | 3.5         | 1.5       | 26.0         | 10.3         |
| Point-SLAM [53] | 4.3         | 1.3       | 3.5          | 3.0          |
| SplaTAM∗ [23]   | 3.4         | 1.2       | 5.2          | 3.3          |
| Gaussian-SLAM   | 2.6         | 1.3       | 4.6          | 2.9          |

数据来源：TUM-RGBD数据集【12:15†Yugay et al_2024_Gaussian-SLAM2.pdf】

##### ScanNet数据集上的跟踪性能

表格展示了不同方法在ScanNet数据集上的跟踪性能比较：

| 方法              | 0000 (cm)↓ | 0059 (cm)↓ | 0106 (cm)↓ | 0169 (cm)↓ | 0181 (cm)↓ | 0207 (cm)↓ | 平均值 (cm)↓ |
|-----------------|-------------|------------|------------|------------|------------|------------|--------------|
| NICE-SLAM [89]  | 12.00       | 14.00      | 7.90       | 10.90      | 13.40      | 6.20       | 10.70         |
| Vox-Fusion [78] | 68.84       | 24.18      | 8.41       | 27.28      | 23.30      | 9.41       | 26.90         |
| Point-SLAM [53] | 10.24       | 7.81       | 8.65       | 22.16      | 14.77      | 9.54       | 12.19         |
| SplaTAM∗ [23]   | 12.83       | 10.10      | 17.72      | 12.08      | 11.10      | 7.46       | 11.88         |
| Gaussian-SLAM   | 24.75       | 8.63       | 11.27      | 14.59      | 18.70      | 14.36      | 15.38         |

数据来源：ScanNet数据集【12:15†Yugay et al_2024_Gaussian-SLAM2.pdf】

##### ScanNet++数据集上的跟踪性能

表格展示了不同方法在ScanNet++数据集上的跟踪性能比较：

| 方法              | b20a261fdf (cm)↓ | 8b5caf3398 (cm)↓ | fb05e13ad1 (cm)↓ | 2e74812d00 (cm)↓ | 281bc17764 (cm)↓ | 平均值 (cm)↓ |
|-----------------|-------------------|-------------------|-------------------|-------------------|-------------------|--------------|
| Point-SLAM [53] | 246.16            | 632.99            | 830.79            | 271.42            | 574.86            | 511.24       |
| ESLAM [34]      | 25.15             | 2.15              | 27.02             | 20.89             | 35.47             | 22.14        |
| SplaTAM∗ [23]   | 1.50              | 0.57              | 0.31              | 443.10            | 1.58              | 89.41        |
| Gaussian-SLAM   | 1.37              | 5.97              | 2.70              | 2.35              | 1.02              | 2.68         |

数据来源：ScanNet++数据集【

12:15†Yugay et al_2024_Gaussian-SLAM2.pdf】

##### Replica数据集上的跟踪性能

表格展示了不同方法在Replica数据集上的跟踪性能比较：

| 方法              | Rm0 (cm)↓ | Rm1 (cm)↓ | Rm2 (cm)↓ | Off0 (cm)↓ | Off1 (cm)↓ | Off2 (cm)↓ | Off3 (cm)↓ | Off4 (cm)↓ | 平均值 (cm)↓ |
|-----------------|------------|-----------|-----------|------------|------------|------------|------------|------------|--------------|
| NICE-SLAM [89]  | 1.69       | 2.04      | 1.55      | 0.99       | 0.90       | 1.39       | 3.97       | 3.08       | 1.95         |
| Vox-Fusion [78] | 0.27       | 1.33      | 0.47      | 0.70       | 1.11       | 0.46       | 0.26       | 0.58       | 0.65         |
| ESLAM [34]      | 0.71       | 0.70      | 0.52      | 0.57       | 0.55       | 0.58       | 0.72       | 0.63       | 0.63         |
| Point-SLAM [53] | 0.61       | 0.41      | 0.37      | 0.38       | 0.48       | 0.54       | 0.72       | 0.63       | 0.52         |
| SplaTAM∗ [23]   | 0.31       | 0.40      | 0.29      | 0.47       | 0.27       | 0.29       | 0.32       | 0.55       | 0.36         |
| Gaussian-SLAM   | 0.29       | 0.29      | 0.22      | 0.37       | 0.23       | 0.41       | 0.30       | 0.35       | 0.31         |

数据来源：Replica数据集【12:15†Yugay et al_2024_Gaussian-SLAM2.pdf】

这些数据展示了Gaussian-SLAM在不同数据集上的跟踪性能，表明其在绝对轨迹误差（ATE）上的优越性能。


