#!/usr/bin/python3
import pygame
import pygame_gui
import random
import math

pygame.init()
width = 800
height = 600
pygame.display.set_caption('Hexomata')
screen = pygame.display.set_mode((width, height))

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
	ruleset = '23/2'
	background = pygame.Surface((width, height))
	background.fill((0,0,0))
	manager = pygame_gui.UIManager((width, height))
	ruleset_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (100, 50)),
														manager=manager,
														initial_text=ruleset)
	clock = pygame.time.Clock()
	is_running = True
	hex_width = 20
	hex_radius = hex_width / 2
	hex_height = int(hex_width * 0.8660254)
	hexagon_poss = []
	grid_width = int(3*width/hex_width/4)
	grid_height = int(1.2*height/hex_radius)
	hex_counter = 0
	for y in range(grid_height):
		y_offset = hex_height * y / 2
		for x in range(grid_width):
			
			if not y%2:
				x_offset = (hex_width + hex_width / 2 ) * x
			else:
				x_offset = (hex_width + hex_width / 2 ) * x - 3 * hex_width / 4
			
			hexagon = pygame.draw.polygon(screen,'Black',[(x_offset,y_offset + hex_height/2),
										(x_offset + hex_width/4,y_offset + hex_height),
										(x_offset + 3*hex_width/4,y_offset + hex_height),
										(x_offset + hex_width,y_offset + hex_height/2),
										(x_offset + 3*hex_width/4,y_offset),
										(x_offset + hex_width/4,y_offset)]
									,1)
			hexagon_poss.insert(hex_counter,[hexagon,random.randint(0,1),0])
			hex_counter += 1
	while is_running:
		time_delta = clock.tick(60)/1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_running = False
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				if is_running: is_running = False
			if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
				if event.ui_element == ruleset_field:
					ruleset = event.text
			manager.process_events(event)
		manager.update(time_delta)
		#screen.blit(background, (0, 0))
		for k,pos in enumerate(hexagon_poss):
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
			neighbors = []
			neighbor_count = 0
			
			neighborhood_index_offsets = [-grid_width, #not too sure about these offsets
											-grid_width+1,
											grid_width+1,
											grid_width,
											grid_width*2,
											-grid_width*2]
			
			for offset in neighborhood_index_offsets:
				collision = False
				if k+offset > 0 and k+offset < grid_width*grid_height:
					collision = pos[0].colliderect(hexagon_poss[k+offset][0])
				if collision:
					if hexagon_poss[k+offset][1]:
						neighbor_count += 1
			survival, birth = explode_rules(ruleset)
			if pos[1]:
				#survival rules
				if neighbor_count in survival:
					hexagon_poss[k] = [pos[0],1,neighbor_count]
				else:
					hexagon_poss[k] = [pos[0],0,neighbor_count]
			if not pos[1]:
				#birth rules
				if neighbor_count in birth:
					hexagon_poss[k] = [pos[0],1,neighbor_count]
				else:
					hexagon_poss[k] = [pos[0],0,neighbor_count]
		manager.draw_ui(screen)
		pygame.display.update()
	main()
if __name__ == "__main__":
    main()
