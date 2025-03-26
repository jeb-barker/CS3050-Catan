import pyglet
from render import Renderer

if __name__ == "__main__": 
    config = pyglet.gl.Config(sample_buffers=1, samples=8, double_buffer=True)
    window = pyglet.window.Window(config=config, width=3000, height=1500, caption="Catan")
    renderer = Renderer(window)

    @window.event
    def on_draw():
        renderer.update()
    
    pyglet.app.run()
