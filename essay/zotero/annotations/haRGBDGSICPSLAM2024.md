---
Title: "RGBD GS-ICP SLAM"
Authors: Seongbo Ha, Jiung Yeon, Hyeonwoo Yu

Date: 2024-03-22
citekey: haRGBDGSICPSLAM2024
tags: #Computer-Science---Computer-Vision-and-Pattern-Recognition
---

## RGBD GS-ICP SLAM

**Bibliographie :** [1]

S. Ha, J. Yeon, and H. Yu, ‘RGBD GS-ICP SLAM’, Mar. 22, 2024, _arXiv_: arXiv:2403.12550. Accessed: May 23, 2024. [Online]. Available: [http://arxiv.org/abs/2403.12550](http://arxiv.org/abs/2403.12550)

**Lien de la publication :** http://arxiv.org/abs/2403.12550

**Lien Zotero :** [Ha et al. - 2024 - RGBD GS-ICP SLAM.pdf](zotero://select/library/items/HJ4D53M9)

**Tags :** #Computer-Science---Computer-Vision-and-Pattern-Recognition

> [!abstract]+
> _« Simultaneous Localization and Mapping (SLAM) with dense representation plays a key role in robotics, Virtual Reality (VR), and Augmented Reality (AR) applications. Recent advancements in dense representation SLAM have highlighted the potential of leveraging neural scene representation and 3D Gaussian representation for high-fidelity spatial representation. In this paper, we propose a novel dense representation SLAM approach with a fusion of Generalized Iterative Closest Point (G-ICP) and 3D Gaussian Splatting (3DGS). In contrast to existing methods, we utilize a single Gaussian map for both tracking and mapping, resulting in mutual benefits. Through the exchange of covariances between tracking and mapping processes with scale alignment techniques, we minimize redundant computations and achieve an efficient system. Additionally, we enhance tracking accuracy and mapping quality through our keyframe selection methods. Experimental results demonstrate the effectiveness of our approach, showing an incredibly fast speed up to 107 FPS (for the entire system) and superior quality of the reconstructed map. »_

> [!Annotation|#ff6666]+
> _« Method »_([7](zotero://open-pdf/library/items/HJ4D53M9?page=7&annotation=6S7HGIB6))

> 1. **广义迭代最近点（G-ICP）算法**
>       - **定义**: G-ICP是一种3D点云配准算法,通过最小化两个点云之间的误差来进行配准。
>       - **过程**: G-ICP计算当前帧和地图的高斯分布,找到最佳的变换矩阵,使源高斯(当前帧)与目标高斯(地图)最大程度对齐。
>       - **公式**:
>         - 设有点集 $X = \{x_m\}_{m=1,\dots,M}$ 及其协方差集 $C = \{C_m\}_{m=1,\dots,M}$,其中 $x = [x, y, z]^T$。一个3D点 $x$ 的协方差 $C$ 通过其 $k$ 近邻计算得到。
>         - 定义高斯集合 $G = \{X, C\}$。G-ICP 的目标是找到最佳变换矩阵 $T$,使得源高斯 $G_s = \{X_s, C_s\}$ 和目标高斯 $G_t = \{X_t, C_t\}$ 对齐。
>         - 假设我们知道 $X_s$ 和 $X_t$ 之间的对应关系,通过最近邻搜索得到:
>           $$T^* = \arg\min_T \sum_i d_i^T \left( C_t^i + T C_s^i T^T \right)^{-1} d_i$$
>           其中,误差项 $d_i = x_t^i - T x_s^i$,最佳变换 $T^*$ 可以作为当前帧与地图之间的相对姿态。

2. **尺度正则化**
      - **定义**: 在使用G-ICP进行跟踪时,通过对当前帧和地图的尺度对齐来提高相机姿态估计的性能。
      - **过程**: 通过奇异值分解(SVD)计算协方差矩阵的尺度:
        $$C = R \Lambda^2 R^T$$
        其中,$\Lambda = \text{diag}(s_2, s_1, s_0)$ 是尺度矩阵,$R$ 是高斯的方向。为了在扫描匹配中达到鲁棒性性能,将尺度正则化为:
        $$\Lambda' = \frac{1}{\text{median}(S)} \text{diag}(s_2, s_1, s_0)$$
        其中,$\Lambda'$ 是椭圆正则化后的尺度矩阵。

3. **关键帧选择**
      - **定义**: 根据G-ICP计算的几何对应关系,动态选择关键帧。
      - **过程**: 如果当前帧与地图之间的对应比例低于特定阈值,则选择该帧为关键帧。选择的关键帧只包含与当前地图不重叠的高斯,以减少跟踪误差累积。

总的来说,G-ICP是一种基于高斯分布的3D点云配准算法,通过尺度正则化和关键帧选择来提高其性能和鲁棒性。

> [!Annotation|#2ea8e5]+
> _« Note that in G-ICP and GS, the key common factor is Gaussians G = {X , C}, allowing these Gaussians to be shared mutually »_([9](zotero://open-pdf/library/items/HJ4D53M9?page=9&annotation=ERIIHV3A))
>
> <b>协方差共享与尺度对齐</b>：在G-ICP跟踪过程中，计算每一帧的协方差并将其用于3DGS地图扩展中。这种方法避免了每次扩展地图时重新计算协方差，从而减少了冗余计算。G-ICP和3DGS通过共享相同的高斯世界，利用协方差来优化跟踪和映射性能

> [!Annotation|#ff6666]+
> _« where Λ′ is the ellipse-regularized scale matrix. »_([11](zotero://open-pdf/library/items/HJ4D53M9?page=11&annotation=4A9C5PGM))
>
> <b>椭圆正则化</b>：在G-ICP跟踪过程中，使用奇异值分解（SVD）对协方差矩阵进行分解并正则化，使得每个高斯的尺度在保持其原始特征的基础上得到正则化。这种方法通过保持目标高斯的原始特性，同时进行尺度对齐，增强了G-ICP的扫描匹配性能

> [!Annotation|#f19837]+
> _« Scale Aligning »_([13](zotero://open-pdf/library/items/HJ4D53M9?page=13&annotation=KYNAFJLJ))
>
> <b>尺度归一化</b>：为了减少单帧添加到3DGS地图时的尺度不一致问题，文章提出了通过距离归一化的方式对当前帧的尺度进行归一化。具体方法是通过计算奇异值分解得到的尺度矩阵，并根据距离参数进行归一化处理，以确保新添加的关键帧高斯与现有地图中的高斯在尺度上保持一致，从而提高映射性能和跟踪精度

> [!Annotation|#ff6666]+
> _« Table 1: Tracking Performance on Replica (ATE RMSE ↓ [cm]) »_([19](zotero://open-pdf/library/items/HJ4D53M9?page=19&annotation=DW2MKNCY))
>
> #### 实验数据展示

**Replica 数据集上的实验结果**：

| Method                                     | RMSE (cm) ↓ | PSNR ↑  | SSIM ↑  | LPIPS ↓ | FPS ↑ |
| ------------------------------------------ | ----------- | ------- | ------- | ------- | ----- |
| NICE-SLAM [47]                             | 1.42        | -       | -       | -       | -     |
| Point-SLAM [32]                            | 0.54        | -       | -       | -       | -     |
| GS-SLAM [44]                               | 0.50        | -       | -       | -       | -     |
| Photo-SLAM [12]                            | 0.60        | -       | -       | -       | -     |
| SplaTAM [14]                               | 0.36        | -       | -       | -       | -     |
| Ours (limited to 30 FPS)                   | 0.16        | 38.83   | 0.975   | 0.041   | 29.98 |
| RGBD GS-ICP SLAM (no tracking speed limit) | 0.16        | 35.93   | 0.962   | 0.066   | 98.11 |

**TUM-RGBD 数据集上的实验结果**：

| Method                                     | RMSE (cm) ↓ | PSNR ↑  | SSIM ↑  | LPIPS ↓ | FPS ↑ |
| ------------------------------------------ | ----------- | ------- | ------- | ------- | ----- |
| NICE-SLAM [47]                             | 4.0         | -       | -       | -       | -     |
| Point-SLAM [32]                            | 2.6         | -       | -       | -       | -     |
| GS-SLAM [44]                               | 3.7         | -       | -       | -       | -     |
| SplaTAM [14]                               | 3.2         | -       | -       | -       | -     |
| Ours (limited to 30 FPS)                   | 2.4         | 20.72   | 0.768   | 0.218   | 29.99 |
| RGBD GS-ICP SLAM (no tracking speed limit) | 2.37        | 19.62   | 0.750   | 0.240   | 73.92 |

这些结果展示了RGBD GS-ICP SLAM在定位精度和重建地图质量方面的优越性能，同时保持了极快的系统速度【15†source】。
