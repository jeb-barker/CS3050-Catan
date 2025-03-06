import pyglet
from pyglet.gl import *
from board import Board

class Renderer(pyglet.window.Window):
    
    # ratio of tile height to screen height
    TILE_SCALE = 0.1

    def __init__(self, board):
        super().__init__(width=2000, height=1000, caption="Catan")
        
        self.board = Board()
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


    def load_tiles_batch(self):
        mountains_tile_img = pyglet.image.load("assets/mountain.png")
        fields_tile_img    = pyglet.image.load("assets/field.png")
        pasture_tile_img   = pyglet.image.load("assets/pasture.png")
        hills_tile_img     = pyglet.image.load("assets/hill.png")
        forest_tile_img    = pyglet.image.load("assets/forest.png")
        desert_tile_img    = pyglet.image.load("assets/desert.png")
        images = [mountains_tile_img, fields_tile_img, pasture_tile_img, 
                  hills_tile_img, forest_tile_img, desert_tile_img]

        # assume all images are the same size and calculate the scale factor for the sprite
       
        image_width = images[0].width
        image_height = images[0].height

        tile_width = self.TILE_SCALE * self.width 
        tile_height = tile_width * image_height / self.height
    
        scale = tile_width / image_width

        self.tile_sprites = []
 
        center_x = self.width / 2 - tile_width / 2
        center_y = self.height / 2 - tile_height / 2

        for tile in self.board.tiles:
            image = images[tile.resource.value]
            axial_x, axial_y = tile.coords
            x = center_x + (axial_x * tile_width)
            y = center_y + (axial_y * tile_height)
           
            sprite = pyglet.sprite.Sprite(image, batch=self.tiles_batch, x=x, y=y)
            sprite.scale = scale
            self.tile_sprites.append(sprite)
    

renderer = Renderer(None)
pyglet.app.run()
