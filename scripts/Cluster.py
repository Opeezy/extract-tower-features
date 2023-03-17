import numpy as np
import laspy
import threading
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import open3d as o3d

class Cluster:

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

			print(f'{len(noise)} noise points detected')
			
			data = [max_label, noise, las_data, labels]
			return data

	def ransac(las_data, dis, r_n, loops):

		points = las_data[:, [0,1,2]]
		pcd = o3d.geometry.PointCloud()
		pcd.points = o3d.utility.Vector3dVector(points)	

		plane_model,  inliers = pcd.segment_plane(distance_threshold=dis, ransac_n=r_n, num_iterations=loops)

		[a,b,c,d] = plane_model

		inlier_cloud = pcd.select_by_index(inliers)
		outlier_cloud = pcd.select_by_index(inliers, invert=True)
		inlier_cloud = np.asarray(inlier_cloud.points)
		outlier_cloud = np.asarray(outlier_cloud.points)

		classes = las_data[:, 8]
		classes = np.vstack(classes)
		inliers = np.isin(points, inlier_cloud)
		outliers = np.isin(points, outlier_cloud)

		new_inliers = np.empty([len(inliers), 1])
		new_outliers = np.empty([len(outliers), 1])

		for i in range(0, len(points)):
			ip = inliers[i]
			op = outliers[i]

			if ip.all() == True:
				new_inliers[i] = 1
			else:
				new_inliers[i] = 0

			if op.all() == True:
				new_outliers[i] = 1
			else:
				new_outliers[i] = 0

		classes[new_inliers == 1] = 6
		classes[new_outliers == 1] = 7
		classes = np.hstack(classes)
		las_data[:, 8] = classes
		noise = las_data[las_data[:, 8] == 7]

		print(f'{len(noise)} noise points detected')

		return las_data

		



	