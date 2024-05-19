### paper

[nerf_nav](../../docs/papers/nerf_nav.pdf)
2024-03-17
这篇论文主要是在nerf中，给定空间轨迹的情况，使用自己的一种姿态检测算法，并且研究一种在实际空间运动轨迹优化方法来符合无人机动力学特性

[SplaTAM](../../docs/papers/SplaTAM.pdf)
2024-03-28
$$f(\mathbf{x})=o\exp\left(-\frac{\|\mathbf{x}-\mathbf{\mu}\|^2}{2r^2}\right).$$
$$C(\mathbf{p})=\sum_{i=1}^n\mathbf{c}_if_i(\mathbf{p})\prod_{j=1}^{i-1}(1-f_j(\mathbf{p}))$$
$$D(\mathbf{p})=\sum_{i=1}^{n}d_{i}f_{i}(\mathbf{p})\prod_{j=1}^{i-1}(1-f_{j}(\mathbf{p}))$$
$$S(\mathbf{p})=\sum_{i=1}^{n}f_i(\mathbf{p})\prod_{j=1}^{i-1}(1-f_j(\mathbf{p})).$$
$$L_{\mathrm{t}}=\sum\limits_{\mathbf{p}}\left(S(\mathbf{p})>0.99\right)\left(\mathrm{L}_{\mathrm{l}}\left(D(\mathbf{p})\right)+0.5\mathrm{L}_{\mathrm{l}}\left(C(\mathbf{p})\right)\right)$$

## idea

