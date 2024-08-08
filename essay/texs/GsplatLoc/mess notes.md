GSplatLoc，这是我的一个基于3d高斯显示场景表示法的重投影误差方法，你给我取几个标题并且一个标题后面的介绍就像这样SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM，Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting，重投影3d高斯姿态估计超高精度估计方法，旋转误差几乎为0


侧重点应该是重投影和姿态优化方法


**GSplatLoc: Ultra-Precise Pose Optimization via 3D Gaussian Reprojection** GSplatLoc offers an ultra-precise approach to pose optimization using 3D Gaussian reprojection. By meticulously minimizing reprojection errors, this method achieves exceptional accuracy in 3D pose estimation, essential for detailed and realistic scene reconstruction.


Abstract. We present a dense simultaneous localization and mapping (SLAM) method that uses 3D Gaussians as a scene representation. Our approach enables interactive-time reconstruction and photo-realistic rendering from real-world single-camera RGBD videos. To this end, we propose a novel effective strategy for seeding new Gaussians for newly explored areas and their effective online optimization that is independent of the scene size and thus scalable to larger scenes. This is achieved by organizing the scene into sub-maps which are independently optimized and do not need to be kept in memory. We further accomplish frame-tomodel camera tracking by minimizing photometric and geometric losses between the input and rendered frames. The Gaussian representation allows for high-quality photo-realistic real-time rendering of real-world scenes. Evaluation on synthetic and real-world datasets demonstrates competitive or superior performance in mapping, tracking, and rendering compared to existing neural dense SLAM methods.，Dense simultaneous localization and mapping (SLAM) is crucial for robotics and augmented reality applications. However, current methods are often hampered by the nonvolumetric or implicit way they represent a scene. This work introduces SplaTAM, an approach that, for the first time, leverages explicit volumetric representations, i.e., 3D Gaussians, to enable high-fidelity reconstruction from a single unposed RGB-D camera, surpassing the capabilities of existing methods. SplaTAM employs a simple online tracking and mapping system tailored to the underlying Gaussian representation. It utilizes a silhouette mask to elegantly capture the presence of scene density. This combination enables several benefits over prior representations, including fast rendering and dense optimization, quickly determining if areas have been previously mapped, and structured map expansion by adding more Gaussians. Extensive experiments show that SplaTAM achieves up to 2× superior performance in camera pose estimation, map construction, and novel-view synthesis over existing methods, paving the way for more immersive high-fidelity SLAM applications.，模仿他们的风格，给我写一个abstract，标题我选用了GSplatLoc: Ultra-Precise Pose Optimization via 3D Gaussian Reprojection，我们提出来一种基于3d高斯显示体积表示时的一种高精度姿态优化方法，3d高斯的重投影，适用于没有姿态的RGB-D相机，主要针对于rgb-d数据，主要利用了通过观察不同视角的现有3d高斯和实际拍摄的深度图的进行优化当前姿态，实现了旋转误差几乎为0，平移误差为0.01mm以内，并且和现有对rgb0d数据姿态估计的点云对其算法做了详细的比较，姿态误差实现百倍提升




然后你开始给我写一些公式，深度图的定义，2.2 Depth Compositing of Gaussians We directly follow the tile sorting method introduced by [Kerbl et al., 2023], which bins the 2D Gaussians into 16 × 16 tiles and sorts them per tile by depth. For each Gaussian, we compute the axis-aligned bounding box around the 99% confidence ellipse of each 2D projected covariance (3 sigma), and include it in a tile bin if its bounding box intersects with the tile. We then apply the tile sorting algorithm as presented in Appendix C of [Kerbl et al., 2023] to get a list of Gaussians sorted by depth for each tile. We then rasterize the sorted Gaussians within each tile. For a color at a pixel i, let n index the N Gaussians involved in that pixel. Ci = ∑ n≤N cn · αn · Tn , where Tn = ∏ m<n (1 − αm ). (7) We compute α with the 2D covariance Σ′ ∈R2× 2 and opacity parameters: αn = on · exp(−σn ), σn = 1 2 ∆⊤ n Σ ′−1∆ n , where ∆ ∈R2 and is the offset between the pixel center and the 2D Gaussian center μ′ ∈R2. We compute Tn online as we iterate through the Gaussians front to back，帮我先定义一下深度信息的数学公式，根据图片内容，我需要定义重投影采用的方法是什么？以及损失是如何设计的，采用一部分深度l1损失，一部分深度轮廓损失，



