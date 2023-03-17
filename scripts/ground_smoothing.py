import numpy as np
import laspy
import threading
import time


points = []
smoothed = []

with laspy.open('ground.las') as fh:
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

for i in points:
    if len(points)%10 == 0:        
        break
    else:
        points = points[1:]

parse_1 = points[0::5]  
parse_2 = points[1::5]
parse_3 = points[2::5]
parse_4 = points[3::5]
parse_5 = points[4::5]

neighbors_len = []

def parse(arr, thd):
    p=0
    print(len(arr))
    for i in arr:
        xj = []        
        yj = []
        zj = []        
        p+=1
        pe = p/len(arr)
        per = pe*100
        if p%100 == 0:
            print("Thread " + thd + " progress: " + str(float(per)))
        distances = np.sqrt(np.sum((arr - i) ** 2, axis=1))
        mask = distances < 1
        neighbors = arr[mask]
        neighbors_len.append(len(neighbors))
        for j in neighbors:
            x = j[0]
            y = j[1]
            z = j[2]
            xj.append(x)                       
            yj.append(y)
            zj.append(z)
        xi = (1/len(neighbors)*sum(xj))
        yi = (1/len(neighbors)*sum(yj))
        zi = (1/len(neighbors)*sum(zj))
        smoothi = (xi,yi,zi)
        smoothed.append(smoothi)

p1_thread = threading.Thread(target=parse, args=(parse_1, "one"))
p2_thread = threading.Thread(target=parse, args=(parse_2, "two"))
p3_thread = threading.Thread(target=parse, args=(parse_3, "three"))
p4_thread = threading.Thread(target=parse, args=(parse_4, "four"))
p5_thread = threading.Thread(target=parse, args=(parse_5, "five"))

try:
    p1_thread.start()
    p2_thread.start()
    p3_thread.start()
    p4_thread.start()
    p5_thread.start()

    p1_thread.join()
    p2_thread.join()
    p3_thread.join()
    p4_thread.join()
    p5_thread.join()
except:
    print("Error")


header = laspy.LasHeader(point_format=3, version="1.2")
header.add_extra_dim(laspy.ExtraBytesParams(name="random", type=np.int32))
header.offsets = np.min(smoothed, axis=0)
header.scales = np.array([0.1, 0.1, 0.1])

smoothed_las = laspy.LasData(header)

sx = []
sy = []
sz = []

for i in smoothed:
    x = i[0]   
    y = i[1]
    z = i[2]
    sx.append(x)
    sy.append(y)
    sz.append(z)

smoothed_las.x = sx
smoothed_las.y = sy
smoothed_las.z = sz

smoothed_las.write("smoothed.las")
print("Written to file")
