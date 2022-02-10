from ensenso_nxlib import api
from camera.helpers import *
import numpy as np

class Camera:
    def __init__(self, serial, settings_path, saving_path, filename):
        self.serial = serial
        self.settings_path = settings_path
        self.saving_filename = filename
        self.saving_path = create_path(saving_path, self.saving_filename)

    def get_point_cloud(self):      
        # Waits for the cameras to be initialized
        api.initialize()
        
        # Calls functions to start camera, capture and rectify image, create and display point cloud, and close camera
        open_camera(self.serial)
        set_camera_parameters(self.serial, self.settings_path)
        capture_img(self.serial)
        rectify_raw_img()
        #recalibrate(self.serial)
        compute_disparity()
        
        # Obtains point cloud and normals, reshapes it, and remove the nan values
        point_cloud = create_point_map(self.serial)
        point_cloud = reshape_point_cloud(point_cloud)
        normals = compute_normals(self.serial)
        normals = reshape_point_cloud(normals)
        point_cloud_with_normals = np.concatenate([point_cloud, normals], axis= 1)
        point_cloud_with_normals = filter_nans(point_cloud_with_normals)
        point_cloud, normals = np.hsplit(point_cloud_with_normals, 2)
        
        # Saves point cloud with normals to a .pcd and .xyz file
        save_point_cloud(point_cloud, normals, point_cloud_with_normals, self.saving_path, self.saving_filename)
        
        #Saves images from the camera
        save_img(self.saving_path, self.saving_filename, self.serial)
        save_ply(self.saving_path, self.saving_filename)
        # Closes the camera
        close_camera()    
        return 'Images and point cloud files have been saved in the ' + self.saving_path + ' folder'
