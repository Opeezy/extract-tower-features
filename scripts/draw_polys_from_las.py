import numpy as np
import laspy
import threading
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import open3d as o3d
from scipy.spatial import ConvexHull, convex_hull_plot_2d

file = "D://Macros//Python//Wolfpack 2.0//_Las_//T_Struct_Clouds.las"

def read(file):
	with laspy.open(file) as fh:
		print('Points from Header:', fh.header.point_count)
		las = fh.read()
		print(las)
		print('Points from data:', len(las.points))    	

	#GRABBING METADATA FROM LAS FILE
	points = np.vstack((las.x, las.y, las.z)).transpose()
	intensity = np.array(las.intensity)
	return_number = np.array(las.return_number)
	number_of_returns = np.array(las.number_of_returns)
	scan_direction_flag = np.array(las.scan_direction_flag)
	edge_of_flight_line = np.array(las.edge_of_flight_line)
	classification = np.array(las.classification)
	synthetic = np.array(las.synthetic)
	key_point = np.array(las.key_point)
	withheld = np.array(las.withheld)
	scan_angle_rank = np.array(las.scan_angle_rank)
	user_data = np.array(las.user_data)
	point_source_id = np.array(las.point_source_id)
	gps_time = np.array(las.gps_time)

	#MASTER ARRAY WITH POINTS AND CORRESPONDING METADATA
	las_data = np.empty([len(points), 16])
	las_data[:, 0] = points[:, 0]
	las_data[:, 1] = points[:, 1]
	las_data[:, 2] = points[:, 2]
	las_data[:, 3] = intensity
	las_data[:, 4] = return_number
	las_data[:, 5] = number_of_returns
	las_data[:, 6] = scan_direction_flag
	las_data[:, 7] = edge_of_flight_line
	las_data[:, 8] = classification
	las_data[:, 9] = synthetic
	las_data[:, 10] = key_point
	las_data[:, 11] = withheld
	las_data[:, 12] = scan_angle_rank
	las_data[:, 13] = user_data
	las_data[:, 14] = point_source_id
	las_data[:, 15] = gps_time

	return las_data

def write(las_data):
	header = laspy.LasHeader(point_format=3, version="1.2")
	header.add_extra_dim(laspy.ExtraBytesParams(name="random", type=np.int32))
	
	new_las = laspy.LasData(header)
	
	new_las.x = las_data[:, 0]
	new_las.y = las_data[:, 1]
	new_las.z = las_data[:, 2]
	new_las.intensity = las_data[:, 3]
	new_las.return_number = las_data[:, 4]
	new_las.number_of_returns = las_data[:, 5]
	new_las.scan_direction_flag = las_data[:, 6]
	new_las.edge_of_flight_line = las_data[:, 7]
	new_las.classification = las_data[:, 8]
	new_las.synthetic = las_data[:, 9]
	new_las.key_point = las_data[:, 10]
	new_las.withheld = las_data[:, 11]
	new_las.scan_angle_rank = las_data[:, 12]
	new_las.user_data = las_data[:, 13]
	new_las.point_source_id = las_data[:, 14]
	new_las.gps_time = las_data[:, 15]
	
	
	new_las.write("D:/Macros/Python/Wolfpack 2.0/Ver_0.2/bin/Barry-Flomation_000001.las")
	print("Written to file")

def dbscan(las_data, eps, min_count):

			'''
			Dbscan requires 3 arguments:

			First being the las data read from file 
			Second being the "EPS" or max distance of points away from each other in cluster 
			Third being the minimum number of points required to create a cluster
			'''
			points = las_data[:, [0,1,2]]
			pcd = o3d.geometry.PointCloud()
			pcd.points = o3d.utility.Vector3dVector(points)

			labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_count))

			classes = las_data[:, 8]
			classes[labels == -1] = 7
			classes[labels > -1] = 6
			noise = las_data[las_data[:, 8] == 7]
			las_data[:, 8] = classes
			max_label = labels.max()

			print(f'{len(noise)} noise points detected')
			
			data = [max_label, noise, las_data, labels]
			return data

def plot_data(data):
	
	max_label = data[0]
	noise = data[1]
	las_data = data[2]
	labels = data[3]

	labeled_points = np.zeros((len(labels), 4))
	labeled_points[:, 0] = labels
	labeled_points[:, 1] = las_data[:, 0]
	labeled_points[:, 2] = las_data[:, 1]
	labeled_points[:, 3] = las_data[:, 2]

	print(labeled_points[0])

	#\\\PLOT POINTS\\\
	for i in range(0, max_label):
			cluster = labeled_points[labeled_points[:, 0] == i]
			cluster = np.delete(cluster, 0, 1)
			cluster = np.delete(cluster, 2, 1)
			hull = ConvexHull(cluster)
			plt.plot(cluster[:,0], cluster[:,1], 'o')
			for simplex in hull.simplices:
				plt.plot(cluster[simplex, 0], cluster[simplex, 1], 'k-')

	plt.show()

las_data = read(file)
las_data = dbscan(las_data, 1, 10)
plot_data(las_data)

