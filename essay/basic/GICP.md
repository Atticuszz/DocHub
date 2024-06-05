### 残差函数的定义
给定：
- $\mathbf{p}_{\text{target}}$ 为目标点云中的点。
- $\mathbf{p}_{\text{source}}$ 为源点云中经过变换 $T$ 的点。
- $\mathbf{r}$ 为残差向量 $\mathbf{r} = \mathbf{p}_{\text{target}} - T \mathbf{p}_{\text{source}}$。
-  $RCR$（Rotated Combined Covariance）为误差变换的协方差矩阵$\begin{aligned}\text{di} & \sim\mathcal{N}{\left(\hat{b}_{i}-\mathbf{T}\hat{a}_{i},C_{i}^{B}+\mathbf{T}C_{i}^{A}\mathbf{T}^{T}\right)}\\  & =\mathcal{N}\left(0,C_{i}^{B}+\mathbf{T}C_{i}^{A}\mathbf{T}^{T}\right)\end{aligned}$，这个矩阵反映了点云的不确定性和形状信息。*RCR取3x3,否则没有逆，而且只有3x3和xyz有关*
$$
RCR = \text{cov}_{\text{target}} + T \cdot \text{cov}_{\text{source}} \cdot T^T
$$
残差函数 $E$ 可以表示为：
$$
E = \frac{1}{2} \mathbf{r}^T RCR^{-1} \mathbf{r}
$$
这个公式计算了考虑协方巨矩阵后的点之间的加权欧氏距离，反映了点云之间的几何误差。
#### 为什么有1/2
在优化理论和应用中，通常在定义二次形式的误差函数时会包含一个系数 $\frac{1}{2}$。
当对误差函数进行微分求导时，系数 $\frac{1}{2}$ 可以帮助取消在导数计算中出现的常数因子。具体来说，考虑一个一般的二次函数形式：
$$
f(\mathbf{x}) = \frac{1}{2} \mathbf{x}^T A \mathbf{x} + \mathbf{b}^T \mathbf{x} + c
$$
当我们对这个函数求导以找到其梯度时：
$$
\nabla f(\mathbf{x}) = A \mathbf{x} + \mathbf{b}
$$
如果没有前面的 $\frac{1}{2}$，导数将会包含额外的常数因子 2（来自于 $A \mathbf{x}$ 的导数），这会使最终的表达式更加复杂。

### 求解雅可比矩阵 $J$
*也可以采用自动微分工具*
为了求解雅可比矩阵，我们需要计算残差 $\mathbf{r}$ 对变换 $T$ 的微分。由于 $T$ 是一个刚体变换，包含旋转 $R$ 和平移 $\mathbf{t}$，我们考虑旋转的无穷小变化 $\delta \theta$ 和平移的无穷小变化 $\delta \mathbf{t}$。


#### 1. 对旋转的偏导数

对于旋转部分，假设变换 $T$ 将点 $\mathbf{p}_{\text{source}}$ 通过旋转 $R$ 和平移 $\mathbf{t}$ 变换到 $\mathbf{p}_{\text{transformed}}$：

$$
\mathbf{p}_{\text{transformed}} = R \mathbf{p}_{\text{source}} + \mathbf{t}
$$

残差 $\mathbf{r}$ 是目标点 $\mathbf{p}_{\text{target}}$ 与变换后的点 $\mathbf{p}_{\text{transformed}}$ 的差：

$$
\mathbf{r} = \mathbf{p}_{\text{target}} - (R \mathbf{p}_{\text{source}} + \mathbf{t})
$$

旋转矩阵 $R$ 对应的无穷小变化可以通过旋转向量 $\delta \boldsymbol{\theta}$ 表示，这个向量通过斜对称矩阵 $\text{skew}(\delta \boldsymbol{\theta})$ 进行表达。这里的斜对称矩阵 $\text{skew}(\mathbf{v})$ 对于任何向量 $\mathbf{v}$ 定义为：
$$
\text{skew}(\mathbf{v}) = \begin{bmatrix}
0 & -v_z & v_y \\
v_z & 0 & -v_x \\
-v_y & v_x & 0
\end{bmatrix}
$$
这个矩阵的特点是它可以表示向量 $\mathbf{v}$ 和任意其他向量 $\mathbf{u}$ 的叉乘，即：
$$
\text{skew}(\mathbf{v}) \mathbf{u} = \mathbf{v} \times \mathbf{u}
$$

当旋转矩阵 $R$ 应用一个无穷小旋转 $\delta \boldsymbol{\theta}$，旋转矩阵的变化可以表示为：
$$
\delta R = R \cdot \text{skew}(\delta \boldsymbol{\theta})
$$
这表示旋转的变化直接通过 $\delta \boldsymbol{\theta}$ 的斜对称矩阵进行线性近似。
当我们考虑旋转变化 $\delta R$ 对点 $\mathbf{p}_{\text{source}}$ 的影响时，位置的变化由下式给出：
$$
\delta \mathbf{p}_{\text{transformed}} = \delta R \cdot \mathbf{p}_{\text{source}} = R \cdot \text{skew}(\delta \boldsymbol{\theta}) \cdot \mathbf{p}_{\text{source}}
$$
使用向量叉乘的性质，上式可以重写为：
$$
\delta \mathbf{p}_{\text{transformed}} = R \cdot (\delta \boldsymbol{\theta} \times \mathbf{p}_{\text{source}})
$$
根据叉乘的反对称性，这可以重新表达为：
$$
\delta \mathbf{p}_{\text{transformed}} = -R \cdot \text{skew}(\mathbf{p}_{\text{source}}) \cdot \delta \boldsymbol{\theta}
$$

因此，对旋转向量 $\boldsymbol{\theta}$ 的偏导数是：

