import open3d as o3d

class Point_cloud:
    def remove_outliers(pcd):
        
        voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.000001)
        cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=20,
                                                    std_ratio=2.0)

        return voxel_down_pcd, ind