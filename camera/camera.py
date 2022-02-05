from ensenso_nxlib import api
from camera.helpers import *
import datetime
import numpy as np

class Camera:
    def get_point_cloud():
        # Variables
        camera_serial = '217617'
        settings_path = './others/calibrations_and_patterns/parameters_28_01_22_patchmatch.json'
        path = 'test/'
        file_name = str(datetime.datetime.now().strftime('%Y%m%dT%H%M')).split('.')[0]
        file_path = create_path(path, file_name)
        
        # Waits for the cameras to be initialized
        api.initialize()
        
        # Calls functions to start camera, capture and rectify image, create and display point cloud, and close camera
        open_camera(camera_serial)
        set_camera_parameters(camera_serial, settings_path)
        capture_img(camera_serial)
        rectify_raw_img()
        #recalibrate(camera_serial)
        compute_disparity()
        
        # Obtains point cloud and normals, reshapes it, and remove the nan values
        point_cloud = create_point_map(camera_serial)
        point_cloud = reshape_point_cloud(point_cloud)
        normals = compute_normals(camera_serial)
        normals = reshape_point_cloud(normals)
        point_cloud_with_normals = np.concatenate([point_cloud, normals], axis= 1)
        point_cloud_with_normals = filter_nans(point_cloud_with_normals)
        point_cloud, normals = np.hsplit(point_cloud_with_normals, 2)
        
        # Saves point cloud with normals to a .pcd and .xyz file
        save_point_cloud(point_cloud, normals, point_cloud_with_normals, file_path, file_name)
        
        #Saves images from the camera
        save_img(file_path, file_name, camera_serial)
        
        # Closes the camera
        close_camera()    
        return 'Images and point cloud files have been saved in the ' + file_path + ' folder'
