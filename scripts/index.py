import numpy as np
import laspy
import threading


points = []
included = []
not_included = []
smoothed = []

with laspy.open('Canadys_000241.las') as fh:
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

p = 0
total = len(las.points)

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

print("Working...")
def parse(arr, thd):
    p=0
    for i in arr:      
        p+=1
        pe = p/len(arr)
        per = pe*100
        if per%1 == 0:
            print("Thread " + thd + " progress: " + str(int(per)))
        distances = np.sqrt(np.sum((arr - i) ** 2, axis=1))
        mask = distances < 15
        neighbors = arr[mask]
        neighbors_len.append(len(neighbors))
        if len(neighbors) < 40:
            included.append(i)
        else:
            not_included.append(i)
    
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
header.offsets = np.min(included, axis=0)
header.scales = np.array([0.1, 0.1, 0.1])

new_las = laspy.LasData(header)
exc_las = laspy.LasData(header)

xx = []
yy = []
zz = []
low_z = 0
new_points = []

for i in included:
    z = i[2]
    if z < low_z or low_z == 0:
        low_z = z
    else:
        pass

stack_x = []
stack_y = []
stack_z = []

for i in included:
    if i[2] > (low_z + 10):
        x = i[0]
        y = i[1]
        z = i[2]
        stack_x.append(x)        
        stack_y.append(y)
        stack_z.append(z)        

new_points = np.vstack((stack_x, stack_y, stack_z)).transpose()

        
print(low_z)

final_points = []

p=0

print("Removing outliers...")
print(len(new_points))

for i in new_points:
    if len(new_points)%10 == 0:        
        break
    else:
        new_points = new_points[1:]

n_parse_1 = new_points[0::5]  
n_parse_2 = new_points[1::5]
n_parse_3 = new_points[2::5]
n_parse_4 = new_points[3::5]
n_parse_5 = new_points[4::5]

def remove_noise(arr, thd):
    p = 0
    for i in arr:
        c = 0     
        p+=1
        pe = p/len(arr)
        per = pe*100
        if per%1 == 0:
            print("Thread " + thd + " progress: " + str(int(per)))
        distances = np.sqrt(np.sum((arr - i) ** 2, axis=1))
        mask = distances < 50
        neighbors = distances[mask]
        for j in neighbors:
            if j < 40:
                x = i[0]
                y = i[1]
                z = i[2]
                final_points.append([x,y,z])
            break

n_p1_thread = threading.Thread(target=remove_noise, args=(n_parse_1, "one"))
n_p2_thread = threading.Thread(target=remove_noise, args=(n_parse_2, "two"))
n_p3_thread = threading.Thread(target=remove_noise, args=(n_parse_3, "three"))
n_p4_thread = threading.Thread(target=remove_noise, args=(n_parse_4, "four"))
n_p5_thread = threading.Thread(target=remove_noise, args=(n_parse_5, "five"))

try:
    n_p1_thread.start()
    n_p2_thread.start()
    n_p3_thread.start()
    n_p4_thread.start()
    n_p5_thread.start()
    n_p1_thread.join()
    n_p2_thread.join()
    n_p3_thread.join()
    n_p4_thread.join()
    n_p5_thread.join()
except:
    print("Error")


print(len(final_points))
for i in final_points:
    x = i[0]   
    y = i[1]
    z = i[2]
    xx.append(x)
    yy.append(y)
    zz.append(z)

nx = []
ny = []
nz = []

for i in not_included:
    x = i[0]   
    y = i[1]
    z = i[2]
    nx.append(x)
    ny.append(y)
    nz.append(z)

new_las.x = xx
new_las.y = yy
new_las.z = zz

exc_las.x = nx
exc_las.y = ny
exc_las.z = nz

new_las.classification == 3

print(new_las.points)
print(exc_las.points)
#print(neighbors_len)
print(new_las.classification)

new_las.write("included.las")
exc_las.write("not_included.las")
print("Written to file")


