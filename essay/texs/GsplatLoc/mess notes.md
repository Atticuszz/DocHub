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


## Normalization

```python
@torch.no_grad()
# @torch.compile
def similarity_from_cameras(
    c2w: torch.Tensor, strict_scaling: bool = False, center_method: str = "focus"
) -> torch.Tensor:
    """
    Calculate a similarity transformation that aligns and scales camera positions.

    Parameters
    ----------
    c2w : torch.Tensor
        A batch of camera-to-world transformation matrices of shape (N, 4, 4).
    strict_scaling : bool, optional
        If True, use the maximum distance for scaling, otherwise use the median.
    center_method : str, optional
        Method for centering the scene, either "focus" for focusing method or "poses" for camera poses centering.

    Returns
    -------
    torch.Tensor
        A 4x4 similarity transformation matrix that aligns, centers, and scales the input cameras.

    Raises
    ------
    ValueError
        If the `center_method` is not recognized.
    """
    t = c2w[:, :3, 3]
    R = c2w[:, :3, :3]

    # Rotate the world so that z+ is the up axis
    ups = torch.sum(R * torch.tensor([0, -1.0, 0], device=R.device), dim=-1)
    world_up = torch.mean(ups, dim=0)
    world_up /= torch.norm(world_up)

    up_camspace = torch.tensor([0.0, -1.0, 0.0], device=R.device)
    c = torch.dot(up_camspace, world_up)
    cross = torch.linalg.cross(world_up, up_camspace)
    skew = torch.tensor(
        [
            [0.0, -cross[2], cross[1]],
            [cross[2], 0.0, -cross[0]],
            [-cross[1], cross[0], 0.0],
        ],
        device=R.device,
    )

    if c > -1:
        R_align = torch.eye(3, device=R.device) + skew + (skew @ skew) * 1 / (1 + c)
    else:
        R_align = torch.tensor(
            [[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], device=R.device
        )

    R = R_align @ R
    fwds = torch.sum(R * torch.tensor([0, 0.0, 1.0], device=R.device), dim=-1)
    t = (R_align @ t.unsqueeze(-1)).squeeze(-1)

    # Recenter the scene
    if center_method == "focus":
        nearest = t + (fwds * -t).sum(dim=-1).unsqueeze(-1) * fwds
        translate = -torch.median(nearest, dim=0)[0]
    elif center_method == "poses":
        translate = -torch.median(t, dim=0)[0]
    else:
        raise ValueError(f"Unknown center_method {center_method}")

    transform = torch.eye(4, device=R.device)
    transform[:3, 3] = translate
    transform[:3, :3] = R_align

    # Rescale the scene using camera distances
    scale_fn = torch.max if strict_scaling else torch.median
    scale = 1.0 / scale_fn(torch.norm(t + translate, dim=-1))
    transform[:3, :] *= scale

    return transform


@torch.no_grad()
# @torch.compile
def align_principle_axes(point_cloud: torch.Tensor) -> torch.Tensor:
    """
    Align the principal axes of a point cloud to the coordinate axes using PCA.

    Parameters
    ----------
    point_cloud : torch.Tensor
        Nx3 tensor containing the 3D point cloud.

    Returns
    -------
    torch.Tensor
        A 4x4 transformation matrix that aligns the point cloud along principal axes.
    """
    # Compute centroid
    centroid = torch.median(point_cloud, dim=0).values

    # Translate point cloud to centroid
    translated_point_cloud = point_cloud - centroid

    # Compute covariance matrix
    covariance_matrix = torch.cov(translated_point_cloud.t())

    # Compute eigenvectors and eigenvalues
    eigenvalues, eigenvectors = torch.linalg.eigh(covariance_matrix)

    # Sort eigenvectors by eigenvalues in descending order
    sort_indices = eigenvalues.argsort(descending=True)
    eigenvectors = eigenvectors[:, sort_indices]

    # Check orientation of eigenvectors. If the determinant is negative, flip an eigenvector.
    if torch.det(eigenvectors) < 0:
        eigenvectors[:, 0] *= -1

    # Create rotation matrix
    rotation_matrix = eigenvectors.t()

    # Create SE(3) matrix (4x4 transformation matrix)
    transform = torch.eye(4, device=point_cloud.device)
    transform[:3, :3] = rotation_matrix
    transform[:3, 3] = -torch.mv(rotation_matrix, centroid)

    return transform


@torch.no_grad()
# @torch.compile
def transform_points(matrix: torch.Tensor, points: torch.Tensor) -> torch.Tensor:
    """
    Transform points using a SE(3) transformation matrix.

    Parameters
    ----------
    matrix : torch.Tensor
        A 4x4 SE(3) transformation matrix.
    points : torch.Tensor
        An Nx3 tensor of points to be transformed.

    Returns
    -------
    torch.Tensor
        An Nx3 tensor of transformed points.
    """
    assert matrix.shape == (4, 4)
    assert len(points.shape) == 2 and points.shape[1] == 3
    return torch.addmm(matrix[:3, 3], points, matrix[:3, :3].t())，@torch.no_grad()
# @torch.compile
def transform_cameras(
    matrix: torch.Tensor, c2w: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply a SE(3) transformation to a set of camera-to-world matrices.

    Parameters
    ----------
    matrix : torch.Tensor
        A 4x4 SE(3) transformation matrix.
    c2w : torch.Tensor
        An Nx4x4 tensor of camera-to-world matrices.

    Returns
    -------
    torch.Tensor
        An Nx4x4 tensor of transformed camera-to-world matrices.
    """
    assert matrix.shape == (4, 4)
    assert len(c2w.shape) == 3 and c2w.shape[1:] == (4, 4)
    # Perform the matrix multiplication with einsum for better control
    transformed = torch.einsum("ki,nij->nkj", matrix, c2w)

    # Normalize the 3x3 rotation matrices to maintain scale: Use the norm of the first row
    scaling = torch.norm(transformed[:, 0, :3], p=2, dim=1, keepdim=True)
    transformed[:, :3, :3] /= scaling.unsqueeze(
        -1
    )  # Unsqueeze to match the shape for broadcasting
    return transformed, scaling，@torch.no_grad()
def normalize_2C(tar: RGBDImage, src: RGBDImage) -> tuple[RGBDImage, RGBDImage, Tensor]:
    """normalize two rgb-d image with tar.pose"""
    pose = tar.pose.unsqueeze(0)  # -> N,4,4
    # calculate tar points normalization transform
    points = tar.points
    T1 = similarity_from_cameras(pose)
    T2 = align_principle_axes(transform_points(T1, points))
    transform = T2 @ T1

    # apply transform
    tar.points = transform_points(transform, tar.points)
    src.points = transform_points(transform, src.points)
    normed_tar_pose, _ = transform_cameras(transform, tar.pose.unsqueeze(0))
    tar.pose = normed_tar_pose.squeeze(0)
    normed_src_pose, scale_factor = transform_cameras(transform, src.pose.unsqueeze(0))
    src.pose = normed_src_pose.squeeze(0)
    return tar, src, scale_factor
```
## Gaussian Splatting

