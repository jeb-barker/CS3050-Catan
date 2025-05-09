"""This file contains functions useful for handling game logic after buttons are clicked"""

from board_config import Building, BUILDING_COSTS

def on_click(x, y, renderer):
    """Handle click events from the window."""
    state = renderer.board.game_state
    for clickable in renderer.get_clickables():
        if clickable.contains((x,y)):
            match clickable.button_name:
                case "roll_dice":
                    # Only allowed if the board_state is in the pre-roll phase
                    if not state.is_start_phase() and state.roll_dice():
                        renderer.board.start_turn(state.get_current_player())
                        state.start_building_phase()
                case "build_settlement":
                    # Only allowed if the board_state is in the build phase
                    if state.is_build_allowed() and \
                    not state.tags['city'] and \
                    not state.tags['road']:
                        # "toggle" the build button
                        if state.tags['settlement']:
                            state.tags['settlement'] = False
                        else:
                            state.tags['settlement'] = True
                case "build_city":
                    # Only allowed if the board_state is in the build phase
                    # Also other tags can't be active at the same time.
                    # Also cannot be in the start phase
                    if state.is_build_allowed() and \
                    not state.tags['settlement'] and \
                    not state.tags['road'] and \
                    not state.is_start_phase():
                        # toggle the button
                        if state.tags['city']:
                            state.tags['city'] = False
                        else:
                            state.tags['city'] = True
                case "end_turn":
                    # Only allowed if in the building phase
                    if not state.is_start_phase() and state.end_turn():
                        # clear building flags when turn ends
                        state.tags['settlement'] = False
                        state.tags['city'] = False
                        state.tags['road'] = False
                case "build_road":
                    # Only allowed if the board_state is in the build phase
                    # Also other tags can't be active at the same time.
                    if state.is_build_allowed() and \
                    not state.tags['settlement'] and \
                    not state.tags['city']:
                        # In the start phase, roads cannot be placed before settlements
                        if (not state.is_start_phase()) or \
                        state.tags['settlements_placed_turn'] == 1:
                            # toggle the button
                            if state.tags['road']:
                                state.tags['road'] = False
                            else:
                                state.tags['road'] = True
                case "run_ai_turn":
                    # Button for the user to press to advance the game
                    if not state.get_current_player().is_user and not state.is_start_phase():
                        # clear building flags when turn ends
                        state.tags['settlement'] = False
                        state.tags['city'] = False
                        state.tags['road'] = False
                        # check if the (new) player is AI
                        if not state.get_current_player().is_user:
                            renderer.board.ai_turn(state.get_current_player())
                    elif state.is_start_phase():
                        if not state.get_current_player().is_user:
                            renderer.board.ai_start_turn(state.get_current_player())
                case _:
                    pass

    for vertex_index in renderer.board.get_clickable_vertices():
        button = renderer.vertex_buttons[vertex_index]
        if button.contains((x,y)):
            curr_player = state.get_current_player()
            match button.button_name:
                case "vertex":
                    # vertex buttons can only be clicked if building tags are active
                    if state.tags['city']:
                        renderer.board.place_building(Building.CITY, curr_player, vertex_index)
                        state.tags['city'] = False
                    elif state.tags['settlement']:
                        # if the state is in the start phase,
                        # give the player the requisite resources to place a settlement
                        if state.is_start_phase():
                            cost = BUILDING_COSTS[Building.SETTLEMENT]
                            renderer.board.add_resources(curr_player, cost)
                            state.tags['settlement_pos'] = vertex_index
                        renderer.board.place_building(Building.SETTLEMENT, curr_player, vertex_index)
                        state.tags['settlement'] = False
                    elif state.tags['road']:
                        # if the first point hasn't been assigned,
                        # the button clicked is the first point
                        if state.tags['road_v1'] is None:
                            state.tags['road_v1'] = vertex_index
                        else:
                        # if the first point has been assigned,
                        # the button clicked is the second point.
                            vertex1 = state.tags['road_v1']
                            if state.is_start_phase():
                                # give the player the cost of the road if we're in the start phase
                                cost = BUILDING_COSTS[Building.ROAD]
                                renderer.board.add_resources(curr_player, cost)
                            renderer.board.place_road(curr_player, vertex1, vertex_index)
                            state.tags['road_v1'] = None
                            state.tags['road'] = False
                            # check if settlement has been placed already this turn for start_phase
                            if state.is_start_phase():
                                if state.tags['settlements_placed_turn'] == 1:
                                    previous_player = curr_player
                                    second_settle = state.end_turn_start_phase()
                                    if second_settle:
                                        # give resources to previous player
                                        resources = renderer.board.get_resources_from_vertex(state.tags['settlement_pos'])
                                        renderer.board.add_resources(previous_player, resources)
                            state.tags['settlement_pos'] = None
                case _:
                    pass
