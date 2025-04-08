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
                    renderer.board.add_resources(state.get_current_player(), [Resource(4)])
                case "roll_dice":
                    # Only allowed if the board_state is in the pre-roll phase
                    if state.roll_dice():
                        renderer.board.start_turn(state.get_current_player())
                        state.start_building_phase()
                case "build_settlement":
                    # Only allowed if the board_state is in the build phase
                    if state.is_build_allowed and not state.tags['city']:
                        state.tags['settlement'] = True
                case "build_city":
                    # Only allowed if the board_state is in the build phase
                    # Also other tags can't be active at the same time.
                    if state.is_build_allowed and not state.tags['settlement']:
                        state.tags['city'] = True
                case _:
                    pass
    vertex_buttons = renderer.get_vertex_buttons()
    for vertex_index in vertex_buttons:
        if vertex_buttons[vertex_index].contains((x,y)):
            match vertex_buttons[vertex_index].button_name:
                case "vertex":
                    # vertex buttons can only be clicked if building tags are active
                    if state.tags['city']:
                        renderer.board.place_building(Building.city, state.get_current_player(), vertex_index)
                        state.tags['city'] = False
                    elif state.tags['settlement']:
                        renderer.board.place_building(Building.settlement, state.get_current_player(), vertex_index)
                        state.tags['settlement'] = False
                    elif state.tags['road']:
                        #renderer.board.place_road(renderer.board.players[0], )
                        # TODO - add roads
                        pass
                case _:
                    pass
