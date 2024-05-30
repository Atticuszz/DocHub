## optimization

**目标函数**: 目标函数（或称为损失函数）是一个标量，它度量整个模型的预测值与观测值之间的差异。在优化问题中，目标函数通常是所有残差的某种汇总（如总和、平均值或其他统计度量），用于评估模型的整体拟合程度。


在优化和数据拟合问题中，**残差向量**和**目标函数**是两个关键的概念，它们虽然密切相关但有本质的区别：

1. **残差向量**: 残差向量通常指的是单一观测值与模型预测值之间的差异。在点云配准的上下文中，如果我们考虑每个点对之间的差异，残差向量可以具体表示为点$p_i$在变换$T$下的位置$s(p_i, T)$与其目标匹配点$q_i$之间的差异向量。

   对于**几何残差向量**：
  $$
   r_{G}^{(i)}(T) = s(p_i, T) - q_i
  $$
   这里$s(p_i, T)$表示点$p_i$在变换$T$下的位置，$q_i$是其匹配点的位置。

   对于**光度残差向量**（如果存在颜色信息的话）：
  $$
   r_{C}^{(i)}(T) = C_p(f(s(p_i, T))) - C_q(q_i)
  $$
   其中$C_p$和$C_q$表示从空间位置到颜色值的映射（比如转换到L*a*b*颜色空间），而$f$是应用变换$T$的函数。

2. **目标函数**: 目标函数（或称为损失函数）是一个标量，它度量整个模型的预测值与观测值之间的差异。在优化问题中，目标函数通常是所有残差的某种汇总（如总和、平均值或其他统计度量），用于评估模型的整体拟合程度。

   以点云配准为例，几何误差的目标函数为：
  $$
   E_{geom}(T) = \sum_{i=1}^n \left(r_{G}^{(i)}(T)\right)^T C_{q_i}^{-1} \left(r_{G}^{(i)}(T)\right)
  $$
   其中$C_{q_i}^{-1}$是点$q_i$的协方差矩阵的逆，用于调整残差向量的权重，以反映点云中不同点的不确定性或重要性。

   颜色误差的目标函数可以是：
  $$
   E_{color}(T) = \sum_{i=1}^n \Delta E_{00}(L_{p_i}, a_{p_i}, b_{p_i}, L_{q_i}(T), a_{q_i}(T), b_{q_i}(T))
  $$
   其中$\Delta E_{00}$是计算两个颜色之间差异的CIEDE2000颜色差异公式。

总结来说，残差向量是单个数据点级别的差异表示，而目标函数是将所有这些差异汇总成一个单一标量，用于评估和优化整个模型。在实际应用中，优化算法通常通过最小化目标函数来找到最佳的模型参数$T$，以减小这些残差。


雅可比矩阵是一个非常重要的数学工具，尤其在优化问题和多变量函数的微分中扮演关键角色。在讨论雅可比矩阵在LM（Levenberg-Marquardt）优化器中的用处之前，先来了解一下雅可比矩阵本身。

### Jacobian matrix
#### definition
给定一个从$\mathbb{R}^n$到$\mathbb{R}^m$的函数$\mathbf{F}$：
$$\mathbf{F}(\mathbf{x}) = [f_1(\mathbf{x}), f_2(\mathbf{x}), \ldots, f_m(\mathbf{x})]^T$$
其中$\mathbf{x} = [x_1, x_2, \ldots, x_n]^T$是$n$维实数向量。每个函数$f_i$是$\mathbb{R}^n$到$\mathbb{R}$的映射。

雅可比矩阵是函数$\mathbf{F}$的所有一阶偏导数组成的矩阵，形式如下：
$$J = \begin{bmatrix}
\frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} & \cdots & \frac{\partial f_1}{\partial x_n} \\
\frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2} & \cdots & \frac{\partial f_2}{\partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f_m}{\partial x_1} & \frac{\partial f_m}{\partial x_2} & \cdots & \frac{\partial f_m}{\partial x_n}
\end{bmatrix}$$
这个矩阵展示了函数$\mathbf{F}$输出的每个分量对输入的每个分量的局部线性依赖。

#### Jacobian  in Levenberg-Marquardt

Levenberg-Marquardt (LM) 算法是一种用于非线性最小化问题的数值优化方法，特别适用于最小二乘问题。在LM算法中，雅可比矩阵起到了核心作用。

