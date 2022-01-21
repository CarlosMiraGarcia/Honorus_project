import open3d as o3d
import numpy as np
from angle.angle import Angle
from plane.plane import Plane
from point_cloud.point_cloud import Point_cloud

def run(filename):
    pc_leaf = o3d.io.read_point_cloud(filename)
    pc_leaf.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=10))

    distances = pc_leaf.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 1.5 * avg_dist   
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
           pc_leaf,
           o3d.utility.DoubleVector([radius, radius * 2]))
    
    np_triangles = np.asanyarray(mesh.triangles)
    # for line in np_triangles:
    #     print(line)
        
    # Calculate angles
    list_angles = []
    list_sum = 0
    print("")
    print("\033[4mCalculating angle\033[0m")
    

    
    line_np = np.asarray(pc_leaf.points)
    floor_plane_a, floor_plane_b, floor_plane_c, floor_plane_d = Plane.get_plane(Point_cloud.array_to_point_cloud(line_np))
    angle = Angle.calculate_angles(0.60, 0.01, 0.80, floor_plane_a, floor_plane_b, floor_plane_c)
    list_angles.append(angle)
    list_sum += angle
    
    avg = list_sum / len(list_angles)
    print(90 - avg)
    
    #o3d.visualization.draw_geometries([mesh] , mesh_show_back_face=True)
if __name__ ==  '__main__':
    #filename = sys.argv[1]
    filename = "others/test/5/leaf_1.pcd"
    run(filename)