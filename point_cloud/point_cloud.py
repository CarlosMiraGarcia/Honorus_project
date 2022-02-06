import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

class Point_cloud:
    def remove_outliers(pcd, neighbors, ratio):
        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=neighbors,
                                                    std_ratio=ratio)
        return pcd, ind
    
    def array_to_point_cloud(pc_array):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pc_array)
        return pcd
    
    def array_to_point_cloud_with_normals(pc_array_points, pc_array_normals):
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(pc_array_points)
            pcd.normals = o3d.utility.Vector3dVector(pc_array_normals)
            return pcd
        
    def save_as_pcd(savefilename, point_cloud):
        o3d.io.write_point_cloud(savefilename, point_cloud, write_ascii=False, compressed=True)
           
    def append_points_to_array(npa1, npa2):
        npa = np.vstack((npa1, npa2))
        return npa

    def crop_using_plane(list_points, floor_a, floor_b, floor_c, floor_d):
        diff_adj = 5
        list_points_kept = []
        
        if floor_a * floor_b * floor_c < 0:
            for line in list_points:
                if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) >= - floor_d + diff_adj:
                    list_points_kept.append(line)     
                       
        else:
            for line in list_points:
                if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) <= - floor_d - diff_adj:
                    list_points_kept.append(line)        

        return list_points_kept
    
    def leaves_segmentation(point_cloud, eps_value, min_points_value):
        # Uses DBSCAN [Ester1996]
        # http://www.open3d.org/docs/latest/tutorial/Basic/pointcloud.html

        labels = np.array(point_cloud.cluster_dbscan(eps=eps_value, min_points=min_points_value, print_progress=True)) # creates a label por each of the points depending on the cluster they are in,
                                                                                             # with a -1 for whatever is considered noise

        max_label = labels.max()
        print(f"point cloud has {max_label + 1} clusters")
        colors = plt.get_cmap("viridis")(labels / (max_label if max_label > 0 else 1)) # selects a colour based on the assigned label using the palette viridis
        colors[labels < 0] = 0 # If the cluster is too small (noise), set the colour to black
        point_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
        
        print("Remember to display the leaves with different colours for the dissertation!")
        print("This can be done on the leaves_segmentation module")        
        out_pc_points = []
        out_pc_normals = []
        
        for label in range (max_label + 1):
            out_pc_points.append(np.asarray(point_cloud.points)[labels == label])
            out_pc_normals.append(np.asarray(point_cloud.normals)[labels == label])            
                   
        return out_pc_points, out_pc_normals