假设我们要最小化误差函数$S(\mathbf{x})$，其形式通常是：
$$S(\mathbf{x}) = \frac{1}{2} \sum_{i=1}^m r_i(\mathbf{x})^2$$
这里，$r_i(\mathbf{x})$是残差项，即数据点与模型预测之间的差异。

LM算法的更新步骤可以描述为：
$$\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta \mathbf{x}$$
其中，$\Delta \mathbf{x}$的求解涉及到雅可比矩阵$J$：
$$(J^T J + \lambda \mathbf{I}) \Delta \mathbf{x} = J^T \mathbf{r}$$
- $J$是关于当前参数$\mathbf{x}_k$的雅可比矩阵。
- $\mathbf{r}$是关于$\mathbf{x}_k$的残差向量。
- $\lambda$是调整因子，用于在梯度下降和高斯牛顿算法之间做平衡。
- $\mathbf{I}$是单位矩阵。

在这里，雅可比矩阵$J$提供了函数关于当前估计的局部线性近似，这对于计算搜索方向$\Delta \mathbf{x}$至关重要。它使得LM算法能够在每一步都根据函数的局部结构调

整步长和方向，从而提高收敛速度和稳定性。

海森矩阵（Hessian matrix）是多变量函数的二阶偏导数矩阵，对于非线性优化问题的解法具有重要意义。它提供了函数的局部曲率信息，这对于理解优化问题的几何结构和调整算法步长至关重要。

### Hessian Matrix
#### definition

对于一个从 $\mathbb{R}^n$ 到 $\mathbb{R}$ 的函数 $f(\mathbf{x})$，其中 $\mathbf{x} = [x_1, x_2, \ldots, x_n]^T$，海森矩阵定义为：

$$H(f) = \begin{bmatrix}
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2}
\end{bmatrix}$$

这个矩阵展示了函数 $f$ 在每个输入维度上的局部凹凸性（curvature）。一个函数的海森矩阵对称性体现了混合偏导数的对称性，即 $\frac{\partial^2 f}{\partial x_i \partial x_j} = \frac{\partial^2 f}{\partial x_j \partial x_i}$。

#### Hessian in Levenberg-Marquardt

虽然海森矩阵在纯粹的Levenberg-Marquardt算法中并不直接使用，它更常在牛顿方法及其变体中使用。然而，理解海森矩阵的作用对于理解LM算法提供了深入的洞见，特别是在算法调整为牛顿方法或高斯-牛顿方法的情况下。

在高斯-牛顿算法中，我们通常考虑问题的海森矩阵近似：
$$H \approx J^T J$$
其中 $J$ 是雅可比矩阵。这种近似省略了误差函数的二阶导数项（因为假设误差函数是平方和形式，其二阶导数项相对较小或可以忽略）。

Levenberg-Marquardt算法通过引入调整因子 $\lambda$ 来改善高斯-牛顿方法的鲁棒性：
$$(J^T J + \lambda \mathbf{I}) \Delta \mathbf{x} = J^T \mathbf{r}$$
在这里，当 $\lambda$ 较大时，更新步骤类似于梯度下降，适用于远离最小值的情况；而当 $\lambda$ 较小或接近零时，该方法则趋向于高斯-牛顿方法，适用于接近最小值的情况。这种调整使得算法在面对不同的问题结构时更加灵活和稳定。

通过理解海森矩阵，我们可以更好地把握LM算法中 $J^T J$ 的物理意义和作用，这有助于调整算法的性能，尤其是在需要精确控制算法收敛行为时。


####  linearization
1. **泰勒展开**：
   在优化问题中，目标函数 $f(\mathbf{x})$ 通常会在当前估计点 $\mathbf{x}_0$ 附近进行泰勒展开：
   $$
   f(\mathbf{x}) \approx f(\mathbf{x}_0) + \nabla f(\mathbf{x}_0)^T (\mathbf{x} - \mathbf{x}_0) + \frac{1}{2} (\mathbf{x} - \mathbf{x}_0)^T \mathbf{H} (\mathbf{x} - \mathbf{x}_0)
  $$
   其中 $\nabla f(\mathbf{x}_0)$ 是梯度，$\mathbf{H}$ 是海森矩阵，即目标函数的二阶偏导数矩阵。

