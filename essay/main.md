确实，为了确保梯度计算和阈值选择的数学定义清晰和完整，我们应当详细描述这些处理步骤的数学原理，特别是梯度计算在图像处理中的离散形式。下面我将提供完整的数学公式和概念的详细解释。

### 计算梯度

在图像处理中，梯度计算通常用来识别图像中亮度变化最显著的位置，即边缘。由于图像是离散的数据，我们使用差分代替微分来计算梯度。

**数学公式：**

- 水平梯度 $G_x$ 和垂直梯度 $G_y$ 的计算通常通过以下离散近似公式实现：
 $$G_x[i, j] = I[i, j+1] - I[i, j-1]$$
  $$G_y[i, j] = I[i+1, j] - I[i-1, j]$$
  这里 $I$ 表示图像，$i, j$ 表示像素位置。

- 梯度幅度 $Magnitude$ 通常计算为：
$$Magnitude[i, j] = \sqrt{G_x[i, j]^2 + G_y[i, j]^2}$$
### 阈值选择方法

#### 双阈值法（仿 Canny 方法）

**数学公式：**
- 双阈值检测方法使用两个阈值：一个高阈值和一个低阈值。只有当梯度幅度超过高阈值时，像素点才被标记为强边缘。如果梯度幅度介于两个阈值之间，则视为弱边缘。

#### Otsu 方法自动选取阈值

**数学公式：**
- Otsu 方法通过计算图像直方图并最大化类间方差来自动选择阈值。类间方差表示的是前景（边缘）和背景（非边缘）之间的差异，其计算公式为：
$$
  \sigma^2_{\text{between}}(t) = \omega_0(t) \omega_1(t) [\mu_0(t) - \mu_1(t)]^2$$
  其中 $t$ 是阈值，$\omega$ 和 $\mu$ 分别是两个类的权重（概率）和均值，这些都基于直方图计算。

### 代码实现

以下是阈值选择方法的具体实现：

#### 双阈值法（仿 Canny 方法）

```python
from scipy.ndimage import binary_dilation

def apply_double_threshold(grad, low_threshold, high_threshold):
    strong_edges = grad >= high_threshold  # 强边缘
    weak_edges = (grad >= low_threshold) & (grad < high_threshold)  # 弱边缘
    # 使用形态学膨胀连接弱边缘与强边缘
    connected_edges = binary_dilation(strong_edges, structure=np.ones((3,3)))
    final_edges = connected_edges & weak_edges | strong_edges
    return final_edges
```

#### Otsu 方法自动选取阈值

```python
from skimage.filters import threshold_otsu

def adaptive_thresholding(grad):
    # 使用 Otsu 方法自动确定阈值
    threshold = threshold_otsu(grad)
    edges = grad > threshold
    return edges
```

通过这些数学定义和代码实现，我们可以更准确地描述和实施图像的边缘检测过程，特别是在处理深度图像时。这些方法提供了从基本的梯度计算到复杂的自动阈值选择的全面框架。