"""This file contains functions useful for handling game logic after buttons are clicked"""

from texture_enums import Resource
from board_config import Building

def on_click(x, y, renderer):
    """Handle click events from the window."""
    state = renderer.board.game_state
    for clickable in renderer.get_clickables():
        if clickable.contains((x,y)):
            match clickable.button_name:
                case "add_resource":
                    # debug button TODO: remove
                    renderer.board.add_resources(renderer.board.players[0], [Resource(4)])
                case "roll_dice":
                    # Only allowed if the board_state is in the pre-roll phase
                    if state.roll_dice():
                        renderer.board.start_turn(renderer.board.players[0])
                case _:
                    pass
    vertex_buttons = renderer.get_vertex_buttons()
    for vertex_index in vertex_buttons:
        if vertex_buttons[vertex_index].contains((x,y)):
            match vertex_buttons[vertex_index].button_name:
                case "vertex":
                    # vertex buttons can only be clicked if building tags are active
                    if state.tags['city']:
                        renderer.board.place_building(Building.city, renderer.board.players[0], vertex_index)
                    elif state.tags['settlement']:
                        renderer.board.place_building(Building.settlement, renderer.board.players[0], vertex_index)
                    elif state.tags['road']:
                        #renderer.board.place_road(renderer.board.players[0], )
                        # TODO - add roads
                        pass
                case _:
                    pass
