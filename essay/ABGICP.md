## Abstract
为GICP增加约束，并且去除LAB的L分量，减少光照影响
## 1. Introduction

## 2. Related Work

## 3. Method
### pixel to point cloud
最基本的图像变换点云，对于RGB图像只是深度值变成了$\begin{bmatrix} r & g & b \end{bmatrix}^\top$

Variables:
- $u, v$: Pixel coordinates in the image plane.
- $c_x, c_y$: Coordinates of the principal point (optical center) in the image, typically given in pixels.
- $f_x, f_y$: Focal lengths of the camera in the $x$ and $y$ directions, respectively, typically given in pixels.
- $d$: Depth value at the pixel $(u, v)$ after scaling, given in meters.
- $I_d(u, v)$: Depth value from the *original depth image* at pixel $(u, v)$, typically given in the units used by the depth sensor.
- $s$: Scale factor to convert the depth values from the depth image units to meters.
- $\mathbf{p}$ : 3D point in *camera coordinates*, represented as a vector $\begin{bmatrix} x & y & z \end{bmatrix}^\top$ or $\begin{bmatrix} x & y & z & 1 \end{bmatrix}^\top$

$$
\mathbf{p} = \begin{bmatrix} \frac{u - c_x}{f_x} d \\ \frac{v - c_y}{f_y} d \\ d \end{bmatrix}, \quad d = \frac{I_d(u, v)}{s}
$$


5. **Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
$$
\text{points} = \begin{bmatrix} X & Y & Z & 1 \end{bmatrix}
$$
The final array, `points`, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.




### ABGICP
**核心算法**
1. 去除L分量，给定光源的情况下，尤其是室外，在不同角度下，同一个物体表面的彩色值是不一样的，可能会变成错误的噪音提供了错误的配准信息，使得算法收敛速度慢，或者求解不正确等等
2. 现有方法[@kornColorSupportedGeneralizedICP2014a] 采用的是对`LAB`数值使用一个比例参数$α$，协调`LAB`分量对于整个优化过程提供的影响程度，有点机械化，该论文使用了一系列的比例对齐技术，**椭圆正则化**[@haRGBDGSICPSLAM2024]

> gicp部分还没有进行比例对齐
#### BGR->LAB
_RGB->LAB转换过程包括了颜色空间的转换和非线性的调整，以适应人眼对亮度的非线性感知_

```python
import cv2
# Load an image in BGR color space
image = cv2.imread('path_to_your_image.png')
lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
```
#### GICP
在您的要求中，您需要将原始的公式和定义重新整理和格式化，以适应您的笔记风格。这里我将调整原有内容的表达方式，使其更符合您的要求：

### 数学公式和定义

1. **点的定义**：
   - 两个点云 $P$ 和 $Q$ 中的点包括空间坐标和颜色信息，定义如下：
     $$p_i = (x_{p_i}, y_{p_i}, z_{p_i}, L_{p_i}, a_{p_i}, b_{p_i})$$
     $$q_i = (x_{q_i}, y_{q_i}, z_{q_i}, L_{q_i}, a_{q_i}, b_{q_i})$$

2. **GICP 几何误差** ($E_{geom}$)：
   - 通过 $Mahalanobis$ 距离计算每个点的局部几何结构误差，具体公式为：
     $$E_{geom}(T) = \sum_{i=1}^n \left(s(p_i, T) - q_i\right)^T C_{q_i}^{-1} \left(s(p_i, T) - q_i\right)$$
   - 这里 $s(p_i, T)$ 表示在变换 $T$ 下点 $p_i$ 的位置，$C_{q_i}$ 是点 $q_i$ 的协方巧矩阵。

 3. **颜色误差** $E_{color}$：
   - 在 L\*a\*b\* 空间中，颜色差异使用 CIEDE2000 方法计算：
     $$E_{color}(T) = \sum_{i=1}^n \Delta E_{00}(L_{p_i}, a_{p_i}, b_{p_i}, L_{q_i}(T), a_{q_i}(T), b_{q_i}(T))$$
   - 这里 $L_{q_i}(T)$, $a_{q_i}(T)$, $b_{q_i}(T)$ 分别代表在变换 $T$ 下的点 $q_i$ 的颜色分量。
