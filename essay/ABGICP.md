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
The final array, `points`, is reshaped to \((-1, 4)\) to flatten the point cloud into a two-dimensional array where each row represents a 3D point in homogeneous coordinates.
### point cloud rejector via image filter

1. 双边滤波（Bilateral Filter）：既保证能够出去离群值也能够保证不太影响图像边缘

```python
import cv2
image = cv2.imread('path_to_image')
filtered_image = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
```

其中，`d` 是领域直径，`sigmaColor` 控制颜色的高斯函数标准差，`sigmaSpace` 控制空间的高斯函数标准差。
2. 中值滤波: 但可能对边缘部分的离群值处理不太好，并且是用于减少噪声，特别是“椒盐”类型的噪声，但不清楚会不会引入
```c++
cv::Mat depthImage; // 假设这是你的深度图
cv::medianBlur(depthImage, depthImage, 5); // 使用5x5的核进行滤波
```

没有太多的原创性，主要是应用层面迁移，从处理经典图像到深度图的适用，避免在pcd层面的rejector效率不高，毕竟是三维的，能在二维解决为什么要三维呢？并且也可以解决一小部分像素避免进行



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
Math:
1. points
   $p_i = (x_{p_i}, y_{p_i}, z_{p_i}, A_{p_i}, B_{p_i})$
   $q_i = (x_{q_i}, y_{q_i}, z_{q_i}, A_{q_i}, B_{q_i})$

2. Extended points including the AB component
   $$Lp_i = \begin{pmatrix} p_i \\ L_{p_i}^* \end{pmatrix}, \quad Lq_i = \begin{pmatrix} q_i \\ L_{q_i}^* \end{pmatrix}$$

3. Assuming the error $e_i$ is normally distributed, focusing only on the spatial and AB components:
   $$e_i = Lp_i - (TLq_i) \sim \mathcal{N}(0, C_{Lp_i} + TC_{Lq_i}T^T)$$

4. Define the loss function using Mahalanobis distance for spatial and AB components:
   $$d_i(T) = (Lp_i - (TLq_i))^T (C_{Lp_i} + TC_{Lq_i}T^T)^{-1} (Lp_i - (TLq_i))$$

5. Objective function and MLE are then defined as:
   $$T^* = \arg \min_T \sum_{i=1}^n d_i(T)$$

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

#### point cloud rejector via image filter

**experiment data**
-  需要手动生成离群值，在干净数据集上面进行模拟因为可以验证离群处理的效果

[@guptaNDT6DColor2023] 该论文也是RGB-D相机但是直接在点云层面上进行预处理
```c++
import pclpy
from pclpy import pcl

def pc_filter(pointcloud, cloud_filtered):
    # Create temporary PointClouds
    temp = pcl.PointCloud.PointXYZRGBA()
    temp2 = pcl.PointCloud.PointXYZRGBA()

    # Distance based filter
    passthrough = pcl.filters.PassThrough[pcl.PointXYZRGBA]()
    passthrough.setInputCloud(pointcloud)
    passthrough.setFilterFieldName("z")
    passthrough.setFilterLimits(0.0, 3.0)
    passthrough.filter(temp)

    # Voxel grid filter
    voxel_filter = pcl.filters.VoxelGrid[pcl.PointXYZRGBA]()
    voxel_filter.setInputCloud(temp)
    voxel_filter.setLeafSize(0.005, 0.005, 0.005)
    voxel_filter.filter(temp2)

    # Radius outlier removal
    out_rem = pcl.filters.RadiusOutlierRemoval[pcl.PointXYZRGBA]()
    out_rem.setInputCloud(temp2)
    out_rem.setRadiusSearch(0.01)
    out_rem.setMinNeighborsInRadius(10)
    out_rem.filter(cloud_filtered)

# Example usage
pointcloud = pcl.PointCloud.PointXYZRGBA()
cloud_filtered = pcl.PointCloud.PointXYZRGBA()
pc_filter(pointcloud, cloud_filtered)

```


**evaluation**
- 该滤波方法生成点云时候和标准rejector生成的点云进行比较
	- 同时和干净点云进行配准，评估 *配准精度*和 *运算帧率* 的影响

### registration
**experiment data**
- 偶数个RGB图像，按比例放大数值，代表光线增强
**evaluation** 
1. [Colored point cloud registration - Open3D 0.18.0 documentation](https://www.open3d.org/docs/release/tutorial/pipelines/colored_pointcloud_registration.html)和open3d的`colored_pointcloud_registration`方法系列进行比较精度，实现的是该论文的方法[@parkColoredPointCloud2017]，是`RGB`空间
2. [Point Cloud Library (PCL): pcl::GeneralizedIterativeClosestPoint6D Class Reference](https://pointclouds.org/documentation/classpcl_1_1_generalized_iterative_closest_point6_d.html)这应该是*对标的方案*[@kornColorSupportedGeneralizedICP2014a],是这篇文章的实现，`LAB`空间额外的约束`GICP`算法
*从配准精度的角度计算时间角度考虑*
## 5. Results & Discussion
