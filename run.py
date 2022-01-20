from stem.stem import Stem
from angle.angle import Angle
from plane.plane import Plane
from point_cloud.point_cloud import Point_cloud
import open3d as o3d
import time
import numpy as np

def run(filename):
    # Variables
    index = 0
    kept = 0
    list_points_kept = []
    diff_adj = 5
    # Records the starting time when the script was run
    start = time.time()
    
    # Creates a new name for the file to be saved based on the original name of the file
    savefilename = filename[:-4] + '_plane' + '.pcd'
    # Reads the point cloud from the filename
    pc_raw = o3d.io.read_point_cloud(filename)
       
    # Removes outliers and returns the inliners and index 
    pc_inliners, ind = Point_cloud.remove_outliers(pc_raw)
    pc_cleaned = pc_inliners.select_by_index(ind)

    #o3d.visualization.draw_geometries([pc_raw])

    # Finds the segment plane equation for the floor
    floor_a, floor_b, floor_c, floor_d = Plane.get_plane(pc_cleaned)

    # Returns two numpy arrays: floor and stem
    floor, stem = Stem.create_stem(pc_cleaned, floor_a, floor_b, floor_c, floor_d)
    
    # Inserts planes into original point cloud
    #np_array_cleaned = Point_cloud.read_lines(pc_cleaned)
    #np_array_cleaned = Point_cloud.append_points_to_array(floor, np_array_cleaned)
    #np_array_cleaned = Point_cloud.append_points_to_array(stem, np_array_cleaned)  
    #pc_cleaned = Point_cloud.array_to_point_cloud(np_array_cleaned)

    #o3d.visualization.draw_geometries([pc_cleaned])
    
    # Finds the segment plane equation for the stem
    stem_pc = Point_cloud.array_to_point_cloud(stem)
    stem_a, stem_b, stem_c, stem_d = Plane.get_plane(stem_pc)
    
    # Removes everything under plane
    list_points = np.asarray(pc_cleaned.points)    

    print("Initial array size: ", list_points.size)
    for line in list_points:
        if (floor_a * line[0]) + (floor_b * line[1]) + (floor_c * line[2]) > - floor_d + diff_adj:
            list_points_kept.append(line)
            kept += 1        
            index -= 1
        index += 1
        
    array_points_kept = np.asarray(list_points_kept)
    print("Array size after cropping: ", array_points_kept.size)
    
    point_cloud_kept = Point_cloud.array_to_point_cloud(array_points_kept)
    o3d.visualization.draw_geometries([point_cloud_kept])

    # Save point cloud as pcd
    Point_cloud.save_as_pcd(savefilename, point_cloud_kept)
    
    # Calculate angles
    Angle.calculate_angles(floor_a, floor_b, floor_c, stem_a, stem_b, stem_c)
    
    # Calculates execution time for the program
    end = time.time()
    print("Execution time:", end - start)
    
if __name__ ==  '__main__':
    #filename = sys.argv[1]
    filename = "others/test/5.ply"
    run(filename)