$$
\frac{\partial \mathbf{r}}{\partial \boldsymbol{\theta}} = -R \cdot \text{skew}(\mathbf{p}_{\text{source}})
$$

这里，使用 $\text{skew}(\mathbf{p}_{\text{source}})$ 是为了直接将旋转向量 $\boldsymbol{\theta}$ 的影响通过 $\mathbf{p}_{\text{source}}$ 转换为残差 $\mathbf{r}$ 的变化。这个变换充分利用了叉乘和斜对称矩阵的性质来简化表达和计算,这体现了李代数的核心应用，即利用向量的叉乘来模拟旋转的微小变化。

#### 2. 对平移的偏导数

对平移向量 $\mathbf{t}$ 的影响相对更直接。考虑 $\mathbf{t}$ 的微小变化 $\delta \mathbf{t}$，对 $\mathbf{p}_{\text{transformed}}$ 的影响是直接的加和：

$$
\delta \mathbf{p}_{\text{transformed}} = \delta \mathbf{t}
$$

残差 $\mathbf{r}$ 对 $\mathbf{t}$ 的偏导数是：

$$
\frac{\partial \mathbf{r}}{\partial \mathbf{t}} = -I
$$

因为 $\delta \mathbf{t}$ 直接从 $\mathbf{p}_{\text{transformed}}$ 减去，表明每个分量的独立线性影响。

因此，雅可比矩阵 $J$ 形式为：
$$
J = \begin{bmatrix}
-R \cdot \text{skew}(\mathbf{p}_{\text{source}}) & -I
\end{bmatrix}
$$

### 线性化矩阵的计算

雅可比矩阵 $J$ 计算后，可以利用它来构建信息矩阵 $H$ 和信息向量 $b$：
$$
H = J^T M J, \quad b = J^T M \mathbf{r}
$$
这里，$M$ 作为一个系数矩阵，是从马氏距离定义中得到的，它与变换 $T$ 无关，因此可以在求导过程后作为一个常量系数处理。
#### 为什么 $M$ 在中间

$M$ 在 $J^T$ 和 $J$ 之间的位置可以这样理解：$J$ 转置 $J^T$ 表示可能的方向变化，而 $J$ 代表了这些变化如何影响最终的输出。将 $M$ 置于中间，意味着在计算方向变化对输出的影响之前，先对这些变化进行“加权”处理，这反映了不同方向上的变化对总体目标函数的影响不是均匀的，而是依赖于点之间关系的复杂性（如协方差结构）。





```python

import torch
from torch import nn

def skew_symmetric(v):
    """ 生成向量 v 的斜对称矩阵 """
    zero = torch.zeros_like(v[0])
    return torch.tensor([
        [zero, -v[2], v[1]],
        [v[2], zero, -v[0]],
        [-v[1], v[0], zero]
    ], dtype=v.dtype, device=v.device)

class GICPJacobian(nn.Module):
    def __init__(self):
        super(GICPJacobian, self).__init__()

    def forward(self, source_points, target_points, source_covariances, target_covariances, T):
        """ 计算雅可比矩阵
        :param source_points: 源点云 [N, 3]
        :param target_points: 目标点云 [N, 3]
        :param source_covariances: 源点云的协方巧矩阵 [N, 3, 3]
        :param target_covariances: 目标点云的协方巧矩阵 [N, 3, 3]
        :param T: 变换矩阵 [4, 4]
        :return: J 雅可比矩阵 [N, 6], 加权残差 [N, 3]
        """
        # 变换源点云
        ones = torch.ones((source_points.shape[0], 1), device=source_points.device, dtype=source_points.dtype)
        homogeneous_source = torch.cat([source_points, ones], dim=1)  # [N, 4]
        transformed_sources = (T @ homogeneous_source.T).T[:, :3]  # [N, 3]

        # 计算残差
        residuals = target_points - transformed_sources  # [N, 3]

        # 计算残差的加权
        weighted_residuals = torch.zeros_like(residuals)
        J = torch.zeros((source_points.shape[0], 6), dtype=source_points.dtype, device=source_points.device)
        for i in range(source_points.shape[0]):
            RCR = target_covariances[i] + T[:3, :3] @ source_covariances[i] @ T[:3, :3].T
            mahalanobis_weight = RCR.inverse()
            weighted_residuals[i] = mahalanobis_weight @ residuals[i]

            J[i, :3] = skew_symmetric(transformed_sources[i]) @ residuals[i]
            J[i, 3:] = -residuals[i]

        return J, weighted_residuals

# 示例使用
source_points = torch.rand(10, 3)  # 随机生成源点云
target_points = torch.rand(10, 3)  # 随机生成目标点云
source_covariances = torch.stack([torch.eye(3) for _ in range(10)])  # 源点协方巧矩阵
target_covariances = torch.stack([torch.eye(3) for _ in range(10)])  # 目标点协方巧矩阵
T = torch.eye(4)  # 单位变换矩阵

jacobian_module = GICPJacobian()
jacobian, weighted_residuals = jacobian_module(source_points, target_points, source_covariances, target_covariances, T)
print("雅可比矩阵:", jacobian)
print("加权残差:", weighted_residuals)
```

### 实验方法
**主要基于torchmize**
#### 雅可比矩阵是否提供 
1. 提供雅可比矩阵模仿small_gicp
2. 直接使用`pytorch`的雅可比矩阵，自动追踪梯度
#### 优化策略
1. 模仿纯的优化目标数学公式，一群对一群进行优化取均值error判断是否收敛
2. 模仿small_gicp的模式，每次每次只对`src_pcd`的一个点进行，单个error判断是否收敛，遍历所有`src_pcd`
#### 验证策略
1. 粗看轨迹和pcd_vis可视化效果
2. 细看四个基本误差