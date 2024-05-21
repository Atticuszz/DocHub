

## Abstract

## 1. Introduction

## 2. Related Work

## 3. Method

### compute depth image edge
#### compute gradients

**数学公式：**
	水平梯度 $G_x$ 和垂直梯度 $G_y$ 的计算通常通过以下离散近似公式实现：
 $$G_x[i, j] = I[i, j+1] - I[i, j-1]$$
  $$G_y[i, j] = I[i+1, j] - I[i-1, j]$$
  这里 $I$ 表示图像，$i, j$ 表示像素位置。

- 梯度幅度 $Magnitude$ 通常计算为：
$$Magnitude[i, j] = \sqrt{G_x[i, j]^2 + G_y[i, j]^2}$$

```python
from numba import jit

@jit(nopython=True)
def compute_gradients_numba(depth_map):
    # 使用 Numba 加速梯度计算
    horizontal_grad = np.abs(np.diff(depth_map, axis=1))
    vertical_grad = np.abs(np.diff(depth_map, axis=0))
    grad_magnitude = np.sqrt(horizontal_grad[:, :-1]**2 + vertical_grad[:-1, :]**2)
    return grad_magnitude

@jit(nopython=True)
def simple_edge_detection_numba(depth_map, threshold=10):
    grad = compute_gradients_numba(depth_map)
    edges = grad > threshold
    return edges

```


### select threshold 
#### 双阈值法（仿 Canny 方法）

**数学公式：**
- 双阈值检测方法使用两个阈值：一个高阈值和一个低阈值。只有当梯度幅度超过高阈值时，像素点才被标记为强边缘。如果梯度幅度介于两个阈值之间，则视为弱边缘。

```python
from scipy.ndimage import binary_dilation

def apply_double_threshold(grad, low_threshold, high_threshold):
    strong_edges = grad >= high_threshold
    weak_edges = (grad >= low_threshold) & (grad < high_threshold)
    # Use binary dilation to connect weak edges that are adjacent to strong edges
    connected_edges = binary_dilation(strong_edges, structure=np.ones((3,3)))
    final_edges = connected_edges & weak_edges | strong_edges
    return final_edges

```
#### Otsu 方法自动选取阈值

**数学公式：**
- Otsu 方法通过计算图像直方图并最大化类间方差来自动选择阈值。类间方差表示的是前景（边缘）和背景（非边缘）之间的差异，其计算公式为：
$$
  \sigma^2_{\text{between}}(t) = \omega_0(t) \omega_1(t) [\mu_0(t) - \mu_1(t)]^2$$
  其中 $t$ 是阈值，$\omega$ 和 $\mu$ 分别是两个类的权重（概率）和均值，这些都基于直方图计算。

```python
from skimage.filters import threshold_otsu

def adaptive_thresholding(grad):
    # 使用Otsu方法自动确定阈值
    threshold = threshold_otsu(grad)
    edges = grad > threshold
    return edges

```

### downsample


#### downsample-stride



#### random in base area


## 4. Experimental Setup


## 5. Results & Discussion