localization for Dense simultaneous localization and mapping (SLAM)中的定位方法部分

# abstract

We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.

这种定位方法既可以集成到基于高斯的slam，也可以集成到gs的navigation中，提供了

# Relate works
和orb特征点相关的有[@huangPhotoSLAMRealtimeSimultaneous2024]这个过程的目标是最小化匹配帧的2D几何关键点和3D点之间的重新投影误差。
[@huCGSLAMEfficientDense2024]，跟踪损失由颜色损失和几何损失组成，
[@matsukiGaussianSplattingSlam2024]优化目标函数结合了光度残差和几何残差,
# Methods


这是一段参考文本，但是描述的不是我的方法，需要修改成我的方法，我会在对应的句子后面添加应该修改的内容
**Problem formulation:** Our goal is to estimate the 6-DoF pose (R , t) ∈ SE(3) of a query image I q，这里查询的应该是是深度图像, where R is a rotation matrix and t is a translation vector in the camera frame.姿态确实是深度相机的姿态 We are given a 3D representation of the environment, such as a sparse or dense 3D point cloud我们这里不是点云了应该是3D Gaussians,是3D高斯 { P i } and posed reference images { I k }和有姿态的参考深度图 , collectively called the reference data.




In the context of depth projection and rasterization for Gaussian splatting, the process involves several mathematical transformations to project 3D Gaussians onto a 2D image plane. Here’s a detailed explanation of the implementation based on the provided code and mathematical principles:

1. **Camera Transformations**:
    - **Extrinsics $T_{cw}$**: This matrix transforms points from the world coordinate space to the camera coordinate space. It is defined as:
      $$
      T_{cw} = \begin{bmatrix} R_{cw} & t_{cw} \\ 0 & 1 \end{bmatrix} \in SE(3)
      $$
      where $R_{cw}$ is the rotation matrix, and $t_{cw}$ is the translation vector.

    - **Projection Matrix $P$**: This matrix transforms points from camera space to normalized device coordinates (ND). It is defined as:
      $$
      P = \begin{bmatrix} \frac{2f_x}{w} & 0 & 0 & 0 \\ 0 & \frac{2f_y}{h} & 0 & 0 \\ 0 & 0 & \frac{f+n}{f-n} & -\frac{2fn}{f-n} \\ 0 & 0 & 1 & 0 \end{bmatrix}
      $$
      where $w$ and $h$ are the width and height of the output image, and $n$ and $f$ are the near and far clipping planes.

2. **Projection of 3D Gaussians**:
    - The 3D mean $\mu$ of the Gaussian is projected into pixel space:
      $$
      t = T_{cw} \begin{bmatrix} \mu \\ 1 \end{bmatrix}, \quad t' = P t, \quad \mu' = \begin{bmatrix} \frac{w \cdot t'_x / t'_w + 1}{2} + c_x \\ \frac{h \cdot t'_y / t'_w + 1}{2} + c_y \end{bmatrix}
      $$

3. **Covariance Transformation**:
    - The 3D Gaussian covariance $\Sigma$ is approximated in the 2D pixel space using the Jacobian $J$:
      $$
      J = \begin{bmatrix} \frac{f_x}{t_z} & 0 & -\frac{f_x t_x}{t_z^2} \\ 0 & \frac{f_y}{t_z} & -\frac{f_y t_y}{t_z^2} \end{bmatrix}
      $$
      The 2D covariance $\Sigma'$ is then:
      $$
      \Sigma' = J R_{cw} \Sigma R_{cw}^T J^T
      $$

