import math
import open3d as o3d
import numpy as np
from plane_ops import plane_ops
from point_cloud_ops import point_cloud_ops
import statistics

def _calculate_angles(a1, b1, c1, a2, b2, c2):
    """Calculates the angle between two planes:\n
    \ta1*x + b1*y + c1*z + d1 = 0 \n
    and \n
    \ta2*x + b2*y + c2*z + d2 = 0
    """    
    # Calculates the angle between two planes
    temp = (a1 * a2 + b1 * b2 + c1 * c2)
    e1 = math.sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = math.sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    temp = temp / (e1 * e2)    
    angle = math.degrees(math.acos(temp)) # Converts the angle from radians to degrees
    
    return angle # Returns the angle

def calculate_leaf_angle(floor_plane_a, floor_plane_b, floor_plane_c, filename):
    """Calculates the angle between the zenith and a plane inserte into a leaf point cloud\n
       Requires the floor plane equation (a*x + b*y + c*z+d=0) where:\n
       \tfloor_plane_a = a,\n
       \tfloor_plane_b = b,\n
       \tfloor_plane_c = c,\n
       \tand filename is the leaf point cloud file
       """
    pc_leaf = o3d.io.read_point_cloud(filename) # Reads point cloud from file  
    
    # Gets best fitting plane from the point cloud, returning its plane equation
    leaf_plane_a, leaf_plane_b, leaf_plane_c, leaf_plane_d =  plane_ops.get_plane(pc_leaf, 1, 5000)      
                
    leaf_np_points = np.asarray(pc_leaf.points) # Creates a numpy array with the points
    leaf_np_normals = np.asarray(pc_leaf.normals) # Creates a numpy array with the normals    
        
    # Creates a plane using the point cloud array and the plane equation    
    plane = plane_ops.create_plane(leaf_np_points, leaf_plane_a, leaf_plane_b, leaf_plane_c, leaf_plane_d) 
               
    array_with_plane = point_cloud_ops.append_points_to_array(leaf_np_points, plane) # Inserts plane to the point cloud
    pc_with_plane = point_cloud_ops.array_to_point_cloud(array_with_plane) # Converts array to point cloud class
    point_cloud_ops.save_as_pcd(filename[:-4] + '_with_plane.pcd', pc_with_plane) # Saves point cloud with inserted plane
    
    # Calculates the angles using the plane equation
    # 90 is added to the result to include the distance between the floor plane and the zenit
    angle_using_planes = 90 + _calculate_angles(floor_plane_a, floor_plane_b, floor_plane_c, leaf_plane_a, leaf_plane_b, leaf_plane_c)
    
    # Since we don't know the direction of the leaf
    # this fixes the cases where the leaf is facing backwards
    if angle_using_planes > 180:
        angle_using_planes = 360 - angle_using_planes       

    # Calculates the angles using the normals
    list_angle = []
    for normal in leaf_np_normals:
        list_angle.append(_calculate_angles(floor_plane_a, floor_plane_b, floor_plane_c, normal[0], normal[1], normal[2]))
        
    # Calculates the median from all the angles
    angle_using_normals = statistics.median(list_angle)
    
    return angle_using_planes, angle_using_normals # Returns angles calculations