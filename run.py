from stem.stem import Stem
from angle.angle import Angle
from plane.plane import Plane
from point_cloud.point_cloud import Point_cloud
import open3d as o3d
import time

def run(filename):
    # records the starting time when the script was run
    start = time.time()
    
    # creates a new name for the file to be saved based on the original name of the file
    savefilename = filename[:-4] + '_plane' + '.pcd'
    # reads the point cloud from the filename
    pc_raw = o3d.io.read_point_cloud(filename)
       
    # removes outliers and returns the inliners and index 
    pc_inliners, ind = Point_cloud.remove_outliers(pc_raw)
    pc_cleaned = pc_inliners.select_by_index(ind)

    #o3d.visualization.draw_geometries([pc_raw])

    # Finds the segment plane equation for the floor
    floor_a, floor_b, floor_c, floor_d = Plane.get_plane(pc_cleaned)

    # Returns two point clouds: floor and stem
    floor, stem = Stem.create_stem(pc_cleaned, floor_a, floor_b, floor_c, floor_d)
    
    # Finds the segment plane equation for the stem
    stem_a, stem_b, stem_c, stem_d = Plane.get_plane(stem)
    
    # list_points = np.asarray(pc_cleaned.points)
    
    # index = 0
    # deleted = 0
    # list_points_kepts = []
    # print(list_points.size)
    # for line in list_points:
    #     if stem_a * line[0] + stem_b * line[1] + (-stem_c * line[2]) + stem_d < 100:
    #         list_points_kepts.append(list_points)
    #         deleted += 1        
    #         index -= 1
    #         #print(line)
    #     index += 1
        
    # print(list_points.size)
    # print("Deleted: ", deleted, " points")  
    
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(list_points)
    # o3d.visualization.draw_geometries([pcd])

    # save point cloud as pcd
    Point_cloud.save_as_pcd(savefilename, pc_cleaned)
    
    # calculate angles
    Angle.calculate_angles(floor_a, floor_b, floor_c, stem_a, stem_b, stem_c)
    
    # calculates execution time for the program
    end = time.time()
    print("Execution time:", end - start)
    
if __name__ ==  '__main__':
    #filename = sys.argv[1]
    filename = "others/test/5.ply"
    run(filename)