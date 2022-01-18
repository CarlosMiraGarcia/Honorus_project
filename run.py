from stem.stem import Stem
from angle.angle import Angle
from plane.plane import Plane
from point_cloud.point_cloud import Point_cloud
import open3d as o3d
import time
def run():
    start = time.time()
    filename = "others/test/8.ply"
    savefilename = filename[:-4] + '_plane' + '.pcd'
    pc_raw = o3d.io.read_point_cloud(filename)

    pc_inliners, ind = Point_cloud.remove_outliers(pc_raw)
    pc_cleaned = pc_inliners.select_by_index(ind)

    #Returns the plane point cloud
    stem = Stem.create_stem(pc_cleaned, savefilename)
    
    stem_a, stem_b, stem_c, stem_d = Plane.get_plane(stem)
    
    Angle.calculate_angles(Stem.floor_a, Stem.floor_b, Stem.floor_c, stem_a, stem_b, stem_c)
    end = time.time()
    print(end - start)
    
if __name__ ==  '__main__':
    run()