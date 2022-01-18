from ensenso_nxlib import api
from camera.helpers import *
import datetime

class Camera:
    def get_point_cloud():
        camera_serial = '217617'
        settings_path = './others/calibrations_and_patterns/latest_settings_carlos_patchmatch.json'
        path = 'test/'
        file_name = str(datetime.datetime.now().strftime('%Y%m%dT%H%M')).split('.')[0]

        # Waits for the cameras to be initialized
        api.initialize()

        # Calls functions to start camera, capture and rectify image, create and display point cloud, and close camera
        open_camera(camera_serial)
        set_camera_parameters(camera_serial, settings_path)
        capture_img(camera_serial)
        rectify_raw_img()
        #recalibrate(camera_serial)
        compute_disparity()
        point_cloud = create_point_map(camera_serial)
        point_cloud = reshape_point_cloud(point_cloud)
        point_cloud = filter_nans(point_cloud)
        path = create_path(path, file_name)
        save_point_cloud(point_cloud, path, file_name)
        save_img(path, file_name, camera_serial)
        save_ply(path, file_name, camera_serial)
        close_camera()
        return_str = 'Images and point cloud files have been saved in the ' + path + ' folder'
        return return_str
