import numpy as np
import laspy

class Read:

	def read_las(file):
		with laspy.open(file) as fh:
			print('Points from Header:', fh.header.point_count)
			las = fh.read()
			print(las)
			print('Points from data:', len(las.points))       
			print('Ground Point Return Number distribution:')
	
	
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


'''

	Point format for LAS File is as follows:

	[ X | Y | Z | INTENSITY | RETURN_NUMBER | NUMBER_OF_RETURNS | SCAN_DIRECTION_FLAG_ | EDGE_OF_FLIGHT_LINE | CLASSIFICATION | SYNTHETIC | KEY_POINT | WITHHELD | SCAN_ANGLE_RANK | USER_DATA | POINT_SOURCE_ID | GPS_TIME]

	EACH VALUE IS PLACED IN COLUMNS RANGING FROM 0-14 STARTING AT X AND GOIN RIGHT TO POINT_SOURCE_ID

	ACCESS EACH COLUMN INDIVIDUALLY USING 'las_data[:, n]' WHERE N = COLUMN NUMBER

'''

	


