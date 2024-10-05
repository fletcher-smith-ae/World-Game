import pygame
import sys
import json
import os
import pygame.gfxdraw
import math
import random
import time
import numpy as np
import tracemalloc
import gpustat
import psutil

# TO-DO
# - Add import old save files (easy)

# Initialize pygame
pygame.init()

# Scaling factor to fit window on screen
scale = 1

# Set up the main window
width = int(800 * scale)
height = int(480 * scale)
screen = pygame.display.set_mode((width, height), 0, 32)  # Add a flag later for hardware implementation
pygame.display.set_caption("Worlds")
# pygame.transform.smoothscale(screen, (width, height))
screen_width = screen.get_width()
screen_height = screen.get_height()

# Drawing surface size
res_scale = 5
draw_width = width * res_scale  # Make the drawing surface have 10x resolution
draw_height = height * res_scale
pen_thickness = 10
# Page 1 drawing surface
drawing_surface1 = pygame.Surface((draw_width, draw_height), pygame.SRCALPHA)
drawing_surface1.fill((0, 0, 0, 0))  # Transparent background
# Page 2 screen drawing surface
drawing_surface2 = pygame.Surface((draw_width, draw_height), pygame.SRCALPHA)
drawing_surface2.fill((0, 0, 0, 0))  # Transparent background
# Page3 screen drawing surface
drawing_surface3 = pygame.Surface((draw_width, draw_height), pygame.SRCALPHA)
drawing_surface3.fill((0, 0, 0, 0))  # Transparent background
# Eraser Surface that is Invisible
eraser_surface = pygame.Surface((draw_width, draw_height), pygame.SRCALPHA)
eraser_surface.fill((0, 0, 0, 0))  # Transparent background
# Inventory screen drawing surface
inventory_drawing_surface = pygame.Surface((draw_width, draw_height), pygame.SRCALPHA)
inventory_drawing_surface.fill((0, 0, 0, 0))  # Transparent background

# Load in the background image
background_image = pygame.image.load('linedpaper.png')
background_image = pygame.transform.scale(background_image, (width, height))

# Load in World Logo
logo = pygame.image.load('World Logo.png')
logo_width = logo.get_width() / 4
logo_height = logo.get_height() / 4
logo = pygame.transform.scale(logo, (logo_width, logo_height))

# Define colors
background_color = (255, 255, 255)
default_button_color = (0, 0, 0)
button_hover_color = (240, 240, 240)
text_color = (255, 255, 255)
pen_color = (0, 0, 0)
eraser_color = (255, 255, 255)
inactive_button_color = (200, 200, 200) # If the player has not changed the name of the game the start button is 'inactive'
active_tool_color = (0, 0, 0)
inactive_tool_color = (200, 200, 200)

# General Button Settings
button_width = 320 * 0.5
button_height = 50 * 0.5

# Set up fonts
font = pygame.font.SysFont(None, int(36 * 0.5))

# Tool Selector Buttons
# Pencil Tool
pen_str = "Pen"
pen_rect = pygame.Rect(screen_width / 2 - button_width / 2, screen_height - button_height, button_width / 2, button_height)
pen = True # Whether the pen tool is active
# Eraser Tool
eraser_str = "Eraser"
eraser_rect = pygame.Rect(screen_width / 2 + button_width / 2, screen_height - button_height, button_width / 2, button_height)
eraser = False # Whether eraser tool is active

# Login Button
login_str = 'LOGIN' # Initialize as this to que login
login_rect = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 2 - button_height / 2 + 150 * scale, 
                         button_width, button_height)

# Load Game Buttons
game1_str = 'Load New Game 1'
game1_rect = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 3 - button_height / 2,
                          button_width, button_height)
game1_load = False  # If a game has been saved to this load option
game2_str = 'Load New Game 2'
game2_rect = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 2 - button_height / 2,
                          button_width, button_height)
game2_load = False
game3_str = 'Load New Game 3'
game3_rect = pygame.Rect(screen_width / 2 - button_width / 2, screen_height*(1- 1/3) - button_height / 2,
                          button_width, button_height)
game3_load = False

# Start Game Button
start_rect = pygame.Rect(screen_width / 3 - button_width / 2, screen_height*(1- 1/3) - button_height / 2,
                          button_width, button_height)

# Game Name Button
game_name_rect = pygame.Rect(screen_width / 3 - button_width / 2, screen_height / 3, button_width, button_height)

# Return to the world's drawing screen
return_button_rect = pygame.Rect(screen_width - button_width, screen_height - button_height, button_width, button_height)