2. **假设函数近似为二次形式**：
   当目标函数 $f$ 可以近似为二次形式时，海森矩阵 $\mathbf{H}$ 提供了关于函数局部曲率的信息。如果函数是由误差向量 $\mathbf{r}$ 的二范数的平方组成，即
   $$
   f(\mathbf{x}) = \frac{1}{2} \|\mathbf{r}(\mathbf{x})\|^2 = \frac{1}{2} \mathbf{r}(\mathbf{x})^T \mathbf{r}(\mathbf{x}),
  $$
   则通过链式法则，其海森矩阵 $\mathbf{H}$ 可以展开为：
   $$
   \mathbf{H} = \mathbf{J}^T \mathbf{J} + \sum_{i=1}^m r_i \mathbf{H}_i,
  $$
   其中 $\mathbf{J}$ 是雅可比矩阵，$r_i$ 是残差向量的第 $i$ 个分量，$\mathbf{H}_i$ 是 $r_i$ 相对于 $\mathbf{x}$ 的海森矩阵。

3.  近似的合理性
	在很多实际应用中，特别是误差项 $r_i$ 相对较小的情况下，$\sum_{i=1}^m r_i \mathbf{H}_i$ 通常可以被忽略，使得
$$
\mathbf{H} \approx \mathbf{J}^T \mathbf{J}
$$
	成为一个有效的近似。这种近似在以下情况下尤其有效：
- **误差项较小**：当残差 $\mathbf{r}(\mathbf{x})$ 较小时，$\sum_{i=1}^m r_i \mathbf{H}_i$ 对海森矩阵的贡献较小，因此主要由 $\mathbf{J}^T \mathbf{J}$ 控制。
- **问题接近线性**：对于接近线性的系统，雅可比矩阵在参数变化下不会有太大变化，因此 $\mathbf{J}^T \mathbf{J}$ 是对 $\mathbf{H}$ 的一个很好的近似。

4.  实用性考虑
- **计算复杂度**：直接计算完整的海森矩阵需要大量的计算资源，尤其是在参数维度较高时。使用 $\mathbf{J}^T \mathbf{J}$可以显著减少计算量。
- **数值稳定性**：在某些情况下，海森矩阵可能会变得病态（ill-conditioned），而 $\mathbf{J}^T \mathbf{J}$ 通常具有更好的数值稳定性。

因此，LM优化器采用这种近似方式，是在保证计算效率和稳定性的同时，尽可能地接近真实的海森矩阵，以提高优化过程的准确性和速度。

### Levenberg-Marquardt

#### example

 1. **优化目标**
假设我们的模型是一个简单的二次方程，形式为：
$$f(x, \mathbf{p}) = p_1 \cdot x^2 + p_2 \cdot x + p_3$$
其中，$\mathbf{p} = [p_1, p_2, p_3]^T$ 是模型参数。

如果我们有一组数据点 $(x_i, y_i)$（$i=1, 2, ..., m$），我们的目标是调整参数 $\mathbf{p}$ 使得模型预测值与实际数据值之间的误差最小。误差可以通过残差平方和来量化：
$$S(\mathbf{p}) = \frac{1}{2} \sum_{i=1}^m (y_i - f(x_i, \mathbf{p}))^2$$

 2. **残差向量**
残差向量 $\mathbf{r}(\mathbf{p})$ 表示为：
$$\mathbf{r}(\mathbf{p}) = [y_1 - f(x_1, \mathbf{p}), y_2 - f(x_2, \mathbf{p}), \ldots, y_m - f(x_m, \mathbf{p})]^T$$

 3. **雅可比矩阵**
对于我们的模型，雅可比矩阵 $J$ 的元素是每个残差对每个参数的偏导数：
$$J = \begin{bmatrix}
\frac{\partial r_1}{\partial p_1} & \frac{\partial r_1}{\partial p_2} & \frac{\partial r_1}{\partial p_3} \\
\frac{\partial r_2}{\partial p_1} & \frac{\partial r_2}{\partial p_2} & \frac{\partial r_2}{\partial p_3} \\
\vdots & \vdots & \vdots \\
\frac{\partial r_m}{\partial p_1} & \frac{\partial r_m}{\partial p_2} & \frac{\partial r_m}{\partial p_3}
\end{bmatrix}$$
具体到我们的模型：
- $\frac{\partial r_i}{\partial p_1} = -x_i^2$
- $\frac{\partial r_i}{\partial p_2} = -x_i$
- $\frac{\partial r_i}{\partial p_3} = -1$

