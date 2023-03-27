#!/usr/bin/python3
import pygame
import pygame_gui
import random

pygame.init()
width = 1024
height = 768
pygame.display.set_caption('Hexomata')
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font = pygame.font.SysFont(None, 24)
sound = True
grow_sound = pygame.mixer.Sound('sounds/click.wav')
tile_sound = pygame.mixer.Sound('sounds/clack.wav')
fps = 5
nnum = 6 #the neighbor numbers either 6 or 18
survival_rules = [False,False,True,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False,False]
birth_rules = [False,True,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False,False,False]
hex_width = 20
hex_radius = hex_width / 2
hex_height = int(hex_width * 0.8660254)
show_grid = False
show_numbers = False
render = False
paused = False
animated_hexagons = [] #highlights neighbors when tile is clicked
hexagons = [] #the master list [rect,active,neighbor_count,6-neighbors, 12-cousins
colors = {'n6' : ['#FFFF00','#FFA500','#FF0000','#FF00FF','#800080','#0000FF','#008000'],
			'n18' : ['#FFFF00','#BFFF00','#80FF00','#40FF00','#00FF00','#00FF40',
					'#00FF80','#00FFBF','#00FFFF','#00BFFF','#0080FF','#0040FF',
					'#0000FF','#4000FF','#8000FF','#BF00FF','#FF00FF','#FF00BF','#FF0080']}
