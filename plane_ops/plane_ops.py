import numpy as np
import open3d as o3

def get_plane(pcd, threshold, iterations):
    """Segments a plane in the point cloud using the RANSAC algorithm.\n
    Finds the largest plane in a point cloud where:\n
    \tdistance_threshold (threshold) defines the max distance from the plane to be considered an inlier,\n
    \transac_n defines the number of points used to consider a plane,\n
    \tand num_iterations (iterations) defines the number of times a plane is sampled
    """
    plane_model, inliers = pcd.segment_plane(distance_threshold= threshold, 
                                             ransac_n=3,
                                             num_iterations=iterations)                                        
   
    return plane_model # Returns the plane equation for the plane
     
def create_plane(point_cloud, a, b, c, d):
    """Creates a plane.\n
        Requires a point cloud and a plane equation a*x + b*y + c*z+d=0"""
    plane = [] # List that will contian the created plane data points       
    min_xyz = np.min(point_cloud, axis=0) # Finds the min x, y, z value
    max_xyz = np.max(point_cloud, axis=0) # Finds the max x, y, z value
    # Creates a plane using a plane equation
    for i in range (int(min_xyz[0] * 10), int(max_xyz[0]* 10)):
        for j in  range (int(min_xyz[1]* 10), int(max_xyz[1]* 10)):
            x = i/10
            y = j/10
            if c == 0:
                z = 0
            else:
                z = (-d - a*x - b*y)/c
            plane.append([x, y, z])
            
    return np.asarray(plane) # Returns a numpy array containing the created plane