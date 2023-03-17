import numpy as np
import laspy
import threading
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import open3d as o3d

class Dbscan:

	def cluster(las_data):
			noise = las_data[las_data[:, 8] == 7]
			print(f'{noise.sum()}')
			points = las_data[:, [0,1,2]]
			pcd = o3d.geometry.PointCloud()
			pcd.points = o3d.utility.Vector3dVector(points)		
			labels = np.array(pcd.cluster_dbscan(eps=2, min_points=10))		
			classes = las_data[:, 8]
			classes[labels == -1] = 7
			classes[labels > -1] = 6
			noise = las_data[las_data[:, 8] == 7]
			las_data[:, 8] = classes
			
			return las_data
	



	