4. **Depth Compositing**:
    - Gaussians are sorted by depth and composited from front to back. The colour $C_i$ at pixel $i$ is computed as:
      $$
      C_i = \sum_{n \leq N} c_n \cdot \alpha_n \cdot T_n, \quad T_n = \prod_{m<n} (1 - \alpha_m)
      $$
    - The opacity $\alpha$ is computed as:
      $$
      \alpha_n = o_n \cdot \exp(-\sigma_n), \quad \sigma_n = \frac{1}{2} \Delta_n^T \Sigma'^{-1} \Delta_n
      $$
      where $\Delta$ is the offset between the pixel center and the 2D Gaussian center $\mu'$.

#### Gaussian Model Explanation
The Gaussian model in the provided code involves several parameters and transformations:

1. **3D Means and Covariance**:
    - The 3D means ($\mu$) are derived from the point cloud data.
    - The 3D covariance ($\Sigma$) is parameterized by scale ($s$) and rotation quaternion ($q$). The covariance is computed as:
      $$
      \Sigma = R S S^T R^T, \quad R = \text{rotation matrix from quaternion } q, \quad S = \text{diag}(s)
      $$



To generate the depth map, we employ a front-to-back compositing strategy. For each pixel $p$, its depth value $d_p$ is computed as:
$$d_p = \sum_i w_i z_i$$
where $z_i$ represents the depth of the $i$-th Gaussian's mean, and $w_i$ is the weight derived from the 2D Gaussian distribution:
$$w_i = \exp\left(-\frac{1}{2}(x_p - \mu_{I,i})^T \Sigma_{I,i}^{-1} (x_p - \mu_{I,i})\right)$$
Here, $x_p$ is the 2D coordinate of pixel $p$, $\mu_{I,i}$ and $\Sigma_{I,i}$ denote the projected mean and covariance of the $i$-th Gaussian.

This approach enables efficient depth map generation by leveraging the dense point cloud captured by the depth camera, without requiring colour information.

## Depth Compositing 


Depth at a pixel $i$ is represented by combining contributions from multiple Gaussian elements, each associated with a certain depth and confidence. Depth $D_i$ can be expressed as[@kerbl3dGaussianSplatting2023]:
$$ 
D_i = \frac{\sum_{n \leq N} d_n \cdot c_n \cdot \alpha_n \cdot T_n}{\sum_{n \leq N} c_n \cdot \alpha_n \cdot T_n} 
$$
$d_n$ is the depth value from the $n$-th Gaussian, $c_n$ is the confidence or weight of the $n$-th Gaussian,$\alpha_n$ is the opacity calculated from Gaussian parameters, $T_n$ is the product of transparencies from all Gaussians in front of the $n$-th Gaussian.

The reprojection method utilizes the alignment of 2D Gaussian projections with observed depth data from an RGB-D camera. This involves adjusting the parameters of the Gaussians to minimize the discrepancy between the projected depth and the observed depth. The offset $\Delta_n$ and the covariance matrix $\Sigma'$ are crucial for calculating the Gaussian weights $\alpha_n$ and their impact on reprojection accuracy.


