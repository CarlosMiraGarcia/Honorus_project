class Plane:
    def get_plane(pcd):
        """Segments a plane in the point cloud using the RANSAC algorithm."""
        plane_model, inliers = pcd.segment_plane(distance_threshold= 0.005,
                                                 ransac_n=3,
                                                 num_iterations=1000)
        [a,b,c,d] = plane_model
        print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
        return plane_model
    
    def append_plane_to_pcd(plane, rotated_plane, a1, b1, c1, d1):
        for i in range(0, 300):
            for j in range(0, 100):          
                x = -i
                y = j
                z = ((a1*x) + (b1*y) + d1) / -c1
                plane.append([x, y, z])
                rotated_plane.append([-z, y, x])
        
        return plane, rotated_plane