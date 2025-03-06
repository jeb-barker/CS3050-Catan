import pyglet
from pyglet.gl import *

class Renderer(pyglet.window.Window):
    
    def __init__(self, board):
        super().__init__(width=1280, height=720, caption="Catan")
        
        self.board = board
        self.tiles_batch = pyglet.graphics.Batch()
        self.gen_nums_batch = pyglet.graphics.Batch()
        


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
        hills_tile_img     = pyglet.image.load("/assets/hill.png")
        forest_tile_img    = pyglet.image.load("/assets/forest.png")
        mountains_tile_img = pyglet.image.load("/assets/mountain.png")
        fields_tile_img    = pyglet.image.load("/assets/field.png")
        pasture_tile_img   = pyglet.image.load("/assets/pasture.png")
        desert_tile_img    = pyglet.image.load("/assets/desert.png")
        self.tile_sprites = []        

        for tile in board.tiles:
            image = 1#? # make list of tiles and index in tile enum value
            x = 2#? # compute based on tile coord displacement from center
            y = 3#? # same as x
            sprite = pyglet.sprite.Sprite(image, batch=batch, x=x, y=y)
            self.tile_sprites.append(sprite)
    

renderer = Renderer(None)
pyglet.app.run()
