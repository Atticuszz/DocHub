---
Title: "CG-SLAM: Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field"
Authors: Jiarui Hu, Xianhao Chen, Boyin Feng, Guanglin Li, Liangjing Yang, Hujun Bao, Guofeng Zhang, Zhaopeng Cui

Date: 2024-03-24
citekey: huCGSLAMEfficientDense2024
tags: #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics
---

## CG-SLAM: Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field

**Bibliographie :** [1]

J. Hu _et al._, ‘CG-SLAM: Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field’, Mar. 24, 2024, _arXiv_: arXiv:2403.16095. Accessed: Jul. 16, 2024. [Online]. Available: [http://arxiv.org/abs/2403.16095](http://arxiv.org/abs/2403.16095)

**Lien de la publication :** http://arxiv.org/abs/2403.16095

**Lien Zotero :** [Hu et al_2024_CG-SLAM.pdf](zotero://select/library/items/4SWEXA56)

**Tags :** #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics

> [!abstract]+
> _« Recently neural radiance fields (NeRF) have been widely exploited as 3D representations for dense simultaneous localization and mapping (SLAM). Despite their notable successes in surface modeling and novel view synthesis, existing NeRF-based methods are hindered by their computationally intensive and time-consuming volume rendering pipeline. This paper presents an efficient dense RGB-D SLAM system, i.e., CG-SLAM, based on a novel uncertainty-aware 3D Gaussian field with high consistency and geometric stability. Through an in-depth analysis of Gaussian Splatting, we propose several techniques to construct a consistent and stable 3D Gaussian field suitable for tracking and mapping. Additionally, a novel depth uncertainty model is proposed to ensure the selection of valuable Gaussian primitives during optimization, thereby improving tracking efficiency and accuracy. Experiments on various datasets demonstrate that CG-SLAM achieves superior tracking and mapping performance with a notable tracking speed of up to 15 Hz. We will make our source code publicly available. Project page: https://zju3dv.github.io/cg-slam. »_

> [!Annotation|#ff6666]+
>_« 3.4 Tracking »_([9](zotero://open-pdf/library/items/4SWEXA56?page=9&annotation=HWPMW9GI))
>
> 在《CG-SLAM: Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field》论文中，定位方式基于一个不确定性感知的三维高斯场（3D Gaussian Field）。下面我将详细解析定位方式的原理和依赖的场景表示，并结合论文中的数学公式进行说明。

### 定位方式的原理

CG-SLAM系统使用3D高斯场来表示场景，其中每个高斯点代表场景中的一个位置。该系统通过不确定性建模和优化技术，实现高效的位姿跟踪和场景重建。

#### 1. 三维高斯场建模

高斯点表示一个位置的概率分布，定义如下：

$$
\Sigma = RSST^T
$$

其中，$$R$$为旋转矩阵，$$S$$为缩放矩阵，表示高斯点的形状和方向。

#### 2. 不确定性建模

在渲染图像和高斯点中添加不确定性属性，以删除地图优化中的异常值，并确保使用信息量高的高斯点进行跟踪。渲染图像的深度不确定性定义为：

$$
U = \sum_{i=1}^N \alpha_i T_i (d_i - D)^2
$$

几何方差损失：

$$
L_{var} = \frac{1}{HW} \sum_{n=1}^{HW} |U_n|
$$

高斯点的不确定性由其主导像素的深度偏差确定：

$$
\nu_i = \frac{1}{M_1 + \cdots + M_k} \sum_{f_k \in F} \sum_{p=1}^{M_k} \alpha_{k,p}^i T_{k,p}^i (D_p^k - d_i^k)^2
$$

#### 3. 位姿优化

位姿优化分为顺序跟踪和滑动窗口优化。相机位姿的优化目标函数如下：

$$
\{so(3)|T\} = \arg \min_{\{so(3)|T\}} (L_{tracking})
$$

其中，跟踪损失由颜色损失和几何损失组成：

$$
L_{tracking} = \lambda_1 L_{color} + \lambda_2 L_{geo}
$$

具体来说，颜色损失和几何损失的定义为：

$$
L_{color} = \frac{1}{HW} \sum_{n=1}^{HW} |I_n - \hat{I}_n|
$$

$$
L_{geo} = \frac{1}{HW} \sum_{n=1}^{HW} |D_n - \hat{D}_n|
$$

### 场景表示

CG-SLAM的场景表示依赖于RGB-D序列中的3D高斯点，每个高斯点包含位置、形状、旋转和不确定性等属性。系统通过不确定性建模和几何约束，确保高斯点在场景中的一致性和稳定性。具体而言，系统通过高斯点的不确定性来过滤不稳定的高斯点，从而提高跟踪的效率和准确性。

#### 不确定性建模

渲染图像的不确定性基于深度的不确定性计算：

$$
U = \sum_{i=1}^N \alpha_i T_i (d_i - D)^2
$$

高斯点的不确定性计算公式为：

$$
\nu_i = \frac{1}{M_1 + \cdots + M_k} \sum_{f_k \in F} \sum_{p=1}^{M_k} \alpha_{k,p}^i T_{k,p}^i (D_p^k - d_i^k)^2
$$

通过这些公式，CG-SLAM系统能够有效地表示和处理场景中的不确定性，从而实现高效的位姿跟踪和场景重建。

### 总结

CG-SLAM通过不确定性感知的三维高斯场，结合不确定性建模和几何约束，实现了高效的定位和映射。其关键在于利用高斯点表示场景中的位置，通过不确定性过滤和几何约束，确保高斯点的稳定性和一致性。

参考的主要公式均来自于论文中的公式，以上分析综合了论文中的数学描述和一些扩展说明，以便更好地理解CG-SLAM的定位方式和场景表示。您可以参考原文档中的详细内容以获取更深入的理解：[Hu et al_2024_CG-SLAM3.pdf](file:///mnt/data/Hu%20et%20al_2024_CG-SLAM3.pdf)

> [!Annotation|#ff6666]+
>_« Experiments »_([9](zotero://open-pdf/library/items/4SWEXA56?page=9&annotation=QUYIZY6E))
>
> ### 定位部分的评估标准

在CG-SLAM的研究中，定位部分的评估标准主要是通过绝对轨迹误差（ATE RMSE）来衡量的。以下是具体的公式和实验数据展示。

#### 绝对轨迹误差（ATE RMSE）

绝对轨迹误差用于评估系统在定位上的准确性，定义如下：

$$
RMSE_{ATE} = \sqrt{\frac{1}{N} \sum_{i=1}^N \| p_i^{\text{est}} - p_i^{\text{gt}} \|^2}
$$

其中，$$p_i^{\text{est}}$$表示估计的位姿，$$p_i^{\text{gt}}$$表示真实的位姿，$$N$$是位姿的数量。

### 实验数据展示

#### Replica数据集

| Method       | rm-0 | rm-1 | rm-2 | off-0 | off-1 | off-2 | off-3 | off-4 | Avg  |
|--------------|------|------|------|-------|-------|-------|-------|-------|------|
| NICE-SLAM    | 0.97 | 1.31 | 1.07 | 0.88  | 1.00  | 1.06  | 1.10  | 1.13  | 1.06 |
| Co-SLAM      | 0.77 | 1.04 | 1.09 | 0.58  | 0.53  | 2.05  | 1.49  | 0.84  | 0.99 |
| Point-SLAM   | 0.56 | 0.47 | 0.30 | 0.35  | 0.62  | 0.55  | 0.72  | 0.73  | 0.54 |
| Vox-Fusion   | 0.40 | 0.54 | 0.54 | 0.50  | 0.46  | 0.75  | 0.50  | 0.60  | 0.54 |
| GS-SLAM      | 0.48 | 0.53 | 0.33 | 0.52  | 0.41  | 0.59  | 0.46  | 0.70  | 0.50 |
| SplaTAM      | 0.31 | 0.40 | 0.29 | 0.47  | 0.27  | 0.29  | 0.32  | 0.55  | 0.36 |
| **Ours**     | 0.29 | 0.27 | 0.25 | 0.33  | 0.14  | 0.28  | 0.31  | 0.29  | 0.27 |
| Ours-light   | 0.44 | 0.40 | 0.34 | 0.31  | 0.30  | 0.43  | 0.48  | 0.63  | 0.42 |

*表1：Replica数据集的定位结果 (ATE RMSE [cm] ↓)*

#### TUM-RGBD数据集

| Method       | fr1/desk | fr1/desk2 | fr1/room | fr2/xyz | fr3/office | Avg  |
|--------------|----------|-----------|----------|---------|------------|------|
| NICE-SLAM    | 4.26     | 4.99      | 34.49    | 31.73   | 3.87       | 15.87|
| Co-SLAM      | 2.7      | 4.57      | 30.16    | 1.9     | 2.6        | 8.38 |
| Point-SLAM   | 4.34     | 4.54      | 30.92    | 1.31    | 3.48       | 8.92 |
| Vox-Fusion   | 3.52     | 6.00      | 19.53    | 1.49    | 26.01      | 11.31|
| GS-SLAM      | 3.3      | -         | -        | 1.3     | 6.6        | -    |
| SplaTAM      | 3.35     | 6.54      | 11.13    | 1.24    | 5.16       | 5.48 |
| **Ours**     | 2.43     | 4.54      | 9.39     | 1.20    | 2.45       | 4.0  |
| Ours-light   | 3.14     | 4.73      | 10.67    | 1.28    | 2.60       | 4.48 |

*表2：TUM-RGBD数据集的定位结果 (ATE RMSE [cm] ↓)*

#### ScanNet数据集

| Method       | Sc.0000 | Sc.0059 | Sc.0106 | Sc.0169 | Sc.0181 | Sc.0207 | Avg  |
|--------------|---------|---------|---------|---------|---------|---------|------|
| NICE-SLAM    | 12.00   | 14.00   | 7.90    | 10.90   | 13.40   | 6.20    | 10.70|
| Co-SLAM      | 7.18    | 12.29   | 10.9    | 6.62    | 13.43   | 7.13    | 9.37 |
| Point-SLAM   | 10.24   | 8.29    | 11.86   | 22.16   | 14.77   | 9.54    | 12.19|
| Vox-Fusion   | 8.39    | 8.95    | -       | 9.50    | 12.20   | 6.43    | -    |
| SplaTAM      | 12.83   | 10.10   | 17.72   | 12.08   | 11.10   | 7.46    | 11.88|
| **Ours**     | 7.09    | 7.46    | 8.88    | 8.16    | 11.60   | 5.34    | 8.08 |
| Ours-light   | 6.90    | 8.36    | 8.72    | 8.21    | 12.72   | 5.70    | 8.44 |

*表3：ScanNet数据集的定位结果 (ATE RMSE [cm] ↓)*


