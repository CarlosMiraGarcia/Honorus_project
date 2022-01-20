import open3d as o3d
from plane.plane import *
from point_cloud.point_cloud import *

class Stem:   
    def create_stem(point_cloud, floor_a, floor_b, floor_c, floor_d):
        np_array = Point_cloud.read_lines(point_cloud)
               
        xyz_plane, xyz_plane_rotated = Plane.append_plane_to_pcd(floor_a, floor_b, floor_c, floor_d)
        
        np_array = Point_cloud.append_points_to_array(xyz_plane, np_array)
        np_array = Point_cloud.append_points_to_array(xyz_plane_rotated, np_array)        
      
        xyz_plane_pcd = o3d.geometry.PointCloud()
        xyz_plane_pcd.points = o3d.utility.Vector3dVector(xyz_plane)
        xyz_plane_rotated_pcd = o3d.geometry.PointCloud()
        xyz_plane_rotated_pcd.points = o3d.utility.Vector3dVector(xyz_plane_rotated)
        
        return xyz_plane_pcd, xyz_plane_rotated_pcd