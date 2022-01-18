from stem.stem import Stem
from angle.angle import Angle
from plane.plane import Plane
import open3d as o3d

def run():
    filename = "others/test/6.xyz"
    savefilename = filename[:-4] + '_plane' + '.pcd'

    #Returns the plane point cloud
    stem = Stem.create_stem(filename, savefilename)
    
    pcd = o3d.io.read_point_cloud(savefilename)
    o3d.visualization.draw_geometries([pcd])

    #stem_a, stem_b, stem_c, stem_d = Plane.get_plane(stem)
    
    #Angle.calculate_angles(Stem.floor_a, Stem.floor_b, Stem.floor_c, stem_a, stem_b, stem_c)
    
if __name__ ==  '__main__':
    run()