Gsplat 场景表示法下的，
在使用[Replica-Dataset](https://github.com/SupaVision/Replica-Dataset)或者`matterport3d`数据集的仿真环境下[habitat-sim](https://github.com/facebookresearch/habitat-sim)或者 [Blender](https://docs.blender.org/api/current/info_quickstart.html)，根据
[SplaTAM](../../docs/papers/SplaTAM.pdf)的方法进行高精度空间定位，在给定空间轨迹路线下，出现新的障碍物，使用动态空间`A*`局部修正路轨迹，并且同时根据建图结果比对原始地图进行修正

## Innovation

2024-03-15
2024-03-17
重点应该关注实时的性能和资源问题，~~空间搜索的性能~~，定位和建图的性能

1. 比如建图应该是最开始就基本完成，采用一种 **缓冲**的做法，因为大部分时候不需要实现全额功率的建图，**创造一种高斯建图中相似性的判断方法，就比如大部分时候仅仅是相似性比对，达到阈值才唤醒全额功率的建图**，这个应该是对 **建图和修图的性能的优化**，也就是**选择什么时机进行**修正地图
   2024-03-16
   ~~应该是想办法让导航预先计算好所有的路线，然后进行贴合路线，实时定位建图的轨迹来贴合这个预先计算的轨迹，**避免加载预先全部的地图进行实时的路径规划**（像人一样，走自己走过的路），如果**出现了地图的修正，障碍物，自动贴合选择其他的规划好的路径**（自己按照经验选择可选的路径），保证了动态修正性和不必要的资源浪费~~
   [GPU Module (gpu) — Blender Python API](https://docs.blender.org/api/current/gpu.html)空间行驶仿真的库

轨迹定位使用[SplaTAM](../../docs/papers/SplaTAM.pdf)

~~图形的存储应该进行压缩，保留地面平面和和空间占用，导航计算应该是压缩过的空间占用地图~~

2024-03-17
不考虑规划的情况，现在修改成给定空间轨迹的，出现障碍物的使用空间`A*`空间局部重规划

## representation

### nerf

#### 模型概述

`nerf` 模型可以理解为三位重建的深度学习模型，给定空间位置`x,y,x`和观察方向`方向向量`,输出该位置的`RPG`和体积密度\(表示空间的透明度)

#### 训练NeRF模型所需信息

1. **彩色图像**：NeRF通过对一系列从不同视角拍摄的彩色图像进行训练，学习场景的3D表示。
2. **相机参数**：传统的NeRF模型训练需要知道每张图像对应的相机参数，包括相机的位置、朝向（姿态）和内参（焦距、光心等）。这些参数用于将3D场景映射到2D图像平面，帮助模型理解不同视角下观察到的场景变化。

### 3DGS

## solution

### 3-d reconstruction

2024-02-16
_场景表示法选什么？_
_怎么重建？_
有深度图像就可以直接生成点云，重点关注19年时候英特尔开源的点云处理库`open3d`这是现有的正常维护中的库，有深度图就可以实现点云的三维重建了
_没有深度图像咋办？或者深度图像质量不高咋办?_
[GitHub - LiheYoung/Depth-Anything: Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data. Foundation Model for Monocular Depth Estimation](https://github.com/LiheYoung/Depth-Anything)
![../../assets/Pasted_image_20240216143622.png](../../assets/Pasted_image_20240216143622.png)
现在已经有了直接从`RPG`转化成深度图像的模型了，根据他的模型参数，性能是非常好的，可以直接接近实时

2024-03-15

- [x] 目前流行的是 _nerf_ 和 _3DGS_,但是nerf的性能不咋地，根据深度图进行点云重建这都算最基本的了，*3DGS*应该是首选的场景表示法

> [In this paper, we set out to explore this option and develop Marigold, a la- tent diffusion model (LDM) based on Stable Diffusion [36 ],](../../docs/papers/RepurposingDiffusion-BasedImageGeneratorsforMonocularDepthEstimation.pdf)

- [x] `Depth-Anything`的深度估计精度应该还不行，但是性能不错,这篇文章对输入输出和基于流行的扩散模型进行微调，RGP生成深度图，精度貌似看他点云重建的效果还不错

_怎么进行重建得看[SplaTAM](../../docs/papers/SplaTAM.pdf),他的重建的pipeline需要搞清楚，代码也需要重构，写的太随意了_

_当然，首先得明白，3DGS究竟是如何进行场景表示的？_

2024-03-17
打算采用预先生成好的地图重建，遇到障碍进行修正

### loaclization

2024-02-16
_怎么解决定位问题？_
只要实现了点云构造，对连续帧深度图生成的点云图像进行 **对齐**，就可以直接推算出相机的位置参数，`open3d`应该是有成熟的点云对齐函数[open3d.registration.GlobalOptimizationGaussNewton — Open3D 0.6.0 documentation](https://www.open3d.org/docs/0.6.0/python_api/open3d.registration.GlobalOptimizationGaussNewton.html)
![../../assets/Pasted_image_20240216144139.png](../../assets/Pasted_image_20240216144139.png)

直接构建不需要定位，或者说从点云对齐得到的连续帧率得到的相对运动信息可以辅助加速点云对齐

初始全局定位可能会麻烦一点，要全局搜索？或者开始粗略几个初始点，然后根据移动，后续连续帧的一系列信息才开始定位，精确空间定位需要仔细设计

2024-03-15

- [x] 定位方法需要测试选择最优的
      貌似使用点云对齐的性能没有那么理想[splat_nav](../../docs/papers/splat_nav.pdf)，
      这篇论文是用传统的点云对齐算法，比如 *open3d*的那个，来估计机器人姿态
  > re-planning at 5 Hz and pose estimation at 20 Hz
  > [splat_nav, page 1](../../docs/papers/splat_nav.pdf)

使用cpu计算的，路径规划性能不咋地，这种频率不能做到实时的避开障碍
，并且姿态估计的速度也一般

_如果假设地图已经建图完成，那么传统的点云对齐运算的精度和性能和[SplaTAM](../../docs/papers/SplaTAM.pdf)谁更好？_ 当然也可以用3DGS中提到的

> [仅使⽤ SfM 点作为输⼊就获得了⾼质量的结果](../../docs/papers/3DGS.pdf)

计算性能很差的，使用图片估计出空间点云的办法SfM

### Avoidance

2024-03-17
打算使用空间空间`A*`进行
_空间`A_`如何进行实现？\*

2024-03-20

- [x] A*，D* 作为参照方法，优先方法应该是RRT\*，并且可能是双向的

_`rrt_`需要额外设计实验验证他的效率\*

EasyChair-Preprint-2703 (2).pdf

PDF

为什么vgicp不需要像gicp那样的昂贵的最近临近搜索？具体说说和依赖kdtree的gicp之间的区别是什么？

VGICP (Voxelized Generalized Iterative Closest Point) 通过体素化技术提高了处理速度，避免了传统 GICP 中昂贵的最近邻搜索。VGICP 将每个点的分布聚合到体素中，这种方法即使在体素内点数较少时也能有效估算分布，从而在处理速度和注册精度上都有优势。具体来说，VGICP 把多点的分布聚合到单个体素的分布中，通过平行处理优化算法，使得算法能够更快执行，特别是在 GPU 上。

传统的 GICP 算法依赖于对每个点的最近邻搜索来匹配对应点，这个过程计算量大且速度慢，尤其是当点云数据量大时。而 VGICP 通过将点云体素化，每个体素代表了其中所有点的统计分布，减少了单个点匹配的需要，从而大幅提升了算法的执行效率。

关于体素化不需要如 GICP 那样依赖 KD-tree 的原因是，体素化本身通过空间划分简化了点的关联过程，不再需要进行复杂的空间搜索来找到最近的点，而是直接在体素级别上进行匹配和优化，这大大减少了计算量和提高了并行计算的效率。

因此，VGICP 适合于需要快速且准确处理大规模点云数据的应用，如实时 3D LIDAR 应用，它通过利用 GPU 加速提供了极高的处理速度，而且由于它减少了依赖于精确最近邻搜索的需求，使得算法更适合在现代多核 CPU 和 GPU 上并行处理。

**体素间的匹配**：通过比较源点云中的点与目标体素中的均值之间的距离来进行匹配。由于每个体素代表了其内部所有点的统计信息，这种方法可以在保持较高精度的同时减少计算量。

怎么匹配的？这相对kdtree的匹配方法为什么可以方便并行计算

在VGICP中，体素间的匹配方法相比传统基于KD树的方法更适合并行计算的原因主要有以下几点：

### 体素化简化数据结构

- **数据预处理**：在VGICP中，点云数据首先被分组到体素中，并计算每个体素的均值和协方差。这个过程可以并行进行，每个体素可以独立处理其内部的点云数据。
- **简化的数据结构**：每个体素代表了它包含的所有点的统计信息，这样在匹配过程中不需要考虑体素内部的每个点，而只需使用体素的均值和协方差。这减少了数据量，提高了处理速度。

### 匹配过程的并行化

- **减少比较次数**：传统的KD树方法需要对每个查询点进行最近邻搜索，涉及到大量的点到点比较。而在VGICP中，查询点仅与体素的均值进行比较，大大减少了比较的次数。
- **统一的操作**：由于每个体素的结构相同（均值和协方差），这使得匹配过程中的计算可以很容易地在多个处理单元上并行执行。每个处理单元可以独立地处理一部分体素与查询点的比较和匹配。

### 适合GPU并行运算的特性

- **矩阵运算**：体素的均值和协方差涉及到的是矩阵运算，这种类型的运算是GPU擅长的，可以利用GPU的高并行性能进行快速计算。
- **内存访问模式**：体素化数据结构更规整，内存访问模式更可预测，这对于GPU这类有大量并行处理单元的硬件非常重要，能有效提高内存访问效率。

### 优化并行执行

- **批量处理**：在VGICP中可以将多个查询点同时发送到GPU进行处理，每个点的处理过程相互独立，适合进行批量并行处理。

总结来说，VGICP通过利用体素化的数据结构和统计信息，以及矩阵运算的并行性，提高了点云配准的效率和并行计算的可行性。这使得VGICP在处理大规模点云数据时，尤其是在使用GPU等并行计算平台时，能显示出更好的性能。
