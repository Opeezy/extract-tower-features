tower_points = []

a = 'D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\attach_points.txt'
b = 'D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\pole_bottoms.txt'
c = 'D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\pole_tops.txt'
d = 'D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\shieldwire.txt'
e = 'D:\\Macros\\Python\\Wolfpack 2.0\\Towers\\Exports\\Lattice\\config_a\\tower_full.txt'


with open(a) as f, open(b) as g, open(c) as h, open (d) as j, open(e,'w') as k :
    for line in f.readlines():
        tower_points.append(line)
    f.close()
    for line in g.readlines():
        tower_points.append(line)
    g.close()
    for line in h.readlines():
        tower_points.append(line)
    h.close()
    for line in j.readlines():
        tower_points.append(line)
    j.close()
    for i in tower_points:
        k.write(i)
    k.close()

  