import open3d as o3d
from stem.helpers import *
from plane.plane import *

class Stem:   
    def create_stem(filename, savefilename):
        xlist = read_lines(filename)
        
        pcd = o3d.io.read_point_cloud(filename)
        
        Stem.floor_a, Stem.floor_b, Stem.floor_c, Stem.floor_d = Plane.get_plane(pcd)
               
        xyz_plane, xyz_plane_rotated = Plane.append_plane_to_pcd(Stem.floor_a, Stem.floor_b, Stem.floor_c, Stem.floor_d)
        
        xlist = append_points_to_list(xyz_plane, xlist)
        xlist = append_points_to_list(xyz_plane_rotated, xlist)        
      
        xyz_plane_pcd = o3d.geometry.PointCloud()
        xyz_plane_rotated_pcd = o3d.geometry.PointCloud()
        xyz_plane_pcd.points = o3d.utility.Vector3dVector(xyz_plane)
        xyz_plane_rotated_pcd.points = o3d.utility.Vector3dVector(xyz_plane_rotated)
        
        create_pcd(savefilename, xlist)
        
        return xyz_plane_rotated_pcd