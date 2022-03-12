from camera_ops.camera_ops import Camera
from angle_ops import angle_ops
from point_cloud_ops import point_cloud_ops
from plane_ops import plane_ops
import open3d as o3d
import numpy as np
import os
import datetime
import json

def run():
    file_name = str(datetime.datetime.now().strftime('%Y%m%dT%H%M')).split('.')[0] # Creates a string with current time stamp
    plant_ID = file_name # Sets the plant_ID to the current time stamp string
    json_plant = {plant_ID: []} # Creates dictionary for the JSON file entry
    leaves = [] # List for the leaves found in the folder
    
    # Checks for the JSON file with the current angles data,
    # if it doesn't exist, creates one
    json_file = "others/data/data.json"
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            f.write('[]')
            
    # Creates an instance of the class Camera and creates a point cloud
    camera = Camera('217617', './others/camera_settings/parameters_28_01_22.json', 'others/data/', file_name)
    camera.get_point_cloud()
        
    # Reads the point cloud from the filename
    pc_raw = o3d.io.read_point_cloud(camera.saving_path + camera.saving_filename + ".pcd")
       
    # Removes outliers and creates a list with the points and normals
    pc_cleaned = point_cloud_ops.remove_outliers(pc_raw, 20, 2)
    array_points = np.asarray(np.concatenate([pc_cleaned.points, pc_cleaned.normals], axis= 1))
     
    # Removes the data points under the floor plane
    floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d = plane_ops.get_plane(pc_cleaned, 0.5, 1000) # Finds the plane equation for the floor
    point_cloud_nofloor = point_cloud_ops.crop_using_plane( 
        array_points, floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d) # Crops the point cloud using the floor's plane equation
    
    # Removes the data points under crop tray plane
    tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d = plane_ops.get_plane(point_cloud_nofloor, 0.5, 3000) # Finds the plane equation for the tray
    point_cloud_leaves = point_cloud_ops.crop_using_plane(np.asarray(np.concatenate(
        [point_cloud_nofloor.points, point_cloud_nofloor.normals], axis= 1)), 
        tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d) # Crops the point cloud using the tray's plane equation
        
    # Saves point cloud as pcd
    point_cloud_ops.save_as_pcd(camera.saving_path_postprocessing + 'leaves.pcd', point_cloud_leaves)    
    
    # Segments the leaves into clusters. Returns a list with points and normals for each leaf
    point_cloud_ops.leaves_segmentation(point_cloud_leaves, 5, 400, camera.saving_path_postprocessing)  

    # Finds all the leaves in the folder, and appends them to the list
    for i in os.listdir(camera.saving_path_postprocessing):
        if os.path.isfile(os.path.join(camera.saving_path_postprocessing,i)) and 'leaf_' in i:
            leaves.append(camera.saving_path_postprocessing + i)
            
    # Calculates the leaf angle for each of the leaves    
    for leaf in leaves:
        angle_using_planes, angle_using_normals = angle_ops.calculate_leaf_angle(floor_plane_a, floor_plane_b, floor_plane_c, leaf)
        leaf_id = leaf.rsplit('/')[4][:-4] # Keeps the leaf filename as the leaf_id
        leaf_data = {'leaf_id': leaf_id, 'angle_with_plane': angle_using_planes, 'angle_with_normals': angle_using_normals}
        json_plant[plant_ID].append(leaf_data) # Appends the data to the dictionary
        
    # Appends data to the JSON file            
    with open(json_file) as f:
        json_data = json.load(f) # Loads content from the JSON file
    with open(json_file, 'w') as f:
        json_data.append(json_plant) # Appends entry to the JSON file content
        json.dump(json_data, f) # Writes the content to the JSON file

if __name__ ==  '__main__':
    run() # Runs the main script