# Back button for game detail screen
back_button_rect = pygame.Rect((screen_width / 3 - button_width / 2)*2, screen_height*(1- 1/3) - button_height / 2,
                                  button_width, button_height)

# Return from world button
world_return_button_rect = pygame.Rect(screen_width - button_width, screen_height - button_height, button_width, button_height)

# Inventory Button
inventory_button_rect = pygame.Rect(0, screen_height - button_height, button_width, button_height)

# World Title Box
world_rect = pygame.Rect(screen_width / 2 - button_width / 2, 0, button_width, button_height)

# Inventory Title Box
inventory_rect = pygame.Rect(screen_width / 2 - button_width / 2, 0, button_width, button_height)

# Dice Button 
dice_button_width = button_width / 2
dice_button_rect = pygame.Rect(screen_width - dice_button_width, 0, dice_button_width, button_height)

# Page Turn Forward Button
page_button_width = button_width / 2
page_forward_button_rect = pygame.Rect(screen_width - page_button_width, screen_height / 2, page_button_width, button_height)
# Page Turn Backward Button
page_back_button_rect = pygame.Rect(0, screen_height / 2, page_button_width, button_height)

class game:
    '''
    Game objects
    Each object will have it's data altered once saving is figured out
    Would like a preview picture of the game.
    '''
    def __init__(self):
        # Clear the surfaces
        self.name = "Load New Game"
        
        # Draw default inventory lines
        # Column
        self.add_pixels(inventory_drawing_surface, (250, 0), (250, draw_height), pen_thickness)
        self.add_pixels(inventory_drawing_surface, (450, 0), (450, draw_height), pen_thickness)
        self.add_pixels(inventory_drawing_surface, (650, 0), (650, draw_height), pen_thickness)
        # Row
        self.add_pixels(inventory_drawing_surface, (0, 200), (draw_width, 200), pen_thickness)
        self.add_pixels(inventory_drawing_surface, (0, 400), (draw_width, 400), pen_thickness)
        self.add_pixels(inventory_drawing_surface, (0, 600), (draw_width, 600), pen_thickness)
        self.add_pixels(inventory_drawing_surface, (0, 800), (draw_width, 800), pen_thickness)
        self.page1_pixels = pygame.surfarray.pixels2d(drawing_surface1)
        self.page2_pixels = pygame.surfarray.pixels2d(drawing_surface2)
        self.page3_pixels = pygame.surfarray.pixels2d(drawing_surface3)
        self.inv_pixels = pygame.surfarray.pixels2d(inventory_drawing_surface)
        self.page1_pixels_save = pygame.surfarray.array2d(drawing_surface1)
        self.page2_pixels_save = pygame.surfarray.array2d(drawing_surface2)
        self.page3_pixels_save = pygame.surfarray.array2d(drawing_surface3)
        self.inv_pixels_save = pygame.surfarray.array2d(inventory_drawing_surface)
        self.name_changed = False    # Only can change the name once
        

    def change_name(self, new_name):
        self.name = new_name
        self.name_changed = True

    def draw_lines(self):
        pygame.surfarray.blit_array(drawing_surface1, self.page1_pixels_save)
        pygame.surfarray.blit_array(drawing_surface2, self.page2_pixels_save)
        pygame.surfarray.blit_array(drawing_surface3, self.page3_pixels_save)
        pygame.surfarray.blit_array(inventory_drawing_surface, self.inv_pixels_save)
    
    def remove_intersecting_lines(self, start, end, thickness, page): 
        # Create the eraser line
        pygame.draw.line(eraser_surface, pen_color, start, end, thickness)
        # Convert the lines to a numpy array
        eraser_pixels = pygame.surfarray.pixels2d(eraser_surface)
        eraser_path = np.argwhere(eraser_pixels == 4278190080)  # Only get the pixel locations of the drawn eraser
        
        # Check for intersections between the eraser's line and the pen's line
        for ind in eraser_path:
            # print(intersect)
            if page == 1:
                if self.page1_pixels[ind[0]][ind[1]] == 4278190080:
                    self.page1_pixels[ind[0]][ind[1]] = 0
            elif page == 2:
                if self.page2_pixels[ind[0]][ind[1]] == 4278190080:
                    self.page2_pixels[ind[0]][ind[1]] = 0
            elif page == 3:
                if self.page3_pixels[ind[0]][ind[1]] == 4278190080:
                    self.page3_pixels[ind[0]][ind[1]] = 0
            elif page == 0:
                if self.inv_pixels[ind[0]][ind[1]] == 4278190080:
                    self.inv_pixels[ind[0]][ind[1]] = 0

        eraser_surface.fill((0, 0, 0, 0))   # Clear the eraser

    def add_pixels(self, surface, start, end, thickness):
        """ Adds the pixels between the start and end of a line"""
        pygame.draw.line(surface, pen_color, start, end, thickness)

    def bresenham(self, x1, y1, x2, y2):
        pixels = []
        # Calculate the differences
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # Determine the direction of the iteration
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy
        while True:
            # Add the current point to the list
            pixels.append((x1, y1))
            # If the current point is the end point, break out of the loop
            if x1 == x2 and y1 == y2:
                break
            # Calculate error
            e2 = 2 * err
            # Move horizontally
            if e2 > -dy:
                err -= dy
                x1 += sx
            # Move vertically
            if e2 < dx:
                err += dx
                y1 += sy
        return pixels

    def save_game(self):
        '''
        Saves pixel data to individual file.
        Only saves game when either the game is exited through the menu or program is closed.
        '''
        print("Game save")
        # Copy over the pixel arrays
        self.page1_pixels_save = pygame.surfarray.array2d(drawing_surface1)
        self.page2_pixels_save = pygame.surfarray.array2d(drawing_surface2)
        self.page3_pixels_save = pygame.surfarray.array2d(drawing_surface3)
        self.inv_pixels_save = pygame.surfarray.array2d(inventory_drawing_surface)

        str_page1 = self.name + "1.txt"
        str_page2 = self.name + "2.txt"
        str_page3 = self.name + "3.txt"
        str_inv = self.name + "Inv.txt"
        save_lines_to_file(str_page1, self.page1_pixels)
        save_lines_to_file(str_page2, self.page2_pixels)
        save_lines_to_file(str_page3, self.page3_pixels)
        save_lines_to_file(str_inv, self.inv_pixels)
    
