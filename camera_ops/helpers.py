from ensenso_nxlib import NxLibCommand, NxLibException, NxLibItem
from ensenso_nxlib.constants import *
import os
import numpy
import open3d as o3d

def open_camera(camera_serial):
    # Opens the camera with the serial stored in camera_serial variable
    print('Initializing camera...')
    cmd = NxLibCommand(CMD_OPEN)
    cmd.parameters()[ITM_CAMERAS] = camera_serial
    try:
        cmd.execute()
    except NxLibException as e:
        print(e.get_error_text())
        print(cmd.result().as_json_meta())
        print('If you called the getPointCloud end point recently (less than 10 seconds), wait 10 seconds and try again')
        return
    print('Camera initialized')

def close_camera():
    # Closes all open cameras
    print('Closing camera...')
    close = NxLibCommand(CMD_CLOSE)
    try:
        close.execute(wait=False)
    except NxLibException as e:
        print(e.get_error_text())
        print(close.result().as_json_meta())
        return    
    print('Camera closed')

def set_camera_parameters(camera_serial, settings_path):
    # Updates the camera settings
    param = json.dumps(json.load(open(settings_path, 'r')))
    itm = NxLibItem()
    camera_node = itm[ITM_CAMERAS][camera_serial]
    camera_node << param
    #itm[ITM_CAMERAS][camera_serial][ITM_PARAMETERS][ITM_CAPTURE][ITM_PROJECTOR] = True 
    #itm[ITM_CAMERAS][camera_serial][ITM_PARAMETERS][ITM_CAPTURE][ITM_FRONT_LIGHT] = True 
    print('Settings updated')

def capture_img(camera_serial):
    # Captures with the previous openend camera
    print('Capturing image...')
    capture = NxLibCommand(CMD_CAPTURE)
    capture.parameters()[ITM_CAMERAS] = camera_serial
    try:
        capture.execute()
    except NxLibException as e:
        print(e.get_error_code())
        print(capture.result()[ITM_ERROR_TEXT])
        print('If you called the getPointCloud end point recently (less than 10 seconds), wait 10 seconds and try again')
        return
    print('Image captured')

def rectify_raw_img():
    # Rectify the the captures raw images
    rectification = NxLibCommand(CMD_RECTIFY_IMAGES)
    try:
        rectification.execute()
    except NxLibException as e:
        if e.get_error_code() == NXLIB_ITEM_INEXISTENT:
            print(e.get_error_text())
            print(rectification.result().as_json_meta())

def compute_disparity():
    # Compute the disparity map
    disparity_map = NxLibCommand(CMD_COMPUTE_DISPARITY_MAP)
    try:
        disparity_map.execute()
    except NxLibException as e:
        print(e.get_error_text())
        print(disparity_map.result().as_json_meta())

def filter_nans(point_map):
    return point_map[~numpy.isnan(point_map).any(axis=1)]

def reshape_point_cloud(point_map):
    # Reshapes the point cloud array from (m x n x 3) to ((m*n) x 3)
    return point_map.reshape(
          (point_map.shape[0] * point_map.shape[1]), point_map.shape[2])

def _get_camera_node(serial):
    root = NxLibItem()  # References the root
    cameras = root[ITM_CAMERAS][ITM_BY_SERIAL_NO]  # References the cameras subnode
    for i in range(cameras.count()):
        found = cameras[i].name() == serial
        if found:
            return cameras[i]
        
def create_path(path, file_name):
    path = path + file_name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_point_map(camera_serial):
    # Compute the point map from the disparity map
    print('Creating point map...')
    point_map = NxLibCommand(CMD_COMPUTE_POINT_MAP)
    try:
        point_map.execute()
        points = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_POINT_MAP].get_binary_data()
    except NxLibException as e:
        print(e.get_error_text())
        print(point_map.result().as_json_meta())
        return    
    print('Point map created')
    return points
     
def save_point_cloud(points, normals, path, file_name):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)  
    point_cloud.normals = o3d.utility.Vector3dVector(normals)
    
    # Save as pcd file    
    o3d.io.write_point_cloud(path + file_name + '.pcd', point_cloud, write_ascii=False, compressed=False, print_progress=False)

def compute_normals(camera_serial):
    normals = NxLibCommand(CMD_COMPUTE_NORMALS)
    try:
        normals.execute()
        normals = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_NORMALS].get_binary_data()
    except NxLibException as e:
        print(e.get_error_text())
        print(normals.result().as_json_meta())
        return
    return normals

def save_img(path, file_name, camera_serial):
    # Get the item node of the openend camera
    camera = _get_camera_node(camera_serial)
    
    # Save images
    save_img_cmd = NxLibCommand(CMD_SAVE_IMAGE) 
    save_img_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RECTIFIED][ITM_LEFT].path
    save_img_cmd.parameters()[ITM_FILENAME] = path + file_name + '_left.png'
    save_img_cmd.execute()  

    save_img_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RECTIFIED][ITM_RIGHT].path
    save_img_cmd.parameters()[ITM_FILENAME] = path + file_name + '_right.png'
    save_img_cmd.execute()  