current_swatch = None
legend_buttons = []
def build_grid():
	left_margin = 140
	right_margin = 10
	top_margin = 70
	bottom_margin = 10
	grid_width = int((width-(left_margin+right_margin))/(hex_width+hex_width/2))
	if grid_width%2: grid_width -= 1 #we only want an even number of columns
	grid_height = int((height-(top_margin+bottom_margin))/(hex_height/2))
	if grid_height%2: grid_height -= 1 #we only want an even number of rows
	grid_total = grid_width*grid_height
	hex_counter = 0
	for y in range(grid_height):
		y_offset = hex_height * y / 2 + top_margin
		for x in range(grid_width):
			
			if not y%2:
				x_offset = (hex_width + hex_width / 2 ) * x + left_margin
			else:
				x_offset = (hex_width + hex_width / 2 ) * x - 3 * hex_width / 4 + left_margin
			
			hexagon = pygame.draw.polygon(screen,'Black',[(x_offset,y_offset + hex_height/2),
										(x_offset + hex_width/4,y_offset + hex_height),
										(x_offset + 3*hex_width/4,y_offset + hex_height),
										(x_offset + hex_width,y_offset + hex_height/2),
										(x_offset + 3*hex_width/4,y_offset),
										(x_offset + hex_width/4,y_offset)]
									,1)
			hex_neighbor_offsets = []
			hex_cousin_offsets = [] #cousins are the second row of 12 more neighbors
			#calculate neighbor offsets once and store in hexagons
			if y == 0: #top row
				if x == 0: #top left corner
					hex_neighbor_offsets = [grid_width,
												grid_width+1,
												grid_total-grid_width,
												grid_total-grid_width+1,
												grid_width*2,
												grid_total-grid_width*2]
				elif x == grid_width-1: #top right corner
					hex_neighbor_offsets = [grid_width,
												1,
												grid_total-grid_width,
												grid_total-grid_width*2+1,
												grid_width*2,
												grid_total-grid_width*2]
				else:#rest of top row
					hex_neighbor_offsets = [grid_width,
												grid_width+1,
												grid_total-grid_width,
												grid_total-grid_width+1,
												grid_width*2,
												grid_total-grid_width*2]
			elif y == 1: #second row
				if x == 0:
					hex_neighbor_offsets = [-1,
												grid_width*2-1,
												-grid_width,
												grid_width,
												grid_total-grid_width*2,
												grid_width*2]
				else:
					hex_neighbor_offsets = [-grid_width-1,
												grid_width-1,
												grid_width,
												-grid_width,
												grid_total-grid_width*2,
												grid_width*2]
			elif y == grid_height-2: #second to bottom row
				if x == grid_width-1:
					hex_neighbor_offsets = [-grid_width,
												grid_width,
												-grid_width*2+1,
												1,
												-grid_width*2,
												-grid_total+grid_width*2]
				else:
					hex_neighbor_offsets = [-grid_width,
												grid_width,
												-grid_width+1,
												grid_width+1,
												-grid_width*2,
												-grid_total+grid_width*2]
			elif y == grid_height-1: #bottom row
				if x == 0: #bottom left corner
					hex_neighbor_offsets = [-1,
												-grid_total+grid_width*2-1,
												-grid_total+grid_width,
												-grid_width,
												-grid_width*2,
												-grid_total+grid_width*2]
				elif x == grid_width-1: #bottom right corner
					hex_neighbor_offsets = [-grid_width-1,
												-grid_width,
												-grid_total+grid_width-1,
												-grid_total+grid_width,
												-grid_width*2,
												-grid_total+grid_width*2]
				else: #the rest of the bottom row
					hex_neighbor_offsets = [-grid_width-1,
												-grid_width,
												-grid_total+grid_width-1,
												-grid_total+grid_width,
												-grid_width*2,
												-grid_total+grid_width*2]
			else: #interior rows alternating left and rightmost tiles
				if y%2 and x == 0: #leftmost tile on odd rows
					hex_neighbor_offsets = [-1,
												grid_width*2-1,
												-grid_width,
												grid_width,
												-grid_width*2,
												grid_width*2]
				elif not y%2 and x == grid_width-1: #rightmost tile on even rows
					hex_neighbor_offsets = [1,
												-grid_width*2+1,
												-grid_width,
												grid_width,
												-grid_width*2,
												grid_width*2]
			#calculate cousin offsets
			if y == 0: #top row
				if x == 0: #top left corner
					hex_cousin_offsets = [grid_width-1,
											1,
											grid_width*4,
											grid_total-grid_width*4,
											grid_total-grid_width*3,
											grid_total-grid_width-1,
											grid_width*3-1,
											grid_width*3,
											grid_width*3+1,
											grid_width*2+1,
											grid_total-grid_width*3+1,
											grid_total-grid_width*2+1]
				elif x == grid_width-1: #top right corner
					hex_cousin_offsets = [-1,
											-grid_width+1,
											grid_total-grid_width*4,
											grid_width*4,
											grid_total-grid_width*2-1,
											grid_width*2-1,
											grid_total-grid_width*3+1,
											grid_width+1,
											grid_total-grid_width*3,
											grid_width*3,
											grid_width*2+1,
											grid_total-grid_width*4+1]
				else:#rest of top row
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											1,
											grid_total-grid_width*2-1,
											grid_width*2-1,
											grid_total-grid_width*2+1,
											grid_width*2+1,
											grid_total-grid_width*3,
											grid_width*3,
											grid_total-grid_width*3+1,
											grid_width*3+1]
			elif y == 1: #second row
				if x == 0:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											grid_width-1,
											1,
											grid_total-grid_width-1,
											grid_width*3-1,
											grid_total-grid_width*2+1,
											grid_width*3+1,
											grid_total-grid_width*2-1,
											grid_width*4-1,
											grid_total-grid_width*3,
											grid_width*3]
				if x == grid_width-1:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											-grid_width+1,
											grid_total-grid_width*2-1,
											grid_width*2-1,
											grid_total-grid_width*3+1,
											grid_width+1,
											grid_total-grid_width*3-1,
											grid_width*3-1,
											grid_total-grid_width*3,
											grid_width*3]
				else:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											1,
											grid_total-grid_width*2-1,
											grid_width*2-1,
											grid_total-grid_width*2+1,
											grid_width*2+1,
											grid_total-grid_width*3-1,
											grid_width*3-1,
											grid_total-grid_width*3,
											grid_width*3]
			elif y == 2: #third row
				if x == 0:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											grid_width-1,
											1,
											-grid_width-1,
											grid_width*3-1,
											-grid_width*2+1,
											grid_width*2+1,
											grid_total-grid_width*3,
											grid_width*3,
											grid_total-grid_width*3+1,
											grid_width*3+1]
				elif x == grid_width-1:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											-grid_width+1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*3+1,
											grid_width+1,
											grid_total-grid_width*3,
											grid_width*3,
											grid_total-grid_width*4+1,
											grid_width*2+1]
				else:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*2+1,
											grid_width*2+1,
											grid_total-grid_width*3,
											grid_width*3,
											grid_total-grid_width*3+1,
											grid_width*3+1]
			elif y == 3: #fourth row
				if x == 0:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											grid_width-1,
											1,
											-grid_width-1,
											grid_width*3-1,
											-grid_width*2+1,
											grid_width*2+1,
											-grid_width*2-1,
											grid_width*4-1,
											-grid_width*3,
											grid_width*3]
				elif x == grid_width-1:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											-grid_width+1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*3+1,
											grid_width+1,
											-grid_width*3-1,
											grid_width*3-1,
											-grid_width*3,
											grid_width*3]
				else:
					hex_cousin_offsets = [grid_total-grid_width*4,
											grid_width*4,
											-1,
											1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*2+1,
											grid_width*2+1,
											-grid_width*3-1,
											grid_width*3-1,
											-grid_width*3,
											grid_width*3]
			elif y == grid_height-4: #fourth to bottom row
				if x ==0:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											grid_width-1,
											1,
											-grid_width-1,
											grid_width*3-1,
											-grid_width*2+1,
											grid_width*2+1,
											-grid_width*3,
											grid_width*3,
											-grid_width*3+1,
											grid_width*3+1]
				elif x == grid_width-1:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											-grid_width+1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*3+1,
											grid_width+1,
											-grid_width*3,
											grid_width*3,
											-grid_width*4+1,
											grid_width*2+1]
				else:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*2+1,
											grid_width*2+1,
											-grid_width*3,
											grid_width*3,
											-grid_width*3+1,
											grid_width*3+1]
			elif y == grid_height-3: #third to bottom row
				if x == 0:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											grid_width-1,
											1,
											-grid_width-1,
											grid_width*3-1,
											-grid_width*2+1,
											grid_width*2+1,
											-grid_width*2-1,
											-grid_total+grid_width*4-1,
											-grid_width*3,
											-grid_total+grid_width*3]
				elif x == grid_width-1:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											-grid_width+1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*3+1,
											grid_width+1,
											-grid_width*3-1,
											-grid_total+grid_width*3-1,
											-grid_width*3,
											-grid_total+grid_width*3]
				else:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											1,
											-grid_width*2-1,
											grid_width*2-1,
											-grid_width*2+1,
											grid_width*2+1,
											-grid_width*3-1,
											-grid_total+grid_width*3-1,
											-grid_width*3,
											-grid_total+grid_width*3]
			elif y == grid_height-2: #second to bottom row
				if x == 0:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											grid_width-1,
											1,
											-grid_width-1,
											-grid_total+grid_width*3-1,
											-grid_width*2+1,
											-grid_total+grid_width*2+1,
											-grid_width*3,
											-grid_total+grid_width*3,
											-grid_width*3+1,
											-grid_total+grid_width*3+1]
				elif x == grid_width-1:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											-grid_width+1,
											-grid_width-1,
											-grid_total+grid_width*2-1,
											-grid_width*3+1,
											-grid_total+grid_width+1,
											-grid_width*3,
											-grid_total+grid_width*3,
											-grid_width*4+1,
											-grid_total+grid_width*2+1]
				else:
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											1,
											-grid_width*2-1,
											-grid_total+grid_width*2-1,
											-grid_width*2+1,
											-grid_total+grid_width*2+1,
											-grid_width*3,
											-grid_total+grid_width*3,
											-grid_width*3+1,
											-grid_total+grid_width*3+1]
			elif y == grid_height-1: #bottom row
				if x == 0: #bottom left corner
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											grid_width-1,
											1,
											-grid_width-1,
											-grid_total+grid_width*3-1,
											-grid_width*2+1,
											-grid_total+grid_width*2+1,
											-grid_width*2-1,
											-grid_total+grid_width*4-1,
											-grid_width*3,
											-grid_total+grid_width*3]
				elif x == grid_width-1: #bottom right corner
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											-grid_width+1,
											-grid_width*2-1,
											-grid_total+grid_width*2-1,
											-grid_width*3+1,
											-grid_total+grid_width+1,
											-grid_width*3-1,
											-grid_total+grid_width*3-1,
											-grid_width*3,
											-grid_total+grid_width*3]
				else: #the rest of the bottom row
					hex_cousin_offsets = [-grid_width*4,
											-grid_total+grid_width*4,
											-1,
											1,
											-grid_width*2-1,
											-grid_total+grid_width*2-1,
											-grid_width*2+1,
											-grid_total+grid_width*2+1,
											-grid_width*3-1,
											-grid_total+grid_width*3-1,
											-grid_width*3,
											-grid_total+grid_width*3]
			else: #interior rows
				if y%2: #odd rows
					if x == 0:
						hex_cousin_offsets = [-grid_width*4,
												grid_width*4,
												grid_width-1,
												1,
												-grid_width-1,
												grid_width*3-1,
												-grid_width*2+1,
												grid_width*2+1,
												-grid_width*2-1,
												grid_width*4-1,
												-grid_width*3,
												grid_width*3]
					elif x == grid_width-1:
						hex_cousin_offsets = [-grid_width*4,
												grid_width*4,
												-1,
												-grid_width+1,
												-grid_width*2-1,
												grid_width*2-1,
												-grid_width*3+1,
												grid_width+1,
												-grid_width*3-1,
												grid_width*3-1,
												-grid_width*3,
												grid_width*3]
				else: #even rows
					if x == 0:
						hex_cousin_offsets = [-grid_width*4,
												grid_width*4,
												grid_width-1,
												1,
												-grid_width-1,
												grid_width*3-1,
												-grid_width*3,
												grid_width*3,
												-grid_width*3+1,
												grid_width*3+1,
												-grid_width*2+1,
												grid_width*2+1]
					elif x == grid_width-1:
						hex_cousin_offsets = [-grid_width*4,
												grid_width*4,
												-1,
												-grid_width+1,
												-grid_width*2-1,
												grid_width*2-1,
												-grid_width*3+1,
												grid_width+1,
												-grid_width*3,
												grid_width*3,
												-grid_width*4+1,
												grid_width*2+1]
			#any remaining tiles are interior tiles:
			if hex_neighbor_offsets == []:
				if y%2: #odd numbered rows
					hex_neighbor_offsets = [-grid_width,
											-grid_width-1,
											grid_width-1,
											grid_width,
											grid_width*2,
											-grid_width*2]
				else: #even numbered rows
					hex_neighbor_offsets = [-grid_width,
											-grid_width+1,
											grid_width+1,
											grid_width,
											grid_width*2,
											-grid_width*2]
			if hex_cousin_offsets == []:
				if y%2: #odd numbered rows
					hex_cousin_offsets = [-1,
										1,
										-grid_width*4,
										grid_width*4,
										-grid_width*3-1,
										grid_width*3-1,
										-grid_width*3,
										grid_width*3,
										-grid_width*2-1,
										grid_width*2-1,
										-grid_width*2+1,
										grid_width*2+1]
				else: #even numbered rows
					hex_cousin_offsets = [-1,
										1,
										-grid_width*4,
										grid_width*4,
										-grid_width*3,
										grid_width*3,
										-grid_width*3+1,
										grid_width*3+1,
										-grid_width*2-1,
										grid_width*2-1,
										grid_width*2+1,
										-grid_width*2+1]
			#hexagons index-> 0=rect, 1=state, 2=neighbor_count, 3=neighbor_offsets 4=cousin_offsets
			hexagons.insert(hex_counter,[hexagon,random.randint(0,1),0,hex_neighbor_offsets,hex_cousin_offsets])
			hex_counter += 1
	#Calculate and colorize the initial random field
	for k,pos in enumerate(hexagons):
		neighbor_count = 0
		if nnum == 6:
			n = pos[3]
		elif nnum == 18:
			n = pos[3]+pos[4]
		for offset in n:
			if k+offset >= 0 and k+offset < grid_width*grid_height: #shouldn't need this
				if hexagons[k+offset][1]:
					neighbor_count += 1
			#else: print('out of bounds: ',k,'+',offset)
		if pos[1]:
			hexagons[k] = [pos[0],1,neighbor_count,pos[3],pos[4]]
		else:
			hexagons[k] = [pos[0],0,neighbor_count,pos[3],pos[4]]
