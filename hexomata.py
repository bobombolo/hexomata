#!/usr/bin/python3
import pygame
import pygame_gui
import random
import math

pygame.init()
width = 1024
height = 600
pygame.display.set_caption('Hexomata')
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont(None, 24)
fps = 60
ruleset = '23/2'
hex_width = 50
show_grid = True
show_numbers = False
def explode_rules(ruleset):
	survival = []
	birth = []
	splitstring = ruleset.split('/')
	for char in splitstring[0]:
		survival.append(int(char))
	for char in splitstring[1]:
		birth.append(int(char))
	return survival, birth
	
def main():
	global ruleset
	global fps
	global hex_width
	global show_grid
	global show_numbers
	background = pygame.Surface((width, height))
	background.fill((0,0,0))
	manager = pygame_gui.UIManager((width, height))
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-20,10),(100,20)),
														manager=manager,
														text='Ruleset')
	ruleset_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 30), (100, 30)),
														manager=manager,
														initial_text=ruleset)
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
	pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width/2-100,height-30),(200,20)),
														manager=manager,
														text='SPACE to reset')
	clock = pygame.time.Clock()
	is_running = True
	
	hex_radius = hex_width / 2
	hex_height = int(hex_width * 0.8660254)
	hexagons = []
	grid_width = int(width/hex_width/2)
	if grid_width%2: grid_width -= 1 #we only want an even number of columns
	grid_height = int(height/hex_radius)
	if grid_height%2: grid_height -= 1 #we only want an even number of rows
	grid_total = grid_width*grid_height
	hex_counter = 0
	for y in range(grid_height):
		y_offset = hex_height * y / 2 + 20
		for x in range(grid_width):
			
			if not y%2:
				x_offset = (hex_width + hex_width / 2 ) * x +150
			else:
				x_offset = (hex_width + hex_width / 2 ) * x - 3 * hex_width / 4 +150
			
			hexagon = pygame.draw.polygon(screen,'Black',[(x_offset,y_offset + hex_height/2),
										(x_offset + hex_width/4,y_offset + hex_height),
										(x_offset + 3*hex_width/4,y_offset + hex_height),
										(x_offset + hex_width,y_offset + hex_height/2),
										(x_offset + 3*hex_width/4,y_offset),
										(x_offset + hex_width/4,y_offset)]
									,1)
			hex_neighbor_offsets = []
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
												grid_width-1,
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
												+1,
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
				if y%2 and x == 0: #leftmost tile on even rows
					hex_neightbor_offsets = [-1,
												grid_width*2-1,
												-grid_width,
												grid_width,
												-grid_width*2,
												grid_width*2]
				elif not y%2 and x == grid_width-1: #rightmost tile on odd rows
					hex_neighbor_offsets = [1,
												-grid_width*2+1,
												-grid_width,
												grid_width,
												-grid_width*2,
												grid_width*2]
			#any remaining tiles are interior tiles:
			if hex_neighbor_offsets == []:
				if y%2:
					hex_neighbor_offsets = [-grid_width,
											-grid_width-1,
											grid_width-1,
											grid_width,
											grid_width*2,
											-grid_width*2]
				else:
					hex_neighbor_offsets = [-grid_width,
											-grid_width+1,
											grid_width+1,
											grid_width,
											grid_width*2,
											-grid_width*2]
			#hexagons index-> 0=rect, 1=state, 2=neighbor_count, 3=neighbor_offsets
			hexagons.insert(hex_counter,[hexagon,random.randint(0,1),0,hex_neighbor_offsets])
			hex_counter += 1
	while is_running:
		time_delta = clock.tick(fps)/1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_running = False
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				if is_running: is_running = False
			if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
				if event.ui_element == ruleset_field:
					ruleset = event.text
				if event.ui_element == fps_field:
					fps = int(event.text)
				if event.ui_element == hexwidth_field:
					hex_width = int(event.text)
					hex_height = int(hex_width * 0.8660254)
			if event.type == pygame_gui.UI_BUTTON_PRESSED:
				if event.ui_element == showgrid_button:
					if show_grid:
						show_grid = False
					else:
						show_grid = True
				if event.ui_element == shownumbers_button:
					if show_numbers:
						show_numbers = False
					else:
						show_numbers = True
					
			manager.process_events(event)
		manager.update(time_delta)
		screen.blit(background, (0, 0))
		#draw last iteration
		survival, birth = explode_rules(ruleset)
		for k,pos in enumerate(hexagons):
			x_offset = pos[0].x
			y_offset = pos[0].y
			color='Black'
			if pos[1]:
				if pos[2] == 0: color='White'
				elif pos[2] == 1: color='Yellow'
				elif pos[2] == 2: color='Green'
				elif pos[2] == 3: color='Blue'
				elif pos[2] == 4: color='Purple'
				elif pos[2] == 5: color='Magenta'
				elif pos[2] == 6: color='Red'
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
			neighbor_count = 0
			for offset in pos[3]:
				#if k+offset >= 0 and k+offset < grid_width*grid_height: #shouldn't need this
				if hexagons[k+offset][1]:
					neighbor_count += 1
				#else: print('out of bounds: ',k,'+',offset)
			survival, birth = explode_rules(ruleset)
			if pos[1]:
				#survival rules
				if neighbor_count in survival:
					hexagons[k] = [pos[0],1,neighbor_count,pos[3]]
				else:
					hexagons[k] = [pos[0],0,neighbor_count,pos[3]]
			if not pos[1]:
				#birth rules
				if neighbor_count in birth:
					hexagons[k] = [pos[0],1,neighbor_count,pos[3]]
				else:
					hexagons[k] = [pos[0],0,neighbor_count,pos[3]]
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
		pygame.display.update()
	main()
if __name__ == "__main__":
    main()
