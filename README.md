# Honours_project
## Software Engineering - Final Project 
### Measuring the leaf inclination angles of basil plants with a stereo camera

This projects measures the leaf inclination angles of basil plants with the use of a stereo camera. The point clouds generated 
with the stereo camera are used to isolate the leaves and posteriorly segment them. Lastly, the leaf inclinatin angles is measured
used two methods: the best fit plane and the surface normals.

In order to make this project work, an Ensesno 45 stereo camera is needed in order to capture the plants' point clouds. However, a different version of the project, where the point clouds are already taken, will be uploaded.
<br/><br/><br/>

First the point cloud is taken.
<br/>
<img src="https://user-images.githubusercontent.com/72560934/159663968-d739c3d8-50ac-4154-bba0-4793fc31e77b.png" width=600px/>
<br/><br/>
After the outliers removed from the initial point cloud, and with the use of RANSAC, the largest plane is identify in order to remove it from the point cloud and everything under said plane. 
<br/>
This is performed twice: one for the floor plane and another one for the grow tray plane.<br/>
<img src="https://user-images.githubusercontent.com/72560934/159663979-936cffd4-fa4d-4816-958f-3d2cd74c2935.png" width=600px/>
<img src="https://user-images.githubusercontent.com/72560934/159663987-4d1f3f4d-7213-487a-aa4a-0196e8c1ea6c.png" width=600px/>
<br/><br/>
After this, the leafs are segmented using DBSCAN.
<br/>
<img src="https://user-images.githubusercontent.com/72560934/159664020-3a2e0bc0-66f2-41a0-82a1-c4c5b06d909e.png" width=600px/>
<br/><br/>
The zenith vector is calculated using the floor plane equation, and then the leaf inclination angle is calculated between each leaf best fitted plane and the zenith vector. For the second method, the angle is calculated using the surface normals and the zenith vector.
