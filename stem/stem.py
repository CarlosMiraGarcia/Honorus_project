import open3d as o3d
from stem.helpers import *
from plane.plane import *

class Stem:   
    def create_stem(point_cloud, savefilename):
        np_array = read_lines(point_cloud)        
        
        Stem.floor_a, Stem.floor_b, Stem.floor_c, Stem.floor_d = Plane.get_plane(point_cloud)
               
        xyz_plane, xyz_plane_rotated = Plane.append_plane_to_pcd(Stem.floor_a, Stem.floor_b, Stem.floor_c, Stem.floor_d)
        
        np_array = append_points_to_list(xyz_plane, np_array)
        np_array = append_points_to_list(xyz_plane_rotated, np_array)        
      
        xyz_plane_pcd = o3d.geometry.PointCloud()
        xyz_plane_rotated_pcd = o3d.geometry.PointCloud()
        xyz_plane_pcd.points = o3d.utility.Vector3dVector(xyz_plane)
        xyz_plane_rotated_pcd.points = o3d.utility.Vector3dVector(xyz_plane_rotated)
        
        create_pcd(savefilename, np_array)
        
        return xyz_plane_rotated_pcd