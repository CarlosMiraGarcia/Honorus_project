import unittest
import numpy as np
from point_cloud_ops import point_cloud_ops
from angle_ops import angle_ops
from plane_ops import plane_ops
import open3d as o3d
import os

class Test_point_cloud_ops(unittest.TestCase):    
    
    def test_remove_outliers(self):
        array_points = np.asarray([[0, 0, 0]])        
        array_points_no_outliers = np.asarray([[0, -3, 0]])   
             
        for i in range (100):
            array_points = np.concatenate((array_points, [[0, -1-i, 0]]), axis=0)
        
        for i in range (94):
            array_points_no_outliers = np.concatenate((array_points_no_outliers, [[0, -4-i, 0]]), axis=0)
            
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(array_points)
        result = point_cloud_ops.remove_outliers(point_cloud, 20, 2)
        

        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertEqual(array_points_no_outliers[i][j], result.points[i][j])

        
    def test_array_to_point_cloud(self):
        array_points = np.random.rand(100, 3)
        result = point_cloud_ops.array_to_point_cloud(array_points)
        
        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertEqual(array_points[i][j], result.points[i][j])
        
        self.assertEqual(array_points.__len__(), result.points.__len__())
        
    def test_array_to_point_cloud_with_normals(self):
        array_points = np.random.rand(100, 3)
        array_normals = np.random.rand(100, 3)
        result = point_cloud_ops.array_to_point_cloud_with_normals(array_points, array_normals)
        
        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertEqual(array_points[i][j], result.points[i][j])
        
        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertEqual(array_normals[i][j], result.normals[i][j])
            
        self.assertEqual(array_points.shape[0], result.points.__len__())
        self.assertEqual(array_normals.shape[0], result.normals.__len__())
        
        
    def test_save_as_pcd(self):
        array_points = np.random.rand(100, 3)
        array_normals = np.random.rand(100, 3) 
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(array_points)
        point_cloud.normals = o3d.utility.Vector3dVector(array_normals)
        
        point_cloud_ops.save_as_pcd("test_files/test3.pcd", point_cloud)
        
        result = o3d.io.read_point_cloud("test_files/test3.pcd")
        os.remove("test_files/test3.pcd")

        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertAlmostEqual(point_cloud.points[i][j], result.points[i][j])
        
        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertAlmostEqual(point_cloud.normals[i][j], result.normals[i][j])
        
    def test_append_points_to_array(self):
        array_1 = np.random.rand(100, 3)
        array_2 = np.random.rand(100, 3) 
        result = point_cloud_ops.append_points_to_array(array_1, array_2)
        
        for i in range(result.__len__()):
            if i >= array_1.shape[0]:
                for j in range (3):
                    self.assertEqual(result[i][j], array_2[i - array_1.shape[0]][j])
            else:
                for j in range (3):
                    self.assertEqual(result[i][j], array_1[i][j])

    def test_crop_using_plane(self):
        array_points = np.asarray([[0, 0, 0]])
        array_normals = np.asarray([[0, 0, 0]])
        array_result = np.asarray([[0, -51, 0]])
        
        for i in range (100):
            array_points = np.concatenate((array_points, [[0, -1-i, 0]]), axis=0)
            array_normals = np.concatenate((array_normals, [[0, -1-i, 0]]), axis=0)
        
        for i in range (49):
            array_result = np.concatenate((array_result, [[0, -52-i, 0]]), axis=0)
            
        array =np.asarray(np.concatenate([array_points, array_normals], axis= 1))
        result = point_cloud_ops.crop_using_plane(array, 0, 1, 0, 46)
        for i in range(result.points.__len__()):
            for j in range (3):
                self.assertEqual(result.points[i][j], array_result[i][j])  
                      
    def test_leaves_segmentation(self):
        point_cloud = o3d.io.read_point_cloud("test_files/test.pcd")
        point_cloud_ops.leaves_segmentation(point_cloud, 5, 400, "test_files/")
        
        leaves = 0
        for i in os.listdir("test_files/"):
            if os.path.isfile(os.path.join("test_files/",i)) and 'leaf_' in i:
                leaves += 1
                os.remove("test_files/" + i)
                
        self.assertEqual(17, leaves)               
        
    def test_calculate_angles(self):
       result = angle_ops._calculate_angles(0, 1, 0, 1, 0, 0)
       self.assertEqual(90, result)
       
    def test_calculate_leaf_angle(self):
        array_points = np.asarray([[0, 0, 0]])        
        array_normals = np.asarray([[0, 1, 0]])   
             
        for i in range (100):
            for j in range (100):
                array_points = np.concatenate((array_points, [[1, -i, 0]]), axis=0)
                array_normals = np.concatenate((array_normals, [[0, -1, 0]]), axis=0)
        
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(array_points)
        point_cloud.normals = o3d.utility.Vector3dVector(array_normals)   
        o3d.io.write_point_cloud("test_files/test2.pcd", point_cloud, write_ascii=False, compressed=True)
        angle_using_planes, angle_using_normals = angle_ops.calculate_leaf_angle(0, 1, 0, "test_files/test2.pcd")
        os.remove("test_files/test2.pcd")
        os.remove("test_files/test2_with_plane.pcd")
        self.assertEqual(180, angle_using_planes)
        self.assertEqual(180, angle_using_normals)
        
    def test_get_plane(self):
        array_points = np.asarray([[0, 0, 0]])        
             
        for i in range (100):
            array_points = np.concatenate((array_points, [[1, -i, 0]]), axis=0)
        
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(array_points)
        result = plane_ops.get_plane(point_cloud, 0.5, 1000)
        point_cloud_plane = np.asarray([0, 0, 1, 0])
        
        for i in range (4):
            self.assertEqual(point_cloud_plane[i], result[i])
            
    def test_create_plane(self):
        array_points = np.asarray([[0, 0, 0]])        
             
        for i in range (2):
            array_points = np.concatenate((array_points, [[1, -i, 0]]), axis=0)
                
        result = plane_ops.create_plane(array_points, 0, 1, 0, 0)
        array_points_plane = []
        for i in range (10):
            for j in range (10):
                array_points_plane.append([i/10, round(j/10 - 1, 1),0])

        for i in range(0, result.shape[0]):
            for j in range (0, 3):
                self.assertEqual(result[i][j], array_points_plane[i][j])  
        
if __name__ == '__main__':
    unittest.main(exit = False)