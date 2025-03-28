"""This file contains functions useful for handling game logic after buttons are clicked"""

from texture_enums import Resource

def on_click(x, y, renderer):
    """Handle click events from the window."""
    for clickable in renderer.get_clickables():
        if clickable.contains((x,y)):
            match clickable.id:
                case "add_resource":
                    renderer.board.add_resources(renderer.board.players[0], [Resource(4)])
                case _:
                    pass
