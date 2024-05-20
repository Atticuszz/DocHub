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

**Lien Zotero :** [Gupta et al_2023_NDT‐6D for color registration in agri‐robotic applications.pdf](zotero://select/library/items/MTL9XXAP)

**Tags :**

> [!abstract]+
> \*« Abstract

            Registration of point cloud data containing both depth and color information is critical for a variety of applications, including in‐field robotic plant manipulation, crop growth modeling, and autonomous navigation. However, current state‐of‐the‐art registration methods often fail in challenging agricultural field conditions due to factors such as occlusions, plant density, and variable illumination. To address these issues, we propose the NDT‐6D registration method, which is a color‐based variation of the Normal Distribution Transform (NDT) registration approach for point clouds. Our method computes correspondences between pointclouds using both geometric and color information and minimizes the distance between these correspondences using only the three‐dimensional (3D) geometric dimensions. We evaluate the method using the GRAPES3D data set collected with a commercial‐grade RGB‐D sensor mounted on a mobile platform in a vineyard. Results show that registration methods that only rely on depth information fail to provide quality registration for the tested data set. The proposed color‐based variation outperforms state‐of‐the‐art methods with a root mean square error (RMSE) of 1.1–1.6 cm for NDT‐6D compared with 1.1–2.3 cm for other color‐information‐based methods and 1.2–13.7 cm for noncolor‐information‐based methods. The proposed method is shown to be robust against noises using the TUM RGBD data set by artificially adding noise present in an outdoor scenario. The relative pose error (RPE) increased 14% for our method compared to an increase of 75% for the best‐performing registration method. The obtained average accuracy suggests that the NDT‐6D registration methods can be used for in‐field precision agriculture applications, for example, crop detection, size‐based maturity estimation, and growth modeling. »*

> [!Annotation|#ffd400]+
>
> The PDF you provided describes a novel method for point cloud registration in agricultural robotics applications, specifically designed to handle the challenges associated with variable lighting conditions, occlusions, and plant density in agricultural fields. The method introduced is called the NDT-6D registration method, which is a color-based variation of the Normal Distribution Transform (NDT) registration approach for point clouds.您提供的 PDF 描述了农业机器人应用中点云配准的一种新颖方法，该方法专门用于应对农业领域中与可变照明条件、遮挡和植物密度相关的挑战。引入的方法称为 NDT-6D 配准方法，它是点云正态分布变换 (NDT) 配准方法的基于颜色的变体。The key advancements proposed in this method include:该方法提出的主要改进包括：<b>Integration of Color Information</b>: Unlike traditional methods that rely only on geometric information, NDT-6D computes correspondences between point clouds using both geometric and color data. This integration allows for more accurate matching in environments where color can provide significant additional information about the scene.颜色信息的集成：与仅依赖几何信息的传统方法不同，NDT-6D 使用几何数据和颜色数据来计算点云之间的对应关系。这种集成可以在颜色可以提供有关场景的重要附加信息的环境中进行更准确的匹配。<b>Robustness to Noise and Outdoor Conditions</b>: The method demonstrates improved robustness against noises typically found in outdoor agricultural settings. It achieves this by effectively minimizing the distance between matched correspondences using only the three-dimensional geometric dimensions.对噪声和室外条件的鲁棒性：该方法证明了对户外农业环境中常见噪声的鲁棒性有所提高。它通过仅使用三维几何尺寸有效地最小化匹配对应关系之间的距离来实现这一点。<b>Empirical Validation</b>: The method was tested using the GRAPES3D data set collected with a commercial-grade RGB-D sensor mounted on a mobile platform in a vineyard. The results show that the NDT-6D method outperforms existing state-of-the-art methods, providing more reliable registration with lower root mean square error (RMSE) in challenging field conditions.经验验证：使用安装在葡萄园移动平台上的商业级 RGB-D 传感器收集的 GRAPES3D 数据集对该方法进行了测试。结果表明，NDT-6D 方法优于现有的最先进方法，在具有挑战性的现场条件下提供更可靠的配准和更低的均方根误差 (RMSE)。<b>Potential for Practical Applications</b>: The paper suggests that the NDT-6D method can significantly enhance the capabilities of in-field precision agriculture applications such as crop detection, size-based maturity estimation, and growth modeling.实际应用潜力：论文表明，NDT-6D 方法可以显着增强田间精准农业应用的能力，例如作物检测、基于大小的成熟度估计和生长建模。This approach addresses critical issues in agricultural robotics by enhancing the accuracy and reliability of point cloud registration in environments that are typically problematic for optical sensors.这种方法通过提高光学传感器通常存在问题的环境中点云配准的准确性和可靠性，解决了农业机器人技术中的关键问题。

> [!Annotation|#e56eee]+
> _« proach for point clouds. Our method computes correspondences between pointclouds using both geometric and color information and minimizes the distance between these correspondences using only the three‐dimensional (3D) geometric dimensions. We evaluate the method using the GRAPES3D data set collected with a commercial‐grade RGB‐D sensor mounted on a mobile platform in a vineyard. Results show that registration methods that only rely on depth information fail to provide quality registration for the tested data set. The proposed color‐based variation outperforms state‐of‐the‐art methods with a root mean square error (RMSE) of 1.1–1.6 »_([1](zotero://open-pdf/library/items/MTL9XXAP?page=1&annotation=JN92XP9Q))
