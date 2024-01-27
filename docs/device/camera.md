

### 相机型号参数
> Astra Pro Plus
![[assets/Pasted image 20240126210527.png]]
- [[assets/Astra_Pro_Plus_instrution.pdf|技术文档]]
### 简介
1. 采用采用深度+彩色双通道相机
2. 驱动问题
	1. 对于`Linux`不需要额外安装驱动，`windows`需要额外装[3D视觉AI开放平台](https://vcp.developer.orbbec.com.cn/documentation?doc=doc-78)
3. sdk问题
	1. 官方提供了`OpenNI2`的·`c++`版本的sdk[GitHub - OpenNI/OpenNI2: OpenNI2](https://github.com/OpenNI/OpenNI2)，GitHub上有[Python版本的包装](https://github.com/severin-lemaignan/openni-python)的，但是比较旧，距离上一次提交大概有5年，`c++`版本也是上一次提交在5年前
	2. `python` sdk也有[pylibfreenect2](https://github.com/r9y9/pylibfreenect2)用他的，但是年代也是有点久远
> 这种情况，不是没有维护，而是大概率有了新的替代品

2022年，`opencv`支持了该相机直接读取[这是官网的c++教程](https://docs.opencv.org/4.x/d4/d65/tutorial_orbbec_astra.html)，`python`也是类似的，并且，读取彩色或者深度图像，都是`cv2.imread()`方法，传递到参数不一样而已
> 因此，`opencv-python` 是标准sdk的解决方案