import sys

import pygame

from util import load_images
from tilemap import Tilemap

RENDER_SCALE = 2.0

class map_editor:
    """
    A class to represent a map editor for a tile-based game.
    Methods
    -------
    __init__():
        Initializes the map editor, sets up the display, loads assets, and initializes variables.
    run():
        Main loop of the map editor. Handles rendering, input events, and tile placement/removal.
    """
    def __init__(self):
        """
        Initializes the map editor.
        This method sets up the Pygame environment, initializes the display, loads assets,
        and prepares the tilemap for editing. It also sets up various control flags and 
        parameters for user interaction.
        Attributes:
            screen (pygame.Surface): The main display surface.
            display (pygame.Surface): The surface used for rendering the map.
            clock (pygame.time.Clock): The clock object to manage the frame rate.
            assets (dict): A dictionary containing loaded images for different tile types.
            movement (list): A list of booleans indicating movement directions.
            tilemap (Tilemap): The tilemap object used for map editing.
            scroll (list): A list containing the scroll offsets for the map.
            tile_list (list): A list of tile types available for editing.
            tile_group (int): The current tile group selected.
            tile_variant (int): The current tile variant selected.
            clicking (bool): A flag indicating if the left mouse button is being clicked.
            right_clicking (bool): A flag indicating if the right mouse button is being clicked.
            shift (bool): A flag indicating if the shift key is pressed.
            ongrid (bool): A flag indicating if the tiles should snap to the grid.
        """
        pygame.init()

        pygame.display.set_caption('MAP_EDITOR')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        

        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            "spawners": load_images("tiles/spawners")
            
        }
        
        self.movement = [False, False, False, False]
        
        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load(r"data\maps\4.json")
        except FileNotFoundError:
            pass    
        
        self.scroll = [0, 0]

        
        self.tile_list = list(self.assets)

        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False

        self.ongrid = True



        
    def run(self):
        """
        Main loop of the map editor.
        This method handles the rendering of the map, user input, and updating the display.
        It runs continuously until the user quits the application.
        Functionality:
        - Fills the display with a black background.
        - Updates the scroll position based on user movement.
        - Renders the tilemap with the current scroll offset.
        - Displays the current tile image with transparency at the mouse position.
        - Handles tile placement and removal on the grid and off the grid.
        - Updates the display with the current tile image.
        - Processes user input events such as mouse clicks, mouse wheel scrolling, and keyboard presses.
        - Handles quitting the application.
        User Controls:
        - Left mouse button: Place tile on the grid or off the grid.
        - Right mouse button: Remove tile from the grid or off the grid.
        - Mouse wheel: Change tile variant or tile group.
        - Arrow keys: Move the view (scroll).
        - 'G' key: Toggle grid snapping.
        - 'O' key: Save the current map.
        - Left Shift key: Enable shift mode for changing tile variants.
        Note:
        - The method assumes that the `pygame` library is initialized and the necessary attributes
          (`display`, `scroll`, `movement`, `tilemap`, `assets`, `tile_list`, `tile_group`, `tile_variant`,
          `clicking`, `right_clicking`, `ongrid`, `shift`, `screen`, `clock`) are properly set up.
        """
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) *2
            self.scroll[1] += (self.movement[3] - self.movement[2]) *2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))


            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mouse_pos)



            if self.clicking and self.ongrid:
                
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)         





            self.display.blit(current_tile_img, (5, 5))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid 
                    if event.key == pygame.K_o:
                        self.tilemap.save(r"data\maps\4.json")
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False  # Aqui desativa o estado Shift
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


map_editor().run()