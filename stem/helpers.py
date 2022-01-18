import numpy as np
import open3d as o3d
def read_lines(point_cloud):
    
    list = np.asarray(point_cloud.points)
    return list

def create_pcd(savefilename, pc_array):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc_array)
    o3d.io.write_point_cloud(savefilename, pcd, write_ascii=True, compressed=True)
            
def append_points_to_list(npa1, npa2):
    npa = np.vstack((npa1, npa2))
    return npa
