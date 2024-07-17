---
Title: "RTG-SLAM: Real-time 3D Reconstruction at Scale using Gaussian Splatting"
Authors: Zhexi Peng, Tianjia Shao, Yong Liu, Jingke Zhou, Yin Yang, Jingdong Wang, Kun Zhou

Date: 2024-05-08
citekey: pengRTGSLAMRealtime3D2024
tags: #Computer-Science---Computer-Vision-and-Pattern-Recognition
---

## RTG-SLAM: Real-time 3D Reconstruction at Scale using Gaussian Splatting

**Bibliographie :** [1]

Z. Peng _et al._, ‘RTG-SLAM: Real-time 3D Reconstruction at Scale using Gaussian Splatting’, May 08, 2024. doi: [10.1145/3658233](https://doi.org/10.1145/3658233).

**Lien de la publication :** http://arxiv.org/abs/2404.19706

**Lien Zotero :** [Peng et al_2024_RTG-SLAM.pdf](zotero://select/library/items/9XZCNXU5)

**Tags :** #Computer-Science---Computer-Vision-and-Pattern-Recognition

> [!abstract]+
> _« We present Real-time Gaussian SLAM (RTG-SLAM), a real-time 3D reconstruction system with an RGBD camera for large-scale environments using Gaussian splatting. The system features a compact Gaussian representation and a highly efficient on-the-fly Gaussian optimization scheme. We force each Gaussian to be either opaque or nearly transparent, with the opaque ones fitting the surface and dominant colors, and transparent ones fitting residual colors. By rendering depth in a different way from color rendering, we let a single opaque Gaussian well fit a local surface region without the need of multiple overlapping Gaussians, hence largely reducing the memory and computation cost. For on-the-fly Gaussian optimization, we explicitly add Gaussians for three types of pixels per frame: newly observed, with large color errors, and with large depth errors. We also categorize all Gaussians into stable and unstable ones, where the stable Gaussians are expected to well fit previously observed RGBD images and otherwise unstable. We only optimize the unstable Gaussians and only render the pixels occupied by unstable Gaussians. In this way, both the number of Gaussians to be optimized and pixels to be rendered are largely reduced, and the optimization can be done in real time. We show real-time reconstructions of a variety of large scenes. Compared with the state-of-the-art NeRF-based RGBD SLAM, our system achieves comparable high-quality reconstruction but with around twice the speed and half the memory cost, and shows superior performance in the realism of novel view synthesis and camera tracking accuracy. »_

> [!Annotation|#ff6666]+
>_« Camera tracking. We utilize the frame-to-model ICP as the frontend odometry for camera tracking. Specifically, we use the optimized Gaussians in the previous frame to render the depth map ˆ D∗ 𝑘 −1 and normal map ˆ N∗ 𝑘−1, and convert ˆ D∗ 𝑘 −1 to the global space ˆ V𝑔∗ 𝑘 −1. Then given the current frame V𝑙 𝑘 , we aim to find the camera pose that minimizes the point-to-plane error between 3D backprojected vertices: 𝐸 (𝝃 ) = ∑ T𝑔,𝑘 V𝑙 𝑘 (u) − ˆ V𝑔∗ 𝑘 −1( ˆ u) · ˆ N∗ 𝑘−1( ˆ u) . (10) Here 𝝃 is the Lie algebra representation of T𝑔,𝑘 . We run a multilevel ICP to solve the objective function as [Newcombe et al. 2011]. Meanwhile, in order to reduce the drift during the scanning of large scenes, we also run a back-end optimization thread similar to ORB-SLAM2 [2017]. While the pose estimation is finished, a set of 3D landmarks are also maintained. These landmarks are used for graph optimization in the back-end, enabling more accurate camera tracking. »_([11](zotero://open-pdf/library/items/9XZCNXU5?page=11&annotation=FVYF8BYJ))
>
> ### 定位方式的原理和公式解析
#### 定位方式原理

RTG-SLAM的定位方式基于高斯表示和优化，通过以下步骤实现：

1. **射线投影**：
   从相机中心投射射线，利用相机的内参和外参矩阵计算射线在3D空间中的路径。

2. **颜色渲染**：
   使用高斯模型渲染颜色图像，通过alpha混合计算每个像素的颜色。

3. **深度渲染**：
   计算射线与椭球圆盘的交点，得到每个像素的深度值。

4. **高斯优化**：
   基于颜色和深度的损失函数，通过反向传播优化高斯参数。

5. **相机跟踪**：
   使用帧到模型的ICP（Iterative Closest Point）算法进行相机跟踪，实现准确的位姿估计。

#### 数学公式解析

1. **射线定义**（论文公式）：
   射线通过相机姿态矩阵和相机内参矩阵定义：
   $$
   \mathbf{r}(\mathbf{u}) = (\mathbf{R}_g \mathbf{K}^{-1} \cdot \mathbf{u}) \theta + \mathbf{t}_g
   $$
   其中，
   $$
   \mathbf{T}_g = \begin{pmatrix} \mathbf{R}_g & \mathbf{t}_g \\ 0 & 1 \end{pmatrix} \in SE(3)
   $$

2. **颜色渲染**（论文公式）：
   使用alpha混合来渲染颜色图像：
   $$
   \hat{\mathbf{C}}(\mathbf{u}) = \sum_{i=1}^{n} c_i f_i(\mathbf{u}) \prod_{j=1}^{i-1} (1 - f_j(\mathbf{u}))
   $$
   其中，\( c_i \) 表示高斯的颜色， \( f_i(\mathbf{u}) \) 表示展开到像素空间的二维高斯：
   $$
   f_i(\mathbf{u}) = \alpha_i \exp\left(-\frac{1}{2} (\mathbf{u} - \mu_i)^\top \Sigma_{2D,i}^{-1} (\mathbf{u} - \mu_i)\right)
   $$

3. **光透射图**（论文公式）：
   用于确定光传输的光透射图：
   $$
   \hat{\mathbf{T}}(\mathbf{u}) = \prod_{i=1}^{n} (1 - f_i(\mathbf{u}))
   $$

4. **深度渲染**（结合论文和描述生成）：
   计算视线与椭球圆盘的交点来获得像素的深度：
   $$
   \mathbf{p}_{G_{r,j},r} = (\mathbf{R}_g \mathbf{K}^{-1} \cdot \mathbf{u}) \theta_u + \mathbf{t}_g, \quad \theta_u = \frac{(\mathbf{p}_{r,j} - \mathbf{t}_g) \cdot \mathbf{n}_{r,j}}{(\mathbf{R}_g \mathbf{K}^{-1} \cdot \mathbf{u}) \cdot \mathbf{n}_{r,j}}
   $$

5. **深度图定义**（论文公式）：
   最终的深度图定义为：
   $$
   \hat{\mathbf{D}}(\mathbf{u}) =
   \begin{cases}
   -1, & \text{if no intersection} \\
   (\mathbf{T}_g^{-1} \mathbf{p}_{G_{r,j},r})_z, & \text{if } \langle \mathbf{n}_{r,j}, \mathbf{r} \rangle < 60^\circ \\
   (\mathbf{T}_g^{-1} \mathbf{p}_{r,j})_z, & \text{otherwise}
   \end{cases}
   $$

#### 数学描述

- **射线投影**：通过相机内参矩阵 \( \mathbf{K} \) 和外参矩阵 \( \mathbf{T}_g \)，将2D图像像素坐标 \( \mathbf{u} \) 映射到3D空间中的射线 \( \mathbf{r}(\mathbf{u}) \)。

- **颜色渲染**：根据每个高斯的颜色和位置，通过alpha混合公式计算每个像素的最终颜色值 \( \hat{\mathbf{C}}(\mathbf{u}) \)。

- **深度渲染**：通过计算射线 \( \mathbf{r}(\mathbf{u}) \) 与椭球圆盘的交点，确定每个像素的深度值 \( \hat{\mathbf{D}}(\mathbf{u}) \)。

- **高斯优化**：通过最小化颜色和深度损失函数，使用反向传播算法优化高斯参数。

- **相机跟踪**：通过ICP算法，利用前后帧的深度信息进行相机位姿估计。

这些公式和方法共同作用，使RTG-SLAM系统能够在较低的内存和计算成本下，实现高效的在线3D重建和相机跟踪。