def sort_pixels(arr):
    arr.sort(key=lambda x: x[0])
    return arr
    
def save_lines_to_file(filename, lines):
    save_path = 'C:/Users/fletc/Documents/Worlds Game/GameSave'
    # Create the directory if it doesn't exist
    filepath = save_path + filename
    f = open(filepath, 'a')
    f.write(str(lines))

def draw_button(screen, color, rect, text):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def login_screen():
    '''
    Login screen presented at the start of the game, requesting a pin to access the game
    '''
    global login_str
    running = True
    logging_in = False
    while running:
        screen.fill(background_color)
        screen.blit(logo, (screen_width / 2 - logo_width / 2 + 20 * scale, screen_height / 3 - logo_height / 2 + 50 * scale))
        mouse_pos = pygame.mouse.get_pos()

        button_color_current = default_button_color
        if login_rect.collidepoint(mouse_pos):
            button_color_current = button_hover_color

        draw_button(screen, button_color_current, login_rect, login_str)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and login_rect.collidepoint(mouse_pos) and logging_in is False:
                print("clicked")
                logging_in = True
                login_str = ''
            elif logging_in:
                if event.type == pygame.KEYDOWN:
                    print("typing")
                    if event.key == pygame.K_BACKSPACE:
                        login_str = login_str[:-1]
                    elif event.key == pygame.K_RETURN and login_str == '1234':
                        print("logging in")
                        login_str = ''
                        load_screen()
                    elif event.key == pygame.K_RETURN and login_str != '1234':
                        print("Password incorrect")
                        login_str = 'Incorrect Password'
                        logging_in = False
                    else:
                        login_str += event.unicode
            

        pygame.display.flip()

