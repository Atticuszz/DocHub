---
Title: "Gaussian splatting slam"
Authors: Hidenobu Matsuki, Riku Murai, Paul HJ Kelly, Andrew J. Davison

Date: 2024-01-01
citekey: matsukiGaussianSplattingSlam2024
tags: #⛔-No-DOI-found
---

## Gaussian splatting slam

**Bibliographie :** [1]

H. Matsuki, R. Murai, P. H. Kelly, and A. J. Davison, ‘Gaussian splatting slam’, in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_, 2024, pp. 18039–18048. Accessed: Jul. 17, 2024. [Online]. Available: [https://openaccess.thecvf.com/content/CVPR2024/html/Matsuki_Gaussian_Splatting_SLAM_CVPR_2024_paper.html](https://openaccess.thecvf.com/content/CVPR2024/html/Matsuki_Gaussian_Splatting_SLAM_CVPR_2024_paper.html)

**Lien de la publication :** https://openaccess.thecvf.com/content/CVPR2024/html/Matsuki_Gaussian_Splatting_SLAM_CVPR_2024_paper.html

**Lien Zotero :** [Matsuki et al_2024_Gaussian splatting slam.pdf](zotero://select/library/items/SZF72XQZ)

**Tags :** #⛔-No-DOI-found

> [!abstract]+
> _« »_

> [!Annotation|#ff6666]+
> _« 3. Method »_([5](zotero://open-pdf/library/items/SZF72XQZ?page=5&annotation=L7N8FVCH))
>
> ## 定位方式及其原理分析

### 定位方式简介

定位方式在计算机视觉中通常涉及估计摄像机的位置和方向。本文主要探讨一种基于3D高斯溅射（3D Gaussian Splatting, 3DGS）的定位方式，它结合了相机跟踪、几何验证和正则化以实现高精度的定位。

### 定位方式的原理

3DGS使用各向异性高斯分布来表示3D空间中的点，通过优化这些高斯的光学和几何参数实现高保真度的场景重建。为了实现准确的相机定位和跟踪，本文引入了基于李群的雅可比矩阵推导方法。

#### 高斯分布的定义

每个高斯分布\( G_i \)包含颜色\( c_i \)和不透明度\( \alpha_i \)，其位置和形状由均值\( \mu_i^W \)和协方差矩阵\( \Sigma_i^W \)表示。

#### 像素颜色的合成公式

通过溅射和混合\( N \)个高斯分布，可以合成像素颜色\( C_p \):

$$
C_p = \sum_{i \in N} c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)
$$

#### 2D高斯与3D高斯的转换

3D高斯\( N(\mu_W, \Sigma_W) \)在图像平面上的2D高斯\( N(\mu_I, \Sigma_I) \)通过投影变换关系如下：

$$
\mu_I = \pi(T_{CW} \cdot \mu_W), \quad \Sigma_I = J_W \Sigma_W J_W^T
$$

其中，\( \pi \)表示投影操作，\( T\_{CW} \in SE(3) \)是视点的相机姿态，\( J \)是投影变换的雅可比矩阵。

#### 相机姿态优化

为了优化相机姿态，我们使用李代数推导最小雅可比矩阵，保证雅可比矩阵的维度与自由度匹配，避免冗余计算。推导公式如下：

$$
\frac{\partial \mu_I}{\partial T_{CW}} = \frac{\partial \mu_I}{\partial \mu_C} \frac{D\mu_C}{DT_{CW}}
$$

$$
\frac{\partial \Sigma_I}{\partial T_{CW}} = \frac{\partial \Sigma_I}{\partial J} \frac{\partial J}{\partial \mu_C} \frac{D\mu_C}{DT_{CW}} + \frac{\partial \Sigma_I}{\partial W} \frac{DW}{DT_{CW}}
$$

#### 使用李代数推导雅可比矩阵

李代数中的微分公式如下：

$$
Df(T) = \lim_{\tau \to 0} \frac{\log(f(\exp(\tau) \cdot T) \cdot f(T)^{-1})}{\tau}
$$

其中，\( \exp \)和\( \log \)是李代数与李群之间的映射。由此，我们得到：

$$
\frac{D\mu_C}{DT_{CW}} = I - \mu_C^\times
$$

$$
\frac{DW}{DT_{CW}} = \begin{bmatrix} 0 & -W^\times_{:,1} \\ 0 & -W^\times_{:,2} \\ 0 & -W^\times_{:,3} \end{bmatrix}
$$

### 场景表示的优势

3DGS作为一种新的SLAM表示方法，相比传统的点云、网格或体素网格具有更高的效率和精度。其平滑、连续可微的几何表示使得高斯云可以联合定义一个连续的体积函数，从而实现高保真度的场景重建。

### 定位方式的数学公式

为了实现准确的相机跟踪，系统通过优化以下光度残差公式：

$$
E_{pho} = I(G, T_{CW}) - \bar{I}
$$

其中，\( I(G, T*{CW}) \)表示从相机姿态\( T*{CW} \)渲染的高斯图像，\( \bar{I} \)为观察到的图像。

在深度观测可用的情况下，几何残差公式为：

$$
E_{geo} = D(G, T_{CW}) - \bar{D}
$$

其中，\( D(G, T\_{CW}) \)为深度光栅化图像，\( \bar{D} \)为观察到的深度。

优化目标函数结合了光度残差和几何残差：

$$
\lambda_{pho} E_{pho} + (1 - \lambda_{pho}) E_{geo}
$$

通过这种方法，可以实现高效、精确的相机定位和3D场景重建。

> [!Annotation|#ff6666]+
> _« 4.2. Quantitative Evaluation »_([11](zotero://open-pdf/library/items/SZF72XQZ?page=11&annotation=AI2RGCRK))
>
> ### 定位方式的评估标准

#### 评估指标

在定位部分，主要使用以下几个指标来评估相机跟踪的准确性：

1. **绝对轨迹误差 (Absolute Trajectory Error, ATE)**:
      用于衡量相机轨迹的全局一致性。ATE的均方根误差（RMSE）计算公式如下：
      $$
   \text{RMSE}_{\text{ATE}} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} \left\| \mathbf{T}_i^{\text{estimated}} - \mathbf{T}_i^{\text{ground truth}} \right\|^2}
   $$

2. **光度残差 (Photometric Residual, \( E\_{pho} \))**:
      $$
   E_{pho} = \| I(G, T_{CW}) - \bar{I} \|_1
   $$
      其中，\( I(G, T\_{CW}) \) 是从高斯图像 \( G \) 渲染得到的图像， \( \bar{I} \) 是观测到的图像。

3. **几何残差 (Geometric Residual, \( E\_{geo} \))**:
      $$
   E_{geo} = \| D(G, T_{CW}) - \bar{D} \|_1
   $$
      其中，\( D(G, T\_{CW}) \) 是深度光栅化图像， \( \bar{D} \) 是观测到的深度图像。

### 实验数据展示

以下是 TUM RGB-D 数据集和 Replica 数据集上的实验数据表格，用于评估相机跟踪的准确性。

#### TUM RGB-D 数据集

表1显示了在TUM RGB-D数据集上的相机跟踪结果，ATE RMSE以厘米为单位报告。

| 方法               | fr1/desk  | fr2/xyz  | fr3/office | 平均值  |
| ------------------ | --------- | -------- | ---------- | ------- |
| DSO [4]            | 22.4      | 1.10     | 9.50       | 11.0    |
| DROID-VO [36]      | 5.20      | 10.7     | 7.30       | 7.73    |
| DepthCov-VO [3]    | 5.60      | 1.20     | 68.8       | 25.2    |
| **我们的**         | 3.78      | 4.60     | 3.50       | 3.96    |
| DROID-SLAM [36]    | 1.80      | 0.50     | 2.80       | 1.70    |
| ORB-SLAM2 [20]     | 1.90      | 0.60     | 2.40       | 1.60    |
| iMAP [33]          | 4.90      | 2.00     | 5.80       | 4.23    |
| NICE-SLAM [46]     | 4.26      | 6.19     | 3.87       | 4.77    |
| DI-Fusion [7]      | 4.40      | 2.00     | 5.80       | 4.07    |
| Vox-Fusion [43]    | 3.52      | 1.49     | 26.01      | 10.34   |
| ESLAM [8]          | 2.47      | 1.11     | 2.42       | 2.00    |
| Co-SLAM [39]       | 2.40      | 1.70     | 2.40       | 2.17    |
| Point-SLAM [27]    | 4.34      | 1.31     | 3.48       | 3.04    |
| **我们的 (RGB-D)** | 1.50      | 1.44     | 1.49       | 1.47    |
| BAD-SLAM [29]      | 1.70      | 1.10     | 1.70       | 1.50    |
| Kintinous [40]     | 3.70      | 2.90     | 3.00       | 3.20    |
| ORB-SLAM2 [20]     | 1.60      | 0.40     | 1.00       | 1.00    |

_数据集：TUM RGB-D_

#### Replica 数据集

表2显示了在Replica数据集上的RGB-D SLAM相机跟踪结果，ATE RMSE以厘米为单位报告。

| 方法            | r0   | r1   | r2   | o0   | o1   | o2   | o3   | o4   | 平均值  |
| --------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ------- |
| iMAP [33]       | 3.12 | 2.54 | 2.31 | 1.69 | 1.03 | 3.99 | 4.05 | 1.93 | 2.58    |
| NICE-SLAM       | 0.97 | 1.31 | 1.07 | 0.88 | 1.00 | 1.06 | 1.10 | 1.13 | 1.07    |
| Vox-Fusion [43] | 1.37 | 4.70 | 1.47 | 8.48 | 2.04 | 2.58 | 1.11 | 2.94 | 3.09    |
| ESLAM [8]       | 0.71 | 0.70 | 0.52 | 0.57 | 0.55 | 0.58 | 0.72 | 0.63 | 0.63    |
| Point-SLAM [27] | 0.61 | 0.41 | 0.37 | 0.38 | 0.48 | 0.54 | 0.69 | 0.72 | 0.53    |
| **我们的**      | 0.44 | 0.32 | 0.31 | 0.44 | 0.52 | 0.23 | 0.17 | 2.25 | 0.58    |
| **我们的 (sp)** | 0.33 | 0.22 | 0.29 | 0.36 | 0.19 | 0.25 | 0.12 | 0.81 | 0.32    |

_数据集：Replica_

这些实验结果表明，在不同的数据集上，我们的方法在相机跟踪准确性方面表现优越，尤其在单目和RGB-D场景下，均达到了最先进的性能。
