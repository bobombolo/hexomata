#!/usr/bin/python3
import pygame
import pygame_gui
import random

pygame.init()
width = 1024
height = 600
pygame.display.set_caption('Hexomata')
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font = pygame.font.SysFont(None, 24)
sound = True
grow_sound = pygame.mixer.Sound('sounds/click.wav')
tile_sound = pygame.mixer.Sound('sounds/clack.wav')
fps = 5
ruleset = '23/2'
survival_rules = [False,True,True,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
birth_rules = [False,True,False,False,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
hex_width = 50
show_grid = False
show_numbers = False
render = False
paused = False

def main():
	global screen
	global width
	global height
	global ruleset
	global fps
	global hex_width
	global show_grid
	global show_numbers
	global render
	global paused
	global sound
	
	background = pygame.Surface((width, height))
	background.fill((0,0,0))
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
	s8 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 0), (45, 30)),
														text='8',
														manager=manager)
	if survival_rules[8]:
		s8.select()
	s9 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((530, 0), (45, 30)),
														text='9',
														manager=manager)
	if survival_rules[9]:
		s9.select()
	s10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((580, 0), (45, 30)),
														text='10',
														manager=manager)
	if survival_rules[10]:
		s10.select()
	s11 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((630, 0), (45, 30)),
														text='11',
														manager=manager)
	if survival_rules[11]:
		s11.select()
	s12 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 0), (45, 30)),
														text='12',
														manager=manager)
	if survival_rules[12]:
		s12.select()
	s13 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((730, 0), (45, 30)),
														text='13',
														manager=manager)
	if survival_rules[13]:
		s13.select()
	s14 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((780, 0), (45, 30)),
														text='14',
														manager=manager)
	if survival_rules[14]:
		s14.select()
	s15 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((830, 0), (45, 30)),
														text='15',
														manager=manager)
	if survival_rules[15]:
		s15.select()
	s16 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((880, 0), (45, 30)),
														text='16',
														manager=manager)
	if survival_rules[16]:
		s16.select()
	s17 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((930, 0), (45, 30)),
														text='17',
														manager=manager)
	if survival_rules[17]:
		s17.select()
	s18 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((980, 0), (45, 30)),
														text='18',
														manager=manager)
	if survival_rules[18]:
		s18.select()
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
	b8 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 30), (45, 30)),
														text='8',
														manager=manager)
	if birth_rules[8]:
		b8.select()
	b9 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((530, 30), (45, 30)),
														text='9',
														manager=manager)
	if birth_rules[9]:
		b9.select()
	b10 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((580, 30), (45, 30)),
														text='10',
														manager=manager)
	if birth_rules[10]:
		b10.select()
	b11 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((630, 30), (45, 30)),
														text='11',
														manager=manager)
	if birth_rules[11]:
		b11.select()
	b12 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 30), (45, 30)),
														text='12',
														manager=manager)
	if birth_rules[12]:
		b12.select()
	b13 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((730, 30), (45, 30)),
														text='13',
														manager=manager)
	if birth_rules[13]:
		b13.select()
	b14 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((780, 30), (45, 30)),
														text='14',
														manager=manager)
	if birth_rules[14]:
		b14.select()
	b15 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((830, 30), (45, 30)),
														text='15',
														manager=manager)
	if birth_rules[15]:
		b15.select()
	b16 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((880, 30), (45, 30)),
														text='16',
														manager=manager)
	if birth_rules[16]:
		b16.select()
	b17 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((930, 30), (45, 30)),
														text='17',
														manager=manager)
	if birth_rules[17]:
		b17.select()
	b18 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((980, 30), (45, 30)),
														text='18',
														manager=manager)
	if birth_rules[18]:
		b18.select()
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-35,60),(100,20)),
														manager=manager,
														text='FPS')
	fps_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 80), (100, 30)),
														manager=manager,
														initial_text=str(fps))
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-30,110),(140,20)),
														manager=manager,
														text='Tile Width')
	hexwidth_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 130), (100, 30)),
														manager=manager,
														initial_text=str(hex_width))
	showgrid_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 160), (100, 30)),
														text='Show Grid',
														manager=manager)
	shownumbers_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 190), (100, 30)),
														text='Show Nums',
														manager=manager)
	paused_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 220), (100, 30)),
														text='Pause',
														manager=manager)
	blank_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 250), (100, 30)),
														text='Blank',
														manager=manager)
	sound_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 280), (100, 30)),
														text='Sound',
														manager=manager)
	if sound:
		sound_button.select()
	render_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 350), (100, 30)),
														text='Render',
														manager=manager)
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width/2-250,height-30),(500,20)),
														manager=manager,
														text='SPACE to reset -- Click Mouse to activate / deactivate a tile')
	clock = pygame.time.Clock()
	is_running = True
	
	hex_radius = hex_width / 2
	hex_height = int(hex_width * 0.8660254)
	hexagons = []
	animated_hexagons = [] #highlights neighbors when tile is clicked
	grid_width = int((width-hex_width*2)/(hex_width+hex_width/2))
	if grid_width%2: grid_width -= 1 #we only want an even number of columns
	grid_height = int((height-hex_height)/(hex_height/2))
	if grid_height%2: grid_height -= 1 #we only want an even number of rows
	grid_total = grid_width*grid_height
	hex_counter = 0
	for y in range(grid_height):
		y_offset = hex_height * y / 2 + 70
		for x in range(grid_width):
			
			if not y%2:
				x_offset = (hex_width + hex_width / 2 ) * x +140
			else:
				x_offset = (hex_width + hex_width / 2 ) * x - 3 * hex_width / 4 +140
			
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
		for offset in pos[3]+pos[4]:
			if k+offset >= 0 and k+offset < grid_width*grid_height: #shouldn't need this
				if hexagons[k+offset][1]:
					neighbor_count += 1
			else: print('out of bounds: ',k,'+',offset)
		if pos[1]:
			hexagons[k] = [pos[0],1,neighbor_count,pos[3],pos[4]]
		else:
			hexagons[k] = [pos[0],0,neighbor_count,pos[3],pos[4]]
	frame_num = 0
	while is_running:
		time_delta = clock.tick(fps)/1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_running = False
				quit()
			if event.type == pygame.WINDOWRESIZED:
				#screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
				width = screen.get_width()
				height = screen.get_height()
				is_running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				if is_running: is_running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				for k,pos in enumerate(hexagons):
					if pos[0].collidepoint(event.pos): 
						if sound:
							tile_sound.play()
						if pos[1]:
							hexagons[k] = pos[0],0,pos[2],pos[3],pos[4]
						else:
							hexagons[k] = pos[0],1,pos[2],pos[3],pos[4]
						#breifly highlight the neighborhood of the selected tile
						for offset in pos[3]+pos[4]:
							x_offset = hexagons[k+offset][0].x
							y_offset = hexagons[k+offset][0].y
							animated_hexagons.append([x_offset,y_offset])
			if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
				if event.ui_element == fps_field:
					fps = int(event.text)
				if event.ui_element == hexwidth_field:
					hex_width = int(event.text)
					hex_height = int(hex_width * 0.8660254)
					if is_running: is_running = False
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
		screen.blit(background, (0, 0))
		if paused:
			screen.blit(font.render('--PAUSED--',0,'White'),(0,height-30))
		#draw last iteration
		old_hexagons = hexagons.copy()
		for k,pos in enumerate(old_hexagons):
			x_offset = pos[0].x
			y_offset = pos[0].y
			color='Black'
			if pos[1]:
				if pos[2] == 0: color='#FFFF00'
				elif pos[2] == 1: color='#BFFF00'
				elif pos[2] == 3: color='#80FF00'
				elif pos[2] == 4: color='#40FF00'
				elif pos[2] == 5: color='#00FF00'
				elif pos[2] == 6: color='#00FF40'
				elif pos[2] == 7: color='#00FF80'
				elif pos[2] == 8: color='#00FFBF'
				elif pos[2] == 9: color='#00FFFF'
				elif pos[2] == 10: color='#00BFFF'
				elif pos[2] == 11: color='#0080FF'
				elif pos[2] == 12: color='#0040FF'
				elif pos[2] == 13: color='#0000FF'
				elif pos[2] == 14: color='#4000FF'
				elif pos[2] == 15: color='#8000FF'
				elif pos[2] == 16: color='#BF00FF'
				elif pos[2] == 17: color='#FF00FF'
				elif pos[2] == 18: color='#FF00BF'
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
				for offset in pos[3]+pos[4]:
					if k+offset >= 0 and k+offset < grid_width*grid_height: #shouldn't need this
						if old_hexagons[k+offset][1]:
							neighbor_count += 1
					else: print('out of bounds: ',k,'+',offset)
				if pos[1]:
					#survival rules
					if survival_rules[neighbor_count]:
						hexagons[k] = [pos[0],1,neighbor_count,pos[3],pos[4]]
					else:
						hexagons[k] = [pos[0],0,neighbor_count,pos[3],pos[4]]
				if not pos[1]:
					#birth rules
					if birth_rules[neighbor_count]:
						hexagons[k] = [pos[0],1,neighbor_count,pos[3],pos[4]]
					else:
						hexagons[k] = [pos[0],0,neighbor_count,pos[3],pos[4]]
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
		#detect a dead grid
		dead = False
		if old_hexagons == hexagons and not paused:
			dead = True
			screen.blit(font.render('--DEAD--',0,'White'),(15,height-60))
		#overlay grid
		if show_grid:
			for k,pos in enumerate(hexagons):
				x_offset = pos[0].x
				y_offset = pos[0].y
				pygame.draw.polygon(screen,'White',[(x_offset,y_offset + hex_height/2),
													(x_offset + hex_width/4,y_offset + hex_height),
													(x_offset + 3*hex_width/4,y_offset + hex_height),
													(x_offset + hex_width,y_offset + hex_height/2),
													(x_offset + 3*hex_width/4,y_offset),
													(x_offset + hex_width/4,y_offset)]
												,1)
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
