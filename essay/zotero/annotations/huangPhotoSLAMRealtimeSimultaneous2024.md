---
Title: "Photo-SLAM: Real-time Simultaneous Localization and Photorealistic Mapping for Monocular Stereo and RGB-D Cameras"
Authors: Huajian Huang, Longwei Li, Hui Cheng, Sai-Kit Yeung

Date: 2024-01-01
citekey: huangPhotoSLAMRealtimeSimultaneous2024
tags: #⛔-No-DOI-found
---

## Photo-SLAM: Real-time Simultaneous Localization and Photorealistic Mapping for Monocular Stereo and RGB-D Cameras

**Bibliographie :** [1]

H. Huang, L. Li, H. Cheng, and S.-K. Yeung, ‘Photo-SLAM: Real-time Simultaneous Localization and Photorealistic Mapping for Monocular Stereo and RGB-D Cameras’, in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_, 2024, pp. 21584–21593. Accessed: Jul. 16, 2024. [Online]. Available: [https://openaccess.thecvf.com/content/CVPR2024/html/Huang_Photo-SLAM_Real-time_Simultaneous_Localization_and_Photorealistic_Mapping_for_Monocular_Stereo_CVPR_2024_paper.html](https://openaccess.thecvf.com/content/CVPR2024/html/Huang_Photo-SLAM_Real-time_Simultaneous_Localization_and_Photorealistic_Mapping_for_Monocular_Stereo_CVPR_2024_paper.html)

**Lien de la publication :** https://openaccess.thecvf.com/content/CVPR2024/html/Huang_Photo-SLAM_Real-time_Simultaneous_Localization_and_Photorealistic_Mapping_for_Monocular_Stereo_CVPR_2024_paper.html

**Lien Zotero :** [Huang et al_2024_Photo-SLAM.pdf](zotero://select/library/items/Z2YGFE58)

**Tags :** #⛔-No-DOI-found

> [!abstract]+
> _« »_

> [!Annotation|#ffd400]+
> _« 3.2. Localization and Geometry Mapping »_([5](zotero://open-pdf/library/items/Z2YGFE58?page=5&annotation=YST2RLUQ))
>
> ### 定位方法详细介绍

**Photo-SLAM的定位方法分为以下几个关键步骤：**

**1. 系统初始化和超基元地图创建：**
   - 系统从相机帧中提取ORB特征，这些特征用于建立2D到2D和2D到3D的对应关系。
   - 一旦通过相邻帧之间的足够2D到2D对应关系成功估计出转换矩阵，超基元地图便通过三角测量进行初始化，并开始进行姿态跟踪【4†source】。

**2. 运动束调整（Motion-Only Bundle Adjustment）：**
   - 在定位线程中，系统使用仅运动束调整来优化相机的方向和位置。
   - 这个过程的目标是最小化匹配帧的2D几何关键点和3D点之间的重新投影误差。
   - 优化问题可以表示为：
     $$
     \{R, t\} = \arg \min_{R, t} \sum_{i \in X} \rho \left( \|p_i - \pi(RP_i + t)\|^2_{\Sigma_g} \right)
     $$
     其中：
     - $R$ 是相机的旋转矩阵。
     - $t$ 是相机的位置向量。
     - $p_i$ 是帧的2D几何关键点。
     - $P_i$ 是3D点。
     - $\pi$ 是3D到2D的投影函数。
     - $\Sigma_g$ 是关键点的标度相关协方差矩阵。
     - $\rho$ 是鲁棒的Huber成本函数【4†source】。

**3. 局部束调整（Local Bundle Adjustment）：**
   - 在几何映射线程中，系统在一组共视点（covisible points）和关键帧（keyframes）上执行局部束调整。
   - 关键帧是从输入摄像机序列中选择的帧，这些帧提供了良好的视觉信息。
   - 系统构建了一个因子图，其中每个关键帧都是一个节点，边缘表示关键帧和匹配的3D点之间的约束。
   - 这个优化过程的目标是通过细化关键帧姿态和3D点来迭代地最小化重投影残差：
     $$
     \{P_i, R_l, t_l \mid i \in P_L, l \in K_L\} = \arg \min_{P_i, R_l, t_l} \sum_{k \in K} \sum_{j \in X_k} \rho(E(k, j))
     $$
     其中重投影残差 $E(k, j)$ 定义为：
     $$
     E(k, j) = \|p_j - \pi(R_k P_j + t_k)\|^2_{\Sigma_g}
     $$
     这个过程会修正观测到共视点但不在局部关键帧中的其他关键帧姿态【4†source】。

**4. 系统优化：**
   - 优化问题通过Levenberg-Marquardt（LM）算法进行求解。
   - 该算法是一种非线性最小二乘算法，结合了高斯-牛顿方法和梯度下降法的优点，适用于解决非线性优化问题。
   - 系统逐步传播其姿态估计，避免昂贵的全局操作，从而实现实时性能【4†source】。

**5. 实时性能和资源管理：**
   - Photo-SLAM在实现高效定位的同时，充分利用硬件资源，能够在嵌入式平台（如Jetson AGX Orin）上以实时速度运行。
   - 定位和几何映射组件的并行处理进一步提高了系统的效率，使其适用于实际机器人应用场景【4†source】。

### 定位方法总结

Photo-SLAM的定位方法结合了运动束调整和局部束调整，通过提取和优化ORB特征，实现了高效的6自由度相机姿态估计。系统采用Levenberg-Marquardt算法进行优化，并利用并行处理和资源管理，实现了在多种相机和硬件平台上的实时性能。

> [!Annotation|#ffd400]+
> _« 4. Experiment »_([9](zotero://open-pdf/library/items/Z2YGFE58?page=9&annotation=I4A5MESP))
>
> ### 实验结果

本文通过一系列实验验证了Photo-SLAM在不同场景和硬件平台上的性能。实验包括与当前最先进的SLAM系统的对比，评估了Photo-SLAM在定位精度、逼真映射质量和资源使用方面的表现。

#### 1. 在Replica数据集上的实验结果

Replica数据集包含了室内环境的RGB-D图像，实验结果如下表所示：

| Camera Type  | Method             | RMSE (cm) ↓ | STD ↓  | PSNR ↑  | SSIM ↑  | LPIPS ↓ | Operation Time ↓ | Tracking FPS ↑ | Rendering FPS ↑  | GPU Memory Usage ↓  |
| ------------ | ------------------ | ----------- | ------ | ------- | ------- | ------- | ---------------- | -------------- | ---------------- | ------------------- |
| Monocular    | ORB-SLAM3 [2]      | 3.942       | 3.115  | -       | -       | -       | <1 min           | 58.749         | -                | 0                   |
|              | DROID-SLAM [34]    | 0.725       | 0.308  | -       | -       | -       | <2 min           | 35.473         | -                | 11 GB               |
|              | Nice-SLAM [46]     | 99.9415     | 35.336 | 16.311  | 0.720   | 0.439   | >10 min          | 2.384          | 0.944            | 12 GB               |
|              | Orbeez-SLAM [4]    | -           | -      | 23.246  | 0.790   | 0.336   | <5 min           | 49.200         | 1.030            | 6 GB                |
|              | Go-SLAM [44]       | 71.054      | 24.593 | 21.172  | 0.703   | 0.421   | <5 min           | 25.366         | 0.821            | 22 GB               |
|              | Ours (Jetson)      | 1.235       | 0.756  | 29.284  | 0.883   | 0.139   | <5 min           | 18.315         | 95.057           | 4 GB                |
|              | Ours (Laptop)      | 0.713       | 0.524  | 33.049  | 0.926   | 0.086   | <5 min           | 19.974         | 353.504          | 4 GB                |
|              | Ours               | 1.091       | 0.892  | 33.302  | 0.926   | 0.078   | <2 min           | 41.646         | 911.262          | 6 GB                |
| RGB-D        | ORB-SLAM3 [2]      | 1.833       | 1.478  | -       | -       | -       | <1 min           | 52.209         | -                | 0                   |
|              | DROID-SLAM [34]    | 0.634       | 0.248  | -       | -       | -       | <2 min           | 36.452         | -                | 11 GB               |
|              | BundleFusion [6]   | 1.606       | 0.969  | 23.839  | 0.822   | 0.197   | <5 min           | 8.630          | -                | 5 GB                |
|              | Nice-SLAM [46]     | 2.350       | 1.590  | 26.158  | 0.832   | 0.232   | >10 min          | 2.331          | 0.611            | 12 GB               |
|              | Orbeez-SLAM [4]    | 0.888       | 0.562  | 32.516  | 0.916   | 0.112   | <5 min           | 41.333         | 1.401            | 6 GB                |
|              | ESLAM [16]         | 0.568       | 0.274  | 30.594  | 0.866   | 0.162   | <5 min           | 6.687          | 2.626            | 21 GB               |
|              | Co-SLAM [36]       | 1.158       | 0.602  | 30.246  | 0.864   | 0.175   | <5 min           | 14.575         | 3.745            | 4 GB                |
|              | Go-SLAM [44]       | 0.571       | 0.218  | 24.158  | 0.766   | 0.352   | <5 min           | 19.437         | 0.444            | 24 GB               |
|              | Point-SLAM [27]    | 0.596       | 0.249  | 34.632  | 0.927   | 0.083   | >2 hrs           | 0.345          | 0.510            | 24 GB               |
|              | Ours (Jetson)      | 0.581       | 0.289  | 31.978  | 0.916   | 0.101   | <5 min           | 17.926         | 116.395          | 4 GB                |
|              | Ours (Laptop)      | 0.590       | 0.289  | 34.853  | 0.944   | 0.062   | <5 min           | 20.597         | 396.082          | 4 GB                |
|              | Ours               | 0.604       | 0.298  | 34.958  | 0.942   | 0.059   | <2 min           | 42.485         | 1084.017         | 5 GB                |

这些结果表明Photo-SLAM在映射质量（PSNR和SSIM）和资源使用（跟踪FPS和GPU内存）方面表现出色，即使在嵌入式平台上也能实现实时性能【4†source】。

#### 2. 在TUM数据集上的实验结果

TUM数据集主要用于评估RGB-D传感器的性能，实验结果如下：

| Camera Type  | Method             | fr1-desk RMSE (cm) ↓ | fr2-xyz RMSE (cm) ↓  | fr3-office RMSE (cm) ↓ | PSNR ↑  | SSIM ↑  | LPIPS ↓ |
| ------------ | ------------------ | -------------------- | -------------------- | ---------------------- | ------- | ------- | ------- |
| Monocular    | ORB-SLAM3 [2]      | 1.534                | 0.720                | 1.400                  | -       | -       | -       |
|              | DROID-SLAM [34]    | 78.245               | 36.050               | 154.383                | -       | -       | -       |
|              | Go-SLAM [44]       | 33.122               | 28.584               | 105.755                | 11.705  | 0.406   | 0.614   |
|              | Ours (Jetson)      | 1.757                | 0.558                | 1.687                  | 18.811  | 0.681   | 0.329   |
|              | Ours (Laptop)      | 1.549                | 0.852                | 1.542                  | 20.515  | 0.733   | 0.241   |
|              | Ours               | 1.539                | 0.984                | 1.257                  | 20.972  | 0.743   | 0.228   |
| RGB-D        | ORB-SLAM3 [2]      | 1.724                | 0.385                | 1.698                  | -       | -       | -       |
|              | DROID-SLAM [34]    | 91.985               | 41.833               | 160.141                | -       | -       | -       |
|              | Nice-SLAM [46]     | 19.317               | 36.103               | 25.309                 | 12.003  | 0.417   | 0.510   |
|              | ESLAM [16]         | 3.359                | 31.448               | 25.808                 | 17.497  | 0.561   | 0.484   |
|              | Co-SLAM [36]       | 3.094                | 31.347               | 25.374                 | 16.419  | 0.482   | 0.591   |
|              | Go-SLAM [44]       | 2.119                | 31.788               | 26.802                 | 15.794  | 0.531   | 0.538   |
|              | Ours (Jetson)      | 4.571                | 0.360                | 1.874                  | 18.273  | 0.663   | 0.338   |
|              | Ours (Laptop)      | 1.891                | 0.361                | 1.315                  | 20.403  | 0.728   | 0.251   |
|              | Ours               | 2.603                | 0.346                | 1.001                  | 20.870  | 0.743   | 0.239   |

在TUM数据集中展示了优越的定位精度和映射质量，特别是在单目和RGB-D场景中【4†source】。

#### 3. 在EuRoC MAV数据集上的实验结果

EuRoC MAV数据集主要用于评估立体相机的性能，实验结果如下：

| Dataset      | Method             | RMSE (cm) ↓ | PSNR ↑  | SSIM ↑  | LPIPS ↓ |
| ------------ | ------------------ | ----------- | ------- | ------- | ------- |
| MH-01        | ORB-SLAM3 [2]      | 4.379       | -       | -       | -       |
|              | DROID-SLAM [34]    | 39.514      | -       | -       | -       |
|              | Ours (Jetson)      | 4.207       | 13.979  | 0.426   | 0.428   |
|              | Ours (Laptop)      | 4.049       | 13.962  | 0.421   | 0.378   |
|              | Ours               | 4.109       | 13.952  | 0.420   | 0.366   |
| MH-02        | ORB-SLAM3 [2]      | 4.525       | -       | -       | -       |
|              | DROID-SLAM [34]    | 39.265      | -       | -       | -       |
|              | Ours (Jetson)      | 4.193       | 14.210  | 0.436   | 0.447   |
|              | Ours (Laptop)      | 4.731       | 14.254  | 0.436   | 0.373   |
|              | Ours               | 4.441       | 14.201  | 0.430   | 0.356   |
| V1-01        | ORB-SLAM3 [2]      | 8.940       | -       | -       | -       |
|              | DROID-SLAM [34]    | 21.646      | -       | -       | -       |
|              | Ours (Jetson)      | 8.830       | 16.933  | 0.626   | 0.321   |
|              | Ours (Laptop)      | 8.836       | 17.025  | 0.622   | 0.284   |
|              | Ours               | 8.821       | 17.069  | 0.618   | 0.266   |
| V2-01        | ORB-SLAM3 [2]      | 26.904      | -       | -       | -       |
|              | DROID-SLAM [34]    | 15.344      | -       | -       | -       |
|              | Ours (Jetson)      | 26.643      | 16.038  | 0.643   | 0.347   |
|              | Ours (Laptop)      | 26.736      | 16.052  | 0.635   | 0.314   |
|              | Ours               | 26.609      | 15.677  | 0.622   | 0.323   |

Photo-SLAM在EuRoC MAV数据集上展示了较好的定位精度和映射质量，特别是在立体相机场景中表现良好【4†source】。

### 实验结果总结

通过在不同数据集上的实验，Photo-SLAM展示了在定位精度、逼真映射质量和资源使用方面的优越性能。系统能够在多种相机和硬件平台上实现实时性能，证明了其在实际机器人应用中的潜力和实用性。

> [!Annotation|#ffd400]+
> _« RMSE »_([11](zotero://open-pdf/library/items/Z2YGFE58?page=11&annotation=QFM5MH7D))

> [!Annotation|#ffd400]+
> _« STD »_([11](zotero://open-pdf/library/items/Z2YGFE58?page=11&annotation=BN97LLUJ))

> [!Annotation|#ffd400]+
> _« DROID-SLAM [ »_([13](zotero://open-pdf/library/items/Z2YGFE58?page=13&annotation=TNQ8NTT4))

> [!Annotation|#ffd400]+
> _« ESLAM »_([13](zotero://open-pdf/library/items/Z2YGFE58?page=13&annotation=FELDZY99))

> [!Annotation|#ffd400]+
> _« Co-SLAM »_([13](zotero://open-pdf/library/items/Z2YGFE58?page=13&annotation=6H3KH95N))

> [!Annotation|#ffd400]+
> _« Go-SLAM »_([13](zotero://open-pdf/library/items/Z2YGFE58?page=13&annotation=QIZ5CKVQ))
