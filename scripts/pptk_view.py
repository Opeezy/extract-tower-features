import numpy as np
import laspy
import sys
import pptk

print(sys.prefix)

with laspy.open('D://Macros//Python//Wolfpack 2.0//_Las_//Las.las') as fh:
    print('Points from Header:', fh.header.point_count)
    las = fh.read()
    print(las)
    print('Points from data:', len(las.points))
    ground_pts = las.classification == 2
    bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
    print('Ground Point Return Number distribution:')
    for r,c in zip(bins,counts):
        print('    {}:{}'.format(r,c))

#colors = np.vstack((las.red, las.green, las.blue)).transpose()
points = np.vstack((las.x, las.y, las.z)).transpose()
v = pptk.viewer(points)
