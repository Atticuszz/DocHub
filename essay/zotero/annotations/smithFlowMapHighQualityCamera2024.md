---
Title: "FlowMap: High-Quality Camera Poses, Intrinsics, and Depth via Gradient Descent"
Authors: Cameron Smith, David Charatan, Ayush Tewari, Vincent Sitzmann

Date: 2024-04-23
citekey: smithFlowMapHighQualityCamera2024
tags: #Computer-Science---Computer-Vision-and-Pattern-Recognition
---

## FlowMap: High-Quality Camera Poses, Intrinsics, and Depth via Gradient Descent

**Bibliographie :** [1]

C. Smith, D. Charatan, A. Tewari, and V. Sitzmann, ‘FlowMap: High-Quality Camera Poses, Intrinsics, and Depth via Gradient Descent’. arXiv, Apr. 23, 2024. Accessed: Jun. 12, 2024. [Online]. Available: [http://arxiv.org/abs/2404.15259](http://arxiv.org/abs/2404.15259)

**Lien de la publication :** http://arxiv.org/abs/2404.15259

**Lien Zotero :** [Smith et al. - 2024 - FlowMap High-Quality Camera Poses, Intrinsics, an.pdf](zotero://select/library/items/JS3WVP2A)

**Tags :** #Computer-Science---Computer-Vision-and-Pattern-Recognition

> [!abstract]+
> _« This paper introduces FlowMap, an end-to-end differentiable method that solves for precise camera poses, camera intrinsics, and per-frame dense depth of a video sequence. Our method performs per-video gradient-descent minimization of a simple least-squares objective that compares the optical flow induced by depth, intrinsics, and poses against correspondences obtained via off-the-shelf optical flow and point tracking. Alongside the use of point tracks to encourage long-term geometric consistency, we introduce differentiable re-parameterizations of depth, intrinsics, and pose that are amenable to first-order optimization. We empirically show that camera parameters and dense depth recovered by our method enable photo-realistic novel view synthesis on 360-degree trajectories using Gaussian Splatting. Our method not only far outperforms prior gradient-descent based bundle adjustment methods, but surprisingly performs on par with COLMAP, the state-of-the-art SfM method, on the downstream task of 360-degree novel view synthesis (even though our method is purely gradient-descent based, fully differentiable, and presents a complete departure from conventional SfM). »_

> [!Annotation|#2ea8e5]+
> _« 除了使用点轨迹来鼓励长期的几何 一致性外，我们还引入了适合一阶优化的深度、内在和姿态的可微分重新参数化。 »_([2](zotero://open-pdf/library/items/JS3WVP2A?page=2&annotation=PDMTSJXT))

> [!Annotation|#ff6666]+
> _« 相反，我们引入了每个可微分的前馈估计：深 度通过神经网络参数化，姿态参数化为涉及深度和流量的最小二乘问题的解，相机内部 函数使用基于光流一致性的可微选择进行参数化 »_([4](zotero://open-pdf/library/items/JS3WVP2A?page=4&annotation=D9KTB92L))

> [!Annotation|#ff6666]+
> _« 取而代之的是，我们使用 每帧深度估计作为几何表示。 »_([6](zotero://open-pdf/library/items/JS3WVP2A?page=6&annotation=93UYKTQG))

> [!Annotation|#ff6666]+
> _« 我们通过CNN（第4节）获得深度，并为 内部函数和姿态实现可微分的前馈求解器（第4节，图4） »_([10](zotero://open-pdf/library/items/JS3WVP2A?page=10&annotation=CEMGCKBC))

> [!Annotation|#f19837]+
> _« 。最简单的选择是将它们参数化为自由变量，即定 义可学习的每相机内部函数和外函数以及每个像素深度。然而，这种方法在经验上无法收 敛到良好的姿势和几何形状，如第 7 节所示。 »_([12](zotero://open-pdf/library/items/JS3WVP2A?page=12&annotation=FD9TST6D))

> [!Annotation|#ffd400]+
> _« 因此，FlowMap 可以提供高质量的深度 »_([12](zotero://open-pdf/library/items/JS3WVP2A?page=12&annotation=MS7RHUHW))

> [!Annotation|#2ea8e5]+
> _« 在这种情况下，这些帧之间的相对位移可以以闭合形式微分计算 »_([12](zotero://open-pdf/library/items/JS3WVP2A?page=12&annotation=PWSG2AAQ))

> [!Annotation|#ff6666]+
> _« 更正式地说，我们将深度图对齐视为正交 Procrustes 问题，使我们能够利用该问题的可 微分闭式解 [11]。 »_([14](zotero://open-pdf/library/items/JS3WVP2A?page=14&annotation=JIJPF6NK))

> [!Annotation|#ff6666]+
> _« ，使用 Adam [29] 优化器实现了 500 到 5,000 步之间的收敛 »_([16](zotero://open-pdf/library/items/JS3WVP2A?page=16&annotation=86LYXKHI))

> [!Annotation|#ff6666]+
> _« 我们使用 RAFT [64] 和 CoTracker V1 [26] 来计算 FlowMap 用作输入的光流和点 轨迹 »_([16](zotero://open-pdf/library/items/JS3WVP2A?page=16&annotation=QMNJ47U7))

> [!Annotation|#5fb236]+
> _« 在每个优化步骤中，FlowMap 都会重新计算每个帧的深度，然后从这些深度派生姿势 和内部函数以生成渐变 »_([16](zotero://open-pdf/library/items/JS3WVP2A?page=16&annotation=LJGNZGA3))

> [!Annotation|#ff6666]+
> _« 。在计算 ATE 时，我们对所有轨 迹进行归一化，使得 tr（XX） = 1，其中 X 是相机位置的 n×3 矩阵。 »_([24](zotero://open-pdf/library/items/JS3WVP2A?page=24&annotation=6QXB4CH2))

> [!Annotation|#ff6666]+
> _« 我们发现 FlowMap 的平均 ATE （0.0056） 低 于 DROID-SLAM 的 （0.0082），并且与通过重新运行 COLMAP 并将结果与提供的姿 势进行比较获得的平均 ATE （0.0038） 相似。 »_([24](zotero://open-pdf/library/items/JS3WVP2A?page=24&annotation=SMJ4RKXG))
