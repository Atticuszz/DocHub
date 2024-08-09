---
first-title-word: GSplatLoc
title-rest: ": Ultra-Precise Pose Optimization via 3D Gaussian Reprojection"
bibliography: C:/Users/18317/DevSpace/DocHub/essay/zotero/bibliography.bib
csl: C:/Users/18317/DevSpace/DocHub/essay/zotero/ieee.csl
resource-path: C:/Users/18317/DevSpace/DocHub/essay;C:/Users/18317/DevSpace/DocHub/assets;
author:
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
    orcid: https://orcid.org/0009-0008-5460-325X
  - name: Atticus Zhou
abstract: We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.
url: https://github.com/Atticuszz/GsplatLoc
---
# Introduction



We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.


# Related Work


Accurate visual localization commonly relies on estimating correspondences between 2D pixel positions and 3D scene coordinates. Such approaches detect, describe [7,49], and match [32,46,48,73,81,96] local features, maintain an explicit sparse 3D representation of the environment, and sometimes leverage image retrieval [33,86] to scale to large scenes [32,57,70,75,82,87]. Recently, many of these components have been learned with great success [2,23,25,58,60,65,67,71,95], but often independently and not end-to-end due to the complexity of such systems. Here we introduce a simpler alternative to feature matching, finally enabling stable end-to-end training. Our solution can learn more powerful priors than individual blocks, yet remains highly flexible and interpretable. End-to-end learning for localization has recently received much attention. Common approaches encode the scene into a deep network by regressing from an input image to an absolute pose [35,37,59,66,90] or 3D scene coordinates [9,13,16,17,80]. Pose regression lacks geometric constraints and thus does not generalize well to novel viewpoints or appearances [76,78], while coordinate regression is more robust. Both do not scale well due to the limited network capacity [11,82] and require for each new scene either costly retraining or adaptation [16,17]. ESAC [11] improves the scalability by training an ensemble of regressors, each specialized in a scene subset, but is still significantly less accurate than feature-based methods in larger environments. Differently, some approaches regress a camera pose relative to one or more training images [5,24,42,97], often after an explicit retrieval step. They do no memorize the scene geometry and are thus scene-agnostic, but, similar to absolute regressors, are less accurate than feature-based methods [76,97]. Closer to ours, SANet [93] takes the scene representation out of the network by regressing 3D coordinates from an input 3D point cloud. Critically, all top-performing learnable approaches are at least trained per-dataset, if not per-scene, and are limited to small environments [37,80]. In this work we demonstrate the first end-to-end learnable network that generalizes across scenes, including from outdoor to indoor, and that delivers performance competitive with complex pipelines on large real-world datasets, thanks to a differentiable pose solver. Learning camera pose optimization can be tackled by unrolling the optimizer for a fixed number of steps [21,51,53, 83,91,92], computing implicit derivatives [13,15,18,34,68], or crafting losses to mimic optimization steps [88,89]. Multiple works have proposed to learn components of these optimizers [21,51,83], with added complexity and unclear generalization. Some of these formulations optimize reprojection errors over sparse points, while others use direct objectives for (semi-)dense image alignment. The latter are attractive for their simplicity and accuracy, but usually do not scale well. Like their classical counterparts [26,38], they also suffer from a small basin of convergence, limiting them to frame tracking. In contrast, PixLoc is explicitly trained for wide-baseline cross-condition camera pose estimation from sparse measurements (Figure 2). By focusing on learning good features, it shows good generalization yet learns sensible data priors that shape the optimization objective.


# Method

**Overview:** 这里你可以自由发挥

**Motivation:** 这里我要参考文献，但你也可以添加一些自己的观点

**Problem formulation**: Our objective is to estimate the 6-DoF pose $(R, t) \in SE(3)$ of a query depth image $D_q$, where $R$ is the rotation matrix and $t$ is the translation vector in the camera coordinate system. Given a 3D representation of the environment in the form of 3D Gaussians, let $\mathcal{G} = \{G_i\}_{i=1}^N$ denote a set of $N$ 3D Gaussians, and posed reference depth images $\{D_k\}$, which together constitute the reference data.


## Scene Representation

额外上下文参考包裹边界###
Gaussian splatting [@kerbl3dGaussianSplatting2023] is an effective method for representing 3D scenes with novel-view synthesis capability. This approach is notable for its speed, without compromising the rendering quality. In  [@kerbl3dGaussianSplatting2023], 3D Gaussians are initialized from a sparse Structure-from-Motion point cloud of a scene. With images observing the scene from different angles, the Gaussian parameters are optimized using differentiable rendering
额外上下文参考包裹边界###，这里应该添加对我当前段落 Scene Representation的一个开头的简介，我是先介绍这篇论文的方法，注意我是用的是高斯spalting可微分的深度图生成过程，当前段落应该是介绍我的场景表示的定义，聚焦于原论文定义中的能够进行深度合成的部分，



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


## Depth Rendering


添加额外术语，a differential depth rendering，因为整个深度合成过程是可微分的,需要强调可微分
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

