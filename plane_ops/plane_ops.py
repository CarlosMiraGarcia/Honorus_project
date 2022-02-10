import numpy as np
import open3d as o3d

def get_plane(pcd, threshold, iterations):
    """Segments a plane in the point cloud using the RANSAC algorithm."""
    plane_model, inliers = pcd.segment_plane(distance_threshold= threshold,
                                             ransac_n=3,
                                             num_iterations=iterations)
    [a,b,c,d] = plane_model
    #inlier_cloud = pcd.select_by_index(inliers)
    #inlier_cloud.paint_uniform_color([1.0, 0, 0])
    #outlier_cloud = pcd.select_by_index(inliers, invert=True)
    #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
    return plane_model     
def create_plane(point_cloud, a1, b1, c1, d1):
    plane = []        
    min = np.min(point_cloud, axis=0)
    max = np.max(point_cloud, axis=0)
    for i in range (int(min[0] * 10), int(max[0]* 10)):
        for j in  range (int(min[1]* 10), int(max[1]* 10)):
            x = i/10
            y = j/10
            z = (-d1 - a1*x - b1*y)/c1
            plane.append([x, y, z])
    return np.asarray(plane)
