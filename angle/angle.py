import math
import open3d as o3d
import numpy as np
from plane.plane import Plane
from point_cloud.point_cloud import Point_cloud
import statistics

class Angle:
    def calculate_angles(a1, b1, c1, a2, b2, c2):
        """Calculates the angle between two planes:\n
        \ta1 * x + b1 * y + c1 * z + d1 = 0 \n
        and \n
        \ta2 * x + b2*y + c2 * z + d2 = 0"""
        temp = (a1 * a2 + b1 * b2 + c1 * c2)
        e1 = math.sqrt(a1 * a1 + b1 * b1 + c1 * c1)
        e2 = math.sqrt(a2 * a2 + b2 * b2 + c2 * c2)
        temp = temp / (e1 * e2)
        angle = math.degrees(math.acos(temp))

        #print(f'The angle is {angle} degrees')
        #print("")
        return angle
    
    def calculate_leaf_angle(floor_plane_a, floor_plane_b, floor_plane_c, filename):
        pc_leaf = o3d.io.read_point_cloud(filename)
        # Calculate angles
        print("")
        print(f'"\033[4mCalculating angle {filename}\033[0m"')

        line_np_points = np.asarray(pc_leaf.points)
        line_np_normals = np.asarray(pc_leaf.normals)
        
        leaf_plane_a, leaf_plane_b, leaf_plane_c, leaf_plane_d = Plane.get_plane(pc_leaf, 50, 1000)
        
        list_angle = []
        for normal in line_np_normals:
                list_angle.append(Angle.calculate_angles(floor_plane_a, floor_plane_b, floor_plane_c, normal[0], normal[1], normal[2]))
        
        
        #plane = Plane.create_plane(line_np_points, leaf_plane_a, leaf_plane_b, leaf_plane_c, leaf_plane_d)        
        #array_with_plane = Point_cloud.append_points_to_array(line_np_points, plane)
        #pc_with_plane = Point_cloud.array_to_point_cloud(array_with_plane)
        #o3d.visualization.draw_geometries([pc_with_plane])
        print("Using normals", statistics.mean(list_angle) - 90)

        print("Using planes", Angle.calculate_angles(floor_plane_a, floor_plane_b, floor_plane_c, leaf_plane_a, leaf_plane_b, leaf_plane_c) - 90)
