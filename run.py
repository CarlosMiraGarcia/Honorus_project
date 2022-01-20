from stem.stem import Stem
from angle.angle import Angle
from plane.plane import Plane
from point_cloud.point_cloud import Point_cloud
import open3d as o3d
import time
import numpy as np

def run(filename):
    # Variables
    list_points_nofloor = []
    list_points_leaves = []
    # Records the starting time when the script was run
    start = time.time()
    
    # Creates a new name for the file to be saved based on the original name of the file
    savefilename = filename[:-4] + '_plane' + '.pcd'
    
    # Reads the point cloud from the filename
    pc_raw = o3d.io.read_point_cloud(filename)
       
    # Removes outliers and returns the inliners and index 
    pc_inliners, ind = Point_cloud.remove_outliers(pc_raw)
    pc_cleaned = pc_inliners.select_by_index(ind)
    list_points = np.asarray(pc_cleaned.points)

    # Finds the segment plane equation for the floor
    floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d = Plane.get_plane(pc_cleaned)

    # Returns two numpy arrays: floor and stem
    floor, stem = Stem.create_stem(pc_cleaned, floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d)

    # Finds the segment plane equation for the stem
    stem_pc = Point_cloud.array_to_point_cloud(stem)
    stem_plane_a, stem_plane_b, stem_plane_c, stem_plane_d = Plane.get_plane(stem_pc)
    
    # Calculate angles
    print("")
    print("\033[4mCalculating angle\033[0m")
    Angle.calculate_angles(floor_plane_a, floor_plane_b, floor_plane_c, stem_plane_a, stem_plane_b, stem_plane_c)
    
    # Removes everything under floor plane
    print("\033[4mRemoving floor from point cloud\033[0m")
    list_points_nofloor = Point_cloud.crop_using_plane(list_points, floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d)
    array_points_nofloor = np.asarray(list_points_nofloor)
    point_cloud_nofloor = Point_cloud.array_to_point_cloud(array_points_nofloor) 
    print("Initial array size: ", list_points.size)
    print("Array size after cropping: ", array_points_nofloor.size)
    print("")
    
    # Removes everything under crops' tray
    print("\033[4mRemoving tray from point cloud\033[0m")
    tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d = Plane.get_plane(point_cloud_nofloor)
    list_points_leaves = Point_cloud.crop_using_plane(array_points_nofloor, tray_plane_a, tray_plane_b, tray_plane_c, tray_plane_d)
    array_points_leaves = np.asarray(list_points_leaves)    
    point_cloud_leaves = Point_cloud.array_to_point_cloud(array_points_leaves)    
    print("Initial array size: ", array_points_nofloor.size)
    print("Array size after cropping: ", array_points_leaves.size)
    
    # Saves point cloud as pcd
    Point_cloud.save_as_pcd(savefilename, point_cloud_leaves)
    
    # Segmentates the leaves into clusters and colours them, returning a list with point clouds for each leaf
    leaf_point_cloud = Point_cloud.leaves_segmentation(point_cloud_leaves)
    
    # Displays each leaf point cloud
    for i in range (len(leaf_point_cloud)):
        o3d.visualization.draw_geometries([Point_cloud.array_to_point_cloud(leaf_point_cloud[i])])
    
    # Calculates execution time for the program
    end = time.time()
    print("")
    print("Execution time:", end - start)
    
if __name__ ==  '__main__':
    #filename = sys.argv[1]
    filename = "others/test/5.xyz"
    run(filename)