4. **LM优化器的执行**
在LM优化器中，参数更新公式为：
$$(\mathbf{J}^T \mathbf{J} + \lambda \mathbf{I}) \Delta \mathbf{p} = \mathbf{J}^T \mathbf{r}(\mathbf{p})$$
这里，$\mathbf{J}^T \mathbf{J}$ 是雅可比矩阵的转置与其自身的乘积，代表了问题的局部几何结构。$\lambda$ 是一个调整因子，控制着算法靠近梯度下降还是高斯-牛顿方法。

5. **可能的变化**
在实际应用中，根据数据的特性和模型的行为，LM算法的表现可以通过调整 $\lambda$ 来优化。开始时可能设置较大的 $\lambda$ 值来确保算法的全局搜索行为，随着迭代的进行，逐渐减小 $\lambda$ 以便更精细地调整参数，靠近高斯-牛顿方法以精确逼近局部最小值。
通过这个流程，LM优化器能够有效地处理包括曲线拟合在内的各种复杂的非线性最小化问题，使模型预测与实际数据尽可能吻合。

####  Algorithm Step

Levenberg-Marquardt (LM) 算法是非线性最小二乘问题的一个高效解法，主要用于当问题可以表示为误差函数最小化时。它结合了高斯-牛顿法的快速收敛性和梯度下降法的全局搜索能力。

1. **初始化参数**
   - 初始化参数 $p$，通常是基于一些先验知识或简单的估计。
   - 初始化阻尼因子 $\lambda$，通常设置为一个较小的值（如 $10^{-3}$）。
   - 初始化迭代次数，和设置最大迭代次数。

2. **迭代过程**
   - 对于每一次迭代，执行以下步骤：

     a. **计算残差和雅可比矩阵**
        - $f = \text{function}(p)$: 在当前参数 $p$ 下计算残差向量。
        - $J = \text{jac\_function}(p)$: 计算残差向量相对于参数 $p$ 的雅可比矩阵。

     b. **构建梯度向量和海森矩阵**
        - $g = J^T f$: 计算梯度向量。
        - $H = J^T J$: 使用雅可比矩阵的转置和雅可比矩阵本身计算海森矩阵的近似。

     c. **求解更新步长**
        - 解方程 $(H + \lambda I) \Delta p = -g$ 来计算更新步长 $\Delta p$，其中 $I$ 是单位矩阵。
        - 使用Cholesky分解或其他数值稳定的方法来求解这个线性系统。

     d. **更新参数**
        - $p \leftarrow p + \Delta p$: 应用计算出的更新步长来修正参数。

     e. **评估更新**
        - 计算更新后的残差 $f_{\text{new}} = \text{function}(p + \Delta p)$。
        - 如果 $\|f_{\text{new}}\|^2 < \|f\|^2$，则减小阻尼因子 $\lambda$，使算法更接近高斯-牛顿法。
        - 如果 $\|f_{\text{new}}\|^2 \geq \|f\|^2$，则增加阻尼因子 $\lambda$，使算法更接近梯度下降法。

3. **终止条件**
   - 检查是否达到最大迭代次数。
   - 检查参数更新量 $\|\Delta p\|$ 是否低于预设阈值，表明收敛。

4. **返回结果**
   - 返回最终的参数估计 $p$ 和相关统计信息（如迭代次数、最终误差等）。

- 关键函数和数学公式
	- **残差和雅可比的计算**:
	  - $f = \text{function}(p)$
	  - $J = \text{jac\_function}(p)$
	
	- **梯度和海森矩阵的构建**:
	  - $g = J^T f$
	  - $H = J^T J$
	
	- **线性方程求解**:
	  - $\Delta p = -(H + \lambda I)^{-1} g$
	  - 常用的求解方法包括Cholesky分解等。

这个过程充分利用了雅可比矩阵和海森矩阵的信息，通过调整阻尼因子平衡了全局搜索和快速局部收敛的需求。整个LM算法
框架可以高效地处理包括机器学习、机器视觉和机器人定位等在内的众多应用中的非线性最小化问题。

### Torchmize

#### 函数输入和功能描述

- `p`: 参数的初始值。
- `function`: 需要拟合的用户提供的函数。
- `jac_function`: 用户提供的雅可比矩阵函数，用于计算残差向量相对于参数的偏导。
- `args`: 传递给目标函数和雅可比函数的额外参数。
- `wvec`: 权重向量，用于在多个成本中进行权重。
- `ftol`, `ptol`, `gtol`: 停止条件，分别代表函数值的相对变化、参数的相对变化和最大梯度容忍度。

