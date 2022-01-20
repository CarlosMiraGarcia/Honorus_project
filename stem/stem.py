import open3d as o3d
from plane.plane import *
from point_cloud.point_cloud import *

class Stem:   
    def create_stem(point_cloud, floor_a, floor_b, floor_c, floor_d):

        # Returns two numpy arrays
        xyz_plane, xyz_plane_rotated = Plane.create_planes(floor_a, floor_b, floor_c, floor_d)     
        
        return xyz_plane, xyz_plane_rotated