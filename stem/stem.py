import open3d as o3d
from stem.helpers import *
from plane.plane import *

class Stem:   
    def create_stem(filename):
        xlist = []
        xyz_plane = []
        xyz_plane_rotated = []
        file_name = filename[:-4] 
        savefilename = file_name + '_plane' + '.pcd'
        
        pcd = o3d.io.read_point_cloud(filename)
        
        Stem.floor_a, Stem.floor_b, Stem.floor_c, Stem.floor_d = Plane.get_plane(pcd)
        
        xlist = read_lines(filename, xlist)
        
        xyz_plane, xyz_plane_rotated = Plane.append_plane_to_pcd(xyz_plane, xyz_plane_rotated, 
                                                                 Stem.floor_a, Stem.floor_b, Stem.floor_c, Stem.floor_d)
        
        xlist = append_points_to_list(xyz_plane, xlist)
        xlist = append_points_to_list(xyz_plane_rotated, xlist)        
      
        xyz_plane_pcd = o3d.geometry.PointCloud()
        xyz_plane_rotated_pcd = o3d.geometry.PointCloud()
        xyz_plane_pcd.points = o3d.utility.Vector3dVector(xyz_plane)
        xyz_plane_rotated_pcd.points = o3d.utility.Vector3dVector(xyz_plane_rotated)
        
        create_pcd(savefilename, xlist)
        pcd = o3d.io.read_point_cloud(savefilename)        
        o3d.visualization.draw_geometries([pcd])
        
        return xyz_plane_rotated_pcd