import numpy as np
import open3d as o3d

def get_plane(pcd, threshold, iterations):
    """Segments a plane in the point cloud using the RANSAC algorithm."""
    # Finds the largest plane in a point cloud
    # where distance_treshold defines the max distance from the plane to be considered an inlier,
    # ransac_n defines the number of points used to consider a plane,
    # and num_iterations defines the number of times a plane is sampled
    plane_model, inliers = pcd.segment_plane(distance_threshold= threshold, 
                                             ransac_n=3,
                                             num_iterations=iterations)
    [a,b,c,d] = plane_model                                                 
    #inlier_cloud = pcd.select_by_index(inliers)
    #inlier_cloud.paint_uniform_color([1.0, 0, 0])
    #outlier_cloud = pcd.select_by_index(inliers, invert=True)
    #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
    
    return plane_model # Returns the plane equation for the plane

     
def create_plane(point_cloud, a, b, c, d):
    """Creates a plane.\n
        Requires a point cloud and a plane equation a*x + b*y + c*z+d=0"""
    plane = [] # List that will contian the created plane data points       
    min = np.min(point_cloud, axis=0) # Finds the min x value
    max = np.max(point_cloud, axis=0) # Finds the max x value
    # Creates a plane using a plane equation
    for i in range (int(min[0] * 10), int(max[0]* 10)):
        for j in  range (int(min[1]* 10), int(max[1]* 10)):
            x = i/10
            y = j/10
            z = (-d - a*x - b*y)/c
            plane.append([x, y, z])
            
    return np.asarray(plane) # Returns a numpy array containing the created plane
