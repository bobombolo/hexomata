#!/usr/bin/python3
import pygame
import pygame_gui
import random
import math
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
width = 1024
height = 600
super_width = 1920
super_height = 1080
current_window_x = super_width/2-(width-110)/2
current_window_y = super_height/2-(height-110)/2
grid_surface = pygame.Surface((super_width,super_height))
rings = 12
pygame.display.set_caption('Hexomata')
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font = pygame.font.Font(None, 24)
sound = True
grow_sound = pygame.mixer.Sound('sounds/click.wav')
tile_sound = pygame.mixer.Sound('sounds/clack.wav')
sounds = {}
for i in range(0,13):
	sounds['piano'+str(i)] = pygame.mixer.Sound('sounds/piano.'+str(i)+'.ogg')
fps = 25
survival_rules = [False,False,True,False,True,False,True]
birth_rules = [False,True,False,True,False,True,False]
hex_width = 30
hex_radius = hex_width / 2
hex_height = int(hex_width * 0.8660254)
middle_tile = ()
show_grid = True
show_numbers = False
render = False
paused = False
animated_hexagons = [] #highlights neighbors when tile is clicked
hexagons = [] #the master list [rect,active,neighbor_count,ring,neighbor_indexes
colors = ['#FFFF00','#FFA500','#FF0000','#FF00FF','#800080','#0000FF','#008000']
current_swatch = None
def draw_hexagon(x,y,color,line_width):
	hexagon = pygame.draw.polygon(grid_surface,color,[(x,y + hex_height/2),
											(x + hex_width/4,y + hex_height),
											(x + 3*hex_width/4,y + hex_height),
											(x + hex_width,y + hex_height/2),
											(x + 3*hex_width/4,y),
											(x + hex_width/4,y)],line_width)
	return hexagon
