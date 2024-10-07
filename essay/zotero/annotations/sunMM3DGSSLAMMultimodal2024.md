---
Title: "MM3DGS SLAM: Multi-modal 3D Gaussian Splatting for SLAM Using Vision, Depth, and Inertial Measurements"
Authors: Lisong C. Sun, Neel P. Bhatt, Jonathan C. Liu, Zhiwen Fan, Zhangyang Wang, Todd E. Humphreys, Ufuk Topcu

Date: 2024-04-01
citekey: sunMM3DGSSLAMMultimodal2024
tags: #Computer-Science---Artificial-Intelligence, #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics
---

## MM3DGS SLAM: Multi-modal 3D Gaussian Splatting for SLAM Using Vision, Depth, and Inertial Measurements

**Bibliographie :** [1]

L. C. Sun _et al._, ‘MM3DGS SLAM: Multi-modal 3D Gaussian Splatting for SLAM Using Vision, Depth, and Inertial Measurements’, Apr. 01, 2024, _arXiv_: arXiv:2404.00923. Accessed: Jul. 16, 2024. [Online]. Available: [http://arxiv.org/abs/2404.00923](http://arxiv.org/abs/2404.00923)

**Lien de la publication :** http://arxiv.org/abs/2404.00923

**Lien Zotero :** [Sun et al_2024_MM3DGS SLAM.pdf](zotero://select/library/items/SZXUNBF8)

**Tags :** #Computer-Science---Artificial-Intelligence, #Computer-Science---Computer-Vision-and-Pattern-Recognition, #Computer-Science---Robotics

> [!abstract]+
> _« Simultaneous localization and mapping is essential for position tracking and scene understanding. 3D Gaussian-based map representations enable photorealistic reconstruction and real-time rendering of scenes using multiple posed cameras. We show for the first time that using 3D Gaussians for map representation with unposed camera images and inertial measurements can enable accurate SLAM. Our method, MM3DGS, addresses the limitations of prior neural radiance field-based representations by enabling faster rendering, scale awareness, and improved trajectory tracking. Our framework enables keyframe-based mapping and tracking utilizing loss functions that incorporate relative pose transformations from pre-integrated inertial measurements, depth estimates, and measures of photometric rendering quality. We also release a multi-modal dataset, UT-MM, collected from a mobile robot equipped with a camera and an inertial measurement unit. Experimental evaluation on several scenes from the dataset shows that MM3DGS achieves 3x improvement in tracking and 5% improvement in photometric rendering quality compared to the current 3DGS SLAM state-of-the-art, while allowing real-time rendering of a high-resolution dense 3D map. Project Webpage: https://vita-group.github.io/MM3DGS-SLAM »_

> [!Annotation|#ff6666]+
> _« B. Tracking »_([5](zotero://open-pdf/library/items/SZXUNBF8?page=5&annotation=UITVQ3YF))
>
> ### 定位方式分析阐述

#### 方法概述

MM3DGS SLAM框架使用视觉、深度和惯性测量数据来实现同步定位和建图（SLAM）。其核心定位部分包括四个主要步骤：姿态优化（跟踪）、关键帧选择、高斯初始化和映射。

#### 1. 姿态优化（Tracking）

姿态优化利用视觉和深度信息来优化相机的姿态。通过以下损失函数进行优化：

$$
L_{\text{tracking}} = \mathbb{1}_{O(G,T_C)} \left( L_{\text{photo}} + \lambda_D L_{\text{depth}} \right)
$$

其中，

- $\mathbb{1}_{O(G,T_C)}$ 是指示函数，定义为：

$$
\mathbb{1}_{O(G,T_C)} =
\begin{cases}
1 & \text{if } O(G, T_C) > 0.99 \\
0 & \text{otherwise}
\end{cases}
$$

- \( L\_{\text{photo}} \) 为光度损失：

$$
L_{\text{photo}} = L_1 (I, C(G, T_C))
$$

- \( L\_{\text{depth}} \) 为深度损失，计算方式为深度图 \( D_e \) 和渲染深度图 \( D_r \) 的线性相关（Pearson相关系数）：

$$
L_{\text{depth}} = \frac{\text{Cov}(D_e, D_r)}{\sqrt{\text{Var}(D_e) \text{Var}(D_r)}}
$$

#### 2. 关键帧选择（Keyframe Selection）

关键帧的选择基于协同可见性和图像质量指标（NIQE）。当协同可见性低于95%时，选择新的关键帧。此外，使用NIQE指标选择滑动窗口中的最高质量帧。

#### 3. 高斯初始化（Gaussian Initialization）

在每个关键帧的每个像素处添加新的高斯分布，如果满足以下条件：

- 不透明度 < 0.5
- 深度误差 > 50 倍中值深度误差

#### 4. 映射（Mapping）

映射阶段优化当前帧和每个选定关键帧中可见的3D高斯分布。优化的损失函数为：

$$
L_{\text{mapping}} = \lambda_C L_{\text{photo}} + \lambda_S L_{\text{SSIM}} + \lambda_D L_{\text{depth}}
$$

其中，\( L\_{\text{SSIM}} \) 是结构相似性损失。
