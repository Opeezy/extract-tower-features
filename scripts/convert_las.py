import numpy as np
import laspy
import threading
import time


points = []
smoothed = []

with laspy.open('D://Macros//Python//Wolfpack 2.0//Ver_0.1//_Las_//Las.las') as fh:
    print('Points from Header:', fh.header.point_count)
    las = fh.read()
    print(las)
    print('Points from data:', len(las.points))
    ground_pts = las.classification == 2
    bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
    print('Ground Point Return Number distribution:')
    for r,c in zip(bins,counts):
        print('    {}:{}'.format(r,c))

points = np.vstack((las.x, las.y, las.z)).transpose()
classification = np.vstack(las.classification)
points = np.hstack((classification, points))
print(ground_pts[0:10])

header = laspy.LasHeader(point_format=6, version="1.4")


smoothed_las = laspy.LasData(header)
smoothed_las.classification = points[:, 0]
smoothed_las.x = points[:, 1]
smoothed_las.y = points[:, 2]
smoothed_las.z = points[:, 3]

smoothed_las.write("smoothed.las")
print("Written to file")