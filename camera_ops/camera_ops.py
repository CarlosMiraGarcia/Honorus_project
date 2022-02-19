from ensenso_nxlib import api
from camera_ops.helpers import *
import numpy as np

class Camera:
    def __init__(self, serial, settings_path, saving_path, filename):
        """Sets the variables for the class where:\n
        \tserial is the camera serial,
        \tsettings_path is where camera settings are saved,
        \tsaving_path is where the point clouds will be save,
        \tand filename is the name for the saved point cloud file"""
        self.serial = serial
        self.settings_path = settings_path
        self.saving_filename = filename
        self.saving_path = create_path(saving_path, self.saving_filename)
        self.saving_path_postprocessing = create_path(self.saving_path, 'pp')

    def get_point_cloud(self):
        """Uses the stereo camera to create a point cloud"""      
        api.initialize() # Initializes the library and waits for the connected cameras to be enumerated
        
        open_camera(self.serial) # Opens the camera using the serial
        set_camera_parameters(self.serial, self.settings_path) # Loads the current parameters to the camera
        capture_img(self.serial) # Captures images
        rectify_raw_img() # Rectifies the images
        compute_disparity() # Creates a disparity map
       
        point_cloud = create_point_map(self.serial) # Creates a point map from the disparity map
        point_cloud = reshape_point_cloud(point_cloud) # Reshapes the point map to the right shape (x, y ,z)
        normals = compute_normals(self.serial) # Compute the normals using the x, y, z data
        normals = reshape_point_cloud(normals) # Reshapes the normals to the right shape (x, y, z)
        point_cloud_with_normals = np.concatenate([point_cloud, normals], axis= 1) # Joins both arrays 
        point_cloud_with_normals = filter_nans(point_cloud_with_normals) # Filters Not a Number values from the array
        point_cloud, normals = np.hsplit(point_cloud_with_normals, 2) # Divides the array into two arrays: points and normals        
        
        save_point_cloud(point_cloud, normals, self.saving_path, self.saving_filename) # Saves point cloud with normals to a .pcd file
        save_img(self.saving_path, self.saving_filename, self.serial) #Saves images from the camera
        close_camera() # Closes the camera    
        return 'Images and point cloud files have been saved in the ' + self.saving_path + ' folder'
