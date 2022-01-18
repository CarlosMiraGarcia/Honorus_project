def read_lines(filename):
    list = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            x, y, z = [i for i in lines.split(' ')]
            list.append(x + " " + y +  " " + z)
    return list

def create_pcd(savefilename, list):
    with open(savefilename, 'w') as file_to_write:
        file_to_write.write("# .PCD v0.7 - Point Cloud Data file format\n")
        file_to_write.write("VERSION 0.7\n")
        file_to_write.write("FIELDS x y z\n")
        file_to_write.write("SIZE 4 4 4\n")
        file_to_write.write("TYPE F F F\n")
        file_to_write.write("COUNT 1 1 1\n")
        file_to_write.write("WIDTH " + str(len(list)) + "\n")
        file_to_write.write("HEIGHT 1\n")
        file_to_write.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        file_to_write.write("POINTS " + str(len(list)) + "\n")
        file_to_write.write("DATA ascii\n")

        for i in list:
            file_to_write.write(i + '\n')
            
def append_points_to_list(points, list):
    for line in points:
        list.append(str(line[0]) + " " + str(line[1]) + " " + str(line[2]))
    return list