额外上下文参考包裹边界###
This differentiable rendering allows us to directly calculate the gradients in the underlying scene representation (Gaussians) and camera parameters with respect to the error between the renders and provided RGB-D frames, and update both the Gaussians and camera parameters to minimize this error, thus fitting both accurate camera poses and an accurate volumetric representation of the world.
额外上下文参考包裹边界###，这是其他论文可以参考的注意他的方法是和我不一样的，他把相机参数直接拿进去进行优化了，我是利用深度渲染的可微分性，就是说深度合成的过程可微分可计算梯度，这里给出参考上下文的目的是让Depth Compositing这个段落能够更好的和上下文衔接在一起，因为这个段落段尾需要指出他的这种可微分性，梯度，才能衔接后面论文的损失优化设计的内容
## Localization as Image alignment


这里应该添加一些符合上文高斯的内容，上文是用来定义了高斯场以及可微分深度合成的过程，Assume we have an existing map (represented via a set of 3D Gaussians) 这里应该假设已经有了一个现有的高斯表示，，然后引出**Problem formulation**提到的，注意在前面的段落中*Problem formulation* 中，已经提到了，Our objective is to estimate the 6-DoF pose $(R, t) \in SE(3)$ of a query depth image $D_q$, where $R$ is the rotation matrix and $t$ is the translation vector in the camera coordinate system,已经解释了相机姿态的定义了，这里不需要再定义Tcw，公式可以省略或者换成其他的重点，比如我自己的段落给出了很多关于采用为什么四元数的描述，查询图像是和splating生成的深度图并且是normalized的，这个章节主要是详细优化姿态的姿态怎么设计的，还有关于优化损失的设计的细节

**Fitting the optimizer to the data:** 可以适当的给段落添加这样的引出

We define the camera pose as

$$
 \mathbf{T}_{cw} = \begin{pmatrix} \mathbf{R}_{cw} & \mathbf{t}_{cw} \\ \mathbf{0} & 1 \end{pmatrix} \in SE(3)
$$

where $\mathbf{T}_{cw}$ represents the camera-to-world transformation matrix. Notably, we parameterize the rotation $\mathbf{R}_{cw} \in SO(3)$ using a quaternion $\mathbf{q}_{cw}$. This choice of parameterization is motivated by several key advantages that quaternions offer in the context of camera pose estimation and optimization. Quaternions provide a compact and efficient representation, requiring only four parameters, while maintaining numerical stability and avoiding singularities such as gimbal lock. Their continuous and non-redundant nature is particularly advantageous for gradient-based optimization algorithms, allowing for unconstrained optimization and simplifying the optimization landscape.这里的描述有点不符合上下文的语境，Depth Rendering是可微分的，重点应该是这个， particularly advantageous for gradient-based optimization algorithms不够具体，好像再单独的说四元数表示旋转的解释，但我这里的情形是如何有助于优化的旋转表示，需要精确符合上下文而且不可以多废话啰嗦


**Fitting the optimizer to the data:** Based on these considerations, we design our optimization variables to separately optimize the normalized  $\mathbf{q}_{cw}$ and  $\mathbf{t}_{cw}$. The loss function is designed to ensure accurate depth estimations and edge alignment, incorporating both depth magnitude and contour accuracy. It can be defined as:

$$ 
L = \lambda_1 \cdot L_{\text{depth}} + \lambda_2 \cdot L_{\text{contour}} 
$$


关于depth_lambda大概是0.8,counter是0.2，其中轮廓计算是通过`kornia.filters.sobel(_input_, _normalized=True_, _eps=1e-6_)[¶](https://kornia.readthedocs.io/en/latest/filters.html#kornia.filters.sobel "Link to this definition")Compute the Sobel operator and returns the magnitude per channel.`计算的，你也需要转化成学术论文的描述，你也要引入采用轮廓损失的优点等等等，你要有自己的观点，我是觉得类似于边缘对其的效果，你要多解释解释，sobel的引用是[@kanopoulosDesignImageEdge1988]


where $L_{\text{depth}}$ represents the L1 loss for depth accuracy, and $L_{\text{contour}}$ focuses on the alignment of depth contours or edges. Specifically:

$$
L_{\text{depth}} = \sum_{i \in M} |D_i^{\text{predicted}} - D_i^{\text{observed}}|
$$

$$
L_{\text{contour}} = \sum_{j \in M} |\nabla D_j^{\text{predicted}} - \nabla D_j^{\text{observed}}|
$$

Here, $M$ denotes the reprojection mask, indicating which pixels are valid for reprojection. Both $L_{\text{depth}}$ and $L_{\text{contour}}$ are computed only over the masked regions. $\lambda_1$ and $\lambda_2$ are weights that balance the two parts of the loss function, tailored to the specific requirements of the application.

提供了新的术语the rendered alpha mask，

The optimization objective can be formulated as:

$$
\min_{\mathbf{q}_{cw}, \mathbf{t}_{cw}} L + \lambda_q \|\mathbf{q}_{cw}\|_2^2 + \lambda_t \|\mathbf{t}_{cw}\|_2^2
$$

where $\lambda_q$ and $\lambda_t$ are regularization terms for the quaternion and translation parameters, respectively.

