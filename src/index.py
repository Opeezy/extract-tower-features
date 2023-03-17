#imports
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import open3d as o3d
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from scipy.spatial.distance import cdist
from shapely.geometry import Polygon, Point
import pptk
import logging
import traceback

#local imports
from lasreader import Read

class MainWindow:
	def __init__(self):

		def err_win(err):

			def kill():
				err_win.destroy()

			err_win = Tk()
			err_win.title("Error")
			err_win.geometry("400x150")
			err_win.resizable(False, False)
			err_win.focus_force()

			err_frame = Frame(err_win, relief=SUNKEN)
			err_frame.pack(fill=BOTH, expand=True)

			err_label = Label(err_frame, text=err, bg="white", relief=SUNKEN, bd=0, height=5)
			err_label.pack(side=TOP, fill=BOTH, expand=True)

			btn_frame = Frame(err_frame, relief=SUNKEN, bd=0)
			btn_frame.pack(side=TOP, fill=BOTH, expand=True)

			btn = Button(btn_frame, command=kill, text='Ok', width=10)
			btn_frame = Frame(err_frame, relief=SUNKEN, bd=0, bg='black')
			btn.pack(side=RIGHT, padx=10, pady=2)

			err_win.mainloop()

		def ask_for_scan_settings():
			self.scan_win.pack(fill=X, expand=True, side=BOTTOM)
			self.eps_label.pack(fill=X, expand=True, side=LEFT)
			self.eps_entry.pack(fill=X, expand=True, side=LEFT)
			self.min_label.pack(fill=X, expand=True, side=LEFT)
			self.min_entry.pack(fill=X, expand=True, side=LEFT)

		def refresh_plot():
			try:
				self.canvas.get_tk_widget().pack_forget() 
				self.tool_bar.pack_forget()		

				# the figure that will contain the plot
				self.fig = Figure(figsize = (5, 5), dpi = 100)
	
				# adding the subplot
				self.plot1 = self.fig.add_subplot(111)
	
				# creating the Tkinter canvas
				# containing the Matplotlib figure
				self.canvas = FigureCanvasTkAgg(self.fig, master = self.window)
				self.canvas.draw()
				self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
	
				# placing the canvas on the Tkinter window
				self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
	
				# creating the Matplotlib toolbar
				self.tool_bar = NavigationToolbar2Tk(self.canvas, self.window, pack_toolbar=False)
				self.tool_bar.update()
				self.tool_bar.pack(side=BOTTOM, fill=X)
				
			except Exception as e:
				err_win(e)

		def load_points():
			try:
				self.files = fd.askopenfilenames()
	
				for file in self.files:
					points = Read(file).points
					self.points_list.append(points)

				refresh_plot()	

				for points in self.points_list:
					self.plot1.plot(points[:, 0], points[:, 1], '.')

			except Exception as e:
				err_win(e)

		def unload_points():
			try:
				self.points_list = []
				self.clusters = []
				self.tops = []

				refresh_plot()

			except Exception as e:
				err_win(e)

		def draw_polygons():
			try:
				if self.eps_entry_one.get() == "" or self.min_entry_one.get() == "":
					err_win("Fill required fields")

				else:
					self.eps = float(self.eps_entry_one.get())
					self.min = int(self.min_entry_one.get())
	
					refresh_plot()
				
					for points in self.points_list:
						self.plot1.plot(points[:, 0], points[:, 1], 'b.')
		
						pcd_points = points
						pcd = o3d.geometry.PointCloud()
						pcd.points = o3d.utility.Vector3dVector(pcd_points)
						labels = np.array(pcd.cluster_dbscan(eps=self.eps, min_points=self.min, print_progress=True))
						self.max_label = labels.max()
						labeled_points = np.empty((len(labels), 4))
						labeled_points[:, 0] = labels
						labeled_points[:, 1] = pcd_points[:, 0]
						labeled_points[:, 2] = pcd_points[:, 1]
						labeled_points[:, 3] = pcd_points[:, 2]			
						
						for i in range(0, self.max_label):		
							cluster = labeled_points[labeled_points[:, 0] == i]
							cluster = np.delete(cluster, 0, 1)
							self.clusters.append(cluster)
							cluster = np.delete(cluster, 2, 1)
							hull = ConvexHull(cluster)
		
							for simplex in hull.simplices:		
								self.plot1.plot(cluster[simplex, 0], cluster[simplex, 1], 'r-')

			except Exception as e:
				err_win(e)

		def draw_tops():
			try:
				if self.eps_entry_two.get() == "" or self.min_entry_two.get() == "":
					err_win("Fill required fields")

				else:
					refresh_plot()

					for cluster in self.clusters:
							# Plotting our original towers
							self.plot1.plot(cluster[:, 0], cluster[:, 1], 'b.')
	
							# Defining highest point in cluster and tolerance
							z_values = cluster[:, 2]
							max_z = max(z_values)							
							self.tolerance = int(self.tolerance_entry.get())
	
							# Defining height window to find points within
							window = max_z - self.tolerance
							points_in_window = cluster[cluster[:, 2] > window]
							self.points_in_window.append(points_in_window)

							groups = []
							centroids_raised = []

							# Finding distances of each point compared to each other
							dist = cdist(points_in_window, points_in_window)
							for d in dist:
								group = []
								for k, v in enumerate(d):
									if v < 3:
										group.append(k)
								groups.append(group)

							tops = list(set(map(tuple, groups)))
							print(f"TOPS:: {tops}\nn")
							
							for t in tops:
								points = [points_in_window[index] for index in t]
								points = np.vstack(points)

								self.plot1.plot(points[:, 0], points[:, 1], 'r.')

								top_of_pole = max(points[:, 2])
								poly = list(map(tuple, points))
								if len(poly) >=4:									
									poly = Polygon(poly)
									center = poly.centroid
									top_point = [center.x, center.y, top_of_pole]									
	
									self.plot1.plot(top_point[0], top_point[1], 'Xy')
								else:
									pass
								
										

							

							## Run dbscan again to find individual tops
							#eps_two = float(self.eps_entry_two.get())
							#min_two = int(self.min_entry_two.get())
							#print(f"DBSCAN WITH EPS:: {eps_two} AND MIN:: {min_two}")
							#pcd = o3d.geometry.PointCloud()
							#pcd.points = o3d.utility.Vector3dVector(points_in_window)
							#labels = np.array(pcd.cluster_dbscan(eps=eps_two, min_points=min_two))
	#
							## Local max_label var assigned to individual clusters within the parent cluster
							#max_label = labels.max()
	#
							#labeled_points = np.empty((len(labels), 4))
							#labeled_points[:, 0] = labels
							#labeled_points[:, 1] = points_in_window[:, 0]
							#labeled_points[:, 2] = points_in_window[:, 1]
							#labeled_points[:, 3] = points_in_window[:, 2]
