from camera_ops.camera_ops import Camera
from angle_ops import angle_ops
from point_cloud_ops import point_cloud_ops
from plane_ops import plane_ops
import open3d as o3d
import time
import numpy as np
import os
import datetime
import json

def run():
    # Records the starting time when the script was run
    start = time.time()
    file_name = str(datetime.datetime.now().strftime('%Y%m%dT%H%M')).split('.')[0]
    plant_ID = file_name
    
    # Checks for JSON file, if it doesn't exist, creates one
    json_file = "others/data/data.json"
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            f.write('[]')
            
    # Creates an instance of the class Camera and creates a point cloud
    camera = Camera('217617', './others/camera_settings/parameters_28_01_22.json', 'others/data/', file_name)
    camera.get_point_cloud()
        
    # Reads the point cloud from the filename
    pc_raw = o3d.io.read_point_cloud(camera.saving_path + camera.saving_filename + ".pcd")
       
    # Removes outliers and returns the inliners and index 
    pc_cleaned = point_cloud_ops.remove_outliers(pc_raw, 20, 2)
    list_points = np.asarray(np.concatenate([pc_cleaned.points, pc_cleaned.normals], axis= 1))
     
    # Removes everything under floor plane
    print("\033[4mRemoving floor from point cloud\033[0m")
    # Finds the segment plane equation for the floor
    floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d = plane_ops.get_plane(pc_cleaned, 0.5, 1000)
    list_points_nofloor = point_cloud_ops.crop_using_plane(list_points, floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d)
    array_nofloor = np.asarray(list_points_nofloor)
    array_nofloor_points, array_nofloor_normals = np.hsplit(array_nofloor, 2)
    point_cloud_nofloor = point_cloud_ops.array_to_point_cloud_with_normals(array_nofloor_points, array_nofloor_normals) 
    
    # Removes everything under crops' tray
    print("\033[4mRemoving tray from point cloud\033[0m")
    tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d = plane_ops.get_plane(point_cloud_nofloor, 0.5, 3000)
    list_points_no_tray = point_cloud_ops.crop_using_plane(array_nofloor, tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d)
    array_leaves = np.asarray(list_points_no_tray)
    array_leaves_points, array_leaves_normals = np.hsplit(array_leaves, 2)
    point_cloud_leaves = point_cloud_ops.array_to_point_cloud_with_normals(array_leaves_points, array_leaves_normals)    
        
    # Saves point cloud as pcd
    point_cloud_ops.save_as_pcd(camera.saving_path_postprocessing + 'leaves.pcd', point_cloud_leaves)    
    
    # Segmentates the leaves into clusters and colours them, returning a list with point clouds for each leaf
    leaf_data_points_list_points, leaf_data_points_list_normals = point_cloud_ops.leaves_segmentation(point_cloud_leaves, 5, 400)  
    
    # Displays each leaf point cloud
    for i in range (len(leaf_data_points_list_points)):
        point_cloud_ops.save_as_pcd(camera.saving_path_postprocessing + 'leaf_' + str(i + 1) + '.pcd', point_cloud_ops.array_to_point_cloud_with_normals(leaf_data_points_list_points[i], leaf_data_points_list_normals[i]))
    
    # Calculates all the leaf angles
    json_plant = {plant_ID: []}
    leaves = []
    for i in os.listdir(camera.saving_path_postprocessing):
        if os.path.isfile(os.path.join(camera.saving_path_postprocessing,i)) and 'leaf_' in i:
            leaves.append(camera.saving_path_postprocessing + i)    
    for leaf in leaves:
        angle_using_planes, angle_using_normals = angle_ops.calculate_leaf_angle(floor_plane_a, floor_plane_b, floor_plane_c, leaf)
        leaf_id = leaf.rsplit('/')[4][:-4]
        leaf_data = {'leaf_id': leaf_id, 'angle_with_plane': angle_using_planes, 'angle_with_normals': angle_using_normals}
        json_plant[plant_ID].append(leaf_data)
        
    # Appends data to the JSON file            
    with open(json_file) as f:
        json_data = json.load(f)
    with open(json_file, 'w') as f:
        json_data.append(json_plant)
        json.dump(json_data, f)
               
    # Calculates execution time for the program
    end = time.time()
    print("")
    print("Execution time:", end - start)
    
if __name__ ==  '__main__':
    run()           