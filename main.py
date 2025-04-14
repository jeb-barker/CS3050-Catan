"""Runs a game of Catan between a single player and 3 AI"""
import pyglet
from render import Renderer
import event_handler

if __name__ == "__main__":
    config = pyglet.gl.Config(sample_buffers=1, samples=8, double_buffer=True)
    window = pyglet.window.Window(config=config, width=3000, height=1500, caption="Catan")
    renderer = Renderer(window)

    @window.event
    def on_draw():
        """The on_draw method called by pyglet"""
        renderer.update()

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        """Whenever a mouse button is released this event is dispatched"""
        if button == pyglet.window.mouse.LEFT:
            event_handler.on_click(x, y, renderer)

    pyglet.app.run()