def main():
	global screen
	global width
	global height
	global nnum
	global fps
	global hex_width
	global hex_height
	global show_grid
	global show_numbers
	global render
	global paused
	global sound
	global animated_hexagons
	global hexagons
	
	manager = pygame_gui.UIManager((width, height))
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(75,20)),
														manager=manager,
														text='Survival:')
	s0 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((80, 0), (45, 30)),
														text='0',
														manager=manager)
	if survival_rules[0]:
		s0.select()
	s1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 0), (45, 30)),
														text='1',
														manager=manager)
	if survival_rules[1]:
		s1.select()
	s2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((180, 0), (45, 30)),
														text='2',
														manager=manager)
	if survival_rules[2]:
		s2.select()
	s3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, 0), (45, 30)),
														text='3',
														manager=manager)
	if survival_rules[3]:
		s3.select()
	s4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 0), (45, 30)),
														text='4',
														manager=manager)
	if survival_rules[4]:
		s4.select()
	s5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 0), (45, 30)),
														text='5',
														manager=manager)
	if survival_rules[5]:
		s5.select()
	s6 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((380, 0), (45, 30)),
														text='6',
														manager=manager)
	if survival_rules[6]:
		s6.select()
	s7 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((430, 0), (45, 30)),
														text='7',
														manager=manager)
	if survival_rules[7]:
		s7.select()
	if nnum == 6:
		s7.disable()
	s8 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 0), (45, 30)),
														text='8',
														manager=manager)
	if survival_rules[8]:
		s8.select()
	if nnum == 6:
		s8.disable()
	s9 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((530, 0), (45, 30)),
														text='9',
														manager=manager)
	if survival_rules[9]:
		s9.select()
	if nnum == 6:
		s9.disable()
	s10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((580, 0), (45, 30)),
														text='10',
														manager=manager)
	if survival_rules[10]:
		s10.select()
	if nnum == 6:
		s10.disable()
	s11 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((630, 0), (45, 30)),
														text='11',
														manager=manager)
	if survival_rules[11]:
		s11.select()
	if nnum == 6:
		s11.disable()
	s12 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 0), (45, 30)),
														text='12',
														manager=manager)
	if survival_rules[12]:
		s12.select()
	if nnum == 6:
		s12.disable()
	s13 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((730, 0), (45, 30)),
														text='13',
														manager=manager)
	if survival_rules[13]:
		s13.select()
	if nnum == 6:
		s13.disable()
	s14 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((780, 0), (45, 30)),
														text='14',
														manager=manager)
	if survival_rules[14]:
		s14.select()
	if nnum == 6:
		s14.disable()
	s15 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((830, 0), (45, 30)),
														text='15',
														manager=manager)
	if survival_rules[15]:
		s15.select()
	if nnum == 6:
		s15.disable()
	s16 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((880, 0), (45, 30)),
														text='16',
														manager=manager)
	if survival_rules[16]:
		s16.select()
	if nnum == 6:
		s16.disable()
	s17 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((930, 0), (45, 30)),
														text='17',
														manager=manager)
	if survival_rules[17]:
		s17.select()
	if nnum == 6:
		s17.disable()
	s18 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((980, 0), (45, 30)),
														text='18',
														manager=manager)
	if survival_rules[18]:
		s18.select()
	if nnum == 6:
		s18.disable()
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10,35),(75,20)),
														manager=manager,
														text='Birth:')
	b0 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((80, 30), (45, 30)),
														text='0',
														manager=manager)
	if birth_rules[0]:
		b0.select()
	b1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 30), (45, 30)),
														text='1',
														manager=manager)
	if birth_rules[1]:
		b1.select()
	b2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((180, 30), (45, 30)),
														text='2',
														manager=manager)
	if birth_rules[2]:
		b2.select()
	b3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, 30), (45, 30)),
														text='3',
														manager=manager)
	if birth_rules[3]:
		b3.select()
	b4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 30), (45, 30)),
														text='4',
														manager=manager)
	if birth_rules[4]:
		b4.select()
	b5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 30), (45, 30)),
														text='5',
														manager=manager)
	if birth_rules[5]:
		b5.select()
	b6 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((380, 30), (45, 30)),
														text='6',
														manager=manager)
	if birth_rules[6]:
		b6.select()
	b7 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((430, 30), (45, 30)),
														text='7',
														manager=manager)
	if birth_rules[7]:
		b7.select()
	if nnum == 6:
		b7.disable()
	b8 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 30), (45, 30)),
														text='8',
														manager=manager)
	if birth_rules[8]:
		b8.select()
	if nnum == 6:
		b8.disable()
	b9 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((530, 30), (45, 30)),
														text='9',
														manager=manager)
	if birth_rules[9]:
		b9.select()
	if nnum == 6:
		b9.disable()
	b10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((580, 30), (45, 30)),
														text='10',
														manager=manager)
	if birth_rules[10]:
		b10.select()
	if nnum == 6:
		b10.disable()
	b11 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((630, 30), (45, 30)),
														text='11',
														manager=manager)
	if birth_rules[11]:
		b11.select()
	if nnum == 6:
		b11.disable()
	b12 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 30), (45, 30)),
														text='12',
														manager=manager)
	if birth_rules[12]:
		b12.select()
	if nnum == 6:
		b12.disable()
	b13 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((730, 30), (45, 30)),
														text='13',
														manager=manager)
	if birth_rules[13]:
		b13.select()
	if nnum == 6:
		b13.disable()
	b14 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((780, 30), (45, 30)),
														text='14',
														manager=manager)
	if birth_rules[14]:
		b14.select()
	if nnum == 6:
		b14.disable()
	b15 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((830, 30), (45, 30)),
														text='15',
														manager=manager)
	if birth_rules[15]:
		b15.select()
	if nnum == 6:
		b15.disable()
	b16 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((880, 30), (45, 30)),
														text='16',
														manager=manager)
	if birth_rules[16]:
		b16.select()
	if nnum == 6:
		b16.disable()
	b17 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((930, 30), (45, 30)),
														text='17',
														manager=manager)
	if birth_rules[17]:
		b17.select()
	if nnum == 6:
		b17.disable()
	b18 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((980, 30), (45, 30)),
														text='18',
														manager=manager)
	if birth_rules[18]:
		b18.select()
	if nnum == 6:
		b18.disable()
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10,66),(45,20)),
														manager=manager,
														text='N:')
	neighbor_menu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((45,60),(45,30)),
														manager=manager,
														options_list=['6','18'],
														starting_option=str(nnum))
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-35,90),(100,20)),
														manager=manager,
														text='FPS')
	fps_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 110), (100, 30)),
														manager=manager,
														start_value=fps,
														value_range=(5,30))
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-30,140),(140,20)),
														manager=manager,
														text='Tile Width')
	tilewidth_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 160), (100, 30)),
														manager=manager,
														start_value=hex_width,
														value_range=(5,100))
	showgrid_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 190), (100, 30)),
														text='Show Grid',
														manager=manager)
	shownumbers_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 220), (100, 30)),
														text='Show Nums',
														manager=manager)
	paused_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 250), (100, 30)),
														text='Pause',
														manager=manager)
	blank_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 280), (100, 30)),
														text='Blank',
														manager=manager)
	random_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 310), (100, 30)),
														text='Random',
														manager=manager)
	sound_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 340), (100, 30)),
														text='Sound',
														manager=manager)
	if sound:
		sound_button.select()
	render_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 370), (100, 30)),
														text='Render',
														manager=manager)
	color_picker = None
	clock = pygame.time.Clock()
	is_running = True
	build_grid()
	frame_num = 0 #for renders
	while is_running:
		time_delta = clock.tick(fps)/1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_running = False
				quit()
			if event.type == pygame.VIDEORESIZE:
				width = event.w
				height = event.h
				#screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
				hexagons = []
				build_grid()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				if paused:
					paused = False
				else:
					paused = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				for k,hex in enumerate(hexagons):
					if hex[0].collidepoint(event.pos): 
						if sound:
							tile_sound.play()
						if hex[1]:
							hexagons[k] = hex[0],0,hex[2],hex[3],hex[4]
						else:
							hexagons[k] = hex[0],1,hex[2],hex[3],hex[4]
						#breifly highlight the neighborhood of the selected tile
						if nnum == 6:
							n = hex[3]
						elif nnum == 18:
							n = hex[3]+hex[4]
						for offset in n:
							x_offset = hexagons[k+offset][0].x
							y_offset = hexagons[k+offset][0].y
							animated_hexagons.append([x_offset,y_offset])
				for k,swatch in enumerate(legend_buttons):
					if swatch.collidepoint(event.pos):
						current_swatch = k
						color =  colors['n'+str(nnum)][k]
						color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect((100, 300), (390, 390)),
														window_title='pick color for '+str(k)+' neighbors',
														manager=manager,
														initial_colour=pygame.Color(color)
														)
			if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
				colors['n'+str(nnum)][current_swatch] = event.colour
				current_swatch = None
			if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
				if event.ui_element == fps_slider:
					fps = event.value
				if event.ui_element == tilewidth_slider:
					hex_width = event.value
					hex_height = int(hex_width * 0.8660254)
					hexagons = []
					build_grid()
			if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
				if event.ui_element == neighbor_menu:
					nnum = int(event.text)
					if nnum == 6:
						s7.disable()
						s8.disable()
						s9.disable()
						s10.disable()
						s11.disable()
						s12.disable()
						s13.disable()
						s14.disable()
						s15.disable()
						s16.disable()
						s17.disable()
						s18.disable()
						b7.disable()
						b8.disable()
						b9.disable()
						b10.disable()
						b11.disable()
						b12.disable()
						b13.disable()
						b14.disable()
						b15.disable()
						b16.disable()
						b17.disable()
						b18.disable()
					elif nnum == 18:
						s7.enable()
						s8.enable()
						s9.enable()
						s10.enable()
						s11.enable()
						s12.enable()
						s13.enable()
						s14.enable()
						s15.enable()
						s16.enable()
						s17.enable()
						s18.enable()
						b7.enable()
						b8.enable()
						b9.enable()
						b10.enable()
						b11.enable()
						b12.enable()
						b13.enable()
						b14.enable()
						b15.enable()
						b16.enable()
						b17.enable()
						b18.enable()
			if event.type == pygame_gui.UI_BUTTON_PRESSED:
				if event.ui_element == showgrid_button:
					if show_grid:
						show_grid = False
						showgrid_button.unselect()
					else:
						show_grid = True
						showgrid_button.select()
				if event.ui_element == shownumbers_button:
					if show_numbers:
						show_numbers = False
						shownumbers_button.unselect()
					else:
						show_numbers = True
						shownumbers_button.select()
				if event.ui_element == render_button:
					if render:
						render = False
						render_button.unselect()
					else:
						render = True
						render_button.select()
						frame_num = 0
				if event.ui_element == paused_button:
					if paused:
						paused_button.unselect()
						paused = False
					else:
						paused = True
						paused_button.select()
				if event.ui_element == random_button:
					hexagons = []
					build_grid()
				if event.ui_element == blank_button:
					if not paused:
						paused = True
						paused_button.select()
					for k,pos in enumerate(hexagons):
						hexagons[k] = [pos[0],0,0,pos[3],pos[4]]
				if event.ui_element == sound_button:
					if sound:
						sound = False
						sound_button.unselect()
					else:
						sound = True
						sound_button.select()
				if event.ui_element == s0:
					if survival_rules[0]:
						survival_rules[0] = False
						s0.unselect()
					else:
						survival_rules[0] = True
						s0.select()
				if event.ui_element == s1:
					if survival_rules[1]:
						survival_rules[1] = False
						s1.unselect()
					else:
						survival_rules[1] = True
						s1.select()
				if event.ui_element == s2:
					if survival_rules[2]:
						survival_rules[2] = False
						s2.unselect()
					else:
						survival_rules[2] = True
						s2.select()
				if event.ui_element == s3:
					if survival_rules[3]:
						survival_rules[3] = False
						s3.unselect()
					else:
						survival_rules[3] = True
						s3.select()
				if event.ui_element == s4:
					if survival_rules[4]:
						survival_rules[4] = False
						s4.unselect()
					else:
						survival_rules[4] = True
						s4.select()
				if event.ui_element == s5:
					if survival_rules[5]:
						survival_rules[5] = False
						s5.unselect()
					else:
						survival_rules[5] = True
						s5.select()
				if event.ui_element == s6:
					if survival_rules[6]:
						survival_rules[6] = False
						s6.unselect()
					else:
						survival_rules[6] = True
						s6.select()
				if event.ui_element == s7:
					if survival_rules[7]:
						survival_rules[7] = False
						s7.unselect()
					else:
						survival_rules[7] = True
						s7.select()
				if event.ui_element == s8:
					if survival_rules[8]:
						survival_rules[8] = False
						s8.unselect()
					else:
						survival_rules[8] = True
						s8.select()
				if event.ui_element == s9:
					if survival_rules[9]:
						survival_rules[9] = False
						s9.unselect()
					else:
						survival_rules[9] = True
						s9.select()
				if event.ui_element == s10:
					if survival_rules[10]:
						survival_rules[10] = False
						s10.unselect()
					else:
						survival_rules[10] = True
						s10.select()
				if event.ui_element == s11:
					if survival_rules[11]:
						survival_rules[11] = False
						s11.unselect()
					else:
						survival_rules[11] = True
						s11.select()
				if event.ui_element == s12:
					if survival_rules[12]:
						survival_rules[12] = False
						s12.unselect()
					else:
						survival_rules[12] = True
						s12.select()
				if event.ui_element == s13:
					if survival_rules[13]:
						survival_rules[13] = False
						s13.unselect()
					else:
						survival_rules[13] = True
						s13.select()
				if event.ui_element == s14:
					if survival_rules[14]:
						survival_rules[14] = False
						s14.unselect()
					else:
						survival_rules[14] = True
						s14.select()
				if event.ui_element == s15:
					if survival_rules[15]:
						survival_rules[15] = False
						s15.unselect()
					else:
						survival_rules[15] = True
						s15.select()
				if event.ui_element == s16:
					if survival_rules[16]:
						survival_rules[16] = False
						s16.unselect()
					else:
						survival_rules[16] = True
						s16.select()
				if event.ui_element == s17:
					if survival_rules[17]:
						survival_rules[17] = False
						s17.unselect()
					else:
						survival_rules[17] = True
						s17.select()
				if event.ui_element == s18:
					if survival_rules[18]:
						survival_rules[18] = False
						s18.unselect()
					else:
						survival_rules[18] = True
						s18.select()
				if event.ui_element == b0:
					if birth_rules[0]:
						birth_rules[0] = False
						b0.unselect()
					else:
						birth_rules[0] = True
						b0.select()
				if event.ui_element == b1:
					if birth_rules[1]:
						birth_rules[1] = False
						b1.unselect()
					else:
						birth_rules[1] = True
						b1.select()
				if event.ui_element == b2:
					if birth_rules[2]:
						birth_rules[2] = False
						b2.unselect()
					else:
						birth_rules[2] = True
						b2.select()
				if event.ui_element == b3:
					if birth_rules[3]:
						birth_rules[3] = False
						b3.unselect()
					else:
						birth_rules[3] = True
						b3.select()
				if event.ui_element == b4:
					if birth_rules[4]:
						birth_rules[4] = False
						b4.unselect()
					else:
						birth_rules[4] = True
						b4.select()
				if event.ui_element == b5:
					if birth_rules[5]:
						birth_rules[5] = False
						b5.unselect()
					else:
						birth_rules[5] = True
						b5.select()
				if event.ui_element == b6:
					if birth_rules[6]:
						birth_rules[6] = False
						b6.unselect()
					else:
						birth_rules[6] = True
						b6.select()
				if event.ui_element == b7:
					if birth_rules[7]:
						birth_rules[7] = False
						b7.unselect()
					else:
						birth_rules[7] = True
						b7.select()
				if event.ui_element == b8:
					if birth_rules[8]:
						birth_rules[8] = False
						b8.unselect()
					else:
						birth_rules[8] = True
						b8.select()
				if event.ui_element == b9:
					if birth_rules[9]:
						birth_rules[9] = False
						b9.unselect()
					else:
						birth_rules[9] = True
						b9.select()
				if event.ui_element == b10:
					if birth_rules[10]:
						birth_rules[10] = False
						b10.unselect()
					else:
						birth_rules[10] = True
						b10.select()
				if event.ui_element == b11:
					if birth_rules[11]:
						birth_rules[11] = False
						b11.unselect()
					else:
						birth_rules[11] = True
						b11.select()
				if event.ui_element == b12:
					if birth_rules[12]:
						birth_rules[12] = False
						b12.unselect()
					else:
						birth_rules[12] = True
						b12.select()
				if event.ui_element == b13:
					if birth_rules[13]:
						birth_rules[13] = False
						b13.unselect()
					else:
						birth_rules[13] = True
						b13.select()
				if event.ui_element == b14:
					if birth_rules[14]:
						birth_rules[14] = False
						b14.unselect()
					else:
						birth_rules[14] = True
						b14.select()
				if event.ui_element == b15:
					if birth_rules[15]:
						birth_rules[15] = False
						b15.unselect()
					else:
						birth_rules[15] = True
						b15.select()
				if event.ui_element == b16:
					if birth_rules[16]:
						birth_rules[16] = False
						b16.unselect()
					else:
						birth_rules[16] = True
						b16.select()
				if event.ui_element == b17:
					if birth_rules[17]:
						birth_rules[17] = False
						b17.unselect()
					else:
						birth_rules[17] = True
						b17.select()
				if event.ui_element == b18:
					if birth_rules[18]:
						birth_rules[18] = False
						b18.unselect()
					else:
						birth_rules[18] = True
						b18.select()
			manager.process_events(event)
		manager.update(time_delta)
		background = pygame.Surface((width, height))
		background.fill((0,0,0))
		screen.blit(background, (0, 0))
		#draw last iteration
		old_hexagons = hexagons.copy()
		
		for k,hex in enumerate(old_hexagons):
			x_offset = hex[0].x
			y_offset = hex[0].y
			color='Black'
			if hex[1]:
				if nnum == 6:
					color = colors['n6'][hex[2]]
				elif nnum == 18:
					color = colors['n18'][hex[2]]
			pygame.draw.polygon(screen,color,[(x_offset,y_offset + hex_height/2),
												(x_offset + hex_width/4,y_offset + hex_height),
												(x_offset + 3*hex_width/4,y_offset + hex_height),
												(x_offset + hex_width,y_offset + hex_height/2),
												(x_offset + 3*hex_width/4,y_offset),
												(x_offset + hex_width/4,y_offset)]
											,0)
			if show_numbers:
				screen.blit(font.render(str(k), True, 'White'), (x_offset+hex_width/2-10, y_offset+hex_height/2-10))
			#compute next iteration
			if not paused:
				neighbor_count = 0
				if nnum == 6:
					n = hex[3]
				elif nnum == 18:
					n = hex[3]+hex[4]
				for offset in n:
					if k+offset >= 0 and k+offset < len(hexagons): #shouldn't need this
						if old_hexagons[k+offset][1]:
							neighbor_count += 1
					#else: print('out of bounds: ',k,'+',offset)
				if hex[1]:
					#survival rules
					if survival_rules[neighbor_count]:
						hexagons[k] = [hex[0],1,neighbor_count,hex[3],hex[4]]
					else:
						hexagons[k] = [hex[0],0,neighbor_count,hex[3],hex[4]]
				if not hex[1]:
					#birth rules
					if birth_rules[neighbor_count]:
						hexagons[k] = [hex[0],1,neighbor_count,hex[3],hex[4]]
					else:
						hexagons[k] = [hex[0],0,neighbor_count,hex[3],hex[4]]
		if animated_hexagons:
			for k, hexagon in enumerate(animated_hexagons):
				x_offset = hexagon[0]
				y_offset = hexagon[1]
				pygame.draw.polygon(screen,'White',[(x_offset,y_offset + hex_height/2),
											(x_offset + hex_width/4,y_offset + hex_height),
											(x_offset + 3*hex_width/4,y_offset + hex_height),
											(x_offset + hex_width,y_offset + hex_height/2),
											(x_offset + 3*hex_width/4,y_offset),
											(x_offset + hex_width/4,y_offset)]
										,0)
		animated_hexagons = []
		#overlay grid
		if show_grid:
			for hex in hexagons:
				x_offset = hex[0].x
				y_offset = hex[0].y
				pygame.draw.polygon(screen,'White',[(x_offset,y_offset + hex_height/2),
													(x_offset + hex_width/4,y_offset + hex_height),
													(x_offset + 3*hex_width/4,y_offset + hex_height),
													(x_offset + hex_width,y_offset + hex_height/2),
													(x_offset + 3*hex_width/4,y_offset),
													(x_offset + hex_width/4,y_offset)]
												,1)
		#draw legend
		swatch_x = 0
		swatch_y = 0
		legend_buttons = []
		for i in range(0,nnum+1):
			swatch_surf = pygame.Surface((25,25))
			if nnum == 6:
				swatch_surf.fill(colors['n6'][i])
			elif nnum == 18:
				swatch_surf.fill(colors['n18'][i])
			rect = screen.blit(swatch_surf,(swatch_x*30+8,swatch_y*30+405))
			screen.blit(font.render(str(i),False,'Black'),(swatch_x*30+12,swatch_y*30+410))
			legend_buttons.append(rect)
			if swatch_x == 2:
				swatch_x = 0
				swatch_y += 1
			else: 
				swatch_x += 1
		if paused:
			screen.blit(font.render('--PAUSED--',0,'White'),(10,height-30))
		#detect a dead grid
		dead = False
		if old_hexagons == hexagons and not paused:
			dead = True
			screen.blit(font.render('--DEAD--',0,'White'),(15,height-60))
		manager.draw_ui(screen)
		if not paused and not dead and sound:
			grow_sound.play()
		if is_running:
			pygame.display.update()
			if render:
				pygame.image.save(screen,'render/hexomata'+str(frame_num)+'.png')
			frame_num += 1
	main()
if __name__ == "__main__":
    main()