#
							#self.plot1.plot(points_in_window[:, 0], points_in_window[:, 1], 'y.')	
	#
							#for i in range(0, max_label):							
							#	# defining our tops
							#	top = labeled_points[labeled_points[:, 0] == i]
							#	top = np.delete(top, 0, 1)
							#	self.tops.append(top)
							#	top = np.delete(top, 2, 1)
							#	top_hull = ConvexHull(top)
	#
							#	self.plot1.plot(top[:, 0], top[:, 1], 'g.')
			#
							#	for top_simplex in top_hull.simplices:			
							#		self.plot1.plot(top[top_simplex, 0], top[top_simplex, 1], 'r-')					

			except Exception as e:
				print(traceback.format_exc())
				err_win(e)

		def view_3D():
			try:
				if len(self.points_list) == 0:
					err_win("No points loaded") 

				else:
					if len(self.tops) == 0:				
						points = np.vstack(self.points_list)
						rgb = np.full((len(points), 3), [0, 255, 0])
						v = pptk.viewer(points, rgb) 

					else:	
						points_in_window = np.vstack(self.points_in_window)				
						tops = np.vstack(self.tops)						
						towers = np.vstack(self.points_list)
						points = np.vstack((points_in_window, tops, towers))						

						rgb_points_in_window = np.full((len(points_in_window), 3), [255, 255, 0])
						rgb_tops = np.full((len(tops), 3), [0, 255, 0])
						rgb_towers = np.full((len(towers), 3), [0, 0, 255])
						rgb = np.vstack((rgb_points_in_window, rgb_tops, rgb_towers))

						v = pptk.viewer(points, rgb)
						v.set(point_size=.5) 

			except Exception as e:
				err_win(e)

		def enable_scan():
			try:
				if self.scan_check_VAR.get() == 1:	
					self.eps_entry_one.config(state=NORMAL)
					self.min_entry_one.config(state=NORMAL)
					self.eps_entry_two.config(state=NORMAL)
					self.min_entry_two.config(state=NORMAL)
					self.tolerance_entry.config(state=NORMAL)
	
				else:	
					self.eps_entry_one.config(state=DISABLED)
					self.min_entry_one.config(state=DISABLED)
					self.eps_entry_two.config(state=DISABLED)
					self.min_entry_two.config(state=DISABLED)
					self.tolerance_entry.config(state=DISABLED)

			except Exception as e:
				err_win(e)

		# settings for initial scan
		self.eps = float(0)
		self.min = 0
		self.tolerance = 0

		# number of cluster found on initial scan and a list of the clusters
		self.points_list = []
		self.max_label = 0
		self.clusters = []
		self.points_in_window = []
		self.tops = []
	
		# The main tkinter window
		self.window = Tk()		
		self.window.title('Tower Planimetrics')		
		self.window.geometry("1000x750")
		self.window.resizable(False, False)
		
		# creating the menu bar
		self.menu_bar = Menu(self.window)
		self.file_menu = Menu(self.menu_bar, tearoff=0)
		self.points_menu = Menu(self.menu_bar, tearoff=0)
		self.draw_menu = Menu(self.menu_bar, tearoff=0)
		
		self.points_menu.add_command(label="Unload points", command=unload_points)
		self.points_menu.add_command(label="Load Points", command=load_points)
		self.points_menu.add_command(label="View 3D", command=view_3D)
		self.draw_menu.add_command(label="Draw poly", command=draw_polygons)
		self.draw_menu.add_command(label="Draw tops", command=draw_tops)
		
		self.menu_bar.add_cascade(label="File", menu=self.file_menu)
		self.menu_bar.add_cascade(label="Points", menu=self.points_menu)
		self.menu_bar.add_cascade(label="Draw", menu=self.draw_menu)

		# the figure that will contain the plot
		self.fig = Figure(figsize = (5, 5), dpi = 100)
		
		# adding the subplot
		self.plot1 = self.fig.add_subplot(111)		
		
		# creating the Tkinter canvas
		# containing the Matplotlib figure
		self.canvas = FigureCanvasTkAgg(self.fig, master = self.window)  
		self.canvas.draw()
		
		# placing the canvas on the Tkinter window
		self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
		
		# creating the Matplotlib toolbar
		self.tool_bar = NavigationToolbar2Tk(self.canvas, self.window, pack_toolbar=False)
		self.tool_bar.update()
		self.tool_bar.pack(side=TOP, fill=X)
		self.window.config(menu=self.menu_bar)

		# first scan settings frame
		self.scan_win = Frame(self.window)

		# labels
		self.scan_label_one = Label(self.scan_win, text='First Scan')
		self.scan_label_two = Label(self.scan_win, text='Second Scan')

		# check button
		self.scan_check_VAR = IntVar(0)
		self.scan_check = Checkbutton(self.scan_win, var=self.scan_check_VAR, command=enable_scan)

		# eps setting
		self.eps_label_one = Label(self.scan_win, text='EPS:')		
		self.eps_entry_one = Entry(self.scan_win)
		self.eps_entry_one.insert(0, '10')
		self.eps_entry_one.config(state=DISABLED)
		self.eps_label_two = Label(self.scan_win, text='EPS:')		
		self.eps_entry_two = Entry(self.scan_win)
		self.eps_entry_two.insert(0, '1')
		self.eps_entry_two.config(state=DISABLED)				

		# min setting
		self.min_label_one = Label(self.scan_win, text='MIN:')	
		self.min_entry_one = Entry(self.scan_win)
		self.min_entry_one.insert(0, '15')	
		self.min_entry_one.config(state=DISABLED)
		self.min_label_two = Label(self.scan_win, text='MIN:')	
		self.min_entry_two = Entry(self.scan_win)
		self.min_entry_two.insert(0, '4')	
		self.min_entry_two.config(state=DISABLED)

		# tolerance setting	
		self.tolerance_label = Label(self.scan_win, text='Tolerance:')	
		self.tolerance_entry = Entry(self.scan_win)
		self.tolerance_entry.insert(0, '5')	
		self.tolerance_entry.config(state=DISABLED)

		self.div = ttk.Separator(self.scan_win, orient='vertical')

		self.scan_win.pack(expand=False, side=BOTTOM, padx=2, pady=2)
		self.scan_label_one.grid(column=0, row=0, padx=2, pady=2, sticky=E, columnspan=4)
		self.scan_check.grid(column=0, row=1, padx=2, pady=2, sticky=W)
		self.eps_label_one.grid(column=1, row=1, padx=2, pady=2, sticky=W)
		self.eps_entry_one.grid(column=2, row=1, padx=2, pady=2, sticky=W)
		self.min_label_one.grid(column=3, row=1, padx=2, pady=2, sticky=W)
		self.min_entry_one.grid(column=4, row=1, padx=2, pady=2, sticky=W)
		self.tolerance_label.grid(column=5, row=1, padx=2, pady=2, sticky=W)
		self.tolerance_entry.grid(column=6, row=1, padx=2, pady=2, sticky=W)
		self.div.grid(column=7, row=1, padx=2, pady=2, sticky=NS)
		self.scan_label_two.grid(column=1, row=0, padx=2, pady=2, sticky=E, columnspan=10)
		self.eps_label_two.grid(column=8, row=1, padx=2, pady=2, sticky=NS)
		self.eps_entry_two.grid(column=9, row=1, padx=2, pady=2, sticky=NS)
		self.min_label_two.grid(column=10, row=1, padx=2, pady=2, sticky=NS)
		self.min_entry_two.grid(column=11, row=1, padx=2, pady=2, sticky=NS)

if __name__ == '__main__':
	app = MainWindow().window	
	app.mainloop()

