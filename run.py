from camera.camera import Camera
from angle.angle import Angle
from point_cloud.point_cloud import Point_cloud
from plane.plane import Plane
import open3d as o3d
import time
import numpy as np
import os
import sys

def run(filename):
    # Records the starting time when the script was run
    start = time.time()
    
    # Creates a new name for the file to be saved based on the original name of the file
    folder_path = filename.rsplit('/', 1)
    savefilename_folder_path = folder_path[0] + '/' + str(folder_path[1].split('.', 1)[0] + '/')
    os.makedirs(os.path.dirname(savefilename_folder_path), exist_ok=True)
    
    # Reads the point cloud from the filename
    pc_raw = o3d.io.read_point_cloud(filename)
       
    # Removes outliers and returns the inliners and index 
    pc_inliners, ind = Point_cloud.remove_outliers(pc_raw, 20, 2)
    pc_cleaned = pc_inliners.select_by_index(ind)
    list_points = np.asarray(np.concatenate([pc_cleaned.points, pc_cleaned.normals], axis= 1))
    Point_cloud.save_as_pcd(savefilename_folder_path + 'cleaned.pcd', pc_cleaned)
   
    # ##### Temp ######
    # Returns two numpy arrays: floor and stem
    #floor, stem = Stem.create_stem(floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d)
    # # Add planes to point cloud 
    # array_with_floor_points, array_with_floor_normals = np.hsplit(list_points, 2)

    # array_with_floor = Point_cloud.append_points_to_array(array_with_floor_points, floor)
    # array_with_stem = Point_cloud.append_points_to_array(array_with_floor_points, stem)
    # pc_with_floor = Point_cloud.array_to_point_cloud(array_with_floor)
    # Point_cloud.save_as_pcd(savefilename_folder_path + 'floor_plane.pcd', pc_with_floor)

    # array_with_stem = Point_cloud.append_points_to_array(array_with_floor, stem)
    # pc_with_stem = Point_cloud.array_to_point_cloud(array_with_stem)
    # Point_cloud.save_as_pcd(savefilename_folder_path + 'stem_plane.pcd', pc_with_stem)
    # ##### Temp ######

    # # Finds the segment plane equation for the stem
    # stem_pc = Point_cloud.array_to_point_cloud(stem)
    # stem_plane_a, stem_plane_b, stem_plane_c, stem_plane_d = Plane.get_plane(stem_pc, 0.5)
    
    # # Calculate angles
    # print("")
    # print("\033[4mCalculating angle\033[0m")
    # Angle.calculate_angles(floor_plane_a, floor_plane_b, floor_plane_c, stem_plane_a, stem_plane_b, stem_plane_c)
    
    # Removes everything under floor plane
    print("\033[4mRemoving floor from point cloud\033[0m")
    # Finds the segment plane equation for the floor
    floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d = Plane.get_plane(pc_cleaned, 0.5, 1000)
    list_points_nofloor = Point_cloud.crop_using_plane(list_points, floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d)
    array_points_nofloor = np.asarray(list_points_nofloor)
    array_points_nofloor_points, array_points_nofloor_normals = np.hsplit(array_points_nofloor, 2)
    point_cloud_nofloor = Point_cloud.array_to_point_cloud_with_normals(array_points_nofloor_points, array_points_nofloor_normals) 
    ##### Temp ######
    Point_cloud.save_as_pcd(savefilename_folder_path + 'floor_removed.pcd', point_cloud_nofloor)

    # Removes everything under crops' tray
    print("\033[4mRemoving tray from point cloud\033[0m")
    tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d = Plane.get_plane(point_cloud_nofloor, 0.5, 3000)
    list_points_no_tray = Point_cloud.crop_using_plane(array_points_nofloor, tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d)
    array_points_leaves = np.asarray(list_points_no_tray)
    array_points_leaves_points, array_points_leaves_normals = np.hsplit(array_points_leaves, 2)
    point_cloud_leaves = Point_cloud.array_to_point_cloud_with_normals(array_points_leaves_points, array_points_leaves_normals)    
        
    # Saves point cloud as pcd
    Point_cloud.save_as_pcd(savefilename_folder_path + 'leaves.pcd', point_cloud_leaves)    
    
    # Segmentates the leaves into clusters and colours them, returning a list with point clouds for each leaf
    leaf_data_points_list_points, leaf_data_points_list_normals = Point_cloud.leaves_segmentation(point_cloud_leaves, 4, 400)  
    
    # Displays each leaf point cloud
    for i in range (len(leaf_data_points_list_points)):
        Point_cloud.save_as_pcd(savefilename_folder_path + 'leaf_' + str(i + 1) + '.pcd', Point_cloud.array_to_point_cloud_with_normals(leaf_data_points_list_points[i], leaf_data_points_list_normals[i]))
    
    # Calculates all the leaf angles
    leaves = []
    for i in os.listdir(savefilename_folder_path):
        if os.path.isfile(os.path.join(savefilename_folder_path,i)) and 'leaf_' in i:
            leaves.append(savefilename_folder_path + i)    

    for leaf in leaves:
        Angle.calculate_leaf_angle(floor_plane_a, floor_plane_b, floor_plane_c, leaf)
    
    # Calculates execution time for the program
    end = time.time()
    print("")
    print("Execution time:", end - start)
    
if __name__ ==  '__main__':
    #filename = sys.argv[1]
    filename = "others/test/2.pcd"
    run(filename)           