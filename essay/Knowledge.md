### image

_format in disk_

1. **JPEG（Joint Photographic Experts Group）**

- 采用有损压缩。
- 优点是可以在不显著降低视觉质量的情况下大幅减小文件大小，适用于存储照片。
- 缺点是重复保存和编辑会逐渐降低图像质量。

2. **PNG（Portable Network Graphics）**

- 采用无损压缩。
- 优点是保留原始图像的完整质量，支持透明度。
- 缺点是文件大小通常比JPEG大。

_format in RAM_

#### Image coordinate system

![300](../assets/Pasted_image_20240329151607.png)
图像坐标系中：

- **原点**（0, 0）位于图像的左上角。
- **X轴**的正方向是向右，表示图像的宽度（w)方向。
- **Y轴**的正方向是向下，表示图像的高度（h）方向。
  _reason_
  这种坐标系统选择主要是基于图像数据在计算机内存中的存储方式。在大多数图像处理库和图形界面系统中，图像数据是按行存储的，每行从左到右，行从上到下排列。因此，图像的第一个像素（位于左上角）对应于坐标（0, 0）。

#### color

1. channel first and RGB(red, green, blue)->pytorch,etc

```python
image.shape = (RGB,Height,Weight)
```

2. channel not first and BGR(blue,green,red) for opencv,etc

```python
image.shape = (Height,Weight,BGR)
```

- **normalize**

```python
image/255.
[0,255] -> [0,1.0]
```

#### depth

1. raw depth data from `.png` with shape(h,w)

```python
depth_image = cv2.imread('depth_image.png', cv2.IMREAD_GRAYSCALE)
```

2. expand_dims for `pytorch`

```python
depth_tensor.unsqueeze(0)
shape->(1,h,w)
```

### camera