额外上下文参考包裹边界###
This is an L1 loss on both the depth and color renders, with color weighted down by half. The color weighting is empirically selected, where we observe the range of C(p) to be [0.01, 0.03] & D(p) to be [0.002, 0.006]. We only apply the loss over pixels that are rendered from well-optimized parts of the map by using our rendered visibility silhouette which captures the epistemic uncertainty of the map. This is very important for tracking new camera poses, as often new frames contain new information that hasn’t been captured or well optimized in our map yet. The L1 loss also gives a value of 0 if there is no ground-truth depth for a pixel.

额外上下文参考包裹边界###这段参考文章的描述，可以体现，需要对一些系数进行介绍，以及类似于这个别人文章的方法silhouette，我这里是the rendered alpha mask在优化过程中的重要性也要展开解释，公式可以根据内容变化而更改

这部分是真实的我写的部分，
**Optimization**: We employ the Adam optimizer for both quaternion and translation optimization, with distinct learning rates and weight decay values for each. The learning rates are set to $5 \times 10^{-4}$ for quaternion optimization and $10^{-3}$ for translation optimization, based on empirical results. The weight decay values are set to $10^{-3}$ for both quaternion and translation parameters, serving as regularization to mitigate overfitting.
这部分是真实的我写的部分，

## Pipeline

注意，术语reprojection应该都换成render比较专业合适主流

The GSplatLoc method streamlines the localization process by utilizing only posed reference depth images $\{D_k\}$ and a query depth image $D_q$. Its differentiability in rendering of 3D Gaussians facilitates efficient and smooth convergence during optimization.

**3D structure**: For evaluation consistency, we initialize 3D Gaussians from point clouds projected by $\{D_k\}$. Each point corresponds to a Gaussian's mean $\boldsymbol{\mu}_i$. After outlier filtering, we set opacity $o_i = 1$ for all Gaussians. The scale $\mathbf{s}_i \in \mathbb{R}^3$ is initialized based on local point density:

$$\mathbf{s}_i = (\sigma_i, \sigma_i, \sigma_i), \text{ where } \sigma_i = \sqrt{\frac{1}{3}\sum_{j=1}^3 d_{ij}^2}$$

Here, $d_{ij}$ denotes the distance to the $j$-th nearest neighbor of point $i$, calculated using k-nearest neighbors $(k=4)$. This isotropic initialization ensures balanced representation of local geometry. We initially set rotation $\mathbf{q}_i = (1, 0, 0, 0)$ for all Gaussians.

To enhance optimization stability and achieve superior final results, we apply standard Principal Component Analysis (PCA) for principal axis alignment of the point cloud, even for pre-existing scenes. This process involves centering the point cloud at its mean and aligning its principal axes with the coordinate axes. The PCA-based alignment normalizes the overall scene orientation, providing a more uniform starting point for optimization across diverse datasets.

This approach significantly improves the stability of loss reduction during optimization and facilitates the achievement of lower final loss values. By aligning the scene's principal components with the coordinate system, we create a more consistent representation that enables the optimization process to focus on refining local details rather than grappling with global orientation discrepancies. This is particularly advantageous for scenes with pronounced directional features or elongated structures, as it aids the optimization process in more effectively capturing and refining the underlying geometry.这里对pca的预处理有些冗余并且不准确，我采用pca的原因是因为在姿态优化过程中深度损失会更加的稳定并且下降的下限更大，然后你可以介绍他的一些优点，但重点不是3d场景表示

这里应该提供关于优化的更多的细节，采用的是阿丹优化器，并且迭代的具体过程时间依赖于rendering的过程，但是由于3D Gaussian Splatting for Real-Time Radiance Field Rendering优点就是可以实时的渲染的，所以渲染速度几乎就是优化器每次迭代的速度，因此优化过程会非常快
**Optimization**: We employ the Adam optimizer for both quaternion and translation optimization, with distinct learning rates and weight decay values for each.

**Convergence**: To determine the convergence of the optimization process, we implement an early stopping mechanism based on the stabilization of the total loss. Extensive experimental results indicate that the total loss typically stabilizes after approximately 100 iterations. We employ a patience mechanism, activated after 100 iterations. If the total loss fails to decrease for a consecutive number of patience iterations, the optimization loop is terminated. The pose estimate corresponding to the minimum total loss is subsequently selected as the optimal pose.


# Experiments


We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.

# Conclusion


We present GSplatLoc, an innovative pose estimation method for RGB-D cameras that employs a volumetric representation of 3D Gaussians. This approach facilitates precise pose estimation by minimizing the loss based on the reprojection of 3D Gaussians from real depth maps captured from the estimated pose. Our method attains rotational errors close to zero and translational errors within 0.01mm, representing a substantial advancement in pose accuracy over existing point cloud registration algorithms, as well as explicit volumetric and implicit neural representation-based SLAM methods. Comprehensive evaluations demonstrate that GSplatLoc significantly improves pose estimation accuracy, which contributes to increased robustness and fidelity in real-time 3D scene reconstruction, setting a new standard for localization techniques in dense mapping SLAM.