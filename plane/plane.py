import numpy as np
import open3d as o3d

class Plane:
    def get_plane(pcd):
        """Segments a plane in the point cloud using the RANSAC algorithm."""
        plane_model, inliers = pcd.segment_plane(distance_threshold= 0.5,
                                                 ransac_n=3,
                                                 num_iterations=1000)
        [a,b,c,d] = plane_model
        print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
        
        inlier_cloud = pcd.select_by_index(inliers)
        inlier_cloud.paint_uniform_color([1.0, 0, 0])
        outlier_cloud = pcd.select_by_index(inliers, invert=True)

        o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
        return plane_model
    
    def create_planes(a1, b1, c1, d1):
        plane = []
        rotated_plane = []
        for i in range(0, 300):
            for j in range(0, 100):          
                x = -i
                y = j
                z = ((a1*x) + (b1*y) + d1) / -c1
                plane.append([x, y, z])
                rotated_plane.append([-z, y, x])
        
        return np.array(plane), np.array(rotated_plane)