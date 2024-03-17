## idea

2024-03-15
最终应该完成在3D高斯splat 场景表示法下的，动态修正地图，可以实现紧急避障碍（修正地图从而自动修正路径）自主空间导航

[SplaTAM](../../docs/papers/SplaTAM.pdf)的方法，基本上已经完成高性能的，空间建图并且可以实时的获取姿态数据
在此基础之上，配合规划算法进行空间导航

## Innovation

2024-03-15
重点应该关注实时的性能和资源问题，空间搜索的性能，定位和建图的性能

1. 比如建图应该是最开始就基本完成，采用一种 **缓冲**的做法，因为大部分时候不需要实现全额功率的建图，**创造一种高斯建图中相似性的判断方法，就比如大部分时候仅仅是相似性比对，达到阈值才唤醒全额功率的建图**，这个应该是对 **建图和修图的性能的优化**，也就是**选择什么时机进行**修正地图
2. 规划空间搜索也应该是类似的想法，如果能**够记住上次规划的结果**，只在**修正地图的时候进行重新规划**
   2024-03-16

应该是想办法让导航预先计算好所有的路线，然后进行贴合路线，实时定位建图的轨迹来贴合这个预先计算的轨迹，**避免加载预先全部的地图进行实时的路径规划**（像人一样，走自己走过的路），如果**出现了地图的修正，障碍物，自动贴合选择其他的规划好的路径**（自己按照经验选择可选的路径），保证了动态修正性和不必要的资源浪费

[GPU Module (gpu) — Blender Python API](https://docs.blender.org/api/current/gpu.html)空间行驶仿真的库

轨迹定位使用[SplaTAM](../../docs/papers/SplaTAM.pdf)

图形的存储应该进行压缩，保留地面平面和和空间占用，导航计算应该是压缩过的空间占用地图

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

### planning

2024-02-16
_导航的地图怎么办，以及导航方法？_

1. 可以将点云数据转化成二位的`占用网格`，传统路径规划算法
2. 或者至今在三维空间实现空间路径规划，可能要找找最新的，香港科技大学，GitHub仓库里面好像是有类似的，是关于无人机的

2024-03-15

- [x] 导航的地图基本确定为[3DGS](../../docs/papers/3DGS.pdf)的场景表示法，非常优异的性能
- [x] 导航的方法目打算先参考[splat_nav](../../docs/papers/splat_nav.pdf)中采用这些，`A*`之类的

_规划算法怎么在3DGS中进行空间搜索还是个问题？_

2024-03-16
- [x]  使用[habitat-sim](https://github.com/facebookresearch/habitat-sim)进行仿真地图，预先加载地图，并且根据渲染的相机视角的RGP-D图像作为splaTAM进行定位
