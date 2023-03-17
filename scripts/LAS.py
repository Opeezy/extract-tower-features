import numpy as np
import laspy
import matplotlib as mpl
import matplotlib.pyplot as plt
import open3d as o3d
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from scipy.spatial.distance import cdist
from shapely.geometry import Polygon, Point
import pptk
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import time
import pandas as pd

class Preview:

	def __init__(self, file, fe, fm, se, sm, tol):

		self.file = file
		self.fe = fe 
		self.fm = fm 
		self.se = se 
		self.sm = sm 
		self.tol = tol
	
		with laspy.open(self.file) as fh:
			las = fh.read()

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
		
		self.points = las_data
		self.x = self.points[:, 0]
		self.y = self.points[:, 1]
		self.z = self.points[:, 2]
		self.intensity = self.points[:, 3]
		self.return_number = self.points[:, 4]
		self.number_of_returns = self.points[:, 5]
		self.scan_direction_fl = self.points[:, 6]
		self.edge_of_flight_li = self.points[:, 7]
		self.classification = self.points[:, 8]
		self.synthetic = self.points[:, 9]
		self.key_point = self.points[:, 10]
		self.withheld = self.points[:, 11]
		self.scan_angle_rank = self.points[:, 12]
		self.user_data = self.points[:, 13]
		self.point_source_id = self.points[:, 14]
		self.gps_time = self.points[:, 15]

		d = {
			"X": self.x,
			"Y": self.y,
			"Z": self.z,
			"Intensity": self.intensity,
			"Return #": self.return_number,
			"# of Returns": self.number_of_returns,
			"Scan Direction": self.scan_direction_fl,
			"Edge of Flight": self.edge_of_flight_li,
			"Classification": self.classification,
			"Synthetic": self.synthetic,
			"Key Point": self.key_point,
			"Withheld": self.withheld,
			"Scan Angle Rank": self.scan_angle_rank,
			"User Data": self.user_data,
			"Point Source ID": self.point_source_id,
			"GPS Time": self.gps_time
		}

		self.table = pd.DataFrame(d)

	def draw_polygons(self, e, m):

		points = self.points[:, [0,1,2]]
		pcd = o3d.geometry.PointCloud()
		pcd.points = o3d.utility.Vector3dVector(points)
		labels = np.array(pcd.cluster_dbscan(eps=e, min_points=m))
		max_label = labels.max()
		labeled_points = np.empty((len(labels), 4))
		labeled_points[:, 0] = labels
		labeled_points[:, 1] = self.x
		labeled_points[:, 2] = self.y
		labeled_points[:, 3] = self.z

		for i in range(0, max_label):

			cluster = labeled_points[labeled_points[:, 0] == i]
			cluster = np.delete(cluster, 0, 1)
			cluster = np.delete(cluster, 2, 1)
			hull = ConvexHull(cluster)
			plt.plot(cluster[:,0], cluster[:,1], 'or')

			for simplex in hull.simplices:
				plt.plot(cluster[simplex, 0], cluster[simplex, 1], 'k-')

		plt.tile(f"Towers detected: {max_label}")
		plt.show()

	
file = sys.argv[1]
fe = input("First scan eps: ")
fm = input("First scan min: ")
se = input("Second scan eps: ")
sm = input("Second scan min: ")
tol = input("Tolerance: ")

P = Preview(file,fe,fm,se,sm,tol)

	

	#def tops(self, e, m, tolerance):
#
	#	max_label = data[0]
	#	labeled_points = data[1]
	#	unique_tops = []		
	#	pole_tops = []		
#
	#	for i in range(0, max_label):
#
	#		#Defining our tower as a cluster
	#		cluster = labeled_points[labeled_points[:, 0] == i]
	#		cluster = np.delete(cluster, 0, 1)
#
	#		#Finding highest Z point and coordinate as well as defining our tolerance to seach for other high points
	#		highest_z = cluster[:, 2].max()
	#		highest_point = cluster[cluster[:, 2] == highest_z]
	#		tolerance = highest_z - tol
#
	#		#Gathering our highest points that are within the tolerance we set
	#		high_points = cluster[cluster[:, 2] > tolerance]
#
	#		for j in high_points:
#
	#			unique_tops.append(j)
#
	#	unique_tops = np.vstack(unique_tops)
	#	tops = Lasso.dbscan(unique_tops, e, m)
	#	tops_to_plot = tops		
#
	#	max_label_tops = tops[0]
	#	labeled_tops = tops[1]		
#
	#	for t in range(0, max_label_tops):
#
	#		cluster = labeled_tops[labeled_tops[:, 0] == t]
	#		cluster = np.delete(cluster, 0, 1)
	#		cluster_z = cluster[:, 2]			
	#		max_height = max(cluster_z)
#
	#		pt = cluster[cluster[:, 2] == max_height]
	#		pt = pt[0]
	#		pt = f"{pt[0]},{pt[1]},{pt[2]}"
	#		pole_tops.append(pt)	
#
	#	data = [tops_to_plot, pole_tops,  max_label]
	#	return data

