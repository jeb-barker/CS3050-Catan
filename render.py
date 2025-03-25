import math
import pyglet
from pyglet.gl import *
from board import Board
from texture_enums import Resource

from threading import Thread

class Renderer(pyglet.window.Window):
    
    # ratio of tile height to screen height
    TILE_SCALE = 0.1

    def __init__(self, board):
        super().__init__(width=3000, height=1500, caption="Catan")
        
        self.board = Board()
        self.load_images()
        self.tiles_batch = pyglet.graphics.Batch()
        self.gen_nums_batch = pyglet.graphics.Batch()
        self.load_tiles_batch()


    def on_draw(self):
        # clear screen
        glClearColor(0.7, 0.8, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        # enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # draw tiles
        self.tiles_batch.draw()
        # draw gen nums
        self.gen_nums_batch.draw()


    def load_images(self):
        self.image_names = [
            "assets/mountains1.png",
            "assets/mountains2.png",
            "assets/mountains3.png",
            "assets/fields1.png",
            "assets/fields2.png",
            "assets/fields3.png",
            "assets/fields4.png",
            "assets/pasture1.png",
            "assets/pasture2.png",
            "assets/pasture3.png",
            "assets/pasture4.png",
            "assets/hills1.png",
            "assets/hills2.png",
            "assets/hills3.png",
            "assets/forest1.png",
            "assets/forest2.png",
            "assets/forest3.png",
            "assets/forest4.png",
            "assets/desert.png",
        ]
        image_count = len(self.image_names)
        self.images = [None for _ in range(image_count)]
        threads = [None for _ in range(image_count)]
        for i in range(image_count):
            threads[i] = Thread(target=self.load_image, args=(i,))
            threads[i].start()
        
        for thread in threads:
            thread.join() 

    def load_image(self, image_index):
        self.images[image_index] = pyglet.image.load(self.image_names[image_index])


    def draw_resource_cards(self, player_id):
        # list of player's resources
        resources = self.board.players[player_id]

        
        

    def load_tiles_batch(self):
        mountains_imgs = self.images[0:3]
        fields_imgs = self.images[3:7] 
        pasture_imgs = self.images[7:11] 
        hills_imgs = self.images[11:14] 
        forest_imgs = self.images[14:18]
        desert_img = self.images[18] 

        mountains_index = 0
        fields_index = 0
        pasture_index = 0
        hills_index = 0
        forest_index = 0

        # assume all images are the same size
        image_width = desert_img.width
        image_height = desert_img.height

        # hexagon tile dimensions
        tile_width = self.TILE_SCALE * self.width 
        tile_height = (image_height / image_width) * tile_width

        # factor to scale tile images by
        scale = tile_width / image_width

        self.tile_sprites = []

        # coordinates of where to position central tile 
        center_x = self.width / 2 - tile_width / 2
        center_y = self.height / 2 - tile_height / 2

        for tile in self.board.tiles:
            match tile.resource.value:
                case 0: # stone
                    image = mountains_imgs[mountains_index % len(mountains_imgs)]
                    mountains_index += 1
                case 1: # wheat
                    image = fields_imgs[fields_index % len(fields_imgs)]
                    fields_index += 1
                case 2: # sheep
                    image = pasture_imgs[pasture_index % len(pasture_imgs)]
                    pasture_index += 1
                case 3: # brick
                    image = hills_imgs[hills_index % len(hills_imgs)]
                    hills_index += 1
                case 4: # wood
                    image = forest_imgs[forest_index % len(forest_imgs)]
                    forest_index += 1
                case _: # none
                    image = desert_img
            
            # axial coordinates specify a signed integer x, y offset from a (0, 0) center
            axial_x, axial_y = tile.coords

            # Tiles above the midline need to be shifted right, likewise below need to be shifted left.
            # the axial_y / 2 term accounts for this shift. The reason for dividing by two is that
            # the hexagon grid is staggered row to row for tesselation.
            x = center_x + tile_width * (axial_x + axial_y / 2)
            
            # If you picture the largest rectangle you could draw within a hexagon,
            # the height of that rectangle is 1/2 the height of the whole shape
            # the pointed section above this rectangle fits into the above row of hexagons.
            # the height of this upper section is 1/4 of the shape's height, meaning
            # the row coordinate must be scaled by 3/4
            y = center_y + tile_height * (axial_y * 0.75)
           
            sprite = pyglet.sprite.Sprite(image, batch=self.tiles_batch, x=x, y=y)
            sprite.scale = scale
            self.tile_sprites.append(sprite)


    

renderer = Renderer(None)
pyglet.app.run()
