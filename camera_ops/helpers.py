from ensenso_nxlib import NxLibCommand, NxLibException, NxLibItem
from ensenso_nxlib.constants import *
import os
import numpy
import open3d as o3d

def open_camera(camera_serial):
    """Opens the camera with the serial stored in camera_serial variable"""
    cmd = NxLibCommand(CMD_OPEN) # Expecifies the execution node name
    cmd.parameters()[ITM_CAMERAS] = camera_serial # Expecfies the camera item to be opened
    try: # Tries to execute the command
        cmd.execute()
    except NxLibException as e: # If the command cannot be executed, prints the error
        print(e.get_error_text())
        print(cmd.result().as_json_meta())
        return

def close_camera():
    """Closes all opened cameras""" 
    close = NxLibCommand(CMD_CLOSE) # Expecifies the execution node name
    try: # Tries to execute the command
        close.execute(wait=False) # Not waiting for the camera to be closed. 
                                  # This allows other code to be run at the same time
    except NxLibException as e: # If the command cannot be executed, prints the error
        print(e.get_error_text())
        print(close.result().as_json_meta())
        return    

def set_camera_parameters(camera_serial, settings_path):
    """Updates the camera settings""" 
    param = json.dumps(json.load(open(settings_path, 'r')))
    itm = NxLibItem()
    camera_node = itm[ITM_CAMERAS][camera_serial] # Expecfies the camera item node
    camera_node << param # Loads the parameters into the camera

def capture_img(camera_serial):
    """Captures with the previous openend camera""" 
    capture = NxLibCommand(CMD_CAPTURE) # Expecifies the execution node name
    capture.parameters()[ITM_CAMERAS] = camera_serial # Reads the parameters for the camera
    try: # Tries to execute the command
        capture.execute()
    except NxLibException as e: # If the command cannot be executed, prints the error
        print(e.get_error_text())
        print(capture.result().as_json_meta())
        return

def rectify_raw_img():
    """Rectifies the captured images to avoid lense distortion"""
    rectification = NxLibCommand(CMD_RECTIFY_IMAGES) # Expecifies the execution node name
    try: # Tries to execute the command
        rectification.execute()
    except NxLibException as e: # If the command cannot be executed, prints the error
        if e.get_error_code() == NXLIB_ITEM_INEXISTENT:
            print(e.get_error_text())
            print(rectification.result().as_json_meta())

def compute_disparity():
    """Compute the disparity map"""
    disparity_map = NxLibCommand(CMD_COMPUTE_DISPARITY_MAP) # Expecifies the execution node name
    try: # Tries to execute the command
        disparity_map.execute()
    except NxLibException as e: # If the command cannot be executed, prints the error
        print(e.get_error_text())
        print(disparity_map.result().as_json_meta())

def filter_nans(point_map):
    """Filters the values where the values are NaN(Not a Number)"""
    return point_map[~numpy.isnan(point_map).any(axis=1)]

def reshape_point_cloud(point_map):
    """Reshapes the point cloud array from (i, j, 3) to ((i * j), 3)""" 
    return point_map.reshape(
          (point_map.shape[0] * point_map.shape[1]), point_map.shape[2])

def _get_camera_node(serial):
    """Finds the camera item matching the serial number"""
    root = NxLibItem()  # References the tree's root
    camera = root[ITM_CAMERAS][serial]  # References the camera
    return camera # Returns the camera item
        
def create_path(path, file_name):
    """Crates the patch by joinning the folder plus the given filename"""
    path = path + file_name + '/'
    if not os.path.exists(path): # If the path doesn't exists, creates it
        os.makedirs(path)
    return path # Returns the path string

def create_point_map(camera_serial):
    """Compute the point map from the disparity map"""
    point_map = NxLibCommand(CMD_COMPUTE_POINT_MAP) # Expecifies the execution node name
    try: # Tries to execute the command
        point_map.execute()
        points = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_POINT_MAP].get_binary_data()
    except NxLibException as e: # If the command cannot be executed, prints the error
        print(e.get_error_text())
        print(point_map.result().as_json_meta())
        return    
    return points
     
def save_point_cloud(points, normals, path, file_name):
    """Saves the point cloud to a pcd file, including the normals"""
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)  
    point_cloud.normals = o3d.utility.Vector3dVector(normals) 
    o3d.io.write_point_cloud(path + file_name + '.pcd', point_cloud, write_ascii=False, compressed=False, print_progress=False)

def compute_normals(camera_serial):
    """Computes the normals using the xyz data from the point map"""
    normals = NxLibCommand(CMD_COMPUTE_NORMALS) # Expecifies the execution node name
    try: # Tries to execute the command
        normals.execute()
        normals = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_NORMALS].get_binary_data()
    except NxLibException as e: # If the command cannot be executed, prints the error
        print(e.get_error_text())
        print(normals.result().as_json_meta())
        return
    return normals

def save_img(path, file_name, camera_serial):
    """Get the item node of the openend camera"""
    camera = _get_camera_node(camera_serial) # Gets the camera item from the tree
     
    save_img_cmd = NxLibCommand(CMD_SAVE_IMAGE) # Expecifies the execution node name
    save_img_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RECTIFIED][ITM_LEFT].path
    save_img_cmd.parameters()[ITM_FILENAME] = path + file_name + '_left.png'
    save_img_cmd.execute() # Execute the command to save the left image

    save_img_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RECTIFIED][ITM_RIGHT].path
    save_img_cmd.parameters()[ITM_FILENAME] = path + file_name + '_right.png'
    save_img_cmd.execute() # Execute the command to save the right image