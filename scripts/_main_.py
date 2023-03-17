import numpy as np
import laspy
import threading
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import open3d as o3d
from scipy.spatial import ConvexHull, convex_hull_plot_2d


class lasso:

	##\\\Opens las file and returns np array of points (argument takes las file you want to read)\\\
	#def read(file):
	#	with laspy.open(file) as fh:
	#		print('Points from Header:', fh.header.point_count)
	#		las = fh.read()
	#		print(las)
	#		print('Points from data:', len(las.points))
	#		ground_pts = las.classification == 2
	#		bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
	#		print('Ground Point Return Number distribution:')
	#		for r,c in zip(bins,counts):
	#			print('    {}:{}'.format(r,c))
	#	points = np.vstack((las.x, las.y, las.z)).transpose()
	#	return points 

	#\\\RETURNS ARRAY OF SEPERATED OBSTACLES\\\ 
	def find_clusters(e, m, f, l):
	
		with laspy.open(f) as fh:
			hc = fh.header.point_count
			print('Points from Header:', fh.header.point_count)
			las = fh.read()
			#class_pts = las.classification == c
			print(las)
			las_len = len(las.points)
			print('Points from data:', len(las.points))

		#class_pts = np.vstack(class_pts)	
		points = np.vstack((las.x, las.y, las.z)).transpose()
		#points = np.hstack((class_pts, points))
		#points = points[points[:, 0] == 1]
		#points = points[:, [1,2,3]]
		pcd = o3d.geometry.PointCloud()
		pcd.points = o3d.utility.Vector3dVector(points)
		o3d.io.write_point_cloud("las.ply", pcd)
		noise = []     
		clusters = []
		#labels = np.array(pcd.cluster_dbscan(eps=e, min_points=m))
		pcd_array = np.asarray(pcd.points)
		#max_label = labels.max()
		#noise = (labels == -1).sum()

		master = np.empty([len(pcd_array), 5])
		indexes = np.arange(len(pcd_array))
		labels = np.zeros((len(pcd_array)))
		master[:, 0] = labels
		master[:, 1] = indexes
		master[:, 2] = pcd_array[:, 0]
		master[:, 3] = pcd_array[:, 1]
		master[:, 4] = pcd_array[:, 2]

		for i in range(l):
			print(i, "iteration")
			print(len(master[master[:, 0] == -1]), "noise")

			sub_array = master[master[:, 0] > -1]
			points = sub_array[:, [2,3,4]]
			sub_indexs = sub_array[:, 1]		
			pcd.points = o3d.utility.Vector3dVector(points)
			labels = np.array(pcd.cluster_dbscan(eps=e, min_points=m))

			labeled = np.empty([len(points), 5])
			labeled[:, 0] = labels
			labeled[:, 1] = sub_indexs
			labeled[:, 2] = points[:, 0]
			labeled[:, 3] = points[:, 1]
			labeled[:, 4] = points[:, 2]
			rows_to_add = len(master)-len(labeled)
			filler = np.zeros((rows_to_add, 5))
			labeled = np.vstack((labeled, filler))
			print(len(labeled))
			print(len(master))

			master[master[:, 1] == labeled[:, 1]] = labeled[labeled[:, 1] == master[:, 1]]

		labels = master[:, 0]
		max_label = labels.max()
		noise = (labels == -1).sum()
		points_labeled = master[:, [0,2,3,4]]
		points = master[:, [2,3,4]]
		pcd.points = o3d.utility.Vector3dVector(points)


		logs = [pcd, labels, max_label, noise, points_labeled, hc, las, las_len]
		return logs



			#print("Plugging into master")
			#for j in range(0, len(master_index)):
			#	print(f"{j}/{len(master_index)}")
			#	index = master_index[j]
			#	to_insert = labeled[labeled[:, 0] == index]
			#	to_insert = to_insert[0]
			#	to_insert = np.array([to_insert[1], to_insert[2], to_insert[3], to_insert[4]])
			#	master[j] = to_insert


	

			
		
			
	
			
		



		#for i in range(0, len(pcd)):
		#	p=pcd[i]
		#	labeled = np.array([labels[i], p[0], p[1], p[2]])
		#	labeled_pcd[i] = labeled

		#noise_points = labeled_pcd[labeled_pcd[:, 0] == -1]
#
#
		#logs = [pcd, labels, max_label, noise, labeled_pcd, hc, las, las_len]
		#return logs

	

	 
		


					
		
	   
	



	

	
 