#### 优化器核心逻辑和实现细节

1. **残差向量和优化目标**:
    - `function(p, *args)`: 这是用户定义的函数，其输出可以被视为残差向量。在最小二乘问题中，通常希望最小化这些残差的平方和，这就构成了优化目标。

2. **雅可比矩阵**:
    - `jac_function`: 如果用户没有提供雅可比函数，则使用 `batch_jacobian_approx_t` 通过自动微分计算雅可比矩阵。雅可比矩阵是关键，因为它提供了目标函数相对于参数变化的敏感度（局部斜率），这对于优化算法调整参数非常重要。

3. **Levenberg-Marquardt调整**:
    - LM算法通过引入阻尼因子来平衡梯度下降法和高斯-牛顿法之间的行为。`u`是阻尼因子，与单位矩阵乘积构成正则化项加到Hessian矩阵上，以保证其正定，从而改善求解过程的稳定性和收敛性。
    - `newton_step_parallel`: 这个函数执行牛顿步骤，其中使用雅可比和Hessian矩阵来更新参数。实际中可能使用近似的Hessian（通过雅可比矩阵计算得到）。

4. **参数更新**:
    - 使用 `torch.linalg.lstsq` 来求解线性系统 $(H + uD)h = -g$，其中 $h$ 是参数更新步，$g$ 是梯度，$H$ 是Hessian矩阵，$D$ 是对角矩阵用于调整阻尼。
    - 根据 LM 算法的标准实践，如果当前迭代改善了优化目标（通过增益比 `rho` 判断），则接受这一步的参数更新。

5. **停止条件**:
    - 检查梯度的最大值、参数更新的大小以及目标函数的改变量，任何一个条件满足即可停止迭代。

通过这种方式，这段代码实现了一个复杂的并行版本的Levenberg-Marquardt优化器，非常适用于处理大规模问题，其中包括多个独立的最小化问题可以同时求解。这种实现方式在计算上是高效的，特别是在使用现代GPU进行计算时。

Levenberg-Marquardt（LM）优化器通过使用雅可比矩阵的转置与雅可比矩阵自身的乘积 $J^T J$ 来近似海森矩阵 $H$，这种做法基于一些数学上的考虑和实用性的权衡。



### 联合优化
#### 1. 联合优化目标的设定

在这篇论文中，优化目标设计了两个主要部分：光度（photometric）和几何（geometric）目标。联合优化目标的形式如下：
$$E(T) = (1 - \sigma)EI(T) + \sigma ED(T)$$
其中：
- $EI(T)$ 是光度目标，基于颜色信息的差异。
- $ED(T)$ 是几何目标，基于空间位置的差异。
- $\sigma$ 是一个介于0和1之间的权重，用于调整两个目标的相对重要性。

#### 2. 残差向量

残差向量是衡量当前模型与目标数据之间差异的量度。在这种情况下，有两组残差向量：光度残差和几何残差。

- **光度残差 $r(p, q)_C$**
  $$r(p, q)_C(T) = C_p(f(s(q, T))) - C(q)$$
  其中 $C_p$ 是在点 $p$ 的切平面上定义的颜色函数，$C(q)$ 是点 $q$ 的颜色。

- **几何残差 $r(p, q)_G$**
  $$r(p, q)_G(T) = (s(q, T) - p)^T n_p$$
  这里 $s(q, T)$ 表示应用变换 $T$ 后的点 $q$ 的新位置，$n_p$ 是点 $p$ 处的法向量。

#### 3. 雅可比矩阵

雅可比矩阵 $J$ 提供了关于变换参数 $T$ 的残差向量的偏导数。这是进行梯度下降或牛顿类优化方法所必需的。雅可比矩阵的每一行对应于一个残差的偏导数，每一列对应于一个参数的偏导数。

- 对于光度残差的雅可比 $J_C$，需要考虑点 $q$ 在点 $p$ 的切平面上的投影如何随 $T$ 变化。
- 对于几何残差的雅可比 $J_G$，主要涉及到点 $q$ 如何随 $T$ 在空间中移动。

#### 4. 将目标函数转化为优化器可以处理的形式

Levenberg-Marquardt 优化器解决的是如下形式的问题：
$$\min_T \| \mathbf{r}(T) \|^2$$
其中 $\mathbf{r}(T)$ 是包含所有残差的向量。为了应用此优化器，我们需要：

