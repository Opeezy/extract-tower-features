import math
import builtins


txt = ''
points = 0


with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\polys.txt') as f:
    for line in f.readlines():
        txt += line.strip(',')
        points +=1
    polys = txt.split('\n')
    f.close()
    print(str(points) + ' points read from file...')

txt = ''

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\polys_tops.txt') as f:
    for line in f.readlines():
        txt += line.strip(',')
        points +=1
    polys_tops = txt.split('\n')
    f.close()
    print(str(points) + ' points read from file...')


for p in polys:
	if len(p) < 1:
		polys.remove(p)

for p in polys_tops:
	if len(p) < 1:
		polys_tops.remove(p)

for i in range(len(polys)):
	temp = polys[i].split(',')
	hold = []
	for t in temp:
		hold.append(float(t))
	tupe = (hold[0],hold[1],hold[2])
	polys[i] = tuple(tupe)

for i in range(len(polys_tops)):
	temp = polys_tops[i].split(',')
	hold = []
	for t in temp:
		hold.append(float(t))
	tupe = (hold[0],hold[1],hold[2])
	polys_tops[i] = tuple(tupe)

del polys[::5]
del polys_tops[::5]

def calc_centroid(x,y):
	x_verts = x
	y_verts = y
	n = len(x_verts)
	x_sum = sum(x_verts)
	y_sum = sum(y_verts)
	cen_x = x_sum/n
	cen_y = y_sum/n
	centroid = (cen_x,cen_y)
	return centroid

def dis(xz,xo,yz,yo):
	x = (xo-xz)**2
	y = (yo-yz)**2
	d = math.sqrt(x+y)
	return d

def find_mid(xz,xo,yz,yo):
	x = (xz+xo)
	y = (yz+yo)
	mid = ((x/2),(y/2))
	return mid

def xt(l,d, xz,xo,yz,yo):
	x = xz - (l*(xz-xo))/d
	y = yz - (l*(yz-yo))/d
	xt = (x,y)	
	return xt


range = builtins.range


length_b = int((len(polys)/4))
length_t = int((len(polys_tops)/4))

p = 0
x_vals_bot = []
y_vals_bot = []
x_vals_top = []
y_vals_top = []
z_vals_top = []
centroids_bot = []
centroids_top = []
top_vectors = []
pole_tops = []
attach_points = []
shield = []

def angle_vector(xt,yt,d,xz,xo,yz,yo):
	dx = xo-xz
	dy = yz-yo
	sqr = math.sqrt((dx**2)+(dy**2))
	div = d/sqr
	nx = div*dx
	ny = div*dy
	new_vec = ((xt+ny), (yt+nx))
	return new_vec	

for i in polys:
	x_vals_bot.append(i[0])
	y_vals_bot.append(i[1])

for i in polys_tops:
	x_vals_top.append(i[0])
	y_vals_top.append(i[1])
	z_vals_top.append(i[2])

for i in range(length_t):
	x = x_vals_top[p:(p+4)]
	y = y_vals_top[p:(p+4)]
	z = 13.7 + max(z_vals_top[p:(p+4)])
	c = calc_centroid(x,y)
	c_ = (c[0],c[1],z)
	p += 4
	centroids_top.append(c_)

p = 0

for i in range(length_b):
	x = x_vals_bot[p:(p+4)]
	y = y_vals_bot[p:(p+4)]
	c = calc_centroid(x,y)
	m = find_mid(x[0],x[1],y[0],y[1])
	d = dis(c[0],m[0],c[1],m[1])
	p += 4
	centroids_bot.append([c,d])

vectors = []
centroids_bot = sorted(centroids_bot)
distances = []

for i in centroids_bot:
	d = i [1]
	i.pop(1)
	distances.append(d)

for i in range(len(centroids_bot)):
	k = centroids_bot[i]
	l = k[0]
	centroids_bot[i] = l

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\distances.txt', 'w') as f:
    for i in distances:
    	f.write(str(i) + '\n')
    f.close()

p = 1

for i in centroids_bot:
	if p == (len(centroids_bot)):
		break
	xz = i[0]
	yz = i[1]
	p2 = centroids_bot[p]	
	xo = p2[0]
	yo = p2[1]	
	m = find_mid(xz,xo,yz,yo)
	vectors.append(m)
	p+=1

centroids_top = sorted(centroids_top)

p = 0

for i in centroids_top:
	for k in vectors:
		if p == 0:
			p = dis(i[0],k[0],i[1],k[1])
			vec_ = k
		elif p > dis(i[0],k[0],i[1],k[1]):
			p = dis(i[0],k[0],i[1],k[1])
			vec_ = k
	top_vec = angle_vector(i[0],i[1],p,i[0],vec_[0],i[1],vec_[1])
	top_vectors.append(top_vec)

vec_ = 0
p = 0
centroids_top = sorted(centroids_top)
top_vectors = sorted(top_vectors)

for i in range(len(centroids_top)):
	c = centroids_top[i]
	v = top_vectors[i]
	z = c[2]
	d = dis(c[0],v[0],c[1],v[1])
	top_one = xt(22.5,d,c[0],v[0],c[1],v[1])
	top_two = xt(-22.5,d,c[0],v[0],c[1],v[1])
	top_one = (top_one[0],top_one[1],z)
	top_two = (top_two[0],top_two[1],z)
	pole_tops.append(top_one)
	pole_tops.append(top_two)

for i in range(len(centroids_top)):
	c = centroids_top[i]
	v = top_vectors[i]
	z = c[2]-28
	d = dis(c[0],v[0],c[1],v[1])
	p1 = (c[0],c[1],z)
	p2 = xt(-28.5,d,c[0],v[0],c[1],v[1])
	p3 = xt(28.5,d,c[0],v[0],c[1],v[1])
	p2 = (p2[0],p2[1],z)
	p3 = (p3[0],p3[1],z)
	attach_points.append(p1)
	attach_points.append(p2)
	attach_points.append(p3)

for i in pole_tops:
	z = i[2]-.7
	sw = (i[0],i[1],z)
	shield.append(sw)

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\centroids.txt', 'w') as f:
    for i in centroids_bot:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(0.000)
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()


with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\centroids_tops.txt', 'w') as f:
    for i in centroids_top:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(i[2])
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\vector_tops.txt', 'w') as f:
    for i in top_vectors:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(0.000)
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()


with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\vectors.txt', 'w') as f:
    for i in vectors:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(0.000)
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\pole_tops.txt', 'w') as f:
    for i in pole_tops:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(i[2])
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\attach_points.txt', 'w') as f:
    for i in attach_points:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(i[2])
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\shieldwire.txt', 'w') as f:
    for i in shield:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(i[2])
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()







