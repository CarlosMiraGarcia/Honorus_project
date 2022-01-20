import open3d as o3d
import numpy as np

class Point_cloud:
    def remove_outliers(pcd):
        voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.000001)
        cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=20,
                                                    std_ratio=2.0)
        return voxel_down_pcd, ind
    
    def array_to_point_cloud(pc_array):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pc_array)
        return pcd
    
    def save_as_pcd(savefilename, point_cloud):
        o3d.io.write_point_cloud(savefilename, point_cloud, write_ascii=True, compressed=True)
        
    def read_lines(point_cloud):    
        list = np.asarray(point_cloud.points)
        return list
            
    def append_points_to_array(npa1, npa2):
        npa = np.vstack((npa1, npa2))
        return npa

    def crop_using_plane(list_points, floor_a, floor_b, floor_c, floor_d):
        diff_adj = 5
        list_points_kept = []
        
        for line in list_points:
            if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) > - floor_d + diff_adj:
                list_points_kept.append(line)
            
        return list_points_kept