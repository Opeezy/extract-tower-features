from shapely import *
from shapely.geometry import Polygon
from shapely import wkt
import math

def create_attach_points():
    coords = []
    x = []
    y = []
    z = []
    p_count = 0

    #opens our points from file and writes to list "coords"
    with open('D:\\Macros\\Python\\Wolfpack 2.0\\APT\\Input\\poletops.txt', 'r') as f:
        for line in f.readlines():
            t = line.strip('\n')
            l = t.replace(',', ', ')
            lis_ = t.split(',')
            x.append(float(lis_[0]))
            y.append(float(lis_[1]))
            z.append(float(lis_[2]))
            coords.append(l)
            lis_.clear()
            p_count += 1
        f.close()
        print(str(p_count) + ' points read from file...')
        print(str(len(x)) + ' x stored to memory...')
        print(str(len(y)) + ' y stored to memory...')
        print(str(len(z)) + ' z stored to memory...')
        print(str(len(coords)) + ' coordinates stored to memory...')

    brk_poins = []
    clusters = []
    break_points = []
    cluster = 0
    x_len = len(x)
    distances = []
    pgrs_bar = ''
    percs = []

    print('Finding clusters...')
    for i in range(x_len):
        perc = int((i/x_len) * 100)
        percs.append(perc)
        if perc % 10 == 0 and percs[i-1] != perc and perc != 0:
            pgrs_bar = pgrs_bar + '|'
            print(pgrs_bar + ' ' + str(perc) + '%')
        base = (x[i],y[i],z[i])
        if base in clusters:
            continue
        else:
            if i == 0:
                clusters.append(base)
            else:
                clusters.append('#')
            base = (x[i],y[i],z[i])
            if i == 0:
                clusters.append(base)
            for k in range(x_len):
                compare = (x[k], y[k], z[k])
                if compare in clusters:
                    continue
                else:
                    dis = math.dist(base, compare)
                    if dis < 1:
                        clusters.append(compare)
                    distances.append(dis)

    count = 0
    for i in clusters:
        if i == '#':
            count += 1
        else:
            continue

    print(str(count + 1) + ' clusters found...')

    count = 0

    for i in clusters:
        if i == '#':
            count += 1
        else:
            continue
    print(str(count) + ' polygons')

    with open('D:\\Macros\\Python\\Wolfpack 2.0\\APT\\Output\\clusters.txt', 'w') as f:
        for i in clusters:
            f.write(str(i) + '\n')
        f.close()

    count = 0
    position = 0
    s_poly = 0
    pos = 0
    z_points = []
    poly = []
    c_count = 0
    centroid = []
    high_points = []
    z_p = 0

    for i in clusters:
        count += 1
        if i != '#':
            poly.append(i)
            z_p = i[2]
            z_points.append(z_p)
        elif i == '#':
            if len(poly) < 3:
                continue
            else:
                c_count += 1
                c = str(Polygon(poly))
                p = wkt.loads(c)
                centroid.append(p.centroid.wkt)
                poly.clear()
                high_z = max(z_points)
                high_points.append(high_z)
                z_points.clear()

    print(str(c_count) + ' centroids found...')

    att_points = []
    count = 0

    for i in centroid:
        l = i.strip('POINT ()')
        l = l.replace(" ", ",")
        l = (l + ',' + str(high_points[count]))
        centroid[count] = l
        count += 1

    print(str(count) + ' centroids formatted...')
    print('Writing to file...')

    count = 0

    with open('D:\\Macros\\Python\\Wolfpack 2.0\\APT\\Output\\tops.txt', 'w') as f:
        for i in centroid:
            f.write(centroid[count] + '\n')
            count += 1
        f.close()

    print(str(count) + ' points written to file...')


    #with open('attach_points.txt'. 'w') as f:



create_attach_points()