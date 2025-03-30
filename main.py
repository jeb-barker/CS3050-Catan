import pyglet
from render import Renderer
import event_handler

from game_state import GameState

if __name__ == "__main__": 
    config = pyglet.gl.Config(sample_buffers=1, samples=8, double_buffer=True)
    window = pyglet.window.Window(config=config, width=1920, height=1080, caption="Catan")

    from player import Player
    from texture_enums import Resource

    p1 = Player(0, "red")
    p2 = Player(1, "blue")
    p3 = Player(2, "black")
    p1.resources = [Resource.ore, Resource.sheep, Resource.wheat, Resource.brick, Resource.wood]

    players = [p1, p2, p3]
    game_state = GameState(players)

    renderer = Renderer(window)

    @window.event
    def on_draw():
        renderer.update()

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        """Whenever a mouse button is released this event is dispatched"""
        if button == pyglet.window.mouse.LEFT:
            event_handler.on_click(x, y, renderer, game_state)

    pyglet.app.run()