def load_screen():
    '''
    Load screen is presented after the login screen asking the user to select from up to 3 saved World games
    '''
    global login_str
    running = True
    while running:
        screen.fill(background_color)
        mouse_pos = pygame.mouse.get_pos()

        # Change color of button if mouse is hovered over
        game1_color_current = default_button_color
        game2_color_current = default_button_color
        game3_color_current = default_button_color
        if game1_rect.collidepoint(mouse_pos):
            game1_color_current = button_hover_color
        elif game2_rect.collidepoint(mouse_pos):
            game2_color_current = button_hover_color
        elif game3_rect.collidepoint(mouse_pos):
            game3_color_current = button_hover_color

        # Draw buttons
        draw_button(screen, game1_color_current, game1_rect, game1.name)
        draw_button(screen, game2_color_current, game2_rect, game2.name)
        draw_button(screen, game3_color_current, game3_rect, game3.name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and game1_rect.collidepoint(mouse_pos):
                game_detail_screen(game1)
            elif event.type == pygame.MOUSEBUTTONDOWN and game2_rect.collidepoint(mouse_pos):
                game_detail_screen(game2)
            elif event.type == pygame.MOUSEBUTTONDOWN and game3_rect.collidepoint(mouse_pos):
                game_detail_screen(game3)
                    
        pygame.display.flip()

def game_detail_screen(self):
    '''
    Screen that shows once a game is selected to show details
    '''
    running = True
    typing = False  # If the player is typing a new name
    game_name = self.name  # Name of the game if being changed
    inactive_button = True
    while running:
        screen.blit(background_image, (0, 0)) # Background image
        mouse_pos = pygame.mouse.get_pos()

        back_color_current = default_button_color
        game_color_current = default_button_color
        if back_button_rect.collidepoint(mouse_pos):
            back_color_current = button_hover_color
        elif game_name_rect.collidepoint(mouse_pos):
            game_color_current = button_hover_color

        # Player can start the game after changing the name once
        if game_name != 'Load New Game' and typing is False:
            draw_button(screen, default_button_color, start_rect, "Start")      # Start Game
            inactive_button = False
        else:
            draw_button(screen, inactive_button_color, start_rect, "Start")     # Button is inactive and cannot be used

        draw_button(screen, back_color_current, back_button_rect, "Back")   # Return to Load Game Screen
        draw_button(screen, game_color_current, game_name_rect, game_name)    # Name of the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                self.save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_name_rect.collidepoint(mouse_pos) and typing is False and self.name_changed is False:
                print("Clicked")
                typing = True
                game_name = '' 
            elif typing is True and event.type == pygame.MOUSEBUTTONDOWN:   # Can click off to commit name change
                typing = False
                self.change_name(game_name)
            elif typing:
                draw_button(screen, default_button_color, game_name_rect, game_name)    # Re-draw button to show typing
                if event.type == pygame.KEYDOWN:
                    print("typing")
                    if event.key == pygame.K_BACKSPACE:
                        game_name = game_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("Name changed")
                        self.change_name(game_name)
                        typing = False
                    else:
                        game_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(mouse_pos):
                load_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN and start_rect.collidepoint(mouse_pos) and inactive_button is False:
                world_screen(self)
        pygame.display.flip()

def world_screen(self):
    running = True
    drawing = False
    pen = True
    draw_color = pen_color
    main = True
    last_pos = None
    rand_int = 1    # Random dice number
    page = 1    # Start on page 1
    screen.fill((0, 0, 0))
    self.draw_lines()
    current_surface = drawing_surface1
    peak_mem = 0
    peak_disk = 0
    peak_cpu = 0
    prev_time = time.time()
    while running:
        curr_time = time.time()
        screen.blit(background_image, (0, 0))
        scaled_drawing_surface = pygame.transform.smoothscale(current_surface, (width,height))
        screen.blit(scaled_drawing_surface, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()

        # Convert mouse position to high-resolution drawing surface coordinates
        high_res_mouse_pos = (mouse_pos[0] * res_scale, mouse_pos[1] * res_scale)

        # print(high_res_mouse_pos)

        # Change color of button hovering over
        return_color_current = default_button_color
        if world_return_button_rect.collidepoint(mouse_pos):
            return_color_current = button_hover_color
        inventory_color_current = default_button_color
        if inventory_button_rect.collidepoint(mouse_pos):
            inventory_color_current = button_hover_color
        page_forward_color_current = default_button_color
        if page_forward_button_rect.collidepoint(mouse_pos):
            page_forward_color_current = button_hover_color
        page_back_color_current = default_button_color
        if page_back_button_rect.collidepoint(mouse_pos):
            page_back_color_current = button_hover_color

        # Assign color to box of active tool
        if pen:
            pen_tool_color_current = active_tool_color
            eraser_tool_color_current = inactive_tool_color
        else:
            pen_tool_color_current = inactive_tool_color
            eraser_tool_color_current = active_tool_color

        # Draw the buttons onto the screen
        if page == 1:
            draw_button(screen, page_forward_color_current, page_forward_button_rect, "-->")
        elif page == 2:
            draw_button(screen, page_forward_color_current, page_forward_button_rect, "-->")
            draw_button(screen, page_back_color_current, page_back_button_rect, "<--")
        elif page == 3:
            draw_button(screen, page_back_color_current, page_back_button_rect, "<--")
        draw_button(screen, default_button_color, dice_button_rect, str(rand_int))
        draw_button(screen, default_button_color, world_rect, "WORLD")    # Title Box
        draw_button(screen, return_color_current, world_return_button_rect, "Return")
        draw_button(screen, inventory_color_current, inventory_button_rect, "Inventory")
        draw_button(screen, pen_tool_color_current, pen_rect, "Pen")
        draw_button(screen, eraser_tool_color_current, eraser_rect, "Eraser")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                self.save_game()
                drawing_surface1.fill((0, 0, 0, 0))
                drawing_surface2.fill((0, 0, 0, 0))
                drawing_surface3.fill((0, 0, 0, 0))
                inventory_drawing_surface.fill((0, 0, 0, 0))
                print(f"Disk Usage: {peak_disk}%")
                print(f"CPU Usage: {peak_cpu}%")
                print(f"Memory Usage: {peak_mem}%")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if world_return_button_rect.collidepoint(mouse_pos):
                        self.save_game()
                        drawing_surface1.fill((0, 0, 0, 0))
                        drawing_surface2.fill((0, 0, 0, 0))
                        drawing_surface3.fill((0, 0, 0, 0))
                        inventory_drawing_surface.fill((0, 0, 0, 0))
                        game_detail_screen(self)
                        running = False
                    elif inventory_button_rect.collidepoint(mouse_pos):
                        self.save_game()
                        inventory_screen(self)
                    elif pen_rect.collidepoint(mouse_pos):
                        pen = True
                        print("Pen Active")
                    elif eraser_rect.collidepoint(mouse_pos):
                        pen = False
                        print("Eraser Active")
                    elif dice_button_rect.collidepoint(mouse_pos):
                        print("Rolling dice")
                        prev_int = 0
                        for i in range(1,5):
                            rand_int = random.randint(1, 6)
                            while rand_int == prev_int:
                                rand_int = random.randint(1, 6)
                            num_str = str(rand_int)
                            prev_int = rand_int
                            print(rand_int)
                            draw_button(screen, default_button_color, dice_button_rect, num_str)
                            time.sleep(0.2)
                            pygame.display.flip()
                    elif page_forward_button_rect.collidepoint(mouse_pos):
                        print("Page Forward")
                        page += 1
                        print("Page: ", page)
                        if page == 2:
                            current_surface = drawing_surface2
                        elif page == 3:
                            current_surface = drawing_surface3
                        scaled_drawing_surface = pygame.transform.smoothscale(current_surface, (width, height))
                        screen.blit(scaled_drawing_surface, (0, 0))
                        pygame.display.flip()
                    elif page_back_button_rect.collidepoint(mouse_pos):
                        print("Page Back")
                        page -= 1
                        print("Page: ", page)
                        if page == 1:
                            current_surface = drawing_surface1
                        elif page == 2:
                            current_surface = drawing_surface2
                        scaled_drawing_surface = pygame.transform.smoothscale(current_surface, (width, height))
                        screen.blit(scaled_drawing_surface, (0, 0))
                        pygame.display.flip()
                    else:
                        drawing = True
                        last_pos = high_res_mouse_pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    current_pos = high_res_mouse_pos
                    if last_pos:
                        if pen:
                            self.add_pixels(current_surface, last_pos, current_pos, pen_thickness)  # Save the drawn line
                        else:
                            thickness = 20
                            self.remove_intersecting_lines(current_pos, last_pos, thickness, page)
                    last_pos = current_pos

        # Update the background image
        screen.blit(background_image, (0, 0))

        # Update the drawing surface on top of the image 
        screen.blit(scaled_drawing_surface, (0, 0))

        # Re-draw the buttons onto the screen
        if page == 1:
            draw_button(screen, page_forward_color_current, page_forward_button_rect, "-->")
        elif page == 2:
            draw_button(screen, page_forward_color_current, page_forward_button_rect, "-->")
            draw_button(screen, page_back_color_current, page_back_button_rect, "<--")
        elif page == 3:
            draw_button(screen, page_back_color_current, page_back_button_rect, "<--")
        draw_button(screen, default_button_color, dice_button_rect, str(rand_int))
        draw_button(screen, default_button_color, world_rect, "WORLD")    # Title Box
        draw_button(screen, pen_tool_color_current, pen_rect, "Pen")
        draw_button(screen, eraser_tool_color_current, eraser_rect, "Eraser")
        draw_button(screen, return_color_current, world_return_button_rect, "Return")
        draw_button(screen, inventory_color_current, inventory_button_rect, "Inventory")

        pygame.display.flip()

        # current, peak = tracemalloc.get_traced_memory()

        # print(f"Current memory usage: {current / 1024} KB")
        # print(f"Peak memory usage: {peak / 1024} KB")

        # dt = curr_time - prev_time
        # prev_time = curr_time
        # print(dt)
        # disk_usage = psutil.disk_usage('/')
        # memory_usage = psutil.virtual_memory()
        # cpu_percent = psutil.cpu_percent(interval=dt)
        # if cpu_percent > peak_cpu:
        #     peak_cpu = cpu_percent
        # if float(disk_usage.percent) > peak_disk:
        #     peak_disk = disk_usage.percent
        # if float(memory_usage.percent) > peak_mem:
        #     peak_mem = memory_usage.percent

def inventory_screen(self):
    '''
    Tracks the inventory of the players.
    Defaults with certain number of columns and rows
    '''
    last_pos = None
    pen = True
    drawing = False
    page = 0
    screen.fill((0, 0, 0))    # Clear drawing surface
    self.draw_lines()
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        scaled_drawing_surface = pygame.transform.smoothscale(inventory_drawing_surface, (width, height))
        screen.blit(scaled_drawing_surface, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        # Convert mouse position to high-resolution drawing surface coordinates
        high_res_mouse_pos = (mouse_pos[0] * res_scale, mouse_pos[1] * res_scale)

        # Change button color when mouse is hovered over
        return_color_current = default_button_color
        if return_button_rect.collidepoint(mouse_pos):
            return_color_current = button_hover_color

        if pen:
            pen_tool_color_current = active_tool_color
            eraser_tool_color_current = inactive_tool_color
        else:
            pen_tool_color_current = inactive_tool_color
            eraser_tool_color_current = active_tool_color

        # Draw the buttons
        draw_button(screen, default_button_color, inventory_rect, "INVENTORY")    # Title Box
        draw_button(screen, return_color_current, return_button_rect, "Return")
        draw_button(screen, pen_tool_color_current, pen_rect, "Pen")
        draw_button(screen, eraser_tool_color_current, eraser_rect, "Eraser")

        # Determine action from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                self.save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if return_button_rect.collidepoint(mouse_pos):
                        self.save_game()
                        world_screen(self)
                        running = False
                    elif pen_rect.collidepoint(mouse_pos):
                        pen = True
                        print("Pen Active")
                    elif eraser_rect.collidepoint(mouse_pos):
                        pen = False
                        print("Eraser Active")
                    else:
                        drawing = True
                        last_pos = high_res_mouse_pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    current_pos = high_res_mouse_pos
                    if last_pos:
                        if pen:
                            self.add_pixels(inventory_drawing_surface, last_pos, current_pos, pen_thickness)  # Save the drawn line
                        else:
                            thickness = 20
                            self.remove_intersecting_lines(current_pos, last_pos, thickness, page)
                    last_pos = current_pos

        # Update the background image
        screen.blit(background_image, (0, 0))

        # Update the drawing surface on top
        screen.blit(scaled_drawing_surface, (0, 0))

        # Re-draw the buttons to update with any work
        draw_button(screen, default_button_color, inventory_rect, "INVENTORY")    # Title Box
        draw_button(screen, pen_tool_color_current, pen_rect, "Pen")
        draw_button(screen, eraser_tool_color_current, eraser_rect, "Eraser")
        draw_button(screen, return_color_current, return_button_rect, "Return")

        pygame.display.flip()

if __name__ == "__main__":
    game1 = game()
    game2 = game()
    game3 = game()
    tracemalloc.start()
    login_screen()
    tracemalloc.stop()


### USELESS STUFF THAT I WANT TO KEEP ###
# margin_x = button_width
# margin_y = button_height

# # inventory_col_width = (screen_width - margin_x) / self.cols 
# # inventory_row_height = (screen_height - margin_y) / self.rows

# draw_button(screen, button_color_current, world_return_button_rect, "Return")

# # # Array of inventory buttons
# # inventory_buttons = []

# # # Draw the button table
# # for rows in range(self.rows):
# #     for cols in range(self.cols):
# #         location_x = inventory_col_width * cols
# #         location_y = inventory_row_height * rows
# #         label = self.inventory_data[rows][cols]
# #         inv_rect = pygame.Rect(location_x, location_y, inventory_col_width, inventory_row_height)
# #         draw_button(screen, button_color_current, inv_rect, label)
