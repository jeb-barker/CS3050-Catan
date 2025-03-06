import pyglet
from pyglet.gl import *
from board import Board

class Renderer(pyglet.window.Window):
    
    # ratio of tile height to screen height
    TILE_SCALE = 0.1

    def __init__(self, board):
        super().__init__(width=1280, height=720, caption="Catan")
        
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
        
        scale = 0.2
        self.tile_sprites = []        

        for tile in self.board.tiles:
            image = images[tile.resource.value]
            x = 0#? # compute based on tile coord displacement from center
            y = 0#? # same as x
            sprite = pyglet.sprite.Sprite(image, batch=self.tiles_batch, x=x, y=y)
            sprite.scale = scale
            self.tile_sprites.append(sprite)
    

renderer = Renderer(None)
pyglet.app.run()
