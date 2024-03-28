## basic

### image
*format in disk*

1. **JPEG（Joint Photographic Experts Group）**
- 采用有损压缩。
- 优点是可以在不显著降低视觉质量的情况下大幅减小文件大小，适用于存储照片。
- 缺点是重复保存和编辑会逐渐降低图像质量。
2. **PNG（Portable Network Graphics）**
- 采用无损压缩。
- 优点是保留原始图像的完整质量，支持透明度。
- 缺点是文件大小通常比JPEG大。
*format in RAM*
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
2. expand_dims for pytorch
```python
depth_tensor.unsqueeze(0)
shape->(1,h,w)
```
### camera
#### pose


#### intrinsic

#### scale