> [cameras · PyTorch3D](https://pytorch3d.org/docs/cameras)

#### camera coordinate system

**相机坐标系**：
一个随相机位置和朝向改变的参考系。在相机坐标系中，原点位于相机的位置，通常Z轴与相机的视线方向对齐，X轴和Y轴分别与相机成横轴和纵轴对齐。
**世界坐标系**：
一个固定的、全局的参考系，通常用来描述场景中物体的位置。在这个坐标系下，每个物体的位置都是相对于一个固定点（世界原点）来定义的。

#### Intrinsic Matrix

**内参矩阵**
[Camera Intrinsic Matrix with Example in Python | by Neeraj Krishna | Towards Data Science](https://towardsdatascience.com/camera-intrinsic-matrix-with-example-in-python-d79bf2478c12)

- **`fx​`** 和 **`fy`​**：分别是相机在图像平面x轴和y轴方向上的焦距，用像素值表示。焦距反映了镜头对场景的放大程度。在理想情况下，对于方形像素，`fx​` 和 `fy`​ 应该是相同的，但由于镜头畸变和制造公差，它们可能略有不同。
- **`cx`​** 和 **`cy`​**：是图像的主点（principal point）坐标，也就是图像坐标系统原点在图像平面上的位置。通常，这个点被假定为图像的中心，但实际上可能会由于镜头制造和装配不精确而有所偏移。
  通常作为相机内参矩阵`K`
  $$\left.K=\left[\begin{array}{ccc}f_x&0&c_x\\0&f_y&c_y\\0&0&1\end{array}\right.\right]$$

#### Extrinsic Matrix

**外参矩阵**
[Camera Extrinsic Matrix with Example in Python | by Neeraj Krishna | Towards Data Science](https://towardsdatascience.com/camera-extrinsic-matrix-with-example-in-python-cfe80acab8dd)

- 描述了相机在全局空间（或称为世界坐标系）中的位置和方向。
  $$E_t=\begin{bmatrix}R&\mathbf{t}\end{bmatrix}$$
- **旋转（Rotation）**：通过`3x3`的旋转矩阵部分，可以围绕原点执行物体的旋转操作。旋转可以是绕`X`轴、`Y`轴或`Z`轴的单轴旋转，也可以是这些旋转的任意组合。
- **平移（Translation）**：通过`Tx`, `Ty`, `Tz`三个元素，可以将物体在三维空间中沿各个方向移动。
  > 在实践中，为了同时处理旋转和平移，我们通常使用`4x4`的齐次坐标变换矩阵。这允许我们通过单一的矩阵乘法来执行整个变换操作，从而简化了计算。

#### Homogeneous coordinate transformation matrix

**齐次坐标变换矩阵**
$$\mathbf{M}_{\mathrm{c2w}}=\begin{bmatrix}R&T\\0&1\end{bmatrix}$$

- **$R$（旋转矩阵）**：描述了相机坐标系的基向量（即相机的前向、上方和右侧方向）如何相对于世界坐标系进行旋转对齐。因此，$R$实际上定义了相机坐标系的朝向相对于世界坐标系的朝向。

- **$T$（平移向量）**：表示相机坐标系的原点（可以理解为相机的光心或中心）在世界坐标系中的位置。换言之，$T$描述了从世界坐标系的原点到相机坐标系原点（相机的位置）的直线距离和方向。

因此可以把相机坐标系中的任意一点转换为世界坐标系中的对应点，该过程包括将点首先通过$R$旋转到正确的朝向，然后通过$T$平移到正确的位置。

对于把$P_w$转化为 $P_c$，依赖于$\mathbf{M}_{\mathrm{w2c}}$,而且可以通过逆变换得到$\mathbf{M}_{\mathrm{w2c}}=\mathbf{M}_{\mathrm{c2w}}^{-1}$

> 轨迹文件`traj.txt`,每行是一个`4*4`的变换矩阵，变量名常作`c2w`

```text
R11 R12 R13 Tx
R21 R22 R23 Ty
R31 R32 R33 Tz
 0   0   0  1
```

$\mathbf{M}_{\mathrm{w2c}}$ 变量名常作`w2c`

#### Projection Transform Matrix

#### Coordinate transformation during imaging

**成像过程中的坐标变换**
![../../assets/Pasted_image_20240329152030.png](../assets/Pasted_image_20240329152030.png)
当我们讨论将三维世界坐标系中的点投影到二维图像平面时，需要进行坐标变换，包括：

1. **从世界坐标系到相机坐标系**：这一步使用齐次坐标形式的外参矩阵$\mathbf{M}_\mathrm{w2c}=\begin{bmatrix}R&T\\0&1\end{bmatrix}$，给定$P_w=(X_w,Y_w,Z_w,1)^T$ 变换$\begin{aligned}\mathbf{P}_c=(X_c,Y_c,Z_c)^T\end{aligned}$
   $$\mathbf{P}_c=\mathbf{M}_{\mathrm{w2c}}\cdot\mathbf{P}_w$$
2. **从相机坐标系到图像平面**：这一步使用内参矩阵$K$，将$\begin{aligned}\mathbf{P}_c=(X_c,Y_c,Z_c)^T\end{aligned}$投影到二维图像平面像素点$P_i=(u,v)$
   $$\mathbf{P}_i=\mathbf{K}\cdot\begin{bmatrix}X_c\\Y_c\\Z_c\end{bmatrix}/Z_c$$

### Point Cloud

#### pixel to Point cloud
$$
\mathbf{p} = \begin{bmatrix} \frac{u - c_x}{f_x} d \\ \frac{v - c_y}{f_y} d \\ d \end{bmatrix}, \quad d = \frac{I_d(u, v)}{s}
$$

#### estimate c2w

**估计相机坐标系到世界坐标系的姿态变换矩阵**

##### ICP(p2p)

_迭代最近点-point to point_
_数学模型_

- **目标函数**：
  - ICP 旨在最小化点云间的欧氏距离之和，通常通过解决最小二乘问题实现：
  - $$ \min*T \sum*{i=1}^N \| R p*i + \mathbf{t} - q*{\text{closest}(i)} \|^2 $$
- **求解方法**：
  - 使用 SVD (奇异值分解) 或其他数值方法求解 $R$ 和 $\mathbf{t}$。
    _算法流程_

1. **初始化**：
   - 设定初始变换$T^{(0)}$。若无先验信息，则 $T^{(0)} = I$（单位矩阵）
2. **最近点搜索**：
   - 对于源点云 $\mathbf{P}$ 中的每个点 $p_i$，找到目标点云$\mathbf{Q}$ 中最近的点 $q_j$。
   - $$ \forall p*i \in \mathbf{P}, \quad q*{\text{closest}} = \arg \min\_{q_j \in \mathbf{Q}} \| p_i - q_j \|^2 $$
3. **变换矩阵求解**：
   - 计算最优变换 $T$ 以最小化配准误差：
   - $$ T^{(k+1)} = \arg \min*T \sum*{i=1}^N \| T p*i - q*{\text{closest}(i)} \|^2 $$
   - 其中$T$ 包含旋转$R$ 和平移$\mathbf{t}$。
4. **迭代更新**：
   - 应用变换 $T^{(k+1)}$ 更新点云 $\mathbf{P}$：
   - $$ \mathbf{P}^{(k+1)} = T^{(k+1)} \mathbf{P}^{(k)} $$
   - 重复步骤2-3，直到满足收敛条件（如迭代次数、变换更新阈值等）。

##### GICP

**GICP (Generalized Iterative Closest Point) 算法** 是一种改进的迭代最近点算法，通过分布到分布的比对来增强点云的匹配精度。它主要用于三维空间中的点云数据对齐。下面是GICP算法的数学表达和详细解释：

#### 数学表达

1. **点的高斯表示**：
   每个点不仅表示为一个位置向量，而是一个带有高斯分布的模型。这意味着，源点云中的每个点$a_i$ 和目标点云中的每个点 $b_i$ 均关联一个高斯分布，其均值分别为 $\hat{a}_i$ 和 $\hat{b}_i$，协方差分别为 $C_{A_i}$ 和 $C_{B_i}$。
   $$
   a_i \sim \mathcal{N}(\hat{a}_i, C_{A_i}), \quad b_i \sim \mathcal{N}(\hat{b}_i, C_{B_i})
   $$
2. **变换误差的定义**：
   定义从 $a_i$ 到 $b_i$ 的变换误差为$hat{d}_i$：

   $$
   \hat{d}_i = \hat{b}_i - T\hat{a}_i
   $$

   其中 $T$ 是待优化的变换矩阵。

3. **误差的高斯分布**：
   误差 $d_i$ 也假设为高斯分布，利用高斯分布的性质，变换后的点的误差分布为：

   $$
   d_i \sim \mathcal{N}(0, C_{B_i} + T C_{A_i} T^T)
   $$

   这里的 $C_{B_i} + T C_{A_i} T^T$ 表示考虑到源点和目标点协方差的变换点的协方差。

4. **优化目标**：
   GICP 的目标是找到变换 $T$，使得转换后的源点云在目标点云分布下的似然性最大化，等同于最小化马氏距离：
   $$
   T = \arg \min_T \sum_i d_i^T (C_{B_i} + T C_{A_i} T^T)^{-1} d_i
   $$
5. **协方差的规范化**：
   为了提高GICP的鲁棒性和避免退化解，通常会对协方差矩阵进行规范化处理。通常在协方差矩阵的对角线元素上添加一个小常数 \(\epsilon\) 来确保它们是良态的。

### mapping

#### build heat_map and binary_map

**生成热度和二值化地图**

##### 1. 点云数据转换

- **原始数据**：
  - 输入的点云数据通常是一个`Nx3`的NumPy数组，每行表示一个点的世界坐标（X, Y, Z）。
- **坐标变换**：
  - 为了将点云数据映射到二维地图上，需要忽略Z坐标，并将X和Y坐标转换为地图的像素索引。
  - 转换公式为：
    $$
    \text{index}_x = \left(\frac{X}{\text{resolution}} + \text{origin}_x\right) \text{（取整）}
    $$
    $$
    \text{index}_y = \left(\frac{Y}{\text{resolution}} + \text{origin}_y\right) \text{（取整）}
    $$
    其中，$\text{resolution}$ 是地图的分辨率，$\text{origin}_x$ 和 $\text{origin}_y$ 是地图原点在地图像素坐标中的位置。

##### 2. 热度图构建

- **热度更新**：
  - 使用累加的方式更新地图上对应像素的值，每当一个点被映射到某个像素时，该像素的值增加1。
  - 这样可以得到每个像素被点云中的点覆盖的次数，从而生成热度图。
- **数学表达**：
  - 对于每个有效的点索引$(i, j)$，执行更新操作：
    $$
    \text{heat\_map}[i, j] += 1
    $$

##### 3. 二维占用网格的构建

- **阈值处理**：
  - 根据设定的阈值（$\text{occupancy\_threshold}$），将热度图转换成二维占用网格。
  - 如果某个像素的热度值小于阈值，则该像素标记为可通行（0），否则标记为障碍（1）。
- **转换公式**：
  $$
  \text{binary\_map} = \begin{cases}
    0, & \text{if }\text{heat\_map}[i, j] < \text{occupancy\_threshold} \\
    1, & \text{otherwise}
  \end{cases}
  $$
