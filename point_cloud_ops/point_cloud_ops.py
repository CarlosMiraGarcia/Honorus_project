import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

def remove_outliers(pcd, neighbors, ratio):
    """ Removes outliers from a point cloud
        \tpcd is the point cloud class,
        \tneighbors is the number of neighbors taken into consideration to calculate the distance between points
        \tand ratio is the threshold level to be consider on the distance between two points
    """
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=neighbors,
                                                std_ratio=ratio)
    
    pc_cleaned = pcd.select_by_index(ind)
    return pc_cleaned # returns the point cloud without outliers

def array_to_point_cloud(pc_array):
    """Converts a numpy array to point cloud class, without normals"""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc_array)
    return pcd

def array_to_point_cloud_with_normals(pc_array_points, pc_array_normals):
    """Converts a numpy array to point cloud class, including the normals"""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc_array_points)
    pcd.normals = o3d.utility.Vector3dVector(pc_array_normals)
    return pcd
    
def save_as_pcd(save_file_path, point_cloud):
    """Saves point cloud to a given path"""
    o3d.io.write_point_cloud(save_file_path, point_cloud, write_ascii=False, compressed=True)
       
def append_points_to_array(nparray1, npaarray2):
    """Appends data points to a numpy array containing a point cloud"""
    npa = np.vstack((nparray1, npaarray2))
    return npa # Returns the merged numpy array

def crop_using_plane(list_points, floor_a, floor_b, floor_c, floor_d):
    """From a point cloud, crops all the data points found a given plane"""
    diff_adj = 5 # Threshold level from a given plane where data points will be removed
    list_points_kept = [] # List of data points not removed               
    
    # Keep - not sure is without this will work everytime
    # if floor_a * floor_b * floor_c < 0:
    #     for line in list_points:
    #         if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) >= - floor_d + diff_adj:
    #             list_points_kept.append(line)     
                   
    # else:
    #     for line in list_points:
    #         if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) <= - floor_d - diff_adj:
    #             list_points_kept.append(line)     
    
    # Keeps all the data points above the plane plus threnshold level           
    for line in list_points:
        if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) <= - floor_d - diff_adj:
            list_points_kept.append(line)        
    return list_points_kept # Returns list with the kept data points

def leaves_segmentation(point_cloud, eps_value, min_points_value):
    """Segments a point cloud containing leaves into individual leaf clusters\n
    \tUses DBSCAN [Martin Ester, 1996]\n
    \thttp://www.open3d.org/docs/latest/tutorial/Basic/pointcloud.html
    """
    # creates a label por each of the points depending on the cluster they are in,
    # with a -1 for whatever is considered noise
    labels = np.array(point_cloud.cluster_dbscan(eps=eps_value, min_points=min_points_value, print_progress=True)) 
    max_label = labels.max() # Finds the number of labels
    print(f"point cloud has {max_label + 1} clusters")
    
    # This is used to display the leaves using open3d with different colours
    colors = plt.get_cmap("viridis")(labels / (max_label if max_label > 0 else 1)) # selects a colour based on the assigned label using the palette viridis
    colors[labels < 0] = 0 # If the cluster is too small (noise), set the colour to black
    point_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
    
    print("Remember to display the leaves with different colours for the dissertation!")
    print("This can be done on the leaves_segmentation module")  
          
    pc_points = [] # List with the different point clouds points
    pc_normals = [] # List with the different point clouds normals
    
    # For each label created, this function appends the data points to each of the lists
    # where the label from each set of data points matches the current cluster label
    for label in range (max_label + 1):
        pc_points.append(np.asarray(point_cloud.points)[labels == label])
        pc_normals.append(np.asarray(point_cloud.normals)[labels == label])            
               
    return pc_points, pc_normals # Returns the list with the point clouds