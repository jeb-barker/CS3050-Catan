import pyglet
from pyglet.gl import *
import tile

if __name__ == "__main__": 
    window = pyglet.window.Window()
    t = tile.Tile()

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        t.draw_tile(window.width/2,window.height/2, 50)

    pyglet.app.run()