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
### grid down sample for depth image 
优点:
不会引入噪声也能够加速点云转换，因为直接转换点云计算量很大，频繁的创建数据
*随机降采样是个彻头彻尾的反例，因为引入了噪声，但这种规整的降采样就不会*
Variables:
- $i, j$: Pixel indices in the depth image.
- $D$: Original depth image.
- $S$: Scale factor to convert depth values from units to meters.
- $K$: Intrinsic camera matrix.
- $\text{downsample\_stride}$: Stride used for down sampling the image and depth values.
1. **Generate pixel indices for the entire depth image:**
$$
(i, j) = \text{np.indices}(D.shape)
$$

2. **Downsampling by taking every nth pixel determined by the downsample_stride:**
$$
i = i[::\text{downsample\_stride}, ::\text{downsample\_stride}], \quad j = j[::\text{downsample\_stride}, ::\text{downsample\_stride}]
$$
$$
D_{\text{downsampled}} = D[::\text{downsample\_stride}, ::\text{downsample\_stride}]
$$

3. **Scale depth values to meters:**
$$
Z = D_{\text{downsampled}} \cdot \frac{1}{S}
$$

4. **Calculate 3D coordinates in the camera coordinate system using the intrinsic parameters:**
- $x$ coordinate:
$$
X = (j - c_x) \cdot \frac{Z}{f_x}
$$
- $y$ coordinate:
$$
Y = (i - c_y) \cdot \frac{Z}{f_y}
$$

5. **Concatenate coordinates to form the 3D points with a homogeneous coordinate:**
$$
\text{points} = \begin{bmatrix} X & Y & Z & 1 \end{bmatrix}
$$
The final array, `points`, is reshaped to $(-1, 4)$ to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.



### point cloud rejector via image filter


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


## 4. Experimental Setup

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