- **计算总残差向量 $\mathbf{r}(T)$**
  $$\mathbf{r}(T) = \begin{bmatrix} \sqrt{1-\sigma} \mathbf{r}_C(T) \\ \sqrt{\sigma} \mathbf{r}_G(T) \end{bmatrix}$$
  其中 $\mathbf{r}_C(T)$ 和 $\mathbf{r}_G(T)$ 分别是光度和几何残差向量。

- **计算雅可比矩阵 $J$**
  $$J = \begin{bmatrix} \sqrt{1-\sigma

} J_C \\ \sqrt{\sigma} J_G \end{bmatrix}$$
  其中 $J_C$ 和 $J_G$ 分别是光度和几何雅可比矩阵。

#### 5. 使用Levenberg-Marquardt优化器求解

Levenberg-Marquardt 方法是一个迭代算法，它通过解决下面的线性方程来更新 $T$：
$$(J^T J + \lambda I) \Delta T = -J^T \mathbf{r}(T)$$
其中 $\lambda$ 是一个动态调整的参数，用于确保算法的稳定性和收敛性。通过逐步更新 $T$，直至满足停止条件（如达到最大迭代次数或残差足够小）。



### $T$线性化

变换矩阵 $T$ 被局部线性化为一个6维向量 $\xi = (\alpha, \beta, \gamma, a, b, c)$，这里 $\alpha, \beta, \gamma$ 代表旋转，而 $a, b, c$ 代表平移。这种表示方法允许在优化过程中以线性形式近似处理变换，而不必直接操作更复杂的非线性变换矩阵。

在许多计算机视觉和机器人领域的应用中，尤其是在处理位姿估计和点云配准问题时，常常需要优化变换矩阵 $T$。直接优化 $T$ 的9个参数（在不考虑缩放的情况下）不仅计算复杂，而且不直观。通过将 $T$ 近似为一个6维向量，我们可以更直接地控制和解释这些参数：

- **旋转**：采用小角度近似，即假设角度 $\alpha, \beta, \gamma$ 足够小，可以使用一阶泰勒展开来近似旋转矩阵的非线性部分。这样可以避免直接计算三维旋转矩阵的复杂三角函数。
- **平移**：直接使用线性分量 $a, b, c$。

#### 线性化变换矩阵的形式

给定6维向量 $\xi$，变换矩阵 $T$ 被近似为：

$$
T \approx \begin{bmatrix}
1 & -\gamma & \beta & a \\
\gamma & 1 & -\alpha & b \\
-\beta & \alpha & 1 & c \\
0 & 0 & 0 & 1
\end{bmatrix} T^k
$$

这里，$T^k$ 是上一次迭代得到的变换矩阵，新的矩阵 $T$ 则通过这个增量向量 $\xi$ 进行更新。







## EVAL

### pcd
**Root Mean Square Error**： $RMSE$
- 均方根误差用于衡量配准后的点云与参考点云之间的平均偏差大小, 是所有点之间的*欧氏距离的平方和的均值的平方根*。
$$\mathrm{RMSE}_{eP}=\sqrt{\frac1N\sum_{i=1}^N\left(\|p_i-p_i^{\prime}\|\right)^2}$$

**Center of Mass**： $COM$
质心是点云的质量中心，即所有点的平均位置。质心之间的距离用于衡量两个点云的整体位置偏差。

$$C_P=\left(\frac1N\sum_{i=1}^Nx_i,\frac1N\sum_{i=1}^Ny_i,\frac1N\sum_{i=1}^Nz_i\right)$$
$$C_Q=\left(\frac1N\sum_{i=1}^Nx_i^\prime,\frac1N\sum_{i=1}^Ny_i^\prime,\frac1N\sum_{i=1}^Nz_i^\prime\right)$$
$$\text{Distance}_{COM}=\|C_P-C_Q\|$$

### pose
对于一段连续N帧的姿态估计
- $eT$ : Translation Error
$$\mathrm{RMSE}_{eT}=\sqrt{\frac1N\sum_{i=1}^N\left(\|t_i-t_i^{\prime}\|\right)^2}$$

- $eR$ : Rotation Error
	1. **相对旋转矩阵**：$\Delta R_i=R_i\cdot(R_i^{\prime})^T$
	2. **旋转角度**$\theta_i=\arccos\left(\frac{\tan(\Delta R_i)-1}2\right)$
$$\mathrm{RMSE}_{eR}=\sqrt{\frac1N\sum_{i=1}^N\theta_i^2}$$