4. **联合优化目标函数**：
   - 几何误差和颜色误差的组合，通过权重 $\alpha$ 和 $\beta$ 调节在总优化目标中的影响：
     $$E(T) = \alpha E_{geom}(T) + \beta E_{color}(T)$$
   - 其中，$\alpha$ 和 $\beta$ 用来平衡几何和颜色误差的重要性。
> [!idea]
> 既然是rgb-d的环境下，也许可以增加对齐后的点云变换回深度图像，确保对齐后的点云符合深度图的损失,[[essay/zotero/attachments/SplaTAM.pdf#page=7&selection=172,0,221,44|SplaTAM, page 7]]
### 优化过程

优化过程通常采用迭代的方式，例如梯度下降法或更复杂的 $Levenberg-Marquardt$算法，以处理非线性最小化问题。这里我们展示使用梯度下降法的步骤：

1. **初始化**：选择一个初始变换  $T_0$。
2. **迭代更新**：在每次迭代  $k$ 中，计算总目标函数  $E(T_k)$ 的梯度，并更新变换  $T$。
   - 使用梯度下降法更新：
     $$T_{k+1} = T_k - \gamma \nabla E(T_k)$$
     其中  $\gamma$ 是学习率， $\nabla E(T_k)$ 是在  $T_k$ 处  $E(T)$ 的梯度。

### 梯度计算

- **几何梯度** $\nabla E_{geom}(T)$：
  $$\nabla E_{geom}(T) = \sum_{i=1}^n 2 C_{q_i}^{-1} \left(s(p_i, T) - q_i\right) \cdot \frac{\partial s(p_i, T)}{\partial T}$$

- **颜色梯度** $\nabla E_{color}(T)$：
  $$\nabla E_{color}(T) = \sum_{i=1}^n \frac{(L_{p_i} - L_{q_i}(T)) \cdot \frac{\partial L_{q_i}(T)}{\partial T} + (a_{p_i} - a_{q_i}(T)) \cdot \frac{\partial a_{q_i}(T)}{\partial T} + (b_{p_i} - b_{q_i}(T)) \cdot \frac{\partial b_{q_i}(T)}{\partial T}}{\sqrt{(L_{p_i} - L_{q_i}(T))^2 + (a_{p_i} - a_{q_i}(T))^2 + (b_{p_i} - b_{q_i}(T))^2}}$$

这里， $\frac{\partial s(p_i, T)}{\partial T}$、 $\frac{\partial L_{q_i}(T)}{\partial T}$、 $\frac{\partial a_{q_i}(T)}{\partial T}$ 和  $\frac{\partial b_{q_i}(T)}{\partial T}$ 需要具体依据变换模型和颜色模型的细节来推导。

合并点云并使其成为可微分的过程可以通过对每个点的贡献进行加权平均来实现。这种方法不仅保持了操作的可微分性，而且还能够根据每个点云中的点的有效性（如深度大于零）来调整它们的权重。下面详细介绍这个数学过程：

### 基本原理

假设我们有两个点云 \( pcd_{\text{last}} \) 和 \( pcd_{\text{current}} \)，每个点云都是一个 \( H \times W \times 4 \) 的张量，其中 \( H \) 和 \( W \) 分别是高度和宽度，而 4 则代表每个点的 \( x, y, z, 1 \) 坐标。

1. **确定有效性（Valid Masks）**：
   - 对于每个点云，我们通过检查 \( z \) 坐标（即深度）是否大于零来确定一个点是否有效。
   - \( \text{valid\_last} = (pcd_{\text{last}}[..., 2] > 0).float() \)
   - \( \text{valid\_current} = (pcd_{\text{current}}[..., 2] > 0).float() \)
   - 这里，有效性被转换为浮点数，有效点为 1.0，无效点为 0.0。

2. **计算权重**：
   - 权重是基于每个点的有效性相对于两个点云中相同位置点的有效性之和来计算的。
   - \( \text{weights\_last} = \frac{\text{valid\_last}}{\text{valid\_last} + \text{valid\_current} + 1e-6} \)
   - \( \text{weights\_current} = \frac{\text{valid\_current}}{\text{valid\_last} + \text{valid\_current} + 1e-6} \)
   - 这里，\( 1e-6 \) 是一个小常数，用于防止除以零。

3. **加权平均合并点云**：
   - 使用计算出的权重，我们可以对每个点云的对应点进行加权，以合并成一个新的点云。
   - \( \text{merged\_pcd} = \text{weights\_last}.unsqueeze(-1) * pcd_{\text{last}} + \text{weights\_current}.unsqueeze(-1) * pcd_{\text{current}} \)
   - `.unsqueeze(-1)` 用于将权重张量的形状从 \( H \times W \) 扩展到 \( H \times W \times 1 \)，使其可以与每个点的四维坐标进行广播乘法。

### 可微分性

这个合并过程是完全可微分的，原因如下：
- **加权平均**：加权平均是一种线性操作，其梯度可以直接通过加权系数传递回权重和原始点云数据。
- **使用平滑的权重计算**：权重的计算涉及基本的算术操作和浮点除法，这些操作都是可微分的。
- **避免使用硬阈值决策**：通过使用加权平均而不是基于硬阈值（如取最大或最小）的决策，避免了梯度不连续性的问题。

这种方法的优势在于它不仅使过程可微分，而且还考虑了点云的空间一致性和每个点的贡献，从而提供了一种有效融合来自不同时间步或视角的深度信息的方法。
## 4. Experimental Setup

如果我的数据集是 meta 开源的 replica，我对与每相邻两张进行配准，从而研究我目前创新的配准算法在 rgbd 的特定的环境下的使用，无论是用来三维重建还是姿态估计，大多数使用 rgbd 相机的时候都是会移动，所以我选用 rgbd 数据集的相邻两帧作为配准 scantoscan 模式连续估计，并且为了避免误差的连续积累，并且我们关注于对两帧作为实验，上一帧姿态采用真实姿态，并且使用上一个真实变换 t 作为 t 的初始估计（但这个可能会影响收敛在大角度旋转的时候，需要额外验证），这种情况下我是关注于验证我的算法在两帧之间的效果，有点像升级视觉里程记的最小单位的估计姿态的精准度，而不是完整的轨迹估计，给我实验描述整理，专业名词用英语，中英结合，不要歪曲含义
### preprocess 

#### grid down sample for depth image 
**experiment data**
- 原生数据集，不修改的

**evaluation** 
1. 单纯[Point cloud - Open3D 0.18.0 documentation](https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html#Voxel-downsampling)`Voxel-downsampling`
2. 单纯image grid down sample
3. 混合两者

1. 配准都采用纯GICP算法情况下，*三者* 都可以比较 *配准精度*
2. 前两者在相同点云数情况下，应该是后者效率更高比较他们的*运算速度*，
3. 不出意外，实验证明，应该是混合两者运算 *效率和精度最高*

### registration
**experiment data**
- 偶数个RGB图像，按比例放大数值，代表光线增强
**evaluation** 
1. [Colored point cloud registration - Open3D 0.18.0 documentation](https://www.open3d.org/docs/release/tutorial/pipelines/colored_pointcloud_registration.html)和open3d的`colored_pointcloud_registration`方法系列进行比较精度，实现的是该论文的方法[@parkColoredPointCloud2017]，是`RGB`空间
2. [Point Cloud Library (PCL): pcl::GeneralizedIterativeClosestPoint6D Class Reference](https://pointclouds.org/documentation/classpcl_1_1_generalized_iterative_closest_point6_d.html)这应该是*对标的方案*[@kornColorSupportedGeneralizedICP2014a],是这篇文章的实现，`LAB`空间额外的约束`GICP`算法
*从配准精度的角度计算时间角度考虑*
## 5. Results & Discussion
