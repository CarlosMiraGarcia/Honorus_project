from stem.stem import Stem
from angle.angle import Angle
from plane.plane import Plane

def run():
    filename = "others/test/6.xyz"

    stem = Stem.create_stem(filename)
    #stem_a, stem_b, stem_c, stem_d = Plane.get_plane(stem)
    
    #Angle.calculate_angles(Stem.floor_a, Stem.floor_b, Stem.floor_c, stem_a, stem_b, stem_c)
    
if __name__ ==  '__main__':
    run()