```python
@dataclass
class GsConfig:
    init_opa: float = 1.0
    sparse_grad: bool = False
    packed: bool = False
    absgrad: bool = False
    antialiased: bool = False
    # Degree of spherical harmonics
    sh_degree: int = 1

    # RasterizeConfig
    # Near plane clipping distance
    near_plane: float = 1e-10
    # Far plane clipping distance
    far_plane: float = 1e10


class GSModel(nn.Module):
    def __init__(
        self,
        # dataset
        points: Tensor,  # N,3
        colors: Tensor,  # N,3
        *,
        # config
        config: GsConfig = GsConfig(),
        batch_size: int = 1,
    ):
        super().__init__()
        self.config = config
        self.batch_size = batch_size
        points = points
        # points = gs_data.points
        rgbs = colors
        # rgbs = gs_data.colors
        # scene_scale = gs_data.scene_scale
        # scene_scale = gs_data.scene_scale

        # Calculate distances for initial scale
        dist2_avg = (knn(points, 4)[:, 1:] ** 2).mean(dim=-1)
        dist_avg = torch.sqrt(dist2_avg)
        scales = torch.log(dist_avg).unsqueeze(-1).repeat(1, 3)

        # Parameters
        self.means3d = points  # [N, 3]
        # self.means3d = nn.Parameter(points)  # [N, 3]
        self.scales = nn.Parameter(scales)
        self.opacities = nn.Parameter(
            torch.logit(
                torch.full((points.shape[0],), self.config.init_opa, device=DEVICE)
            )
        )  # [N,]
        # NOTE: no deformation
        self.quats = torch.nn.Parameter(
            to_tensor([1, 0, 0, 0], requires_grad=True).repeat(points.shape[0], 1)
        )  # [N, 4]
        # self.quats = torch.nn.Parameter(quats)

        # # color is SH coefficients.
        colors = torch.zeros(
            (points.shape[0], (self.config.sh_degree + 1) ** 2, 3), device=DEVICE
        )  # [N, K, 3]
        colors[:, 0, :] = rgb_to_sh(rgbs)  # Initialize SH coefficients
        self.colors = nn.Parameter(rgbs)
        self.sh0 = torch.nn.Parameter(colors[:, :1, :])
        self.shN = torch.nn.Parameter(colors[:, 1:, :])

        # Learning rates (not parameters, stored for optimizer setup)
        # self.lr_means3d = 1.6e-4 * scene_scale
        self.lr_scales = 5e-3
        self.lr_opacities = 5e-2
        self.lr_colors = 2.5e-3
        self.lr_sh0 = 2.5e-3
        self.lr_shN = 2.5e-3 / 20
        self.optimizers = self._create_optimizers()

        # Running stats for prunning & growing.
        n_gauss = points.shape[0]
        self.running_stats = {
            "grad2d": torch.zeros(n_gauss, device=DEVICE),  # norm of the gradient
            "count": torch.zeros(n_gauss, device=DEVICE, dtype=torch.int),
        }

    def __len__(self):
        return self.means3d.shape[0]

    def forward(
        self,
        camtoworlds: Tensor,
        Ks: Tensor,
        width: int,
        height: int,
        render_mode: str = "RGB+ED",
    ):
        assert self.means3d.shape[0] == self.opacities.shape[0]
        opacities = torch.sigmoid(self.opacities)
        colors = torch.cat([self.sh0, self.shN], 1)
        # colors = torch.sigmoid(self.colors)
        scales = torch.exp(self.scales)

        render_colors, render_alphas, info = rasterization(
            means=self.means3d,
            quats=self.quats,
            scales=scales,
            opacities=opacities,
            colors=colors,
            sh_degree=self.config.sh_degree,
            viewmats=torch.linalg.inv(camtoworlds),
            Ks=Ks,
            width=width,
            height=height,
            packed=self.config.packed,
            absgrad=self.config.absgrad,
            sparse_grad=self.config.sparse_grad,
            far_plane=self.config.far_plane,
            near_plane=self.config.near_plane,
            render_mode=render_mode,
            rasterize_mode="antialiased" if self.config.antialiased else "classic",
        )

        return render_colors, render_alphas, info

    def _create_optimizers(self) -> list[Optimizer]:
        params = [
            ("scales", self.scales, self.lr_scales),
            ("opacities", self.opacities, self.lr_opacities),
            ("colors", self.colors, self.lr_colors),
        ]

        # if self.config.turn_on_light:
        #     # params.append(("sh0", self.sh0, self.lr_sh0))
        #     # params.append(("shN", self.shN, self.lr_shN))
        #     # params.append(("means3d", self.means3d, self.lr_means3d))

        optimizers = [
            (SparseAdam if self.config.sparse_grad else Adam)(
                [
                    {
                        "params": param,
                        "lr": lr * math.sqrt(self.batch_size),
                        "name": name,
                    }
                ],
                eps=1e-15 / math.sqrt(self.batch_size),
                betas=(
                    1 - self.batch_size * (1 - 0.9),
                    1 - self.batch_size * (1 - 0.999),
                ),
            )
            for name, param, lr in params
        ]

        return optimizers
```


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


## 收敛判断

### Experements

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

| Methods     | Avg. | R0   | R1   | R2   | Of0  | Of1  | Of2  | Of3  | Of4  |
|-------------|------|------|------|------|------|------|------|------|------|
| DROID-SLAM  | 0.38 | 0.53 | 0.38 | 0.45 | 0.35 | 0.24 | 0.36 | 0.33 | 0.43 |
| Vox-Fusion  | 3.09 | 1.37 | 4.70 | 1.47 | 8.48 | 2.04 | 2.58 | 1.11 | 2.94 |
| NICE-SLAM   | 1.06 | 0.97 | 1.31 | 1.07 | 0.88 | 1.00 | 1.06 | 1.10 | 1.13 |
| ESLAM       | 0.63 | 0.71 | 0.70 | 0.52 | 0.57 | 0.55 | 0.58 | 0.72 | 0.63 |
| Point-SLAM  | 0.52 | 0.61 | 0.41 | 0.37 | 0.38 | 0.48 | 0.54 | 0.69 | 0.72 |
| SplaTAM     | 0.36 | 0.31 | 0.40 | 0.29 | 0.47 | 0.27 | 0.29 | 0.32 | 0.55 |

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
