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

class Read:

	def __init__(self, file):

		self.file = file
	
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
		self.las_data = np.empty([len(points), 16])
		self.las_data[:, 0] = points[:, 0]
		self.las_data[:, 1] = points[:, 1]
		self.las_data[:, 2] = points[:, 2]
		self.las_data[:, 3] = intensity
		self.las_data[:, 4] = return_number
		self.las_data[:, 5] = number_of_returns
		self.las_data[:, 6] = scan_direction_flag
		self.las_data[:, 7] = edge_of_flight_line
		self.las_data[:, 8] = classification
		self.las_data[:, 9] = synthetic
		self.las_data[:, 10] = key_point
		self.las_data[:, 11] = withheld
		self.las_data[:, 12] = scan_angle_rank
		self.las_data[:, 13] = user_data
		self.las_data[:, 14] = point_source_id
		self.las_data[:, 15] = gps_time
		
		self.points = self.las_data[:, [0,1,2]]
		self.x = self.las_data[:, 0]
		self.y = self.las_data[:, 1]
		self.z = self.las_data[:, 2]
		self.intensity = self.las_data[:, 3]
		self.return_number = self.las_data[:, 4]
		self.number_of_returns = self.las_data[:, 5]
		self.scan_direction_fl = self.las_data[:, 6]
		self.edge_of_flight_li = self.las_data[:, 7]
		self.classification = self.las_data[:, 8]
		self.synthetic = self.las_data[:, 9]
		self.key_point = self.las_data[:, 10]
		self.withheld = self.las_data[:, 11]
		self.scan_angle_rank = self.las_data[:, 12]
		self.user_data = self.las_data[:, 13]
		self.point_source_id = self.las_data[:, 14]
		self.gps_time = self.las_data[:, 15]

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

if __name__ == "__main__":
	Read(<FILE PATH>)