def build_grid(random_field=False):
	global hexagons
	old_poss = []
	if not random_field:
		for k,hex in enumerate(hexagons):
			if hex[1] == 1:
				old_poss.append([hex[0],1,hex[2],hex[3],hex[4]])
	hexagons = []
	center_x = int(super_width/2-hex_width/2)
	center_y = int(super_height/2-hex_height/2)
	hexagon = None
	x = 0
	y = 0
	for ring_num in range(rings):
		if ring_num == 0:
			x = center_x
			y = center_y
			hexagon = draw_hexagon(x,y,'black',0)
			hexagons.append([hexagon, 0, 0, ring_num,[]])
		for side_num in range(6):
			for side_member in range(ring_num):
				
				if side_num == 0:
					start_x = center_x
					start_y = center_y-hex_height*ring_num
					x = start_x+0.75*hex_width*(side_member)
					y = start_y+0.5*hex_height*(side_member)
				elif side_num == 1:
					start_x = center_x+0.75*hex_width*ring_num
					start_y = center_y-0.5*hex_height*ring_num
					x = start_x
					y = start_y+hex_height*(side_member)
				elif side_num == 2:
					start_x = center_x+0.75*hex_width*ring_num
					start_y = center_y+0.5*hex_height*ring_num
					x = start_x-0.75*hex_width*(side_member)
					y = start_y+0.5*hex_height*(side_member)
				elif side_num == 3:
					start_x = center_x
					start_y = center_y+hex_height*ring_num
					x = start_x-0.75*hex_width*(side_member)
					y = start_y-0.5*hex_height*(side_member)
				elif side_num == 4:
					start_x = center_x-0.75*hex_width*ring_num
					start_y = center_y+0.5*hex_height*ring_num
					x = start_x
					y = start_y-hex_height*(side_member)
				elif side_num == 5:
					start_x = center_x-0.75*hex_width*ring_num
					start_y = center_y-0.5*hex_height*ring_num
					x = start_x+0.75*hex_width*(side_member)
					y = start_y-0.5*hex_height*(side_member)
		
				hexagon = draw_hexagon(x,y,'black',0)
				
				hexagons.append([hexagon,0, 0, ring_num,[]])
	for k,hex in enumerate(hexagons):
		neighbors = []
		for j, neighbor in enumerate(hexagons):
			if not j == k and hex[0].colliderect(neighbor[0]):
				neighbors.append(j)
		hexagons[k] = [hex[0],hex[1],hex[2],hex[3],neighbors]
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
running = True
build_grid(False)
frame_num = 0 #for renders
angle = 0
while running:
	time_delta = clock.tick(fps)/1000.0
	grid_surface.fill('black')
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			quit()
		if event.type == pygame.VIDEORESIZE:
			width = event.w
			height = event.h
			manager.set_window_resolution((width,height))
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			if paused:
				paused = False
				paused_button.unselect()
			else:
				paused = True
				paused_button.select()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
			current_window_y -= 50
		if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
			current_window_y += 50
		if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
			current_window_x -= 50
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			current_window_x += 50
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not color_picker or not color_picker.relative_rect.collidepoint(event.pos):
				for k,hex in enumerate(hexagons):
					offset_pos = (event.pos[0]+current_window_x-100,event.pos[1]+current_window_y-60)
					if event.pos[0] > 100 and event.pos[1] > 60 and hex[0].collidepoint(offset_pos): 
						if sound:
							tile_sound.play()
						if hex[1]:
							hexagons[k] = [hex[0], 0, hex[2], hex[3], hex[4]]
						else:
							hexagons[k] = [hex[0], 1, hex[2], hex[3], hex[4]]
						#build_grid() #to colorize what we're drawing
						for neighbor in hex[4]:
							x = hexagons[neighbor][0].x
							y = hexagons[neighbor][0].y
							animated_hexagons.append([x,y])
			for k,swatch in enumerate(legend_buttons):
				if swatch.collidepoint(event.pos):
					current_swatch = k
					color =  colors[k]
					if color_picker:
						color_picker.hide()
					color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect((100, 200), (390, 390)),
													window_title='pick color for '+str(k)+' neighbors',
													manager=manager,
													initial_colour=pygame.Color(color)
													)
		#destroy the color picker if it is closed
		if event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_object_id == '#colour_picker_dialog':
			color_picker = None
		if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
			colors[current_swatch] = event.colour
			current_swatch = None
			color_picker = None
		if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
			if event.ui_element == fps_slider:
				fps = event.value
			if event.ui_element == tilewidth_slider:
				hex_width = event.value
				hex_height = int(hex_width * 0.8660254)
				build_grid()
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
				build_grid(True)
			if event.ui_element == blank_button:
				if not paused:
					paused = True
					paused_button.select()
				for k,hex in enumerate(hexagons):
					hexagons[k] = [hex[0],0,0,hex[3],hex[4]]
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
		manager.process_events(event)
	manager.update(time_delta)
	background = pygame.Surface((width, height))
	background.fill((0,0,0))
	screen.blit(background, (0, 0))
	#draw last iteration
	old_hexagons = hexagons.copy()
	for k,hex in enumerate(old_hexagons):
		x = hex[0].x
		y = hex[0].y
		if hex[1] == 1:
			draw_hexagon(x,y,colors[hex[2]],0)
		if show_numbers:
			grid_surface.blit(font.render(str(k), True, 'white'), (x+hex_width/2-10, y+hex_height/2-10))
		#compute next iteration
		if not paused:
			for k, hex in enumerate(old_hexagons):
				neighbor_count = 0
				for neighbor in hex[4]:
					if old_hexagons[neighbor][1]:
						neighbor_count += 1
				hex[2] = neighbor_count
				if hex[1] == 1 and survival_rules[neighbor_count]:
					state = 1
				elif hex[1] == 0 and birth_rules[neighbor_count]:
					state = 1
				else:
					state = 0
				hexagons[k] = [hex[0],state,hex[2],hex[3],hex[4]]
	#overlay grid
	if show_grid:
		for k, hex in enumerate(hexagons):
			line_width = 1
			if k == 0:
				line_width = 3
			x = hex[0].x
			y = hex[0].y
			draw_hexagon(x,y,'white',line_width)
	#draw playhead
	if paused:
		center = (super_width/2,super_height/2)
		endpoint = (super_width/2+rings*hex_height*math.cos(angle),super_height/2+rings*hex_height*math.sin(angle))
		pygame.draw.line(grid_surface, 'white', center, endpoint, width=1)
		angle += .01
		for k,hex in enumerate(old_hexagons):
			hex_center_rect = pygame.Rect(hex[0].x+0.5*hex_width-1, hex[0].y+0.5*hex_height-1, 3, 3)
			#pygame.draw.rect(grid_surface,'green',hex_center_rect,0)
			if hex[1] and hex_center_rect.clipline(center,endpoint):
				animated_hexagons.append([hex[0].x,hex[0].y])
				sounds['piano'+str(hex[3])].play()
	#render the flashing tiles
	if animated_hexagons:
		for k, hexagon in enumerate(animated_hexagons):
			x = hexagon[0]
			y = hexagon[1]
			draw_hexagon(x,y,'white',0)
	animated_hexagons = []
	#draw legend
	swatch_x = 0
	swatch_y = 0
	legend_buttons = []
	for i in range(0,7):
		swatch_surf = pygame.Surface((25,25))
		swatch_surf.fill(colors[i])
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
	cropped_region =  (current_window_x, current_window_y, width-100, height-60)
	screen.blit(grid_surface, (100, 60), cropped_region)
	manager.draw_ui(screen)
	if not paused and not dead and sound:
		grow_sound.play()
	if running:
		pygame.display.update()
		if render:
			pygame.image.save(grid_surface,'render/hexomata'+str(frame_num)+'.png')
		frame_num += 1
