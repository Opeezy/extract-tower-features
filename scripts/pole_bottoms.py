import math

txt = ''
s = ''
points = 0
tops = []
bottoms = []
vectors = []
distances = []

txt = ''
points = 0

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\centroids.txt') as f:
    for line in f.readlines():
        txt += line.strip(',')
        points +=1
    bottoms = txt.split('\n')
    f.close()
    print(str(points) + ' points read from file...')

txt = ''
points = 0

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\vectors.txt') as f:
    for line in f.readlines():
        txt += line.strip(',')
        points +=1
    vectors = txt.split('\n')
    f.close()
    print(str(points) + ' points read from file...')


with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\distances.txt') as f:
    for line in f.readlines():
    	distances.append(float(line))
    f.close()

txt = ''
points = 0

for b in bottoms:
	if len(b) < 1:
		bottoms.remove(b)

for v in vectors:
	if len(v) < 1:
		vectors.remove(v)

for i in range(len(bottoms)):
	temp = bottoms[i].split(',')
	hold = []
	for t in temp:
		hold.append(float(t))
	tupe = (hold[0],hold[1],hold[2])
	bottoms[i] = tuple(tupe)

for i in range(len(vectors)):
	temp = vectors[i].split(',')
	hold = []
	for t in temp:
		hold.append(float(t))
	tupe = (hold[0],hold[1],hold[2])
	vectors[i] = tuple(tupe)

def dis(xz,xo,yz,yo):
	x = (xo-xz)**2
	y = (yo-yz)**2
	d = math.sqrt(x+y)
	return d

def xt(l,d, xz,xo,yz,yo):
	x = xz - (l*(xz-xo))/d
	y = yz - (l*(yz-yo))/d
	xt = (x,y)	
	return xt

def xt_(l,d, xz,xo,yz,yo):
	x = xz - (-l*(xz-xo))/d
	y = yz - (-l*(yz-yo))/d
	xt_ = (x,y)	
	return xt_

def c1(xt,yt,d,xz,yz,xo,yo):
	x=xo-xz
	y=yz-yo
	xj_sqr = (d/math.sqrt((y**2)+(x**2)))
	xp = xj_sqr*x
	yp = xj_sqr*y
	c1 = ((xt+xp),yt+yp)
	return c1

def c2(xt,yt,d,xz,yz,xo,yo):
	x=xo-xz
	y=yz-yo
	xj_sqr = (d/math.sqrt((y**2)+(x**2)))
	xp = xj_sqr*x
	yp = xj_sqr*y
	c2 = ((xt-xp),yt-yp)
	return c2

xt_points= []
corners = []
c = 0

for i in bottoms:
	length = distances[c]
	p = 0
	m = 0
	for k in range(len(vectors)):
		s = vectors[k]
		xz = i[0]
		xo = s[0]
		yz = i[1]
		yo = s[1]		
		dis_= dis(xz,xo,yz,yo)
		if p == 0:
			p = dis_
			m = k
		if p > dis_:
			p = dis_
			m = k
	o = vectors[m]
	f = xt(length,p,i[0],o[0],i[1],o[1])
	f_ = xt_(length,p,i[0],o[0],i[1],o[1])
	w_ = c1(f[0],f[1],length,i[0],i[1],o[0],o[1])
	_w = c2(f[0],f[1],length,i[0],i[1],o[0],o[1])
	j_ = c1(f_[0],f_[1],length,i[0],i[1],o[0],o[1])
	_j = c2(f_[0],f_[1],length,i[0],i[1],o[0],o[1])
	xt_points.append(f)
	xt_points.append(f_)
	corners.append(w_)
	corners.append(_w)
	corners.append(j_)
	corners.append(_j)
	c+=1

print(corners)

with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\bin\\Lattice\\config_a\\xt.txt', 'w') as f:
    for i in xt_points:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(0.000)
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()
with open('D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\pole_bottoms.txt', 'w') as f:
    for i in corners:
    	x=str(i[0])
    	y=str(i[1])
    	z=str(0.000)
    	xy=x+','+y+','+z+'\n'
    	f.write(xy)
    f.close()
   

   

