深度生成
[gsplat/gsplat/rendering.py at main · nerfstudio-project/gsplat · GitHub](https://github.com/nerfstudio-project/gsplat/blob/main/gsplat/rendering.py)
```python
if render_mode in ["ED", "RGB+ED"]: 
	# normalize the accumulated depth to get the expected depth 
	render_colors = torch.cat( [ render_colors[..., :-1],
								render_colors[..., -1:] / render_alphas.clamp(min=1e-10), ], dim=-1, 
							)
```
我是用的是ED方式，也就是说，



## Camera Tracking




这里你要写一个最小化目标，并且我用的是adam优化器，解释优化方法，
```python
@dataclass(frozen=True)
class CameraConfig:
    trans_lr: float = 1e-3
    quat_lr: float = 5 * 1e-4
    quat_opt_reg: float = 1e-3
    trans_opt_reg: float = 1e-3
    def _create_optimizers(self) -> list[Optimizer]:
        params = [
            # name, value, lr
            # ("means3d", self.means3d, self.lr_means3d),
            ("quat", self.quaternion_cur, self.config.quat_lr),
            ("trans", self.translation_cur, self.config.trans_lr),
        ]
        optimizers = [
            Adam(
                [
                    {
                        "params": param,
                        "lr": lr,
                        "name": name,
                    }
                ],
                weight_decay=(
                    self.config.quat_opt_reg
                    if name == "quat"
                    else self.config.trans_opt_reg
                ),
            )
            for name, param, lr in params
        ]
        return optimizers
```
,并且我是定义了weight_decay，,这个你也要体现在优化目标中，总损失应该是定义了 一个正则项的


##  Localization pipeline

在这个定义下，我又产生了新的段落，来描述初始化高斯的过程，
## Localization pipeline


We initialize these Gaussians from a point cloud, where each point corresponds to a Gaussian's mean $\boldsymbol{\mu}_i$.
Unlike traditional 3D reconstruction methods[@kerbl3dGaussianSplatting2023] that often rely on structure-from-motion techniques[@schonbergerStructurefrommotionRevisited2016], our approach is tailored for direct point cloud input, offering greater flexibility and efficiency in various 3D data scenarios. For the initial parameterization, we set $o_i = 1$ for all Gaussians to ensure full opacity. The scale $\mathbf{s}_i \in \mathbb{R}^3$ of each Gaussian is initialized based on the local point density, allowing our model to adaptively adjust to varying point cloud densities:

$$\mathbf{s}_i = (\sigma_i, \sigma_i, \sigma_i), \text{ where } \sigma_i = \sqrt{\frac{1}{3}\sum_{j=1}^3 d_{ij}^2}$$

Here, $d_{ij}$ is the distance to the $j$-th nearest neighbour of point $i$. In practice, we calculate this using the k-nearest neighbours algorithm with $k=4$, excluding the point itself. This isotropic initialization ensures a balanced initial representation of the local geometry.

Initially, we set $\mathbf{q}_i = (1, 0, 0, 0)$ for all Gaussians, corresponding to no rotation. This initialization strategy provides a neutral starting point, allowing subsequent optimization processes to refine the orientations as needed.


就像这篇论文一样，4. Localization pipeline PixLoc can be a competitive standalone localization module when coupled with image retrieval, but can also refine poses obtained by previous approaches. It only requires a 3D model and a coarse initial pose, which we now discuss. Initialization: How accurate the initial pose should be depends on the basin of convergence of the alignment. Features from a deep CNN with a large receptive field ensure a large basin (Figure 5). To further increase it, we apply PixLoc to image pyramids, starting at the lowest resolution, yielding coarsest feature maps of size W=16. To keep the pipeline simple, we select the initial pose as the pose of the first reference image returned by image retrieval. This results in a good convergence in most scenarios. When retrieval is not sufficiently robust and returns an incorrect location, as in the most challenging conditions, one could improve the performance by reranking using covisiblity clustering [70,73] or pose verification with sparse [72,96] or dense matching [82]. 3D structure: For simplicity and unless mentioned, for both training and evaluation, we use sparse SfM models triangulated from posed reference images using hloc [69,70] and COLMAP [77,79]. Given a subset of reference images, e.g. top-5 retrieved, we gather all the 3D points that they observe, extract multilevel features at their 2D observations, and average them based on their confidence.，然后这是我的参考我已经写完的方法论部分，

**Problem formulation**: Our objective is to estimate the 6-DoF pose $(R, t) \in SE(3)$ of a query depth image $D_q$, where $R$ is the rotation matrix and $t$ is the translation vector in the camera coordinate system. Given a 3D representation of the environment in the form of 3D Gaussians, let $\mathcal{G} = \{G_i\}_{i=1}^N$ denote a set of $N$ 3D Gaussians, and posed reference depth images $\{D_k\}$, which together constitute the reference data.


## Gaussian Splatting


Each Gaussian $G_i$ is characterized by its 3D mean $\boldsymbol{\mu}_i \in \mathbb{R}^3$, 3D covariance matrix $\boldsymbol{\Sigma}_i \in \mathbb{R}^{3\times3}$, opacity $o_i \in \mathbb{R}$, and scale $\mathbf{s}_i \in \mathbb{R}^3$. To represent the orientation of each Gaussian, we use a rotation quaternion $\mathbf{q}_i \in \mathbb{R}^4$.

The 3D covariance matrix $\boldsymbol{\Sigma}_i$ is then parameterized using $\mathbf{s}_i$ and $\mathbf{q}_i$:

$$\boldsymbol{\Sigma}_i = R(\mathbf{q}_i) S(\mathbf{s}_i) S(\mathbf{s}_i)^T R(\mathbf{q}_i)^T$$

where $R(\mathbf{q}_i)$ is the rotation matrix derived from $\mathbf{q}_i$, and $S(\mathbf{s}_i) = \text{diag}(\mathbf{s}_i)$ is a diagonal matrix of scales.

To project these 3D Gaussians onto a 2D image plane, we follow the approach described by [@kerbl3dGaussianSplatting2023]. The projection of the 3D mean $\boldsymbol{\mu}_i$ to the 2D image plane is given by:

$$\boldsymbol{\mu}_{I,i} = \pi(P(T_{wc} \boldsymbol{\mu}_{i,\text{homogeneous}}))$$

where $T_{wc} \in SE(3)$ is the world-to-camera transformation, $P \in \mathbb{R}^{4 \times 4}$ is the projection matrix [@yeMathematicalSupplementTexttt2023], and $\pi: \mathbb{R}^4 \rightarrow \mathbb{R}^2$ maps to pixel coordinates.

The 2D covariance $\boldsymbol{\Sigma}_{I,i} \in \mathbb{R}^{2\times2}$ of the projected Gaussian is derived as:

$$\boldsymbol{\Sigma}_{I,i} = J R_{wc} \boldsymbol{\Sigma}_i R_{wc}^T J^T$$

where $R_{wc}$ represents the rotation component of $T_{wc}$, and $J$ is the affine transform as described by [@zwickerEWASplatting2002].


## Depth Compositing



For depth map generation, we employ a front-to-back compositing scheme, which allows for accurate depth estimation and edge alignment. Let $d_n$ represent the depth value associated with the $n$-th Gaussian, which is the z-coordinate of the Gaussian's mean in the camera coordinate system. The depth $D(p)$ at pixel $p$ is computed as [@kerbl3dGaussianSplatting2023]:

$$D(p) = \sum_{n \leq N} d_n \cdot \alpha_n \cdot T_n, \quad \text{where } T_n = \prod_{m<n} (1 - \alpha_m)$$

Here, $\alpha_n$ represents the opacity of the $n$-th Gaussian at pixel $p$, computed as:

$$\alpha_n = o_n \cdot \exp(-\sigma_n), \quad \sigma_n = \frac{1}{2} \Delta_n^T \boldsymbol{\Sigma}_I^{-1} \Delta_n$$

where $\Delta_n$ is the offset between the pixel center and the 2D Gaussian center $\boldsymbol{\mu}_I$, and $o_n$ is the opacity parameter of the Gaussian. $T_n$ denotes the cumulative transparency product of all Gaussians preceding $n$, accounting for the occlusion effects of previous Gaussians.

To ensure consistent representation across the image, we normalize the depth values. First, we calculate the total accumulated opacity $\alpha(p)$ for each pixel:

$$\alpha(p) = \sum_{n \leq N} \alpha_n \cdot T_n$$

The normalized depth $\text{Norm}_D(p)$ is then defined as:

$$\text{Norm}_D(p) = \frac{D(p)}{\alpha(p)}$$

This normalization process ensures that the depth values are properly scaled and comparable across different regions of the image, regardless of the varying densities of Gaussians in the scene. By projecting 3D Gaussians onto the 2D image plane and computing normalized depth values, we can effectively generate depth maps that accurately represent the 3D structure of the scene while maintaining consistency across different viewing conditions.

## Camera Pose



We define the camera pose as

$$
 \mathbf{T}_{cw} = \begin{pmatrix} \mathbf{R}_{cw} & \mathbf{t}_{cw} \\ \mathbf{0} & 1 \end{pmatrix} \in SE(3)
$$

where $\mathbf{T}_{cw}$ represents the camera-to-world transformation matrix. Notably, we parameterize the rotation $\mathbf{R}_{cw} \in SO(3)$ using a quaternion $\mathbf{q}_{cw}$. This choice of parameterization is motivated by several key advantages that quaternions offer in the context of camera pose estimation and optimization. Quaternions provide a compact and efficient representation, requiring only four parameters, while maintaining numerical stability and avoiding singularities such as gimbal lock. Their continuous and non-redundant nature is particularly advantageous for gradient-based optimization algorithms, allowing for unconstrained optimization and simplifying the optimization landscape.

## Optimization
Based on these considerations, we design our optimization variables to separately optimize the normalized quaternion and the translation. The loss function is designed to ensure accurate depth estimations and edge alignment, incorporating both depth magnitude and contour accuracy. It can be defined as:

$$ 
L = \lambda_1 \cdot L_{\text{depth}} + \lambda_2 \cdot L_{\text{contour}} 
$$

where $L_{\text{depth}}$ represents the L1 loss for depth accuracy, and $L_{\text{contour}}$ focuses on the alignment of depth contours or edges. Specifically:

$$
L_{\text{depth}} = \sum_{i \in M} |D_i^{\text{predicted}} - D_i^{\text{observed}}|
$$

$$
L_{\text{contour}} = \sum_{j \in M} |\nabla D_j^{\text{predicted}} - \nabla D_j^{\text{observed}}|
$$

Here, $M$ denotes the reprojection mask, indicating which pixels are valid for reprojection. Both $L_{\text{depth}}$ and $L_{\text{contour}}$ are computed only over the masked regions. $\lambda_1$ and $\lambda_2$ are weights that balance the two parts of the loss function, tailored to the specific requirements of the application.

The optimization objective can be formulated as:

$$
\min_{\mathbf{q}_{cw}, \mathbf{t}_{cw}} L + \lambda_q \|\mathbf{q}_{cw}\|_2^2 + \lambda_t \|\mathbf{t}_{cw}\|_2^2
$$

where $\lambda_q$ and $\lambda_t$ are regularization terms for the quaternion and translation parameters, respectively.

We employ the Adam optimizer for both quaternion and translation optimization, with different learning rates and weight decay values for each. The learning rates are set to $5 × 10^-4$ for quaternion optimization and $10^-3$ for translation optimization, based on experimental results. The weight decay values are set to $10^-3$ for both quaternion and translation parameters, serving as regularization to prevent overfitting.
你需要给方法论部分添加一个Localization pipeline，
第一段应该是说定位pipelind的精确的简介描述，我给出我的描述，你不需要全部写出来，提供给你参考，用给定姿态的深度图生成了gs，给定查询深度图的姿态和深度数据本身，然后进行优化求解，我的描述比较口语化，但你写的必须是符合书面论文要求的，计算机顶会论文的标准 
第二段落 下面这个段落是高斯初始化的详细描述We initialize these Gaussians from a point cloud, where each point corresponds to a Gaussian's mean $\boldsymbol{\mu}_i$.
Unlike traditional 3D reconstruction methods[@kerbl3dGaussianSplatting2023] that often rely on structure-from-motion techniques[@schonbergerStructurefrommotionRevisited2016], our approach is tailored for direct point cloud input, offering greater flexibility and efficiency in various 3D data scenarios. For the initial parameterization, we set $o_i = 1$ for all Gaussians to ensure full opacity. The scale $\mathbf{s}_i \in \mathbb{R}^3$ of each Gaussian is initialized based on the local point density, allowing our model to adaptively adjust to varying point cloud densities:

$$\mathbf{s}_i = (\sigma_i, \sigma_i, \sigma_i), \text{ where } \sigma_i = \sqrt{\frac{1}{3}\sum_{j=1}^3 d_{ij}^2}$$

Here, $d_{ij}$ is the distance to the $j$-th nearest neighbour of point $i$. In practice, we calculate this using the k-nearest neighbours algorithm with $k=4$, excluding the point itself. This isotropic initialization ensures a balanced initial representation of the local geometry.

Initially, we set $\mathbf{q}_i = (1, 0, 0, 0)$ for all Gaussians, corresponding to no rotation. This initialization strategy provides a neutral starting point, allowing subsequent optimization processes to refine the orientations as needed.这部分是相当于是初始化高斯的内容，posed reference depth images $\{D_k\}$,为了方便评估实验，我们使用给定姿态的posed reference depth images来进行初始化gs，然后第三部分应该是优化停止，收敛的描述，，大量实验结果显示大约在100次迭代后总损失基本稳定，并且设置了patience机制，我设置为100次后启动patience机制，如果连续超过patience次数总损失不再下降，就推出优化迭代循环，采用总损失最小值的时候为最佳的估计姿态，这是优化收敛停止的描述，我的描述比较口语化，但你写的必须是符合书面论文要求的，计算机顶会论文的标准，开始你对Localization pipeline三段的英文学术论文写作，前后需要非常的连贯学术化，根据我提供给你所有的资料

### Experements

```GPT
你是ChatGPT，由OpenAI训练的大型语言模型。请仔细遵循用户的指示。使用 Markdown 格式进行回应。用Latex写公式时，公式放在$内返回，确保能用Markdown渲染。请你扮演一名熟知各个研究领域的发展历程和最新进展的高级研究员。

我希望你能担任英语拼写校对和修辞改进的角色。

请严格遵守以下修改要求：

我会发送学术论文的语句或段落给你。请逐句将其中的的词汇和句子替换成更为准确和学术的表达方式，确保意思不变，语言不变，但使其更具学术。

请严格按照下列格式输出回答：

首先给出修改后的全文，语言必须与我发送给你的文本语言相同。
然后使用markdown表格格式逐句输出以下内容：

原文被修改内容，没有被修改的部分则跳过。

修改后的内容，语言必须与我发送给你的文本语言相同。

修改理由，请注意，修改理由必须使用中文输出。

语句通顺，用词准确的部分不进行修改，不在表格里列出。

专业词汇不进行修改，不在表格里列出。

表格中原文整句输出。

示例：

修改后：

<修改后>

解析：

| 原文 | 修改后 | 修改理由 |

|------------------------|-----------------------|---------------------------|

| <原文1> | <修改后1> | <修改理由1> |

| <原文2> | <修改后2> | <修改理由2> |

| <原文3> | <修改后3> | <修改理由3> |

接下来我会发送需要你英语拼写校对和修辞改进的内容，请你开始上述操作。As an experienced academic research writer, your task is to write an Mehtod discussing the Pipeline. This work should be detailed, well-researched, and written in an academic style. It needs to provide a comprehensive overview of the subject matter, present a logical argument or analysis, and substantiate it with relevant sources, theories or data. Make sure to incorporate current and relevant references for supporting your points. The language used should be formal, precise, and clear. The document should be formatted according to the applicable academic writing guidelines or style guide. Proofread for clarity, coherence, grammar, and punctuation before submission. here is my chapter:
```

```GPT
As an experienced academic research writer, your task is to write an [introduction/chapter/conclusion] discussing the [topic]. This work should be detailed, well-researched, and written in an academic style. It needs to provide a comprehensive overview of the subject matter, present a logical argument or analysis, and substantiate it with relevant sources, theories or data. Make sure to incorporate current and relevant references for supporting your points. The language used should be formal, precise, and clear. The document should be formatted according to the applicable academic writing guidelines or style guide. Proofread for clarity, coherence, grammar, and punctuation before submission.
```


```GPT
来你要写成像论文那样。一个整段落的去描述前后句子要衔接起来，不要分开分罗列呢，是像人工智能写的，我是让你帮我润色我的论文，你懂我意思吗？按照计算机学术顶会论文的风格来进行写作。
```

```GTP
公式均用$$风格,公式必须用$$包裹而不是/(这种，我要适配obsidian我的笔记
```

```GPT
分析阐述定位方式是什么？定位方式依赖的场景表示是什么？重点解析定位方式的原理和公式，要有分析和对应的公式，公式均用$$风格,公式必须用$$包裹而不是/(这种，我要适配obsidian我的笔记，主要用论文中的公式来解释，你自己也可以加一些数学描述，要指明数学公式是论文中还是你自己写的
```

```GPT
公式均用$$风格，展示关于定位部分的评估标准注意是定位部分，不需要展示重建质量的评估指标，用了哪些及实验数据展示，公式必须用$$包裹而不是/(这种，我要适配obsidian我的笔记,实验数据表格要给全，也要标注是哪个数据集的实验数据表格,每个数据集的表格数据都需要有
```
RMSE

Standard Deviation

![[assets/Pasted image 20240727181353.png|400]]![[assets/Pasted image 20240727181456.png|300]]

*(ATE RMSE [cm] ↓)*
### Replica Dataset

| Methods    | Avg. | R0   | R1   | R2   | Of0  | Of1  | Of2  | Of3  | Of4  |
| ---------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| DROID-SLAM | 0.38 | 0.53 | 0.38 | 0.45 | 0.35 | 0.24 | 0.36 | 0.33 | 0.43 |
| Vox-Fusion | 3.09 | 1.37 | 4.70 | 1.47 | 8.48 | 2.04 | 2.58 | 1.11 | 2.94 |
| NICE-SLAM  | 1.06 | 0.97 | 1.31 | 1.07 | 0.88 | 1.00 | 1.06 | 1.10 | 1.13 |
| ESLAM      | 0.63 | 0.71 | 0.70 | 0.52 | 0.57 | 0.55 | 0.58 | 0.72 | 0.63 |
| Point-SLAM | 0.52 | 0.61 | 0.41 | 0.37 | 0.38 | 0.48 | 0.54 | 0.69 | 0.72 |
| SplaTAM    | 0.36 | 0.31 | 0.40 | 0.29 | 0.47 | 0.27 | 0.29 | 0.32 | 0.55 |

### TUM-RGBD Dataset

| Methods       | Avg. | fr1/desk | fr1/desk2 | fr1/room | fr2/xyz | fr3/off. |
|---------------|------|----------|-----------|----------|---------|----------|
| Kintinous     | 4.84 | 3.70     | 7.10      | 7.50     | 2.90    | 3.00     |
| ElasticFusion | 6.91 | 2.53     | 6.83      | 21.49    | 1.17    | 2.52     |
| ORB-SLAM2     | 1.98 | 1.60     | 2.20      | 4.70     | 0.40    | 1.00     |
| NICE-SLAM     | 15.87| 4.26     | 4.99      | 34.49    | 31.73   | 3.87     |
| Vox-Fusion    | 11.31| 3.52     | 6.00      | 19.53    | 1.49    | 26.01    |
| Point-SLAM    | 8.92 | 4.34     | 4.54      | 30.92    | 1.31    | 3.48     |
| SplaTAM       | 5.48 | 3.35     | 6.54      | 11.13    | 1.24    | 5.16     |
