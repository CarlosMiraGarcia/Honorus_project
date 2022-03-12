import open3d as o3d
import numpy as np

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

def crop_using_plane(array_points, floor_a, floor_b, floor_c, floor_d):
    """From a point cloud, crops all the data points found under a given plane"""
    diff_adj = 5 # Threshold level from a given plane where data points will be removed
    list_points_kept = [] # List of data points not removed               

    # Keeps all the data points above the plane plus the threnshold level           
    for line in array_points:
        solu = (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2])
        if -((floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2])) >= floor_d + diff_adj:
            list_points_kept.append(line)
            
    array_points_kept = np.asarray(list_points_kept) 
    array_noplane_points, array_noplane_normals = np.hsplit(array_points_kept, 2) # Splits the array into two arrays: points and normals
    point_cloud = array_to_point_cloud_with_normals(
    array_noplane_points, array_noplane_normals) # Converts the numpy array to point cloud class       
    return point_cloud # Returns list with the kept data points

def leaves_segmentation(point_cloud, eps_value, min_points_value, saving_path_postprocessing):
    """Segments a point cloud containing leaves into individual leaf clusters\n
    \tUses DBSCAN [Martin Ester, 1996]\n
    \thttp://www.open3d.org/docs/latest/tutorial/Basic/pointcloud.html
    """
    # creates a label por each of the points depending on the cluster they are in,
    # with a -1 for whatever is considered noise
    labels = np.array(point_cloud.cluster_dbscan(eps=eps_value, min_points=min_points_value, print_progress=False)) 
    total_labels = labels.max() # Finds the number of labels
          
    pc_points = [] # List with the different point clouds points
    pc_normals = [] # List with the different point clouds normals
    
    # For each label created, this function appends the data points to each of the lists
    # where the label from each set of data points matches the current cluster label
    for label in range (total_labels + 1):
        pc_points.append(np.asarray(point_cloud.points)[labels == label])
        pc_normals.append(np.asarray(point_cloud.normals)[labels == label])            
         
    # Saves each leaf into a point cloud file
    for i in range (len(pc_points)):
        save_as_pcd(saving_path_postprocessing + 'leaf_' + str(i + 1) + '.pcd', array_to_point_cloud_with_normals(pc_points[i], pc_normals[i]))