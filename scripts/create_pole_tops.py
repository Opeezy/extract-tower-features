from shapely import *
from shapely.geometry import Polygon
from shapely import wkt
import math

file = 'xy_of_foreign_strc_shapes.txt'

def find_centroid():
    coords = []
    x = []
    y = []
    z = []
    xy = []
    txt = ''
    s = ''
    points = 0

    #this will read the txt file and assing to str "txt"
    with open('D:\\Macros\\Python\\Wolfpack 2.0\\PTT\\strc_tops_shapes_xyz.txt') as f:
        for line in f.readlines():
            txt += line.strip(',')
            points +=1
        f.close()
        print(str(points) + ' points read from file...')

    #remove new lines from string
    txt = txt.split('\n')

    #returns a list of each point seperated by commas
    for t in txt:
        s += t + ','
    coords = s.split(',')

    #removing stray commas
    for c in coords:
        if len(c) < 5:
            coords.remove(c)
    coords.pop()   

    #sorts z list into every z coordinate
    z = coords[2::3]
    x = coords[::3]
    y = coords[1::3]

    count = 0

    #convert xyz points to floats
    for i in range(len(x)):
        x[count] = float(x[count])
        y[count] = float(y[count])
        z[count] = float(z[count])
        count +=1 
    print(str(count) + ' xyz points converted to floats')
    
    count = 0
    polys = 0

    #parse through x values and seperate if > than 1ft   

    count = 0
    break_points = []
    distances = []

    for i in x:
        if count > 0: 
            p1 = (float(x[count]), float(y[count]), float(z[count]))
            p2 = (float(x[count-1]), float(y[count-1]), float(z[count-1]))
            dis = math.dist(p1,p2)
            distances.append(dis)
            if dis > 100:
                break_points.append(count)
                count += 1
            else:
                count += 1
        elif count > len(x):
            break 
        else:
            count += 1

    print(distances)


    print('Sorting polygons...')
    for i in break_points:
        x.insert(i, '#')
        y.insert(i, "#")
        z.insert(i, '#')

    count = 0
    points_removed = 0

    print('Removing stray points...')
    for i in x:
        if i == '#' and x[count-1] == '#':
            x.pop(count)
            x.pop(count + 1)
            y.pop(count)
            y.pop(count + 1)
            z.pop(count)
            z.pop(count + 1)
            count +=1
            points_removed += 1
        else:
            count += 1

    print(str(points_removed) + ' point(s) removed...')

    count = 0

    for i in x:
        if i == '#':
            xy.append('#')
            count += 1
        else: 
            xy.append((x[count], y[count]))
            count += 1

    poly = []
    centroid = []
    count = 0
    cen_count = 0
    poly_point = 0
    z_point = []
    highest_z = 0
    high_points = []

    for i in xy:
        if i == '#':
            polys += 1
        else:
            continue

    print(str(polys) + ' polygons formed...')

    with open('xy_points.txt', 'w') as f:
        for i in xy:
            f.write(str(i) + '\n')
        f.close()

    #sorts points into seperate polgons and calculates centroid of each
    for i in xy:
        if i != '#':
            poly.append(i)
            z_point.append(z[count])
            count += 1
        else: 
            c = str(Polygon(poly))
            p = wkt.loads(c)
            centroid.append(p.centroid.wkt)
            poly.clear()
            cen_count += 1
            highest_z = max(z_point)
            high_points.append(highest_z)
            z_point.clear()
            highest_z = 0
            count += 1
           

    print(str(cen_count) + ' centroids found...')
    count = 0

    #stripping centroids of text        
    for i in centroid:
        centroid[count] = i.strip('POINT ')        
        count +=1 

    count = 0

    #write to new file
    with open('xy_of_foreign_strc_centroids.txt', 'w') as f:
        for i in centroid:
            t = i.strip('()')
            l = t.replace(' ', ',')
            f.write(l + ',' + str(high_points[count]) + '\n')
            count +=1 
        f.close()
    print('Operation complete...' + str(count) + ' pole tops written to file.')  

find_centroid()