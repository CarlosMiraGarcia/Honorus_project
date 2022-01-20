import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

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
    
    def leaves_segmentation(pcd):
        # Uses DBSCAN [Ester1996]
        # http://www.open3d.org/docs/latest/tutorial/Basic/pointcloud.html

        labels = np.array(pcd.cluster_dbscan(eps=2, min_points=30, print_progress=True)) # creates a label por each of the points depending on the cluster they are in,
                                                                                             # with a -1 for whatever is considered noise

        max_label = labels.max()
        print(f"point cloud has {max_label + 1} clusters")
        colors = plt.get_cmap("viridis")(labels / (max_label if max_label > 0 else 1)) # selects a colour based on the assigned label using the palette viridis
        colors[labels < 0] = 0 # If the cluster is too small (noise), set the colour to black
        pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
        o3d.visualization.draw_geometries([pcd])
        
        out_pc = []
        for label in range (max_label + 1):
            out_pc.append(np.asarray(pcd.points)[labels == label])
                   
        return out_pc