---
Title: "NDT‐6D for color registration in agri‐robotic applications"
Authors: Himanshu Gupta, Achim J. Lilienthal, Henrik Andreasson, Polina Kurtser
Publication: "Journal of Field Robotics"
Date: 2023-09-01
citekey: guptaNDT6DColor2023
tags: 
---

## NDT‐6D for color registration in agri‐robotic applications

**Bibliographie :** [1]

H. Gupta, A. J. Lilienthal, H. Andreasson, and P. Kurtser, ‘NDT‐6D for color registration in agri‐robotic applications’, _Journal of Field Robotics_, vol. 40, no. 6, pp. 1603–1619, Sep. 2023, doi: [10.1002/rob.22194](https://doi.org/10.1002/rob.22194).

**Lien de la publication :** https://onlinelibrary.wiley.com/doi/10.1002/rob.22194

**Lien Zotero :** [Gupta et al_2023_NDT‐6D for color registration in agri‐robotic applications.pdf](zotero://select/library/items/K23NLWH2)

**Tags :** 

> [!abstract]+
> _« Abstract
            Registration of point cloud data containing both depth and color information is critical for a variety of applications, including in‐field robotic plant manipulation, crop growth modeling, and autonomous navigation. However, current state‐of‐the‐art registration methods often fail in challenging agricultural field conditions due to factors such as occlusions, plant density, and variable illumination. To address these issues, we propose the NDT‐6D registration method, which is a color‐based variation of the Normal Distribution Transform (NDT) registration approach for point clouds. Our method computes correspondences between pointclouds using both geometric and color information and minimizes the distance between these correspondences using only the three‐dimensional (3D) geometric dimensions. We evaluate the method using the GRAPES3D data set collected with a commercial‐grade RGB‐D sensor mounted on a mobile platform in a vineyard. Results show that registration methods that only rely on depth information fail to provide quality registration for the tested data set. The proposed color‐based variation outperforms state‐of‐the‐art methods with a root mean square error (RMSE) of 1.1–1.6 cm for NDT‐6D compared with 1.1–2.3 cm for other color‐information‐based methods and 1.2–13.7 cm for noncolor‐information‐based methods. The proposed method is shown to be robust against noises using the TUM RGBD data set by artificially adding noise present in an outdoor scenario. The relative pose error (RPE) increased 14% for our method compared to an increase of 75% for the best‐performing registration method. The obtained average accuracy suggests that the NDT‐6D registration methods can be used for in‐field precision agriculture applications, for example, crop detection, size‐based maturity estimation, and growth modeling. »_

> [!Annotation|#ff6666]+
>_« A representative example of this is the TEASER++ algorithm (Yang et al., 2020). »_([9](zotero://open-pdf/library/items/K23NLWH2?page=9&annotation=WKFU5JVY))
>
> 现代化快速配准算法，代码质量高，开源文档好

> [!Annotation|#ffd400]+
>![assets/guptaNDT6DColor2023/guptaNDT6DColor2023-13-x43-y370.png](assets/guptaNDT6DColor2023/guptaNDT6DColor2023-13-x43-y370.png)
>
> RGB-D变换的空间3D点云基本公式

> [!Annotation|#ffd400]+
>![assets/guptaNDT6DColor2023/guptaNDT6DColor2023-14-x56-y502.png](assets/guptaNDT6DColor2023/guptaNDT6DColor2023-14-x56-y502.png)
>
> 边缘溢出点对配准没有太大价值，因为下一帧也采集不到，对配准没有任何帮助

> [!Annotation|#ffd400]+
>_« (1) distance‐based filter: points at a distance of more than 3 m are rejected; (2) radius based filter: the point is rejected if the number of neighboring points in a radius of 0.01 m is less than 20 (3) voxel grid filter: if downsampling is required (in case of NDT P2D registration), the grid size of 0.02 m is used. The same preprocessed clouds are used for all compared methods. »_([15](zotero://open-pdf/library/items/K23NLWH2?page=15&annotation=AS5MYFEL))
>
> 常见降采样方法
1. 基于距离的
2. 基于半径的：根据上述计算，对每个点检查其邻域内的点数是否满足最小点数 \( n_{\text{min}} \) 的条件。具体公式如下：
   $$
   l(p, r) < n_{\text{min}}
   $$
   其中，\( l(p, r) \) 是点 \( p \) 在半径 \( r \) 内的邻近点数。

上述去除异常值
3. 体素化网格进行降采样加速处理

> [!Annotation|#e56eee]+
>_« For the TUM data set, Equation (6) was used to convert the RGBD scans into pointclodus; the camera parameters (focal length and image center) and scale factor used for conversion were taken from Sturm et al. (2012). For this data set, no outlier removal preprocessing procedure was done because pointclouds are inherently less noisy and more feature‐rich, as seen in Figure 2. The only pre‐processing was to artificially introduce noise in pointclouds to evaluate the robustness of the algorithms. These degradation procedures included generating data sets with (1) downsampled pointclouds with a voxel size of 1 cm, and (2) applying a Gaussian blur kernel with window size 5 × 5. »_([15](zotero://open-pdf/library/items/K23NLWH2?page=15&annotation=DZWD87DG))
>
> 手动模糊数据集来验证算法的robust


