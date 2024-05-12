## Abstract

## 1. Introduction

## 2. Related Work

## 3. Method

### definition
#### RGB to L*

##### normalize RGB
$$R^{\prime},G^{\prime},B^{\prime}=\frac R{255},\frac G{255},\frac B{255}$$
##### SRGB
$$C_{linear}=\begin{cases}\frac{C^{\prime}}{12.92}&\text{if }C^{\prime}\leq0.04045\\\left(\frac{C^{\prime}+0.055}{1.055}\right)^{2.4}&\text{otherwise}\end{cases}$$
*$C$ may be $R,G,B$*
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

### estimate camera pose via different approaches in dynamic sim

### estimate path plan via different approaches in dynamic sim

## 5. Results & Discussion
