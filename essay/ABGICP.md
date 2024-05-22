## Abstract
为GICP增加约束，并且去除LAB的L分量，减少光照影响
## 1. Introduction

## 2. Related Work

## 3. Method

### definition

#### RGB to L\*

##### normalize RGB

$$R^{\prime},G^{\prime},B^{\prime}=\frac R{255},\frac G{255},\frac B{255}$$

##### SRGB

$$C_{linear}=\begin{cases}\frac{C^{\prime}}{12.92}&\text{if }C^{\prime}\leq0.04045\\\left(\frac{C^{\prime}+0.055}{1.055}\right)^{2.4}&\text{otherwise}\end{cases}$$
_$C$ may be $R,G,B$_

##### sRGB到XYZ

$$\begin{bmatrix}X\\Y\\Z\end{bmatrix}=\begin{bmatrix}0.4124564&0.3575761&0.1804375\\0.2126729&0.7151522&0.0721750\\0.0193339&0.1191920&0.9503041\end{bmatrix}\begin{bmatrix}R_{linear}\\G_{linear}\\B_{linear}\end{bmatrix}$$

##### XYZ to LAB

归一化XYZ值相对于参考白点D65（假设使用D65，这是最常用的标准光源）
$$X_n,Y_n,Z_n=\frac X{95.047},\frac Y{100.000},\frac Z{108.883}$$
其中95.047, 100.000, 108.883是D65光源下的XYZ参考值。

$$f(t)=\begin{cases}t^{1/3}&\text{if }t>0.008856\\7.787t+\frac{16}{116}&\text{otherwise}\end{cases}$$

$$L^*=116f(Y_n)-16$$
_这个转换过程包括了颜色空间的转换和非线性的调整，以适应人眼对亮度的非线性感知_

#### point

1. $p_i=(x_{p_i},y_{p_i},z_{p_i},R_{p_i},G_{p_i},B_{p_i})$
2. $q_i=(x_{q_i},y_{q_i},z_{q_i},R_{q_i},G_{q_i},B_{q_i})$

$$Lp_i=\begin{pmatrix}p_i\\L_{p_i}^*\end{pmatrix},\quad Lq_i=\begin{pmatrix}q_i\\L_{q_i}^*\end{pmatrix}$$

### solution

**假设误差 $𝑒𝑖$ 是正态分布的**
$$e_i=Lp_i-(TLq_i)\sim\mathcal{N}(0,C_{Lp_i}+TC_{Lq_i}T^T)$$

**定义损失函数马氏距离**
$$d_i(T)=(Lp_i-(TLq_i))^T(C_{Lp_i}+TC_{Lq_i}T^T)^{-1}(Lp_i-(TLq_i))$$

**目标函数和MLE**

$$T^*=\arg\min_T\sum_{i=1}^nd_i(T)$$

## 4. Experimental Setup
> 引入颜色可能要要证明光线强度不会造成影响，手动生成数据集
### preproccess 
#### grid down sample for depth image 
优点:
不会引入噪声也能够加速点云转换，因为直接转换点云计算量很大，频繁的创建数据，
Variables:
- $i, j$: Pixel indices in the depth image.
- $D$: Original depth image.
- $S$: Scale factor to convert depth values from units to meters.
- $K$: Intrinsic camera matrix.
- $\text{downsample\_stride}$: Stride used for down sampling the image and depth values.

Mathematical Formulation:

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


## 5. Results & Discussion
