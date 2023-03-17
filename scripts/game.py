import pygame
import numpy as np
import random
from polygenerator import (
	random_polygon,
	random_star_shaped_polygon,
	random_convex_polygon,
)
from shapely.geometry import Polygon, Point


pygame.init()
display_surface = pygame.display.set_mode((800, 800))

land_color = (173,161,114)
water_color = (27,146,196)
player_color = (0,0,0)
rock_color = (131, 134, 135)
tree_color = (0, 255,0)

land = ((0,0), (800,0), (800,800), (0,800))
poly = Polygon(land)
rock_coords = []
tree_coords = []
player_coords = []
grid = np.zeros((6400,6400))

def draw_grid():
	for i in range(0, 800, 10):
		pygame.draw.line(display_surface, (189,191,191), (i,0), (i,800))
		pygame.draw.line(display_surface, (189,191,191), (0, i), (800,i))

def spawn_player(allowed):
	in_bounds = False

	while not in_bounds:

		poly = Polygon(allowed)
		min_x, min_y, max_x, max_y = poly.bounds
		spawn = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])

		if (spawn.within(poly)):
			spawn = (spawn.x, spawn.y)
			player_coords.append(spawn)
			pygame.draw.circle(display_surface, player_color, spawn, 5)
			in_bounds = True

def spawn_trees(allowed, amount):
	rocks_spawned = 0

	while trees_spawned < amount:

		x = random.randint(0,11)
		y = random.randint(0,11)
		spawn = (x*80,y*80)
		for i in rock_coords:
			if spawn == i:
				pass
			else:
				
		rock = [(spawn), (spawn[0]+10, spawn[1]), (spawn[0]+10, spawn[1]+10), (spawn[0], spawn[1]+10)]
		rock_coords.append(rock)
		pygame.draw.polygon(display_surface, rock_color, rock)
		trees_spawned += 1
		

def spawn_rocks(allowed, amount):
	rocks_spawned = 0

	while rocks_spawned < amount:

		x = random.randint(0,11)
		y = random.randint(0,11)
		spawn = (x*80,y*80)
		rock = [(spawn), (spawn[0]+10, spawn[1]), (spawn[0]+10, spawn[1]+10), (spawn[0], spawn[1]+10)]
		rock_coords.append(spawn)
		pygame.draw.polygon(display_surface, rock_color, rock)
		rocks_spawned += 1
		
		#poly = Polygon(allowed)
		#min_x, min_y, max_x, max_y = poly.bounds
		#spawn = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
		#spawn = (spawn.x, spawn.y)
		#rock = []
		#
		#for i in range(0, smoothness):
		#	if i == 0:
		#		rock.append(spawn)
		#	else:
		#		p_or_m = random.randint(0,10)
		#		prev = rock[i-1]
#
		#		if p_or_m <= 5:
		#			ran_x = prev[0] - random.randint(0,variance)
		#			ran_y = prev[1] - random.randint(0,variance)
		#			rock.append((ran_x, ran_y))
		#		elif p_or_m > 5:
		#			ran_x = prev[0] + random.randint(0,variance)
		#			ran_y = prev[1] + random.randint(0,variance)
		#			rock.append((ran_x, ran_y))
#
		#rock_poly = Polygon(rock)
#
		#if (rock_poly.within(poly)):
		#	rock_coords.append(rock)
		#	pygame.draw.polygon(display_surface, rock_color, rock)
		#	rocks_spawned += 1
#
display_surface.fill(land_color)
draw_grid()
spawn_rocks(land, 100)

running = True

while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		pygame.display.update()